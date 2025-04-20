from app import db
from datetime import datetime

class Category(db.Model):
    """分类模型 - 用于小说分类和标签分类"""
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # 分类名称，必须唯一
    type = db.Column(db.String(20), nullable=False)  # 分类类型：'novel'或'tag'
    description = db.Column(db.Text, nullable=True)  # 分类描述
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)  # 上级分类ID，允许层级分类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 自引用关系，实现层级分类
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 