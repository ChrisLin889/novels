from app import db
from datetime import datetime

class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # 标签名称，唯一
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)  # 标签分类
    description = db.Column(db.Text, nullable=True)  # 标签描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    category = db.relationship('Category', backref='tags')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 