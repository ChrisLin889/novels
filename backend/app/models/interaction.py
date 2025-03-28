from app import db
from datetime import datetime

class UserCollection(db.Model):
    __tablename__ = 'user_collection'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add unique constraint to prevent duplicate collections
    __table_args__ = (db.UniqueConstraint('user_id', 'novel_id', name='uix_user_novel_collection'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'novel_id': self.novel_id,
            'created_at': self.created_at.isoformat()
        }

class UserHistory(db.Model):
    __tablename__ = 'user_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    last_read_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Create composite index for fast query
    __table_args__ = (db.Index('idx_user_novel_history', 'user_id', 'novel_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'novel_id': self.novel_id,
            'chapter_id': self.chapter_id,
            'last_read_time': self.last_read_time.isoformat()
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=True, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    
    # Either novel_id or chapter_id should be provided
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'novel_id': self.novel_id,
            'chapter_id': self.chapter_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'likes': self.likes
        } 