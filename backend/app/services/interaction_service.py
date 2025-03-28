from app.models.interaction import UserCollection, UserHistory, Comment, UserFollowing, PrivateMessage, UserTip
from app.models.novel import Novel, Chapter
from app.models.user import User
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
        
    @staticmethod
    def follow_user(follower_id: int, followed_id: int) -> Optional[UserFollowing]:
        """Follow a user"""
        # Prevent self-following
        if follower_id == followed_id:
            return None
            
        # Check if already following
        existing = UserFollowing.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()
        
        if existing:
            return existing
            
        # Create new following
        following = UserFollowing(
            follower_id=follower_id,
            followed_id=followed_id
        )
        
        db.session.add(following)
        db.session.commit()
        return following
        
    @staticmethod
    def unfollow_user(follower_id: int, followed_id: int) -> bool:
        """Unfollow a user"""
        following = UserFollowing.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()
        
        if not following:
            return False
            
        db.session.delete(following)
        db.session.commit()
        return True
        
    @staticmethod
    def check_following(follower_id: int, followed_id: int) -> bool:
        """Check if a user is following another user"""
        following = UserFollowing.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()
        
        return following is not None
        
    @staticmethod
    def get_followers(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of user's followers"""
        followers = UserFollowing.query.filter_by(
            followed_id=user_id
        ).order_by(
            desc(UserFollowing.created_at)
        ).paginate(page=page, per_page=per_page)
        
        result = []
        for following in followers.items:
            user = User.query.get(following.follower_id)
            if user:
                user_dict = user.to_dict()
                user_dict['following_since'] = following.created_at.isoformat()
                result.append(user_dict)
                
        return {
            'total': followers.total,
            'pages': followers.pages,
            'current_page': page,
            'followers': result
        }
        
    @staticmethod
    def get_following(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of users being followed by user_id"""
        following = UserFollowing.query.filter_by(
            follower_id=user_id
        ).order_by(
            desc(UserFollowing.created_at)
        ).paginate(page=page, per_page=per_page)
        
        result = []
        for follow in following.items:
            user = User.query.get(follow.followed_id)
            if user:
                user_dict = user.to_dict()
                user_dict['following_since'] = follow.created_at.isoformat()
                result.append(user_dict)
                
        return {
            'total': following.total,
            'pages': following.pages,
            'current_page': page,
            'following': result
        }
        
    @staticmethod
    def send_message(sender_id: int, recipient_id: int, content: str) -> Optional[PrivateMessage]:
        """Send a private message to another user"""
        # Prevent self-messaging
        if sender_id == recipient_id:
            return None
            
        message = PrivateMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )
        
        db.session.add(message)
        db.session.commit()
        return message
        
    @staticmethod
    def mark_message_as_read(message_id: int) -> bool:
        """Mark a message as read"""
        message = PrivateMessage.query.get(message_id)
        if not message or message.read_at:
            return False
            
        message.read_at = datetime.datetime.utcnow()
        db.session.commit()
        return True
        
    @staticmethod
    def get_conversation(user1_id: int, user2_id: int, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """Get paginated conversation between two users"""
        messages = PrivateMessage.query.filter(
            ((PrivateMessage.sender_id == user1_id) & (PrivateMessage.recipient_id == user2_id)) |
            ((PrivateMessage.sender_id == user2_id) & (PrivateMessage.recipient_id == user1_id))
        ).order_by(PrivateMessage.created_at)
        
        messages = messages.paginate(page=page, per_page=per_page)
        
        result = []
        for message in messages.items:
            message_dict = message.to_dict()
            message_dict['sender'] = User.query.get(message.sender_id).to_dict()
            result.append(message_dict)
            
        return {
            'total': messages.total,
            'pages': messages.pages,
            'current_page': page,
            'messages': result
        }
        
    @staticmethod
    def get_inbox(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated inbox for a user"""
        messages = PrivateMessage.query.filter_by(
            recipient_id=user_id
        ).order_by(
            desc(PrivateMessage.created_at)
        ).paginate(page=page, per_page=per_page)
        
        result = []
        for message in messages.items:
            sender = User.query.get(message.sender_id)
            if sender:
                message_dict = message.to_dict()
                message_dict['sender'] = sender.to_dict()
                result.append(message_dict)
                
        return {
            'total': messages.total,
            'pages': messages.pages,
            'current_page': page,
            'messages': result,
            'unread_count': PrivateMessage.query.filter_by(
                recipient_id=user_id, 
                read_at=None
            ).count()
        }
        
    @staticmethod
    def send_tip(tipper_id: int, author_id: int, novel_id: int, 
                 amount: int, message: Optional[str] = None, 
                 chapter_id: Optional[int] = None) -> Optional[UserTip]:
        """Send a tip to an author"""
        # Validate novel and author
        novel = Novel.query.get(novel_id)
        if not novel or novel.author != User.query.get(author_id).username:
            return None
            
        # Validate chapter if provided
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return None
                
        # Create tip
        tip = UserTip(
            tipper_id=tipper_id,
            author_id=author_id,
            novel_id=novel_id,
            chapter_id=chapter_id,
            amount=amount,
            message=message
        )
        
        db.session.add(tip)
        db.session.commit()
        return tip
        
    @staticmethod
    def get_tips_received(author_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated tips received by an author"""
        tips = UserTip.query.filter_by(
            author_id=author_id
        ).order_by(
            desc(UserTip.created_at)
        ).paginate(page=page, per_page=per_page)
        
        result = []
        for tip in tips.items:
            tipper = User.query.get(tip.tipper_id)
            novel = Novel.query.get(tip.novel_id)
            chapter = Chapter.query.get(tip.chapter_id) if tip.chapter_id else None
            
            if tipper and novel:
                tip_dict = tip.to_dict()
                tip_dict['tipper'] = tipper.to_dict()
                tip_dict['novel'] = novel.to_dict()
                if chapter:
                    tip_dict['chapter'] = chapter.to_dict()
                result.append(tip_dict)
                
        return {
            'total': tips.total,
            'pages': tips.pages,
            'current_page': page,
            'tips': result,
            'total_amount': sum(tip.amount for tip in UserTip.query.filter_by(author_id=author_id).all())
        }
        
    @staticmethod
    def get_tips_sent(tipper_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated tips sent by a user"""
        tips = UserTip.query.filter_by(
            tipper_id=tipper_id
        ).order_by(
            desc(UserTip.created_at)
        ).paginate(page=page, per_page=per_page)
        
        result = []
        for tip in tips.items:
            author = User.query.get(tip.author_id)
            novel = Novel.query.get(tip.novel_id)
            chapter = Chapter.query.get(tip.chapter_id) if tip.chapter_id else None
            
            if author and novel:
                tip_dict = tip.to_dict()
                tip_dict['author'] = author.to_dict()
                tip_dict['novel'] = novel.to_dict()
                if chapter:
                    tip_dict['chapter'] = chapter.to_dict()
                result.append(tip_dict)
                
        return {
            'total': tips.total,
            'pages': tips.pages,
            'current_page': page,
            'tips': result,
            'total_amount': sum(tip.amount for tip in UserTip.query.filter_by(tipper_id=tipper_id).all())
        }

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
    def add_comment(user_id: int, novel_id: int, content: str, chapter_id: Optional[int] = None) -> Dict[str, Any]:
        """Add a comment to a novel or chapter"""
        # Validate input
        if not content or len(content.strip()) < 1:
            return {
                'success': False,
                'error': 'Comment cannot be empty'
            }
            
        # Check content length
        if len(content) > 1000:
            return {
                'success': False,
                'error': 'Comment is too long (maximum 1000 characters)'
            }
            
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {
                'success': False,
                'error': 'Novel not found'
            }
            
        # Check if chapter exists
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {
                    'success': False,
                    'error': 'Invalid chapter for this novel'
                }
        
        # Add comment
        comment = InteractionDAO.add_comment(user_id, novel_id, chapter_id, content)
        
        # Get user info for response
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
    
    @staticmethod
    def get_comments(novel_id: int, chapter_id: Optional[int] = None, 
                    page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get comments for a novel or chapter"""
        # Check if novel exists
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
            
        # Check if chapter exists
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {'success': False, 'error': 'Invalid chapter for this novel'}
        
        result = InteractionDAO.get_comments(novel_id, chapter_id, page, per_page)
        return {'success': True, **result}
    
    @staticmethod
    def delete_comment(user_id: int, comment_id: int) -> Dict[str, Any]:
        """Delete a comment (by author or admin)"""
        # Check if comment exists
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'success': False, 'error': 'Comment not found'}
        
        # Check permission (must be comment author)
        user = User.query.get(user_id)
        if user.role != 'admin' and comment.user_id != user_id:
            return {'success': False, 'error': 'Permission denied to delete this comment'}
        
        # Delete comment
        InteractionDAO.delete_comment(comment_id)
        return {'success': True, 'message': 'Comment deleted successfully'}
        
    @staticmethod
    def toggle_follow(follower_id: int, followed_id: int) -> Dict[str, Any]:
        """Toggle follow status for a user"""
        # Check if users exist
        follower = User.query.get(follower_id)
        followed = User.query.get(followed_id)
        
        if not follower or not followed:
            return {'success': False, 'error': 'User not found'}
            
        # Check if already following
        is_following = InteractionDAO.check_following(follower_id, followed_id)
        
        if is_following:
            # Unfollow
            InteractionDAO.unfollow_user(follower_id, followed_id)
            return {
                'success': True,
                'message': f'Unfollowed {followed.username}',
                'is_following': False
            }
        else:
            # Follow
            following = InteractionDAO.follow_user(follower_id, followed_id)
            if not following:
                return {'success': False, 'error': 'Cannot follow yourself'}
                
            return {
                'success': True,
                'message': f'Following {followed.username}',
                'is_following': True
            }
    
    @staticmethod
    def get_follow_status(follower_id: int, followed_id: int) -> Dict[str, Any]:
        """Check if a user is following another user"""
        # Check if users exist
        followed = User.query.get(followed_id)
        if not followed:
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
    def send_message(sender_id: int, recipient_id: int, content: str) -> Dict[str, Any]:
        """Send a private message to another user"""
        # Validate input
        if not content or len(content.strip()) < 1:
            return {'success': False, 'error': 'Message cannot be empty'}
            
        if len(content) > 1000:
            return {'success': False, 'error': 'Message is too long (maximum 1000 characters)'}
            
        # Check if users exist
        sender = User.query.get(sender_id)
        recipient = User.query.get(recipient_id)
        
        if not sender or not recipient:
            return {'success': False, 'error': 'User not found'}
            
        # Check if sender can message recipient (must be following or be admin)
        if sender_id != recipient_id and sender.role != 'admin':
            is_following = InteractionDAO.check_following(recipient_id, sender_id)
            if not is_following:
                return {'success': False, 'error': 'This user is not following you and cannot receive your messages'}
        
        # Send message
        message = InteractionDAO.send_message(sender_id, recipient_id, content)
        if not message:
            return {'success': False, 'error': 'Cannot send message to yourself'}
            
        # Format response
        message_dict = message.to_dict()
        message_dict['sender'] = sender.to_dict()
        
        return {
            'success': True,
            'message': 'Message sent successfully',
            'data': message_dict
        }
        
    @staticmethod
    def get_conversation(user_id: int, other_user_id: int, 
                        page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """Get conversation between two users"""
        # Check if users exist
        user = User.query.get(user_id)
        other_user = User.query.get(other_user_id)
        
        if not user or not other_user:
            return {'success': False, 'error': 'User not found'}
            
        # Get conversation
        result = InteractionDAO.get_conversation(user_id, other_user_id, page, per_page)
        
        # Mark messages as read
        for message in result['messages']:
            if message['recipient_id'] == user_id and not message['is_read']:
                InteractionDAO.mark_message_as_read(message['id'])
        
        return {'success': True, **result}
        
    @staticmethod
    def get_inbox(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get inbox for a user"""
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        result = InteractionDAO.get_inbox(user_id, page, per_page)
        return {'success': True, **result}
        
    @staticmethod
    def mark_message_read(user_id: int, message_id: int) -> Dict[str, Any]:
        """Mark a message as read"""
        # Check if message exists and belongs to user
        message = PrivateMessage.query.get(message_id)
        if not message or message.recipient_id != user_id:
            return {'success': False, 'error': 'Message not found or not authorized'}
            
        # Mark as read
        if InteractionDAO.mark_message_as_read(message_id):
            return {'success': True, 'message': 'Message marked as read'}
        else:
            return {'success': False, 'error': 'Message already read or not found'}
            
    @staticmethod
    def send_tip(tipper_id: int, author_id: int, novel_id: int, 
                amount: int, message: Optional[str] = None,
                chapter_id: Optional[int] = None) -> Dict[str, Any]:
        """Send a tip to an author"""
        # Validate input
        if amount <= 0:
            return {'success': False, 'error': 'Tip amount must be positive'}
            
        if message and len(message) > 200:
            return {'success': False, 'error': 'Message is too long (maximum 200 characters)'}
            
        # Check if users exist
        tipper = User.query.get(tipper_id)
        author = User.query.get(author_id)
        
        if not tipper or not author:
            return {'success': False, 'error': 'User not found'}
            
        # Check if novel exists and belongs to author
        novel = Novel.query.get(novel_id)
        if not novel or novel.author != User.query.get(author_id).username:
            return {'success': False, 'error': 'Novel not found or does not belong to this author'}
            
        # Check if chapter exists and belongs to novel
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter or chapter.novel_id != novel_id:
                return {'success': False, 'error': 'Chapter not found or does not belong to this novel'}
                
        # Send tip
        tip = InteractionDAO.send_tip(tipper_id, author_id, novel_id, amount, message, chapter_id)
        if not tip:
            return {'success': False, 'error': 'Failed to send tip'}
            
        return {
            'success': True,
            'message': f'Successfully sent {amount/100:.2f} to {author.username}',
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