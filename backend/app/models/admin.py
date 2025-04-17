from app import db
from datetime import datetime

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
            'created_at': self.created_at.isoformat()
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
            'target_user_id': self.target_user_id,
            'action_type': self.action_type,
            'reason': self.reason,
            'duration': self.duration,
            'created_at': self.created_at.isoformat()
        }

class CrawledNovel(db.Model):
    """
    Temporary model for storing crawled novels before approval
    """
    __tablename__ = 'crawled_novel'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    cover = db.Column(db.String(255), nullable=True)
    intro = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    source_url = db.Column(db.String(255), nullable=True)
    source_site = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    chapters = db.relationship('CrawledChapter', backref='novel', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'cover': self.cover,
            'intro': self.intro,
            'status': self.status,
            'source_url': self.source_url,
            'source_site': self.source_site,
            'created_at': self.created_at.isoformat(),
            'chapter_count': self.chapters.count()
        }

class CrawledChapter(db.Model):
    """
    Temporary model for storing crawled chapters before approval
    """
    __tablename__ = 'crawled_chapter'
    
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('crawled_novel.id'), nullable=False, index=True)
    chapter_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, include_content=False):
        result = {
            'id': self.id,
            'novel_id': self.novel_id,
            'chapter_number': self.chapter_number,
            'title': self.title,
            'source_url': self.source_url,
            'created_at': self.created_at.isoformat()
        }
        
        if include_content:
            result['content'] = self.content
            
        return result