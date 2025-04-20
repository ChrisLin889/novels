from app.models.interaction import UserCollection, UserHistory, Comment, UserFollowing, PrivateMessage, UserTip
from app.models.novel import Novel, Chapter
from app.models.user import User
from app import db
from typing import Dict, Any, List, Optional
from sqlalchemy import desc
import datetime
from app.services.permission_service import PermissionService
from app.dao.interaction_dao import InteractionDAO

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
        return {
            'success': True,
            **result
        }
    
    @staticmethod
    def update_reading_history(user_id: int, novel_id: int, chapter_id: int) -> Dict[str, Any]:
        """Update user's reading history"""
        # Check if novel and chapter exist
        novel = Novel.query.get(novel_id)
        chapter = Chapter.query.get(chapter_id)
        
        if not novel or not chapter or chapter.novel_id != novel_id:
            return {'success': False, 'error': 'Invalid novel or chapter'}
        
        history = InteractionDAO.update_reading_history(user_id, novel_id, chapter_id)
        return {
            'success': True,
            'message': 'Reading history updated'
        }
    
    @staticmethod
    def get_reading_progress(user_id: int, novel_id: int) -> Dict[str, Any]:
        """Get reading progress for a novel"""
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Get reading history and chapter list
        history = InteractionDAO.get_reading_history(user_id, novel_id)
        chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number).all()
        
        # If no history, return first chapter
        if not history and chapters:
            first_chapter = chapters[0]
            return {
                'success': True,
                'current_chapter_id': first_chapter.id,
                'current_chapter_number': first_chapter.chapter_number,
                'current_chapter_title': first_chapter.title,
                'total_chapters': len(chapters),
                'progress_percentage': 0
            }
        
        # If history found, get progress percentage
        if history and chapters:
            current_chapter = Chapter.query.get(history.chapter_id)
            if current_chapter:
                progress_percentage = (current_chapter.chapter_number / len(chapters)) * 100
                return {
                    'success': True,
                    'current_chapter_id': history.chapter_id,
                    'current_chapter_number': current_chapter.chapter_number,
                    'current_chapter_title': current_chapter.title,
                    'last_read_time': history.last_read_time.isoformat(),
                    'total_chapters': len(chapters),
                    'progress_percentage': round(progress_percentage, 2)
                }
        
        return {'success': False, 'error': 'No reading history found'}
    
    @staticmethod
    def get_reading_history(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get user's reading history"""
        result = InteractionDAO.get_user_history(user_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def add_comment(user_id: int, novel_id: int, chapter_id: Optional[int], content: str) -> Dict[str, Any]:
        """Add a comment"""
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
            
        # Check if chapter exists if provided
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {'success': False, 'error': 'Invalid chapter'}
        
        comment = InteractionDAO.add_comment(user_id, novel_id, chapter_id, content)
        user = User.query.get(user_id)
        
        return {
            'success': True,
            'message': 'Comment added',
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
                return {'success': False, 'error': 'Invalid chapter'}
        
        result = InteractionDAO.get_comments(novel_id, chapter_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def delete_comment(user_id: int, comment_id: int) -> Dict[str, Any]:
        """Delete a comment"""
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'success': False, 'error': 'Comment not found'}
            
        # Check if user is the author of the comment
        if comment.user_id != user_id:
            # Check if user has moderation permissions
            if not PermissionService.can_moderate_comments(user_id):
                return {'success': False, 'error': 'Unauthorized'}
        
        result = InteractionDAO.delete_comment(comment_id)
        return {
            'success': result,
            'message': 'Comment deleted' if result else 'Failed to delete comment'
        }
    
    @staticmethod
    def follow_user(follower_id: int, followed_id: int) -> Dict[str, Any]:
        """Follow a user"""
        # Check if users exist
        follower = User.query.get(follower_id)
        followed = User.query.get(followed_id)
        
        if not follower or not followed:
            return {'success': False, 'error': 'User not found'}
            
        # Check if trying to follow self
        if follower_id == followed_id:
            return {'success': False, 'error': 'Cannot follow yourself'}
            
        result = InteractionDAO.follow_user(follower_id, followed_id)
        
        if not result:
            return {'success': False, 'error': 'Failed to follow user or already following'}
            
        return {
            'success': True,
            'message': f'Now following {followed.username}'
        }
    
    @staticmethod
    def unfollow_user(follower_id: int, followed_id: int) -> Dict[str, Any]:
        """Unfollow a user"""
        # Check if users exist
        follower = User.query.get(follower_id)
        followed = User.query.get(followed_id)
        
        if not follower or not followed:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.unfollow_user(follower_id, followed_id)
        
        if not result:
            return {'success': False, 'error': 'Not following this user'}
            
        return {
            'success': True,
            'message': f'Unfollowed {followed.username}'
        }
    
    @staticmethod
    def check_following(follower_id: int, followed_id: int) -> Dict[str, Any]:
        """Check if a user is following another user"""
        # Check if users exist
        follower = User.query.get(follower_id)
        followed = User.query.get(followed_id)
        
        if not follower or not followed:
            return {'success': False, 'error': 'User not found'}
            
        is_following = InteractionDAO.check_following(follower_id, followed_id)
        
        return {
            'success': True,
            'is_following': is_following
        }
    
    @staticmethod
    def get_followers(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get followers for a user"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_followers(user_id, page, per_page)
        return {'success': True, **result}
        
    @staticmethod
    def get_following(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get users followed by a user"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_following(user_id, page, per_page)
        return {'success': True, **result}
        
    @staticmethod
    def get_user_comments(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get comments made by a user"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_user_comments(user_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def send_message(sender_id: int, recipient_id: int, content: str) -> Dict[str, Any]:
        """Send a message to another user"""
        # Check if users exist
        sender = User.query.get(sender_id)
        recipient = User.query.get(recipient_id)
        
        if not sender or not recipient:
            return {'success': False, 'error': 'User not found'}
            
        if sender_id == recipient_id:
            return {'success': False, 'error': 'Cannot send message to yourself'}
            
        message = InteractionDAO.send_message(sender_id, recipient_id, content)
        
        if not message:
            return {'success': False, 'error': 'Failed to send message'}
            
        return {
            'success': True,
            'message': 'Message sent',
            'message_data': message.to_dict()
        }
    
    @staticmethod
    def mark_message_as_read(user_id: int, message_id: int) -> Dict[str, Any]:
        """Mark a message as read"""
        # Check if message exists
        message = PrivateMessage.query.get(message_id)
        if not message:
            return {'success': False, 'error': 'Message not found'}
            
        # Check if user is the recipient
        if message.recipient_id != user_id:
            return {'success': False, 'error': 'Unauthorized'}
            
        result = InteractionDAO.mark_message_as_read(message_id)
        
        return {
            'success': result,
            'message': 'Message marked as read' if result else 'Message already read or error occurred'
        }
    
    @staticmethod
    def get_conversation(user_id: int, other_user_id: int, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """Get conversation with another user"""
        # Check if users exist
        user = User.query.get(user_id)
        other_user = User.query.get(other_user_id)
        
        if not user or not other_user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_conversation(user_id, other_user_id, page, per_page)
        
        # Mark messages as read
        for message in result.get('messages', []):
            if message['recipient_id'] == user_id and not message.get('read_at'):
                InteractionDAO.mark_message_as_read(message['id'])
                
        # Add other user details
        result['other_user'] = other_user.to_dict()
                
        return {'success': True, **result}
    
    @staticmethod
    def get_inbox(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get user's inbox"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_inbox(user_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def send_tip(tipper_id: int, author_id: int, novel_id: int, 
                amount: int, message: Optional[str] = None, 
                chapter_id: Optional[int] = None) -> Dict[str, Any]:
        """Send a tip to an author"""
        # Check if users exist
        tipper = User.query.get(tipper_id)
        author = User.query.get(author_id)
        
        if not tipper or not author:
            return {'success': False, 'error': 'User not found'}
            
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
            
        # Check if the author owns the novel
        if novel.author != author.username:
            return {'success': False, 'error': 'This user is not the author of the novel'}
            
        # Check if chapter exists if provided
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {'success': False, 'error': 'Invalid chapter'}
                
        # Check if amount is valid
        if amount <= 0:
            return {'success': False, 'error': 'Tip amount must be positive'}
            
        # Check if user has enough balance (stub for future implementation)
        # if tipper.balance < amount:
        #     return {'success': False, 'error': 'Insufficient balance'}
            
        tip = InteractionDAO.send_tip(tipper_id, author_id, novel_id, amount, message, chapter_id)
        
        if not tip:
            return {'success': False, 'error': 'Failed to send tip'}
            
        # Update balances (stub for future implementation)
        # tipper.balance -= amount
        # author.balance += amount
        # db.session.commit()
            
        return {
            'success': True,
            'message': f'Sent {amount} coin tip to {author.username}',
            'tip': tip.to_dict()
        }
        
    @staticmethod
    def get_tips_received(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get tips received by a user"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_tips_received(user_id, page, per_page)
        return {'success': True, **result}
        
    @staticmethod
    def get_tips_sent(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get tips sent by a user"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_tips_sent(user_id, page, per_page)
        return {'success': True, **result} 