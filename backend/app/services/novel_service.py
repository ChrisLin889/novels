from app.models.novel import Novel, Chapter, novel_tag
from app.models.interaction import UserCollection, UserHistory, Comment
from app.models.user import User
from app.models.author import Author
from app.models.tag import Tag
from app import db
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import desc, func
from app.services.permission_service import PermissionService
from datetime import datetime

class NovelDAO:
    """
    Data Access Object for Novel and Chapter models
    Only handles direct database interactions with no business logic
    """
    
    @staticmethod
    def get_novel_by_id(novel_id: int) -> Optional[Novel]:
        """Retrieve novel by ID"""
        return Novel.query.get(novel_id)
    
    @staticmethod
    def get_novel_list_query(category: Optional[str] = None, status: Optional[str] = None):
        """Get base query for novels with optional filtering"""
        query = Novel.query
        
        # Apply filters if provided
        if category:
            query = query.filter_by(category=category)
        
        if status:
            query = query.filter_by(status=status)
            
        return query
    
    @staticmethod
    def apply_sorting(query, sort_by: str = 'updated_at', sort_order: str = 'desc'):
        """Apply sorting to a novel query"""
        if sort_by in ['view_count', 'collection_count', 'updated_at', 'created_at']:
            # Get the sort column
            sort_column = getattr(Novel, sort_by)
            
            # Apply sort direction
            if sort_order.lower() == 'asc':
                return query.order_by(sort_column)
            else:
                return query.order_by(desc(sort_column))
        else:
            # Default sort
            return query.order_by(desc(Novel.updated_at))
    
    @staticmethod
    def search_novels_query(keyword: str, category: Optional[str] = None):
        """Create query for searching novels"""
        query = Novel.query.filter(
            db.or_(
                Novel.title.ilike(f'%{keyword}%'),
                Novel.author.ilike(f'%{keyword}%'),
                Novel.intro.ilike(f'%{keyword}%')
            )
        )
        
        # Apply category filter if provided
        if category:
            query = query.filter_by(category=category)
            
        return query
    
    @staticmethod
    def get_novel_by_author_query(author_id: int):
        """Get query for novels by author ID"""
        return Novel.query.filter_by(author_id=author_id)
    
    @staticmethod
    def get_popular_novels_query(category: Optional[str] = None):
        """Get query for popular novels with optional category filter"""
        query = Novel.query.order_by(desc(Novel.view_count))
        
        # Apply category filter if provided
        if category:
            query = query.filter_by(category=category)
            
        return query
    
    @staticmethod
    def get_latest_novels(limit: int = 10) -> List[Novel]:
        """Get latest novels sorted by updated time"""
        return Novel.query.order_by(desc(Novel.updated_at)).limit(limit).all()
    
    @staticmethod
    def increment_view_count(novel_id: int) -> bool:
        """Increment the view count of a novel"""
        novel = Novel.query.get(novel_id)
        if not novel:
            return False
        
        novel.view_count += 1
        db.session.commit()
        return True
    
    @staticmethod
    def get_chapter_by_id(chapter_id: int) -> Optional[Chapter]:
        """Retrieve chapter by ID"""
        return Chapter.query.get(chapter_id)
    
    @staticmethod
    def get_chapter_by_number(novel_id: int, chapter_number: int) -> Optional[Chapter]:
        """Retrieve chapter by novel ID and chapter number"""
        return Chapter.query.filter_by(
            novel_id=novel_id,
            chapter_number=chapter_number
        ).first()
    
    @staticmethod
    def get_novel_chapters(novel_id: int) -> List[Chapter]:
        """Get all chapters for a novel ordered by chapter number"""
        return Chapter.query.filter_by(novel_id=novel_id).order_by(
            Chapter.chapter_number
        ).all()
    
    @staticmethod
    def get_adjacent_chapters(chapter: Chapter) -> Tuple[Optional[Chapter], Optional[Chapter]]:
        """Get previous and next chapters"""
        prev_chapter = Chapter.query.filter_by(
            novel_id=chapter.novel_id
        ).filter(Chapter.chapter_number < chapter.chapter_number).order_by(
            desc(Chapter.chapter_number)
        ).first()
        
        next_chapter = Chapter.query.filter_by(
            novel_id=chapter.novel_id
        ).filter(Chapter.chapter_number > chapter.chapter_number).order_by(
            Chapter.chapter_number
        ).first()
        
        return prev_chapter, next_chapter
    
    @staticmethod
    def create_novel(title: str, author_id: int, author: str, category: str, intro: str, 
                   cover: str = 'default_cover.jpg', status: str = 'ongoing') -> Novel:
        """Create a new novel in the database"""
        novel = Novel(
            title=title,
            author_id=author_id,
            author=author,
            category=category,
            intro=intro,
            cover=cover,
            status=status
        )
        
        db.session.add(novel)
        db.session.commit()
        return novel
    
    @staticmethod
    def create_chapter(novel_id: int, title: str, content: str, 
                     chapter_number: Optional[int] = None) -> Chapter:
        """Create a new chapter in the database"""
        # If chapter number not provided, calculate next chapter number
        if chapter_number is None:
            last_chapter = Chapter.query.filter_by(novel_id=novel_id).order_by(
                desc(Chapter.chapter_number)
            ).first()
            
            chapter_number = 1 if not last_chapter else last_chapter.chapter_number + 1
        
        # Calculate word count
        word_count = len(content)
        
        chapter = Chapter(
            novel_id=novel_id,
            title=title,
            content=content,
            chapter_number=chapter_number,
            word_count=word_count
        )
        
        db.session.add(chapter)
        db.session.commit()
        
        # Update novel's updated_at timestamp
        novel = Novel.query.get(novel_id)
        if novel:
            novel.updated_at = func.now()
            db.session.commit()
        
        return chapter
    
    @staticmethod
    def update_novel_fields(novel: Novel, data: Dict[str, Any]) -> Novel:
        """Update novel fields with provided data"""
        # Update novel attributes
        allowed_fields = ['title', 'author', 'category', 'cover', 'intro', 'status']
        for key, value in data.items():
            if key in allowed_fields and value is not None:
                setattr(novel, key, value)
        
        db.session.commit()
        return novel
    
    @staticmethod
    def update_chapter_fields(chapter: Chapter, data: Dict[str, Any]) -> Chapter:
        """Update chapter fields with provided data"""
        # Update chapter attributes
        if 'title' in data and data['title'] is not None:
            chapter.title = data['title']
        
        if 'content' in data and data['content'] is not None:
            chapter.content = data['content']
            chapter.word_count = len(data['content'])
        
        db.session.commit()
        
        # Update novel's updated_at timestamp
        novel = Novel.query.get(chapter.novel_id)
        if novel:
            novel.updated_at = func.now()
            db.session.commit()
        
        return chapter
    
    @staticmethod
    def delete_novel(novel_id: int) -> bool:
        """Delete a novel and all its chapters"""
        novel = Novel.query.get(novel_id)
        if not novel:
            return False
        
        db.session.delete(novel)
        db.session.commit()
        return True
    
    @staticmethod
    def delete_chapter(chapter_id: int) -> bool:
        """Delete a chapter"""
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return False
        
        # Get the novel to update its timestamp
        novel_id = chapter.novel_id
        
        db.session.delete(chapter)
        db.session.commit()
        
        # Update novel's updated_at timestamp
        novel = Novel.query.get(novel_id)
        if novel:
            novel.updated_at = func.now()
            db.session.commit()
            
        return True
    
    @staticmethod
    def get_categories() -> List[Dict[str, Any]]:
        """Get list of categories with novel counts"""
        categories = db.session.query(
            Novel.category, 
            func.count(Novel.id).label('count')
        ).group_by(Novel.category).all()
        
        return [{'name': category, 'count': count} for category, count in categories]


class NovelService:
    """
    Service for accessing and manipulating novel data
    Handles business logic, error handling, and response formatting
    """
    
    @staticmethod
    def get_novel_by_id(novel_id: int) -> Dict[str, Any]:
        """Get novel details by ID
        
        Args:
            novel_id: Novel ID
            
        Returns:
            Dictionary with novel info and success status
        """
        try:
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
                
            return {
                'success': True,
                'novel': novel.to_dict()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_list(category: Optional[str] = None, page: int = 1, 
                      per_page: int = 10, sort_by: str = 'updated_at',
                      status: Optional[str] = None, sort_order: str = 'desc') -> Dict[str, Any]:
        """Get paginated list of novels with optional filtering
        
        Args:
            category: Optional category filter
            page: Page number
            per_page: Items per page
            sort_by: Sort field
            status: Optional status filter
            sort_order: Sort direction (asc or desc)
            
        Returns:
            Dictionary with novel list and pagination info
        """
        try:
            # Create base query with filters
            query = NovelDAO.get_novel_list_query(category, status)
            
            # Apply sorting
            query = NovelDAO.apply_sorting(query, sort_by, sort_order)
            
            # Execute paginated query
            novels = query.paginate(page=page, per_page=per_page)
            
            return {
                'success': True,
                'total': novels.total,
                'pages': novels.pages,
                'current_page': page,
                'novels': [novel.to_dict() for novel in novels.items]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def search_novels(keyword: str, page: int = 1, per_page: int = 10, 
                     category: Optional[str] = None) -> Dict[str, Any]:
        """Search novels by keyword with optional filtering
        
        Args:
            keyword: Search term
            page: Page number
            per_page: Items per page
            category: Optional category filter
            
        Returns:
            Dictionary with search results and pagination info
        """
        if not keyword:
            return {'success': False, 'error': 'Search keyword is required'}
        
        try:
            # Create search query
            query = NovelDAO.search_novels_query(keyword, category)
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            novels = query.order_by(desc(Novel.updated_at))\
                          .offset((page - 1) * per_page)\
                          .limit(per_page)\
                          .all()
                          
            return {
                'success': True,
                'novels': [novel.to_dict() for novel in novels],
                'total': total,
                'pages': (total + per_page - 1) // per_page,
                'current_page': page
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_detail(novel_id: int) -> Dict[str, Any]:
        """Get detailed information about a novel including its chapters
        
        Args:
            novel_id: Novel ID
            
        Returns:
            Dictionary with novel details and chapters list
        """
        try:
            # Get novel by ID
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Increment view count
            NovelDAO.increment_view_count(novel_id)
            
            # Get chapters for the novel
            chapters = NovelDAO.get_novel_chapters(novel_id)
            
            # Get novel data
            novel_data = novel.to_dict()
            
            # Add chapter list without content
            chapters_data = [
                {
                    'id': chapter.id,
                    'novel_id': chapter.novel_id,
                    'chapter_number': chapter.chapter_number,
                    'title': chapter.title,
                    'word_count': chapter.word_count,
                    'created_at': chapter.created_at.isoformat() if chapter.created_at else None
                }
                for chapter in chapters
            ]
            
            return {
                'success': True,
                'novel': novel_data,
                'chapters': chapters_data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_popular_novels(page: int = 1, per_page: int = 10, category: Optional[str] = None) -> Dict[str, Any]:
        """Get popular novels with pagination and optional category filtering
        
        Args:
            page: Page number
            per_page: Items per page
            category: Optional category filter
            
        Returns:
            Dictionary with popular novels and pagination info
        """
        try:
            # Create query for popular novels
            query = NovelDAO.get_popular_novels_query(category)
                
            # Apply pagination
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return {
                'success': True,
                'novels': [novel.to_dict() for novel in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_latest_novels(limit: int = 10) -> Dict[str, Any]:
        """Get latest novels
        
        Args:
            limit: Number of novels to return
            
        Returns:
            Dictionary with latest novels
        """
        try:
            novels = NovelDAO.get_latest_novels(limit)
            return {
                'success': True,
                'novels': [novel.to_dict() for novel in novels]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_categories() -> Dict[str, Any]:
        """Get list of categories with novel counts
        
        Returns:
            Dictionary with categories and their counts
        """
        try:
            categories = NovelDAO.get_categories()
            return {'success': True, 'categories': categories}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_author_novels(author_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get novels created by a specific author
        
        Args:
            author_id: Author ID
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with author's novels and pagination info
        """
        try:
            # Get query for author novels
            query = NovelDAO.get_novel_by_author_query(author_id)
            
            # Apply pagination
            pagination = query.order_by(desc(Novel.updated_at))\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            # Convert novels to dict
            novels = [novel.to_dict() for novel in pagination.items]
            
            return {
                'success': True,
                'novels': novels,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_novel(title: str, category: str, intro: str, 
                 cover: str = 'default_cover.jpg', tags: list = None,
                 user_id: int = None) -> Dict[str, Any]:
        """Add a new novel
        
        Args:
            title: Novel title
            category: Novel category
            intro: Novel introduction
            cover: Cover image path
            tags: List of tags
            user_id: User ID of the author
            
        Returns:
            Dictionary with created novel info
        """
        try:
            if not user_id:
                return {'success': False, 'error': 'Authentication required'}
            
            # Find author by user_id
            author = Author.query.filter_by(user_id=user_id).first()
            if not author:
                return {'success': False, 'error': 'Author privileges required'}
            
            # 获取作者名称 - 优先使用笔名，如果没有则使用用户名
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'error': 'User not found'}
                
            author_name = author.pen_name or user.username
            
            # Create new novel using DAO
            novel = NovelDAO.create_novel(
                title=title,
                author_id=author.id,
                author=author_name,
                category=category,
                intro=intro,
                cover=cover,
                status='ongoing'
            )
            
            # Add tags if provided
            if tags and isinstance(tags, list):
                NovelService.add_tags_to_novel(novel.id, tags)
            
            return {
                'success': True,
                'novel_id': novel.id,
                'novel': novel.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_novel(novel_id: int, user_id: Optional[int] = None, title: Optional[str] = None, 
                    category: Optional[str] = None, intro: Optional[str] = None,
                    cover: Optional[str] = None, status: Optional[str] = None,
                    tags: Optional[list] = None) -> Dict[str, Any]:
        """Update novel information
        
        Args:
            novel_id: Novel ID
            user_id: User ID performing the update
            title: New title (optional)
            category: New category (optional)
            intro: New introduction (optional)
            cover: New cover image (optional)
            status: New status (optional)
            tags: New tags list (optional)
            
        Returns:
            Dictionary with update result
        """
        try:
            # Get novel
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Check permission: only the author can modify their novel
            if novel.author_id and user_id:
                author = Author.query.filter_by(user_id=user_id).first()
                if not author or novel.author_id != author.id:
                    return {'success': False, 'error': 'Permission denied'}
            
            # Create update data dictionary
            update_data = {
                'title': title,
                'category': category,
                'intro': intro,
                'cover': cover,
                'status': status
            }
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            # Update novel using DAO
            NovelDAO.update_novel_fields(novel, update_data)
            
            # Update tags if provided
            if tags and isinstance(tags, list):
                # Remove old tags and add new ones
                novel.tags = []
                db.session.commit()
                NovelService.add_tags_to_novel(novel.id, tags)
            
            return {
                'success': True,
                'message': 'Novel updated successfully',
                'novel': novel.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_chapter(author_id: int, novel_id: int, title: str, 
                   content: str, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """Add a new chapter to a novel (author only)
        
        Args:
            author_id: Author ID
            novel_id: Novel ID
            title: Chapter title
            content: Chapter content
            chapter_number: Optional chapter number
            
        Returns:
            Dictionary with created chapter info
        """
        # Check for missing required fields
        if not all([title, content]):
            return {'success': False, 'error': 'Missing required fields'}
        
        # Verify novel exists
        novel = NovelDAO.get_novel_by_id(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        try:
            # Create chapter using DAO
            chapter = NovelDAO.create_chapter(novel_id, title, content, chapter_number)
            
            return {
                'success': True,
                'message': 'Chapter added successfully',
                'chapter': chapter.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_chapter(author_id: int, chapter_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update chapter information (author or admin only)"""
        # Verify chapter exists
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            return {'success': False, 'error': 'Chapter not found'}
        
        # Get novel to check ownership
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(author_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(author_id) == 'admin'
        
        # Verify ownership: only the novel author or admin can update chapter
        if not is_admin and novel.author_id != author_id:
            return {'success': False, 'error': 'Permission denied - only the novel author or admin can update chapters'}
        
        try:
            updated_chapter = NovelDAO.update_chapter_fields(chapter, data)
            
            return {
                'success': True,
                'message': 'Chapter updated successfully',
                'chapter': updated_chapter.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_novel(user_id: int, novel_id: int) -> Dict[str, Any]:
        """Delete a novel (author or admin only)"""
        # Verify novel exists
        novel = NovelDAO.get_novel_by_id(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(user_id) == 'admin'
        
        # Find author record for the user
        author = Author.query.filter_by(user_id=user_id).first()
        
        # Verify ownership: only the novel author or admin can delete novel
        if not is_admin and (not author or novel.author_id != author.id):
            return {'success': False, 'error': 'Permission denied - only the novel author or admin can delete this novel'}
        
        try:
            NovelDAO.delete_novel(novel_id)
            
            return {
                'success': True,
                'message': 'Novel deleted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_chapter(author_id: int, chapter_id: int) -> Dict[str, Any]:
        """Delete a chapter (author or admin only)"""
        # Verify chapter exists
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            return {'success': False, 'error': 'Chapter not found'}
        
        # Get novel to check ownership
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(author_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(author_id) == 'admin'
        
        # Verify ownership: only the novel author or admin can delete chapter
        if not is_admin and novel.author_id != author_id:
            return {'success': False, 'error': 'Permission denied - only the novel author or admin can delete chapters'}
        
        novel_id = chapter.novel_id
        
        try:
            NovelDAO.delete_chapter(chapter_id)
            
            return {
                'success': True,
                'message': 'Chapter deleted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def refresh_cache() -> Dict[str, Any]:
        """
        This method previously refreshed Redis cache, now just returns success
        This method is kept for backwards compatibility
        """
        return {'success': True, 'message': 'No cache to refresh'}
    
    @staticmethod
    def get_chapter(chapter_id: int, include_content: bool = True, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get chapter details with optional content"""
        # Get chapter from DAO
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            return {'success': False, 'error': 'Chapter not found'}
            
        # Get novel for this chapter
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
            
        # Get adjacent chapters
        prev_chapter, next_chapter = NovelDAO.get_adjacent_chapters(chapter)
        
        # Update reading history if user is logged in
        if user_id:
            InteractionDAO.update_reading_history(user_id, novel.id, chapter.id)
            
        # Update view count
        NovelDAO.increment_view_count(novel.id)
        
        # Prepare response
        chapter_data = chapter.to_dict(include_content=include_content)
        
        return {
            'success': True,
            'chapter': chapter_data,
            'prev_chapter': prev_chapter.to_dict() if prev_chapter else None,
            'next_chapter': next_chapter.to_dict() if next_chapter else None
        }
    
    @staticmethod
    def get_author_stats(author_id: int) -> Dict[str, Any]:
        """Get statistics for an author"""
        try:
            # 获取作者的小说列表
            novels = NovelDAO.get_novel_by_author_query(author_id).all()
            
            # 统计数据
            novel_count = len(novels)
            novel_ids = [novel.id for novel in novels]
            
            # 总字数
            total_words = db.session.query(func.sum(Chapter.word_count))\
                .filter(Chapter.novel_id.in_(novel_ids))\
                .scalar() or 0
            
            # 总收藏数
            total_collections = db.session.query(func.sum(Novel.collection_count))\
                .filter(Novel.id.in_(novel_ids))\
                .scalar() or 0
            
            # 总浏览量
            total_views = db.session.query(func.sum(Novel.view_count))\
                .filter(Novel.id.in_(novel_ids))\
                .scalar() or 0
            
            # 总章节数
            total_chapters = Chapter.query.filter(Chapter.novel_id.in_(novel_ids)).count()
            
            stats = {
                'novel_count': novel_count,
                'total_words': total_words,
                'total_collections': total_collections,
                'total_views': total_views,
                'total_chapters': total_chapters
            }
            
            return {
                'success': True,
                'stats': stats
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_user_novel_list(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get novels by user ID (for logged-in user)
        
        Args:
            user_id: User ID
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with user's novels and pagination info
        """
        try:
            # Get author ID associated with this user
            author = Author.query.filter_by(user_id=user_id).first()
            if not author:
                return {'success': False, 'error': 'User is not an author'}
                
            # Get novels by author ID
            query = Novel.query.filter_by(author_id=author.id)
            novels = query.order_by(desc(Novel.updated_at)).paginate(page=page, per_page=per_page)
            
            return {
                'success': True,
                'total': novels.total,
                'pages': novels.pages,
                'novels': [novel.to_dict() for novel in novels.items]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_chapters(novel_id: int) -> Dict[str, Any]:
        """Get chapters for a specific novel
        
        Args:
            novel_id: Novel ID
            
        Returns:
            Dictionary with chapters list
        """
        try:
            # Check if novel exists
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Get all chapters for the novel
            chapters = NovelDAO.get_novel_chapters(novel_id)
            
            return {
                'success': True,
                'chapters': [chapter.to_dict(include_content=False) for chapter in chapters]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_tags_to_novel(novel_id: int, tag_names: List[str]) -> Dict[str, Any]:
        """添加标签到小说
        
        Args:
            novel_id: 小说ID
            tag_names: 标签名称列表
            
        Returns:
            操作结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 处理标签
            added_tags = []
            for tag_name in tag_names:
                # 检查标签是否已存在
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    # 创建新标签
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()  # 获取新标签ID
                
                # 检查小说是否已有此标签
                if tag not in novel.tags:
                    novel.tags.append(tag)
                    added_tags.append(tag.to_dict())
            
            db.session.commit()
            
            return {
                'success': True, 
                'message': 'Tags added successfully',
                'added_tags': added_tags
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
            
    @staticmethod
    def remove_tag_from_novel(novel_id: int, tag_id: int) -> Dict[str, Any]:
        """从小说中移除标签
        
        Args:
            novel_id: 小说ID
            tag_id: 标签ID
            
        Returns:
            操作结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
                
            # 检查标签是否存在
            tag = Tag.query.get(tag_id)
            if not tag:
                return {'success': False, 'error': 'Tag not found'}
                
            # 检查小说是否有此标签
            if tag not in novel.tags:
                return {'success': False, 'error': 'Novel does not have this tag'}
                
            # 移除标签
            novel.tags.remove(tag)
            db.session.commit()
            
            return {'success': True, 'message': 'Tag removed successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_tags(novel_id: int) -> Dict[str, Any]:
        """获取小说的所有标签
        
        Args:
            novel_id: 小说ID
            
        Returns:
            包含标签列表的结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 获取小说的所有标签
            tags = [tag.to_dict() for tag in novel.tags]
            
            return {
                'success': True, 
                'tags': tags
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    @staticmethod
    def get_all_tags() -> Dict[str, Any]:
        """获取所有标签列表
        
        Returns:
            包含所有标签的结果字典
        """
        try:
            tags = Tag.query.all()
            
            return {
                'success': True,
                'tags': [tag.to_dict() for tag in tags]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    @staticmethod
    def get_all_chapters(novel_id: int) -> Dict[str, Any]:
        """获取小说的所有章节（不分页）
        
        与get_novel_chapters不同，此方法返回小说的所有章节，不进行分页处理，
        适用于需要获取全部章节列表的场景，如下载或全文搜索。
        
        Args:
            novel_id: 小说ID
            
        Returns:
            包含所有章节列表的结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 获取所有章节，按章节号排序
            chapters = NovelDAO.get_novel_chapters(novel_id)
            
            # 将章节信息转换为字典格式，不包含章节内容
            chapters_data = [chapter.to_dict(include_content=False) for chapter in chapters]
            
            return {
                'success': True,
                'novel_id': novel_id,
                'novel_title': novel.title,
                'total_chapters': len(chapters_data),
                'chapters': chapters_data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)} 