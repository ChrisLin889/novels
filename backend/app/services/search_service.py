from typing import List, Dict, Optional
from sqlalchemy import or_, and_, func
from app import db
from app.models.novel import Novel
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class SearchDAO:
    """
    Data Access Object for search-related operations
    Only handles direct database queries with no business logic
    """
    
    @staticmethod
    def search_novels_query(q: str):
        """
        Create query for searching novels by keyword
        
        Args:
            q: Search keyword
            
        Returns:
            SQLAlchemy query object
        """
        query = Novel.query
        
        # Apply keyword search
        if q:
            query = query.filter(or_(
                Novel.title.ilike(f'%{q}%'),
                Novel.author.ilike(f'%{q}%'),
                Novel.intro.ilike(f'%{q}%')  # Search in intro field
            ))
            
        return query
    
    @staticmethod
    def search_by_tag_query(tag: str):
        """
        Create query for searching novels by tag
        
        Args:
            tag: Tag to search for
            
        Returns:
            SQLAlchemy query object
        """
        # Search for novels with the given tag
        return Novel.query.filter(
            Novel.tags.any(name=tag)
        )
    
    @staticmethod
    def get_similar_novels_query(novel: Novel, limit: int = 5):
        """
        Create query for finding similar novels based on tags and category
        
        Args:
            novel: Novel to find similar ones for
            limit: Maximum number of similar novels
            
        Returns:
            SQLAlchemy query object
        """
        # Check if the novel has tags
        novel_tags = novel.tags.all()
        
        if novel_tags:
            # If the novel has tags, find novels with similar tags
            # First get novels with at least one common tag, ordered by tag count
            from sqlalchemy import func
            
            # Subquery to count matching tags for each novel
            subquery = db.session.query(
                novel_tag.c.novel_id,
                func.count(novel_tag.c.tag_id).label('tag_count')
            ).filter(
                novel_tag.c.tag_id.in_([tag.id for tag in novel_tags]),
                novel_tag.c.novel_id != novel.id
            ).group_by(
                novel_tag.c.novel_id
            ).subquery()
            
            # Query novels with matching tags, ordered by tag count
            query = Novel.query.join(
                subquery, Novel.id == subquery.c.novel_id
            ).order_by(
                subquery.c.tag_count.desc(),  # Sort by tag similarity
                Novel.view_count.desc()       # Then by popularity
            ).limit(limit)
            
            # Check if we have enough results
            results_count = query.count()
            
            # If we don't have enough similar novels by tags, add some from the same category
            if results_count < limit:
                # Get IDs of novels we already have
                existing_ids = [n.id for n in query.all()]
                
                # Get additional novels from the same category
                additional_query = Novel.query.filter(
                    and_(
                        Novel.category == novel.category,
                        Novel.id != novel.id,
                        ~Novel.id.in_(existing_ids)  # Exclude novels we already have
                    )
                ).order_by(
                    Novel.view_count.desc()  # Sort by popularity
                ).limit(limit - results_count)
                
                # Combine the results
                from sqlalchemy import union_all
                query = union_all(query, additional_query)
            
            return query
        else:
            # If the novel has no tags, find novels with the same category
            return Novel.query.filter(
                and_(
                    Novel.category == novel.category,
                    Novel.id != novel.id
                )
            ).order_by(
                Novel.view_count.desc()  # Sort by popularity
            ).limit(limit)

class SearchService:
    """
    Service for handling search operations
    Handles business logic, error handling, and response formatting
    """
    
    @staticmethod
    def search_novels(
        q: str, 
        page: int = 1, 
        per_page: int = 20
    ) -> Dict:
        """
        Search novels by keyword
        
        Args:
            q: Search keyword
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with search results and pagination info
        """
        try:
            # Build the query
            query = SearchDAO.search_novels_query(q)
            
            # Get total count for pagination
            total = query.count()
            
            # Apply pagination
            results = query.order_by(Novel.updated_at.desc()) \
                          .offset((page - 1) * per_page) \
                          .limit(per_page) \
                          .all()
                          
            # Prepare response
            return {
                'success': True,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'results': [novel.to_dict() for novel in results]
            }
        except Exception as e:
            logger.error(f"Error in search_novels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
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
        try:
            # Get query for tag search
            query = SearchDAO.search_by_tag_query(tag)
            
            # Get total count for pagination
            total = query.count()
            
            # Apply pagination
            results = query.order_by(Novel.updated_at.desc()) \
                          .offset((page - 1) * per_page) \
                          .limit(per_page) \
                          .all()
                          
            # Prepare response
            return {
                'success': True,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'results': [novel.to_dict() for novel in results]
            }
        except Exception as e:
            logger.error(f"Error in search_by_tag: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        
    @staticmethod
    def suggest_similar_novels(novel_id: int, limit: int = 5) -> Dict:
        """
        Suggest similar novels based on category and tags
        
        Args:
            novel_id: ID of the novel to find similar ones for
            limit: Number of suggestions to return
            
        Returns:
            Dict with similar novels
        """
        try:
            novel = Novel.query.get(novel_id)
            if not novel:
                return {
                    'success': False,
                    'error': 'Novel not found'
                }
                
            # Get query for similar novels
            query = SearchDAO.get_similar_novels_query(novel, limit)
            similar_novels = query.all()
            
            return {
                'success': True,
                'results': [n.to_dict() for n in similar_novels]
            }
        except Exception as e:
            logger.error(f"Error in suggest_similar_novels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
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
    def get_hot_tags(limit: int = 20, category_id: Optional[int] = None) -> Dict:
        """
        Get hot tags (ordered by usage frequency)
        
        Args:
            limit: Number of tags to return
            category_id: Category ID (optional)
            
        Returns:
            Dict with hot tags
        """
        try:
            from app.models.tag import Tag
            
            # Base query - count how many novels use each tag
            query = db.session.query(
                Tag,
                func.count(novel_tag.c.novel_id).label('novel_count')
            ).outerjoin(
                novel_tag,
                Tag.id == novel_tag.c.tag_id
            )
            
            # Filter by category if provided
            if category_id:
                query = query.filter(Tag.category_id == category_id)
            
            # Group by tag, order by usage count and limit the results
            query = query.group_by(Tag.id).order_by(db.desc('novel_count')).limit(limit)
            
            # Execute query
            result = query.all()
            
            # Format the response
            tags = []
            for tag, novel_count in result:
                tag_dict = tag.to_dict()
                tag_dict['novel_count'] = novel_count
                
                # Add category name if tag has a category
                if tag.category:
                    tag_dict['category_name'] = tag.category.name
                
                tags.append(tag_dict)
            
            return {
                'success': True,
                'tags': tags
            }
        except Exception as e:
            logger.error(f"Error in get_hot_tags: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 