from app.models.novel import Novel, Chapter, AuditStatus
from app.models.interaction import UserCollection, UserHistory, Comment
from app.models.user import User
from app.models.author import Author
from app.models.tag import Tag
from app.models.category import Category
from app import db
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import desc, func, asc, or_
from datetime import datetime
from app.config.settings import get_settings

class NovelDAO:
    """
    Data Access Object for Novel and Chapter models
    Only handles direct database interactions with no business logic
    """
    
    @staticmethod
    def get_novel_by_id(novel_id: int) -> Optional[Novel]:
        """Retrieve novel by ID"""
        return Novel.query.filter_by(id=novel_id, is_deleted=False).first()
    
    @staticmethod
    def get_novel_list_query(category: Optional[str] = None, status: Optional[str] = None, 
                           audit_status: str = AuditStatus.APPROVED):
        """Get base query for novels with filters"""
        query = Novel.query.filter_by(is_deleted=False)
        
        # Enable content audit based on settings
        settings = get_settings()
        if settings.get('enable_content_audit', True):
            query = query.filter_by(audit_status=audit_status)
        
        # Add filters if provided
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
            
        return query
    
    @staticmethod
    def apply_sorting(query, sort_by='updated_at', sort_order='desc'):
        """Apply sorting to a query"""
        # Validate sort fields
        valid_sort_fields = ['created_at', 'updated_at', 'view_count', 'collection_count', 'title']
        if sort_by not in valid_sort_fields:
            sort_by = 'updated_at'
            
        # Apply sorting
        if sort_order.lower() == 'asc':
            return query.order_by(asc(getattr(Novel, sort_by)))
        else:
            return query.order_by(desc(getattr(Novel, sort_by)))
    
    @staticmethod
    def search_novels_query(keyword: str, category: Optional[str] = None):
        """Create query for novel search"""
        # Base query - only return approved novels by default
        settings = get_settings()
        query = Novel.query.filter_by(is_deleted=False)
        
        if settings.get('enable_content_audit', True):
            query = query.filter_by(audit_status=AuditStatus.APPROVED)
        
        # Add search conditions
        search_conditions = or_(
            Novel.title.contains(keyword),
            Novel.intro.contains(keyword),
            Novel.author.contains(keyword)
        )
        query = query.filter(search_conditions)
        
        # Add category filter if provided
        if category:
            query = query.filter_by(category=category)
            
        return query
    
    @staticmethod
    def get_novel_by_author_query(author_id: int):
        """Get query for novels by author ID"""
        return Novel.query.filter_by(author_id=author_id)
    
    @staticmethod
    def get_novel_by_user_id_query(user_id: int):
        """获取用户(通过作者身份)创建的小说查询
        
        此方法处理用户ID到作者ID的映射，解决API层直接使用用户ID的问题。
        首先查找用户对应的作者记录，然后返回该作者创建的小说查询。
        
        Args:
            user_id: 用户ID
            
        Returns:
            对应作者创建的小说查询，如果用户不是作者则返回空查询
        """
        # 先找到该用户对应的作者记录
        author = Author.query.filter_by(user_id=user_id).first()
        if not author:
            return Novel.query.filter(False)  # 返回一个空查询
        # 返回该作者的小说查询
        return Novel.query.filter_by(author_id=author.id)
    
    @staticmethod
    def get_popular_novels_query(category: Optional[str] = None):
        """Create query for popular novels"""
        query = Novel.query.filter_by(is_deleted=False)
        
        # Enable content audit based on settings
        settings = get_settings()
        if settings.get('enable_content_audit', True):
            query = query.filter_by(audit_status=AuditStatus.APPROVED)
        
        # Add category filter if provided
        if category:
            query = query.filter_by(category=category)
            
        # Order by popularity (view count)
        query = query.order_by(desc(Novel.view_count))
        
        return query
    
    @staticmethod
    def get_latest_novels(limit: int = 10) -> List[Novel]:
        """Get latest novels sorted by updated time"""
        return Novel.query.order_by(desc(Novel.updated_at)).limit(limit).all()
    
    @staticmethod
    def increment_view_count(novel_id: int) -> bool:
        """Increment the view count of a novel"""
        try:
            novel = Novel.query.get(novel_id)
            if novel:
                novel.view_count = Novel.view_count + 1
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_chapter_by_id(chapter_id: int) -> Optional[Chapter]:
        """Retrieve chapter by ID"""
        return Chapter.query.filter_by(id=chapter_id, is_deleted=False).first()
    
    @staticmethod
    def get_chapter_by_number(novel_id: int, chapter_number: int) -> Optional[Chapter]:
        """Retrieve chapter by novel ID and chapter number"""
        return Chapter.query.filter_by(
            novel_id=novel_id,
            chapter_number=chapter_number
        ).first()
    
    @staticmethod
    def get_novel_chapters(novel_id: int, include_pending: bool = False):
        """Get chapters for a novel"""
        query = Chapter.query.filter_by(novel_id=novel_id, is_deleted=False)
        
        # Filter by audit status if needed
        settings = get_settings()
        if settings.get('enable_content_audit', True) and not include_pending:
            query = query.filter_by(audit_status=AuditStatus.APPROVED)
            
        return query.order_by(Chapter.chapter_number).all()
    
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
        """Get list of novel categories with counts"""
        # 从Category表中查询分类
        novel_categories = db.session.query(Category).filter_by(type='novel').all()
        
        # 查询每个分类的小说数量
        result = []
        for category in novel_categories:
            count = Novel.query.filter_by(category=category.name).count()
            result.append({
                'name': category.name,
                'count': count,
                'description': category.description
            })
            
        return result
    
    @staticmethod
    def get_author_novels(author_id: int, include_pending: bool = True):
        """Get novels by author ID"""
        query = Novel.query.filter_by(author_id=author_id, is_deleted=False)
        
        # Include all novels regardless of audit status for the author
        if not include_pending:
            settings = get_settings()
            if settings.get('enable_content_audit', True):
                query = query.filter_by(audit_status=AuditStatus.APPROVED)
                
        return query.order_by(desc(Novel.updated_at))
    
    @staticmethod
    def get_pending_novels_query():
        """Get query for pending novels"""
        return Novel.query.filter_by(
            is_deleted=False, 
            audit_status=AuditStatus.PENDING
        ).order_by(desc(Novel.created_at))
    
    @staticmethod
    def get_pending_chapters_query():
        """Get query for pending chapters"""
        return Chapter.query.filter_by(
            is_deleted=False, 
            audit_status=AuditStatus.PENDING
        ).order_by(desc(Chapter.created_at))
    
    @staticmethod
    def get_author_pending_content(author_id: int):
        """Get pending content for an author"""
        # Get pending novels
        pending_novels = Novel.query.filter_by(
            author_id=author_id,
            is_deleted=False
        ).filter(
            Novel.audit_status.in_([AuditStatus.PENDING, AuditStatus.REJECTED])
        ).all()
        
        # Get pending chapters
        pending_chapters_query = db.session.query(Chapter).join(
            Novel, Novel.id == Chapter.novel_id
        ).filter(
            Novel.author_id == author_id,
            Chapter.is_deleted == False,
            Chapter.audit_status.in_([AuditStatus.PENDING, AuditStatus.REJECTED])
        )
        
        pending_chapters = pending_chapters_query.all()
        
        return {
            'novels': [novel.to_dict() for novel in pending_novels],
            'chapters': [chapter.to_dict() for chapter in pending_chapters]
        }
    
    @staticmethod
    def update_audit_status(content_type: str, content_id: int, status: str):
        """Update audit status for novel or chapter"""
        try:
            if content_type == 'novel':
                content = Novel.query.get(content_id)
            elif content_type == 'chapter':
                content = Chapter.query.get(content_id)
            else:
                return False
                
            if not content:
                return False
                
            content.audit_status = status
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False 