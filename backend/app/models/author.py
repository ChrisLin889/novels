from app import db
from datetime import datetime

class Author(db.Model):
    __tablename__ = 'author'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    pen_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    income_account = db.Column(db.String(100))
    works_count = db.Column(db.Integer, default=0)
    fans_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='author')
    novels = db.relationship('Novel', backref='author_info', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pen_name': self.pen_name or self.user.username,
            'bio': self.bio,
            'verified': self.verified,
            'works_count': self.works_count,
            'fans_count': self.fans_count,
            'created_at': self.created_at.isoformat()
        }

class AuthorApplication(db.Model):
    """
    用户申请成为作者的申请记录
    """
    __tablename__ = 'author_application'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pen_name = db.Column(db.String(50), nullable=False)  # 笔名
    bio = db.Column(db.Text, nullable=False)  # 作者简介
    reason = db.Column(db.Text, nullable=False)  # 申请理由
    status = db.Column(db.String(20), default='pending')  # 申请状态：pending, approved, rejected
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)  # 处理申请的管理员ID
    admin_comment = db.Column(db.Text, nullable=True)  # 管理员批注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref=db.backref('author_applications', lazy='dynamic'))
    admin = db.relationship('Admin', backref=db.backref('processed_applications', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username,
            'pen_name': self.pen_name,
            'bio': self.bio,
            'reason': self.reason,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_comment': self.admin_comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }