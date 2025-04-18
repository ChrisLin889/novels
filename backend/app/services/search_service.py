from typing import List, Dict, Optional
from sqlalchemy import or_, and_, func
from app import db
from app.models.novel import Novel
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for handling search operations
    """
    
    @staticmethod
    def search_novels(
        q: str, 
        page: int = 1, 
        per_page: int = 20
    ) -> Dict:
        """
        Search novels by keyword (title or author)
        
        Args:
            q: Search keyword
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with search results and pagination info
        """
        # Build the query
        query = Novel.query
        
        # Apply keyword search (in title or author)
        if q:
            query = query.filter(or_(
                Novel.title.ilike(f'%{q}%'),
                Novel.author.ilike(f'%{q}%')
            ))
        
        # Get total count for pagination
        total = query.count()
        
        # Apply pagination
        results = query.order_by(Novel.updated_at.desc()) \
                      .offset((page - 1) * per_page) \
                      .limit(per_page) \
                      .all()
                      
        # Prepare response
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'results': [novel.to_dict() for novel in results]
        }
    
    @staticmethod
    def record_search_keyword(keyword: str) -> None:
        """
        Record search keyword for trending analysis
        This method is kept for compatibility but no longer stores data in Redis
        
        Args:
            keyword: The search keyword
        """
        # No longer tracking search keywords after Redis removal
        pass
    
    @staticmethod
    def track_search_keyword(keyword):
        """
        Track search keywords for trending
        This method is kept for compatibility but no longer stores data in Redis
        
        Args:
            keyword: Keyword to track
        """
        # No longer tracking search keywords after Redis removal
        pass
    
    @staticmethod
    def get_trending_keywords(limit=10):
        """
        Get trending search keywords
        Now returns empty list since Redis tracking is removed
        
        Args:
            limit: Number of keywords to return
            
        Returns:
            Empty list (Redis functionality removed)
        """
        # No longer have trending keywords after Redis removal
        return []
    
    @staticmethod
    def search_by_tag(tag: str, page: int = 1, per_page: int = 20) -> Dict:
        """
        Search novels by tag
        
        Args:
            tag: Tag to search for
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with search results and pagination info
        """
        # Assuming tags are stored in Novel.tags field or a separate tags table
        # This is a simplified implementation - adjust based on your data model
        
        query = Novel.query.filter(Novel.tags.ilike(f'%{tag}%'))
        
        # Get total count for pagination
        total = query.count()
        
        # Apply pagination
        results = query.order_by(Novel.updated_at.desc()) \
                      .offset((page - 1) * per_page) \
                      .limit(per_page) \
                      .all()
                      
        # Prepare response
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'results': [novel.to_dict() for novel in results]
        }
        
    @staticmethod
    def suggest_similar_novels(novel_id: int, limit: int = 5) -> List[Dict]:
        """
        Suggest similar novels based on category and tags
        
        Args:
            novel_id: ID of the novel to find similar ones for
            limit: Number of suggestions to return
            
        Returns:
            List of similar novels
        """
        novel = Novel.query.get(novel_id)
        if not novel:
            return []
            
        # Find novels with same category
        similar_novels = Novel.query.filter(
            and_(
                Novel.category == novel.category,
                Novel.id != novel_id
            )
        ).order_by(
            Novel.view_count.desc()  # Sort by popularity
        ).limit(limit).all()
        
        return [n.to_dict() for n in similar_novels] 