from app.models.interaction import UserCollection, UserHistory, Comment, UserFollowing, PrivateMessage
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
        print(f"DEBUG - InteractionDAO.update_reading_history 开始: user_id={user_id}, novel_id={novel_id}, chapter_id={chapter_id}")
        
        try:
            # 查询现有历史记录
            history = UserHistory.query.filter_by(
                user_id=user_id,
                novel_id=novel_id
            ).first()
            
            if history:
                print(f"DEBUG - 找到现有历史记录 ID={history.id}, 当前章节={history.chapter_id}, 更新时间={history.last_read_time}")
                history.chapter_id = chapter_id
                history.last_read_time = datetime.datetime.utcnow()
                print(f"DEBUG - 已更新章节ID为 {chapter_id}")
            else:
                print(f"DEBUG - 未找到历史记录, 创建新记录")
                history = UserHistory(
                    user_id=user_id,
                    novel_id=novel_id,
                    chapter_id=chapter_id
                )
                db.session.add(history)
                print(f"DEBUG - 新记录已添加到会话")
            
            # 检查小说和章节是否存在
            novel = Novel.query.get(novel_id)
            chapter = Chapter.query.get(chapter_id)
            if not novel:
                print(f"DEBUG - 警告: 小说ID={novel_id} 不存在")
            if not chapter:
                print(f"DEBUG - 警告: 章节ID={chapter_id} 不存在")
            
            # 明确提交会话
            print(f"DEBUG - 提交数据库会话")
            db.session.commit()
            print(f"DEBUG - 会话提交成功, 历史记录ID={history.id if history else None}")
            
            # 验证更新是否成功
            updated_history = UserHistory.query.filter_by(
                user_id=user_id,
                novel_id=novel_id
            ).first()
            
            if updated_history:
                print(f"DEBUG - 验证成功: 记录ID={updated_history.id}, 章节ID={updated_history.chapter_id}")
            else:
                print(f"DEBUG - 警告: 提交后无法找到记录")
                
            return history
        except Exception as e:
            print(f"DEBUG - 更新阅读历史时发生异常: {str(e)}")
            print(f"DEBUG - 异常类型: {type(e).__name__}")
            import traceback
            print(f"DEBUG - 异常跟踪: {traceback.format_exc()}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_user_history(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get paginated list of user's reading history"""
        print(f"DEBUG - InteractionDAO.get_user_history: user_id={user_id}, page={page}, per_page={per_page}")
        
        history_records = UserHistory.query.filter_by(
            user_id=user_id
        ).order_by(
            desc(UserHistory.last_read_time)
        ).paginate(page=page, per_page=per_page)
        
        print(f"DEBUG - 查询到的历史记录数: {len(history_records.items)}")
        
        # Get novel and chapter details for each history record
        result = []
        for history in history_records.items:
            print(f"DEBUG - 处理历史记录: history_id={history.id}, novel_id={history.novel_id}, chapter_id={history.chapter_id}")
            novel = Novel.query.get(history.novel_id)
            chapter = Chapter.query.get(history.chapter_id)
            
            if novel and chapter:
                record = {
                    'novel': novel.to_dict(),
                    'chapter': chapter.to_dict(),
                    'last_read_time': history.last_read_time.isoformat()
                }
                result.append(record)
                print(f"DEBUG - 添加了历史记录: novel={novel.title}, chapter={chapter.title}")
            else:
                print(f"DEBUG - 跳过历史记录: novel={'存在' if novel else '不存在'}, chapter={'存在' if chapter else '不存在'}")
        
        print(f"DEBUG - 最终返回的历史记录数: {len(result)}")
        
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
        # 先查询与用户有过通信的所有用户ID（发件人）
        senders = db.session.query(PrivateMessage.sender_id).filter_by(
            recipient_id=user_id
        ).distinct().all()
        
        # 提取发件人ID列表
        sender_ids = [sender[0] for sender in senders]
        
        # 查询每个发件人的最新消息
        conversations = []
        for sender_id in sender_ids:
            # 查询这个发件人的最新消息
            latest_message = PrivateMessage.query.filter_by(
                sender_id=sender_id,
                recipient_id=user_id
            ).order_by(desc(PrivateMessage.created_at)).first()
            
            if latest_message:
                sender = User.query.get(sender_id)
                if sender:
                    # 构建会话对象
                    conversation = {
                        'id': sender_id,  # 用对话者ID作为会话ID
                        'user': sender.to_dict(),
                        'last_message': {  # 修改为'last_message'与API文档一致
                            'id': latest_message.id,
                            'content': latest_message.content,
                            'is_read': latest_message.read_at is not None,  # 使用'is_read'布尔值
                            'created_at': latest_message.created_at.isoformat()
                        },
                        'unread_count': PrivateMessage.query.filter_by(
                            sender_id=sender_id,
                            recipient_id=user_id,
                            read_at=None
                        ).count()
                    }
                    conversations.append(conversation)
        
        # 按最新消息时间排序
        conversations.sort(key=lambda x: x['last_message']['created_at'], reverse=True)
        
        # 手动分页
        total = len(conversations)
        start = (page - 1) * per_page
        end = start + per_page
        paged_conversations = conversations[start:end] if start < total else []
        
        return {
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'current_page': page,
            'conversations': paged_conversations,  # 修改为'conversations'直接使用统一字段名
            'unread_count': PrivateMessage.query.filter_by(
                recipient_id=user_id, 
                read_at=None
            ).count()
        }
    
    @staticmethod
    def record_reading_history(user_id: int, novel_id: int, chapter_id: int) -> bool:
        """Record user reading history
        
        Args:
            user_id: User ID
            novel_id: Novel ID
            chapter_id: Chapter ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if history exists
            history = UserHistory.query.filter_by(
                user_id=user_id,
                novel_id=novel_id
            ).first()
            
            if history:
                # Update existing history
                history.chapter_id = chapter_id
                history.last_read_time = datetime.datetime.utcnow()
            else:
                # Create new history
                history = UserHistory(
                    user_id=user_id,
                    novel_id=novel_id,
                    chapter_id=chapter_id,
                    last_read_time=datetime.datetime.utcnow()
                )
                db.session.add(history)
            
            # Commit changes
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error recording reading history: {str(e)}")
            return False 