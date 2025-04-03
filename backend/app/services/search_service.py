from typing import List, Dict, Optional
from sqlalchemy import or_, and_, func
from app import db
from app.models.novel import Novel
from app.services.cache_service import CacheService, cached
from datetime import datetime, timedelta

# Cache prefixes
SEARCH_RESULT_PREFIX = "search_result:"
SEARCH_TRENDING_PREFIX = "search_trending:"
HOT_KEYWORDS_PREFIX = "hot_keywords"

class SearchService:
    """
    Service for handling search operations
    """
    
    @staticmethod
    @cached(SEARCH_RESULT_PREFIX, ttl=600)  # Cache search results for 10 minutes
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
        # Record this keyword in trending searches (non-blocking)
        SearchService.record_search_keyword(q)
        
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
        
        Args:
            keyword: The search keyword
        """
        # Use a Redis sorted set to track keyword frequency
        try:
            # Increment the keyword count in the sorted set
            # This is non-blocking and won't affect search performance
            from redis import Redis
            from app.services.cache_service import redis_client
            
            # Increment score for this keyword
            redis_client.zincrby(HOT_KEYWORDS_PREFIX, 1, keyword.lower())
            
            # Trim to keep only top 100 keywords
            redis_client.zremrangebyrank(HOT_KEYWORDS_PREFIX, 0, -101)
        except Exception as e:
            # Log but don't fail the search
            print(f"Failed to record search keyword: {str(e)}")
    
    @staticmethod
    def track_search_keyword(keyword):
        """
        Track search keywords for trending
        
        Args:
            keyword: Keyword to track
        """
        try:
            # Increment score for the keyword
            redis_client.zincrby("trending_searches", 1, keyword)
            
            # Trim the set to keep only top 100 keywords
            redis_client.zremrangebyrank("trending_searches", 0, -101)
        except Exception as e:
            print(f"Failed to record search keyword: {e}")
    
    @staticmethod
    @cached(SEARCH_TRENDING_PREFIX, ttl=3600)  # Cache for 1 hour
    def get_trending_keywords(limit=10):
        """
        Get trending search keywords
        
        Args:
            limit: Number of keywords to return
            
        Returns:
            List of trending keywords
        """
        try:
            # Get top keywords with scores
            keywords = redis_client.zrevrange("trending_searches", 0, limit-1, withscores=True)
            
            # Format results
            return [{"keyword": kw.decode('utf-8'), "count": int(score)} for kw, score in keywords]
        except Exception as e:
            print(f"Failed to get trending keywords: {e}")
            # Return empty list if Redis not available
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