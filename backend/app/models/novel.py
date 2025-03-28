from app import db
from datetime import datetime

class Novel(db.Model):
    __tablename__ = 'novel'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(30), nullable=False, index=True)
    cover = db.Column(db.String(255), default='default_cover.jpg')
    intro = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='ongoing')  # ongoing, completed
    view_count = db.Column(db.Integer, default=0)
    collection_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chapters = db.relationship('Chapter', backref='novel', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'cover': self.cover,
            'intro': self.intro,
            'status': self.status,
            'view_count': self.view_count,
            'collection_count': self.collection_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'chapter_count': self.chapters.count()
        }

class Chapter(db.Model):
    __tablename__ = 'chapter'
    
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False, index=True)
    chapter_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    word_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_content=False):
        result = {
            'id': self.id,
            'novel_id': self.novel_id,
            'chapter_number': self.chapter_number,
            'title': self.title,
            'word_count': self.word_count,
            'created_at': self.created_at.isoformat()
        }
        
        if include_content:
            result['content'] = self.content
            
        return result 