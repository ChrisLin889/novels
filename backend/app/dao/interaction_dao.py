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
    def get_user_comments(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated comments made by a user"""
        comments = Comment.query.filter_by(user_id=user_id).order_by(
            desc(Comment.created_at)
        ).paginate(page=page, per_page=per_page)
        
        # Get novel and user info for each comment
        result = []
        for comment in comments.items:
            novel = Novel.query.get(comment.novel_id)
            chapter = None
            if comment.chapter_id:
                chapter = Chapter.query.get(comment.chapter_id)
                
            if novel:
                comment_dict = {
                    'id': comment.id,
                    'content': comment.content,
                    'created_at': comment.created_at.isoformat(),
                    'novel': {
                        'id': novel.id,
                        'title': novel.title,
                        'cover': novel.cover
                    }
                }
                
                if chapter:
                    comment_dict['chapter'] = {
                        'id': chapter.id,
                        'title': chapter.title,
                        'chapter_number': chapter.chapter_number
                    }
                    
                result.append(comment_dict)
        
        return {
            'total': comments.total,
            'pages': comments.pages,
            'current_page': page,
            'comments': result
        }
        
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