from app.models.interaction import UserCollection, UserHistory, Comment
from app.models.novel import Novel, Chapter
from app import db
from typing import Dict, Any, List, Optional
from sqlalchemy import desc
import datetime

class InteractionDAO:
    """
    Data Access Object for user interactions (collections, history, comments)
    """
    
    @staticmethod
    def get_user_collection(user_id: int, novel_id: int) -> Optional[UserCollection]:
        """Get collection record for a user and novel"""
        return UserCollection.query.filter_by(
            user_id=user_id,
            novel_id=novel_id
        ).first()
    
    @staticmethod
    def add_to_collection(user_id: int, novel_id: int) -> UserCollection:
        """Add a novel to user's collection"""
        collection = UserCollection(user_id=user_id, novel_id=novel_id)
        db.session.add(collection)
        
        # Update novel's collection count
        novel = Novel.query.get(novel_id)
        if novel:
            novel.collection_count += 1
        
        db.session.commit()
        return collection
    
    @staticmethod
    def remove_from_collection(user_id: int, novel_id: int) -> bool:
        """Remove a novel from user's collection"""
        collection = UserCollection.query.filter_by(
            user_id=user_id,
            novel_id=novel_id
        ).first()
        
        if not collection:
            return False
        
        db.session.delete(collection)
        
        # Update novel's collection count
        novel = Novel.query.get(novel_id)
        if novel:
            novel.collection_count = max(0, novel.collection_count - 1)
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_user_collections(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get paginated list of user's collections"""
        collections = UserCollection.query.filter_by(
            user_id=user_id
        ).order_by(
            desc(UserCollection.created_at)
        ).paginate(page=page, per_page=per_page)
        
        # Get novel details for each collection
        result = []
        for collection in collections.items:
            novel = Novel.query.get(collection.novel_id)
            if novel:
                novel_dict = novel.to_dict()
                novel_dict['collection_time'] = collection.created_at.isoformat()
                result.append(novel_dict)
        
        return {
            'total': collections.total,
            'pages': collections.pages,
            'current_page': page,
            'collections': result
        }
    
    @staticmethod
    def get_reading_history(user_id: int, novel_id: Optional[int] = None) -> Optional[UserHistory]:
        """Get reading history for a user and novel"""
        if novel_id:
            return UserHistory.query.filter_by(
                user_id=user_id,
                novel_id=novel_id
            ).first()
        return None
    
    @staticmethod
    def update_reading_history(user_id: int, novel_id: int, chapter_id: int) -> UserHistory:
        """Update user's reading history"""
        history = UserHistory.query.filter_by(
            user_id=user_id,
            novel_id=novel_id
        ).first()
        
        if history:
            history.chapter_id = chapter_id
            history.last_read_time = datetime.datetime.utcnow()
        else:
            history = UserHistory(
                user_id=user_id,
                novel_id=novel_id,
                chapter_id=chapter_id
            )
            db.session.add(history)
        
        db.session.commit()
        return history
    
    @staticmethod
    def get_user_history(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get paginated list of user's reading history"""
        history_records = UserHistory.query.filter_by(
            user_id=user_id
        ).order_by(
            desc(UserHistory.last_read_time)
        ).paginate(page=page, per_page=per_page)
        
        # Get novel and chapter details for each history record
        result = []
        for history in history_records.items:
            novel = Novel.query.get(history.novel_id)
            chapter = Chapter.query.get(history.chapter_id)
            
            if novel and chapter:
                record = {
                    'novel': novel.to_dict(),
                    'chapter': chapter.to_dict(),
                    'last_read_time': history.last_read_time.isoformat()
                }
                result.append(record)
        
        return {
            'total': history_records.total,
            'pages': history_records.pages,
            'current_page': page,
            'history': result
        }
    
    @staticmethod
    def add_comment(user_id: int, novel_id: int, chapter_id: Optional[int], content: str) -> Comment:
        """Add a comment to a novel or chapter"""
        comment = Comment(
            user_id=user_id,
            novel_id=novel_id,
            chapter_id=chapter_id,
            content=content
        )
        
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def get_comments(novel_id: int, chapter_id: Optional[int] = None, 
                    page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated comments for a novel or chapter"""
        query = Comment.query.filter_by(novel_id=novel_id)
        
        if chapter_id:
            query = query.filter_by(chapter_id=chapter_id)
        
        comments = query.order_by(desc(Comment.created_at)).paginate(page=page, per_page=per_page)
        
        # Get user info for each comment
        from app.models.user import User
        result = []
        for comment in comments.items:
            user = User.query.get(comment.user_id)
            if user:
                comment_dict = {
                    'id': comment.id,
                    'content': comment.content,
                    'created_at': comment.created_at.isoformat(),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'avatar': user.avatar
                    }
                }
                result.append(comment_dict)
        
        return {
            'total': comments.total,
            'pages': comments.pages,
            'current_page': page,
            'comments': result
        }
    
    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """Delete a comment"""
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        
        db.session.delete(comment)
        db.session.commit()
        return True


class InteractionService:
    """
    Service layer for user interactions
    """
    
    @staticmethod
    def toggle_collection(user_id: int, novel_id: int) -> Dict[str, Any]:
        """Toggle collection status for a novel"""
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if already in collection
        collection = InteractionDAO.get_user_collection(user_id, novel_id)
        
        if collection:
            # Remove from collection
            InteractionDAO.remove_from_collection(user_id, novel_id)
            return {
                'success': True,
                'message': 'Removed from collection',
                'is_collected': False
            }
        else:
            # Add to collection
            InteractionDAO.add_to_collection(user_id, novel_id)
            return {
                'success': True,
                'message': 'Added to collection',
                'is_collected': True
            }
    
    @staticmethod
    def get_collection_status(user_id: int, novel_id: int) -> Dict[str, Any]:
        """Check if a novel is in user's collection"""
        collection = InteractionDAO.get_user_collection(user_id, novel_id)
        return {
            'success': True,
            'is_collected': collection is not None
        }
    
    @staticmethod
    def get_user_collections(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get user's collection list"""
        result = InteractionDAO.get_user_collections(user_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def update_reading_history(user_id: int, novel_id: int, chapter_id: int) -> Dict[str, Any]:
        """Update user's reading history"""
        try:
            InteractionDAO.update_reading_history(user_id, novel_id, chapter_id)
            return {'success': True}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_reading_progress(user_id: int, novel_id: int) -> Dict[str, Any]:
        """Get user's reading progress for a novel"""
        history = InteractionDAO.get_reading_history(user_id, novel_id)
        
        if not history:
            return {
                'success': True,
                'has_history': False
            }
        
        chapter = Chapter.query.get(history.chapter_id)
        if not chapter:
            return {
                'success': True,
                'has_history': False
            }
        
        return {
            'success': True,
            'has_history': True,
            'chapter': chapter.to_dict(),
            'last_read_time': history.last_read_time.isoformat()
        }
    
    @staticmethod
    def get_reading_history(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get user's reading history"""
        result = InteractionDAO.get_user_history(user_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def add_comment(user_id: int, novel_id: int, content: str, chapter_id: Optional[int] = None) -> Dict[str, Any]:
        """Add a comment to a novel or chapter"""
        # Validate inputs
        if not content or len(content.strip()) == 0:
            return {'success': False, 'error': 'Comment content cannot be empty'}
        
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if chapter exists if provided
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {'success': False, 'error': 'Chapter not found or does not belong to this novel'}
        
        # Filter content (could use the utility for sensitive word filtering)
        from app.utils.security import filter_sensitive_words
        filtered_content = filter_sensitive_words(content)
        
        try:
            comment = InteractionDAO.add_comment(user_id, novel_id, chapter_id, filtered_content)
            
            # Get user info
            from app.models.user import User
            user = User.query.get(user_id)
            
            return {
                'success': True,
                'message': 'Comment added successfully',
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'created_at': comment.created_at.isoformat(),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'avatar': user.avatar
                    }
                }
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_comments(novel_id: int, chapter_id: Optional[int] = None, 
                    page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get comments for a novel or chapter"""
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if chapter exists if provided
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {'success': False, 'error': 'Chapter not found or does not belong to this novel'}
        
        result = InteractionDAO.get_comments(novel_id, chapter_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def delete_comment(user_id: int, comment_id: int) -> Dict[str, Any]:
        """Delete a comment (owner or admin only)"""
        # 动态导入以避免循环依赖
        from app.services.user_service import UserService
        
        # Get the comment
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'success': False, 'error': 'Comment not found'}
        
        # Check permissions
        is_owner = comment.user_id == user_id
        is_admin = UserService.check_permission(user_id, 'admin')
        
        if not (is_owner or is_admin):
            return {'success': False, 'error': 'Permission denied'}
        
        # Delete the comment
        success = InteractionDAO.delete_comment(comment_id)
        if success:
            return {
                'success': True,
                'message': 'Comment deleted successfully'
            }
        else:
            return {'success': False, 'error': 'Failed to delete comment'} 