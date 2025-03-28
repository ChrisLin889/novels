from typing import List, Dict, Optional
from sqlalchemy import or_, and_, desc, func
from app import db
from app.models.novel import Novel
from datetime import datetime

class SearchDAO:
    """
    Data Access Object for search operations
    """
    
    @staticmethod
    def search_novels(
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        min_words: Optional[int] = None,
        max_words: Optional[int] = None,
        status: Optional[str] = None,
        updated_after: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 20
    ) -> tuple:
        """
        Search novels with filters
        
        Args:
            keyword: Search keyword for title, author, or intro
            category: Novel category
            min_words: Minimum word count
            max_words: Maximum word count
            status: Novel status (ongoing, completed)
            updated_after: Last updated after this date
            page: Page number (1-indexed)
            per_page: Items per page
            
        Returns:
            Tuple of (novels, total_count)
        """
        query = Novel.query
        
        # Apply search criteria
        if keyword:
            query = query.filter(or_(
                Novel.title.ilike(f'%{keyword}%'),
                Novel.author.ilike(f'%{keyword}%'),
                Novel.intro.ilike(f'%{keyword}%')
            ))
        
        if category:
            query = query.filter(Novel.category == category)
            
        if status:
            query = query.filter(Novel.status == status)
        
        if min_words:
            # Assuming total_words field exists, otherwise needs JOIN with Chapter
            query = query.filter(Novel.total_words >= min_words)
            
        if max_words:
            query = query.filter(Novel.total_words <= max_words)
            
        if updated_after:
            query = query.filter(Novel.updated_at >= updated_after)
            
        # Get total count for pagination
        total = query.count()
        
        # Apply pagination and sorting
        novels = query.order_by(desc(Novel.updated_at))\
                      .offset((page - 1) * per_page)\
                      .limit(per_page)\
                      .all()
                      
        return novels, total
    
    @staticmethod
    def search_by_tag(tag: str, page: int = 1, per_page: int = 20) -> tuple:
        """
        Search novels by tag
        
        Args:
            tag: Tag to search for
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (novels, total_count)
        """
        # Assuming tags are stored in Novel.tags field
        query = Novel.query.filter(Novel.tags.ilike(f'%{tag}%'))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        novels = query.order_by(desc(Novel.updated_at))\
                     .offset((page - 1) * per_page)\
                     .limit(per_page)\
                     .all()
                     
        return novels, total
    
    @staticmethod
    def get_similar_novels(novel_id: int, limit: int = 5) -> List[Novel]:
        """
        Find novels similar to the given novel
        
        Args:
            novel_id: ID of the novel to find similar ones for
            limit: Maximum number of similar novels to return
            
        Returns:
            List of similar Novel objects
        """
        # Get the target novel
        novel = Novel.query.get(novel_id)
        if not novel:
            return []
            
        # Find novels with the same category but not the same novel
        similar_novels = Novel.query.filter(
            and_(
                Novel.category == novel.category,
                Novel.id != novel_id
            )
        ).order_by(
            desc(Novel.view_count)  # Sort by popularity
        ).limit(limit).all()
        
        return similar_novels
    
    @staticmethod
    def get_category_novels(category: str, page: int = 1, per_page: int = 20) -> tuple:
        """
        Get novels by category
        
        Args:
            category: Novel category
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (novels, total_count)
        """
        query = Novel.query.filter(Novel.category == category)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        novels = query.order_by(desc(Novel.updated_at))\
                     .offset((page - 1) * per_page)\
                     .limit(per_page)\
                     .all()
                     
        return novels, total
    
    @staticmethod
    def log_search_query(user_id: Optional[int], keyword: str) -> None:
        """
        Log a search query for analytics
        
        Args:
            user_id: ID of user making the search (None for anonymous)
            keyword: Search keyword
        """
        # You would implement this with a SearchHistory model
        # Example implementation:
        # search_log = SearchHistory(
        #     user_id=user_id,
        #     keyword=keyword,
        #     timestamp=datetime.utcnow()
        # )
        # db.session.add(search_log)
        # db.session.commit()
        pass 