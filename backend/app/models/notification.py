from app import db
from datetime import datetime

class UserNotification(db.Model):
    """
    用户通知模型 - 用于存储系统向用户发送的通知
    """
    __tablename__ = 'user_notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(20), nullable=False)  # sensitive_word, system, admin, etc.
    related_object_type = db.Column(db.String(20), nullable=True)  # novel, chapter, comment
    related_object_id = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'notification_type': self.notification_type,
            'related_object_type': self.related_object_type,
            'related_object_id': self.related_object_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        } 