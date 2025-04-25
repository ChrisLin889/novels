from datetime import datetime
from app.models import db

class Chapter(db.Model):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 回收站字段
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # 关联关系
    comments = db.relationship('Comment', backref='chapter', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'novel_id': self.novel_id,
            'title': self.title,
            'content': self.content,
            'chapter_number': self.chapter_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        } 