from app.models.novel import Novel, Chapter, novel_tag
from app.models.interaction import UserCollection, UserHistory, Comment
from app.models.user import User
from app.models.author import Author
from app.models.tag import Tag
from app.models.category import Category
from app import db
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import desc, func
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