from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(255), default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.Integer, default=0)  # 0 = active, 1 = banned
    banned_until = db.Column(db.DateTime, nullable=True)  # 封禁截止日期
    
    # 关系定义
    author = db.relationship('Author', uselist=False, back_populates='user')
    admin = db.relationship('Admin', uselist=False, back_populates='user')
    
    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def debug_check_password(self, password):
        """Debug version that prints the password and hash"""
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = self.password_hash.encode('utf-8')
            
            print(f"Password: {password}")
            print(f"Password bytes: {password_bytes}")
            print(f"Hash: {self.password_hash}")
            print(f"Hash bytes: {hash_bytes}")
            
            result = bcrypt.checkpw(password_bytes, hash_bytes)
            print(f"Check result: {result}")
            return result
        except Exception as e:
            print(f"Password check error: {str(e)}")
            return False
            
    def to_dict(self):
        # 导入 PermissionService 防止循环导入
        from app.services.permission_service import PermissionService
        
        return {
            'id': self.id,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'role': PermissionService.get_user_role(self.id),
            'avatar': self.avatar,
            'created_at': self.created_at.isoformat(),
            'status': 'active' if self.status == 0 else 'banned',
            'banned_until': self.banned_until.isoformat() if self.banned_until else None
        }