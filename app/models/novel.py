from datetime import datetime
from app.models import db

class Novel(db.Model):
    __tablename__ = 'novel'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 回收站字段
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # 关联关系
    chapters = db.relationship('Chapter', backref='novel', lazy='dynamic')
    comments = db.relationship('Comment', backref='novel', lazy='dynamic')
    author = db.relationship('User', backref='novels')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'author_name': self.author.username if self.author else None,
            'cover': self.cover,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        } 