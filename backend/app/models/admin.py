from app import db
from datetime import datetime
from typing import Dict, Any

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    admin_level = db.Column(db.Integer, default=1)  # 1=普通管理员, 2=高级管理员, 3=超级管理员
    permissions = db.Column(db.JSON)
    department = db.Column(db.String(50))
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='admin')
    content_audits = db.relationship('ContentAudit', backref='admin', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'admin_level': self.admin_level,
            'permissions': self.permissions,
            'department': self.department,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# 保留其他管理员相关模型
class SensitiveWord(db.Model):
    """
    Model for storing sensitive words for content filtering
    """
    __tablename__ = 'sensitive_word'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False, unique=True, index=True)
    level = db.Column(db.Integer, default=1)  # 1=warn, 2=block, 3=ban
    category = db.Column(db.String(20), nullable=True)  # political, violence, sex, etc.
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'level': self.level,
            'category': self.category,
            'added_by': self.added_by,
            'created_at': self.created_at.isoformat()
        }

class ContentAudit(db.Model):
    """
    Model for auditing content (novels, chapters, comments)
    """
    __tablename__ = 'content_audit'
    
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20), nullable=False)  # novel, chapter, comment
    content_id = db.Column(db.Integer, nullable=False)  # ID of the content
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    reason = db.Column(db.String(255), nullable=True)  # Reason for rejection
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content_type': self.content_type,
            'content_id': self.content_id,
            'status': self.status,
            'reason': self.reason,
            'admin_id': self.admin_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class UserAction(db.Model):
    """
    Model for logging user management actions (ban, unban, etc.)
    """
    __tablename__ = 'user_action'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)  # Admin who took action
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User affected
    action_type = db.Column(db.String(20), nullable=False)  # ban, unban, warn, etc.
    reason = db.Column(db.String(255), nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # Ban duration in days (null for permanent)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    admin = db.relationship('Admin', backref=db.backref('actions', lazy='dynamic'))
    target_user = db.relationship('User', backref=db.backref('admin_actions', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'admin_name': self.admin.user.username if self.admin and self.admin.user else None,
            'target_user_id': self.target_user_id,
            'target_user_name': self.target_user.username if self.target_user else None,
            'action_type': self.action_type,
            'reason': self.reason,
            'duration': self.duration,
            'created_at': self.created_at.isoformat()
        }