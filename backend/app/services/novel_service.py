from app.models.novel import Novel, Chapter
from app.models.interaction import UserCollection, UserHistory, Comment
from app import db
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import desc, func
from app.services.cache_service import CacheService, cached

class NovelDAO:
    """
    Data Access Object for Novel and Chapter models
    Only handles interactions with the novel-related tables
    """
    
    @staticmethod
    def get_novel_by_id(novel_id: int) -> Optional[Novel]:
        """Retrieve novel by ID"""
        return Novel.query.get(novel_id)
    
    @staticmethod
    def get_novel_list(category: Optional[str] = None, page: int = 1, 
                      per_page: int = 10, sort_by: str = 'updated_at') -> Dict[str, Any]:
        """Get paginated list of novels with optional filtering"""
        query = Novel.query
        
        # Apply category filter if provided
        if category:
            query = query.filter_by(category=category)
        
        # Apply sorting
        if sort_by == 'view_count':
            query = query.order_by(desc(Novel.view_count))
        elif sort_by == 'collection_count':
            query = query.order_by(desc(Novel.collection_count))
        else:  # Default to updated_at
            query = query.order_by(desc(Novel.updated_at))
        
        # Execute paginated query
        novels = query.paginate(page=page, per_page=per_page)
        
        return {
            'total': novels.total,
            'pages': novels.pages,
            'current_page': page,
            'novels': [novel.to_dict() for novel in novels.items]
        }
    
    @staticmethod
    def search_novels(keyword: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Search novels by title or author"""
        query = Novel.query.filter(
            (Novel.title.ilike(f'%{keyword}%')) | 
            (Novel.author.ilike(f'%{keyword}%'))
        )
        
        novels = query.order_by(desc(Novel.updated_at)).paginate(page=page, per_page=per_page)
        
        return {
            'total': novels.total,
            'pages': novels.pages,
            'current_page': page,
            'novels': [novel.to_dict() for novel in novels.items]
        }
    
    @staticmethod
    def get_popular_novels(limit: int = 10) -> List[Novel]:
        """Get popular novels sorted by view count"""
        return Novel.query.order_by(desc(Novel.view_count)).limit(limit).all()
    
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
    def get_novel_chapters(novel_id: int, offset: int = 0, limit: int = 20) -> List[Chapter]:
        """Get chapters for a novel with pagination"""
        return Chapter.query.filter_by(novel_id=novel_id).order_by(
            Chapter.chapter_number
        ).offset(offset).limit(limit).all()
    
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
    def add_novel(title: str, author: str, category: str, intro: str, 
                 cover: str = 'default_cover.jpg', status: str = 'ongoing') -> Novel:
        """Add a new novel to the database"""
        novel = Novel(
            title=title,
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
    def add_chapter(novel_id: int, title: str, content: str, 
                   chapter_number: Optional[int] = None) -> Chapter:
        """Add a new chapter to a novel"""
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
    def update_novel(novel_id: int, data: Dict[str, Any]) -> Optional[Novel]:
        """Update novel information"""
        novel = Novel.query.get(novel_id)
        if not novel:
            return None
        
        # Update novel attributes
        allowed_fields = ['title', 'author', 'category', 'cover', 'intro', 'status']
        for key, value in data.items():
            if key in allowed_fields:
                setattr(novel, key, value)
        
        db.session.commit()
        return novel
    
    @staticmethod
    def update_chapter(chapter_id: int, data: Dict[str, Any]) -> Optional[Chapter]:
        """Update chapter information"""
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return None
        
        # Update chapter attributes
        if 'title' in data:
            chapter.title = data['title']
        
        if 'content' in data:
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
        
        db.session.delete(chapter)
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
    Service layer for novel-related operations
    Implements business logic and interacts with DAO
    """
    
    @staticmethod
    def get_novel_list(category: Optional[str] = None, page: int = 1, 
                      per_page: int = 10, sort_by: str = 'updated_at') -> Dict[str, Any]:
        """Get paginated list of novels with optional filtering"""
        if not category and not sort_by:
            return {'success': False, 'error': 'At least one filter is required'}
            
        result = NovelDAO.get_novel_list(category, page, per_page, sort_by)
        return {'success': True, **result}
    
    @staticmethod
    def search_novels(keyword: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Search novels by title or author"""
        if not keyword:
            return {'success': False, 'error': 'Search keyword is required'}
            
        result = NovelDAO.search_novels(keyword, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def get_novel_detail(novel_id: int) -> Dict[str, Any]:
        """Get novel details with chapters"""
        novel = NovelDAO.get_novel_by_id(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
            
        chapters = NovelDAO.get_novel_chapters(novel_id)
        return {
            'success': True,
            'novel': novel.to_dict(),
            'chapters': [chapter.to_dict() for chapter in chapters]
        }
    
    @staticmethod
    def get_popular_novels(limit: int = 10) -> Dict[str, Any]:
        """Get popular novels"""
        novels = NovelDAO.get_popular_novels(limit)
        return {
            'success': True,
            'novels': [novel.to_dict() for novel in novels]
        }
    
    @staticmethod
    def get_latest_novels(limit: int = 10) -> Dict[str, Any]:
        """Get latest novels"""
        novels = NovelDAO.get_latest_novels(limit)
        return {
            'success': True,
            'novels': [novel.to_dict() for novel in novels]
        }
    
    @staticmethod
    def get_categories() -> Dict[str, Any]:
        """Get list of categories with novel counts"""
        # Try to get from cache
        cached_data = CacheService.get("novel_categories")
        if cached_data:
            return {'success': True, 'categories': cached_data}
        
        # Query database
        categories = NovelDAO.get_categories()
        
        # Cache result
        CacheService.set("novel_categories", categories, 86400)  # Cache for 24 hours
        
        return {'success': True, 'categories': categories}
    
    @staticmethod
    def get_author_novels(author_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get novels created by a specific author"""
        try:
            # Get paginated results for internal author
            pagination = Novel.query.filter_by(author_id=author_id)\
                .order_by(Novel.updated_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            # Convert novels to dict
            novels = [novel.to_dict() for novel in pagination.items]
            
            return {
                'success': True,
                'novels': novels,
                'total': pagination.total,
                'total_pages': pagination.pages,
                'current_page': page
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def add_novel(title: str, author_name: str, category: str, intro: str, 
                  author_id: Optional[int] = None, cover: str = 'default_cover.jpg',
                  status: str = 'ongoing') -> Dict[str, Any]:
        """Add a new novel"""
        try:
            # 创建新小说
            novel = Novel(
                title=title,
                author=author_name,  # 使用作者名称
                author_id=author_id,  # 如果是内部作者，设置作者ID
                category=category,
                intro=intro,
                cover=cover,
                status=status
            )
            
            db.session.add(novel)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Novel added successfully',
                'novel': novel.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def update_novel(novel_id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> Dict[str, Any]:
        """Update novel information"""
        try:
            novel = Novel.query.get(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 检查权限：只有内部作者可以修改自己的小说
            if novel.author_id and novel.author_id != user_id:
                return {'success': False, 'error': 'Permission denied'}
            
            # 更新小说属性
            allowed_fields = ['title', 'author', 'category', 'cover', 'intro', 'status']
            for key, value in data.items():
                if key in allowed_fields:
                    setattr(novel, key, value)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Novel updated successfully',
                'novel': novel.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def add_chapter(author_id: int, novel_id: int, title: str, 
                   content: str, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """Add a new chapter to a novel (author only)"""
        # Check for missing required fields
        if not all([title, content]):
            return {'success': False, 'error': 'Missing required fields'}
        
        # Verify novel exists
        novel = NovelDAO.get_novel_by_id(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        try:
            chapter = NovelDAO.add_chapter(novel_id, title, content, chapter_number)
            
            # Invalidate cache for novel detail
            CacheService.delete(f"novel_detail:{novel_id}")
            
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
        
        try:
            updated_chapter = NovelDAO.update_chapter(chapter_id, data)
            
            # Invalidate cache for chapter
            CacheService.delete(f"chapter:{chapter_id}")
            
            return {
                'success': True,
                'message': 'Chapter updated successfully',
                'chapter': updated_chapter.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_novel(admin_id: int, novel_id: int) -> Dict[str, Any]:
        """Delete a novel (admin only)"""
        # Verify novel exists
        novel = NovelDAO.get_novel_by_id(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Get novel details for cache invalidation
        category = novel.category
        
        try:
            NovelDAO.delete_novel(novel_id)
            
            # Invalidate relevant caches
            CacheService.delete(f"novel_detail:{novel_id}")
            CacheService.delete(f"novel_list:all:1:10:updated_at")
            CacheService.delete(f"novel_list:{category}:1:10:updated_at")
            CacheService.delete("novel_categories")
            
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
        
        novel_id = chapter.novel_id
        
        try:
            NovelDAO.delete_chapter(chapter_id)
            
            # Invalidate relevant caches
            CacheService.delete(f"chapter:{chapter_id}")
            CacheService.delete(f"novel_detail:{novel_id}")
            
            return {
                'success': True,
                'message': 'Chapter deleted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def refresh_cache() -> Dict[str, Any]:
        """Force refresh of all novel-related caches"""
        try:
            result = CacheService.refresh_novel_cache()
            if result:
                return {
                    'success': True,
                    'message': 'Cache refreshed successfully'
                }
            else:
                return {'success': False, 'error': 'Failed to refresh cache'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
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
            novels = Novel.query.filter_by(author_id=author_id).all()
            
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