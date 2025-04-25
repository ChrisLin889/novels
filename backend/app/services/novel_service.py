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
from app.dao.novel_dao import NovelDAO
from app.dao.interaction_dao import InteractionDAO
from app.services.admin_service import AdminService

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
    def get_author_novels(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """获取用户作为作者创建的小说列表
        
        Args:
            user_id: 用户ID（不是作者ID）
            page: 页码
            per_page: 每页数量
            
        Returns:
            包含作者小说列表和分页信息的字典
        """
        try:
            # 获取用户作为作者创建的小说查询
            query = NovelDAO.get_novel_by_user_id_query(user_id)
            
            # 应用分页
            pagination = query.order_by(desc(Novel.updated_at))\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            # 转换小说为字典
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
            
            # 敏感词过滤和检查
            has_sensitive, matches, filtered_intro = AdminService.filter_and_notify_sensitive_content(
                content=intro,
                user_id=user_id,
                content_type='novel',
                content_id=0  # 先设为0，小说创建后再更新
            )
            
            # Create new novel using DAO with filtered intro
            novel = NovelDAO.create_novel(
                title=title,
                author_id=author.id,
                author=author_name,
                category=category,
                intro=filtered_intro,
                cover=cover,
                status='ongoing'
            )
            
            # Add tags if provided
            if tags and isinstance(tags, list):
                NovelService.add_tags_to_novel(novel.id, tags)
            
            return {
                'success': True,
                'novel_id': novel.id,
                'novel': novel.to_dict(),
                'has_sensitive': has_sensitive
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
            # 获取作者对应的用户ID
            author = Author.query.get(author_id)
            if not author or not author.user_id:
                return {'success': False, 'error': 'Author not found or not associated with user'}
            
            # 敏感词过滤和检查
            has_sensitive, matches, filtered_content = AdminService.filter_and_notify_sensitive_content(
                content=content,
                user_id=author.user_id,
                content_type='chapter',
                content_id=0  # 先设为0，章节创建后再更新
            )
            
            # Create chapter using DAO with filtered content
            chapter = NovelDAO.create_chapter(novel_id, title, filtered_content, chapter_number)
            
            return {
                'success': True,
                'message': 'Chapter added successfully',
                'chapter': chapter.to_dict(),
                'has_sensitive': has_sensitive
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_chapter(user_id: int, chapter_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
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
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(user_id) == 'admin'
        
        # If not admin, verify user is the author of the novel
        if not is_admin:
            author = Author.query.filter_by(user_id=user_id).first()
            if not author or novel.author_id != author.id:
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
    def delete_chapter(user_id: int, chapter_id: int) -> Dict[str, Any]:
        """Delete a chapter (author or admin only)
        
        Args:
            user_id: User ID of the requester
            chapter_id: Chapter ID to delete
            
        Returns:
            Dictionary with operation result
        """
        # Verify chapter exists
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            return {'success': False, 'error': 'Chapter not found'}
        
        # Get novel to check ownership
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(user_id) == 'admin'
        
        # If not admin, verify user is the author of the novel
        if not is_admin:
            author = Author.query.filter_by(user_id=user_id).first()
            if not author or novel.author_id != author.id:
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
        print(f"DEBUG - NovelService.get_chapter开始, chapter_id={chapter_id}, user_id={user_id}")
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            print(f"DEBUG - 章节不存在: chapter_id={chapter_id}")
            return {'success': False, 'error': 'Chapter not found'}
            
        # Get novel for this chapter
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            print(f"DEBUG - 小说不存在: novel_id={chapter.novel_id}")
            return {'success': False, 'error': 'Novel not found'}
            
        # Get adjacent chapters
        prev_chapter, next_chapter = NovelDAO.get_adjacent_chapters(chapter)
        
        # Update reading history if user is logged in
        if user_id:
            print(f"DEBUG - 准备更新阅读历史: user_id={user_id}, novel_id={novel.id}, chapter_id={chapter.id}")
            try:
                history = InteractionDAO.update_reading_history(user_id, novel.id, chapter.id)
                print(f"DEBUG - 阅读历史更新成功: history_id={history.id if history else 'None'}")
            except Exception as e:
                print(f"DEBUG - 阅读历史更新失败: {str(e)}")
        else:
            print("DEBUG - 没有用户ID, 跳过阅读历史更新")
            
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
    def get_author_stats(user_id: int) -> Dict[str, Any]:
        """获取用户作为作者的统计数据
        
        Args:
            user_id: 用户ID（不是作者ID）
            
        Returns:
            包含作者统计数据的字典
        """
        try:
            # 获取用户作为作者创建的小说列表
            novels = NovelDAO.get_novel_by_user_id_query(user_id).all()
            
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