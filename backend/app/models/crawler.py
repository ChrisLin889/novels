from app import db
from datetime import datetime

class CrawlTask(db.Model):
    __tablename__ = 'crawl_task'
    
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(255), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # novel, chapter, update
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    success_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'source_url': self.source_url,
            'task_type': self.task_type,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat()
        }

class CrawlTemp(db.Model):
    __tablename__ = 'crawl_temp'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('crawl_task.id'), nullable=False, index=True)
    novel_title = db.Column(db.String(100), nullable=True)
    novel_author = db.Column(db.String(50), nullable=True)
    novel_category = db.Column(db.String(30), nullable=True)
    novel_intro = db.Column(db.Text, nullable=True)
    novel_cover_url = db.Column(db.String(255), nullable=True)
    chapter_title = db.Column(db.String(100), nullable=True)
    chapter_number = db.Column(db.Integer, nullable=True)
    chapter_content = db.Column(db.Text, nullable=True)
    source_url = db.Column(db.String(255), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'novel_title': self.novel_title,
            'novel_author': self.novel_author,
            'novel_category': self.novel_category,
            'novel_intro': self.novel_intro,
            'novel_cover_url': self.novel_cover_url,
            'chapter_title': self.chapter_title,
            'chapter_number': self.chapter_number,
            'source_url': self.source_url,
            'is_approved': self.is_approved,
            'is_rejected': self.is_rejected,
            'created_at': self.created_at.isoformat(),
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        } 