from app.models.notification import UserNotification
from app import db
from typing import List, Dict, Optional, Tuple
from sqlalchemy import desc

class NotificationDAO:
    """
    通知数据访问对象
    """
    
    @staticmethod
    def create_notification(user_id: int, title: str, content: str, 
                           notification_type: str, related_object_type: Optional[str] = None, 
                           related_object_id: Optional[int] = None) -> UserNotification:
        """
        创建一条用户通知
        """
        notification = UserNotification(
            user_id=user_id,
            title=title,
            content=content,
            notification_type=notification_type,
            related_object_type=related_object_type,
            related_object_id=related_object_id
        )
        
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def get_user_notifications(user_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[UserNotification], int]:
        """
        获取用户通知列表
        """
        query = UserNotification.query.filter_by(user_id=user_id)
        total = query.count()
        
        notifications = query.order_by(desc(UserNotification.created_at)) \
                        .offset((page - 1) * per_page) \
                        .limit(per_page) \
                        .all()
                        
        return notifications, total
    
    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> bool:
        """
        将通知标记为已读
        """
        notification = UserNotification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notification:
            return False
            
        notification.is_read = True
        db.session.commit()
        return True
    
    @staticmethod
    def mark_all_as_read(user_id: int) -> bool:
        """
        将用户所有通知标记为已读
        """
        UserNotification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()
        return True
    
    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """
        获取未读通知数量
        """
        return UserNotification.query.filter_by(user_id=user_id, is_read=False).count() 