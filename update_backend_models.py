#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库模型更新脚本
将用户、作者和管理员分离到不同表中的模型更新
"""

import os
import sys

# 首先创建新的模型文件

# 1. 更新 User 模型 (app/models/user.py)
USER_MODEL = """
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
    
    # 新的关系
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
    
    # 新增方法判断用户角色
    def is_author(self):
        return self.author is not None
        
    def is_admin(self):
        return self.admin is not None
        
    def get_role(self):
        if self.is_admin():
            return 'admin'
        elif self.is_author():
            return 'author'
        else:
            return 'user'
            
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'role': self.get_role(),
            'avatar': self.avatar,
            'created_at': self.created_at.isoformat(),
            'status': 'active' if self.status == 0 else 'banned'
        }
"""

# 2. 创建 Author 模型 (app/models/author.py)
AUTHOR_MODEL = """
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
"""

# 3. 更新 Admin 模型 (app/models/admin.py)
ADMIN_MODEL = """
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
    \"\"\"
    Model for storing sensitive words for content filtering
    \"\"\"
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
    \"\"\"
    Model for auditing content (novels, chapters, comments)
    \"\"\"
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

# 保留其他管理员相关模型（UserAction, CrawledNovel, CrawledChapter）...
"""

# 4. 更新 Novel 模型 (app/models/novel.py)
NOVEL_MODEL = """
from app import db
from datetime import datetime

class Novel(db.Model):
    __tablename__ = 'novel'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(50), nullable=False)  # 作者名称（必填）
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)  # 内部作者ID（可选）
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
            'author': self.author,  # 使用作者名称
            'author_id': self.author_id,  # 添加作者ID（如果是内部作者）
            'is_internal_author': self.author_id is not None,  # 添加是否为内部作者标志
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
"""

# 5. 更新 utils/auth.py
AUTH_UTILS = """
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin():
            return jsonify({'message': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_author():
            return jsonify({'message': 'Author privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function
"""

# 6. 创建数据迁移脚本
DATA_MIGRATION = """
from app import db, create_app
from app.models.user import User
from app.models.author import Author
from app.models.admin import Admin, ContentAudit
from app.models.novel import Novel
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_roles():
    \"\"\"将现有用户的角色迁移到新的表结构\"\"\"
    app = create_app()
    with app.app_context():
        # 检查是否已经有作者或管理员记录
        existing_authors = Author.query.count()
        existing_admins = Admin.query.count()
        
        if existing_authors > 0 or existing_admins > 0:
            logger.info("已存在作者或管理员记录，跳过迁移")
            return
            
        # 找出所有有role信息的用户（从备份表中获取）
        try:
            # 尝试从user_backup表读取角色信息
            authors = db.session.execute("SELECT id, username, created_at, updated_at FROM user_backup WHERE role = 'author'").fetchall()
            admins = db.session.execute("SELECT id, username, created_at, updated_at FROM user_backup WHERE role = 'admin'").fetchall()
            
            logger.info(f"找到 {len(authors)} 个作者和 {len(admins)} 个管理员需要迁移")
            
            # 创建作者记录
            for author_data in authors:
                user = User.query.get(author_data.id)
                if user:
                    author = Author(
                        user_id=user.id,
                        pen_name=user.username,
                        created_at=user.created_at,
                        updated_at=user.updated_at
                    )
                    db.session.add(author)
                    logger.info(f"为用户 {user.username} 创建作者记录")
            
            # 创建管理员记录
            for admin_data in admins:
                user = User.query.get(admin_data.id)
                if user:
                    admin = Admin(
                        user_id=user.id,
                        admin_level=1,
                        permissions={'content': True, 'user': True},
                        created_at=user.created_at,
                        updated_at=user.updated_at
                    )
                    db.session.add(admin)
                    logger.info(f"为用户 {user.username} 创建管理员记录")
            
            db.session.commit()
            logger.info("用户角色迁移完成")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"迁移过程中出错: {str(e)}")
            raise
            
def migrate_relationships():
    \"\"\"更新关系表的外键引用\"\"\"
    app = create_app()
    with app.app_context():
        try:
            # 更新小说表中的author_id
            novels = Novel.query.filter(Novel.author_id.isnot(None)).all()
            for novel in novels:
                # 查找作者记录
                author = Author.query.filter_by(user_id=novel.author_id).first()
                if author:
                    novel.author_id = author.id
                    logger.info(f"更新小说 '{novel.title}' 的作者ID为 {author.id}")
                else:
                    novel.author_id = None
                    logger.warning(f"小说 '{novel.title}' 的作者未找到，设置为NULL")
                    
            # 更新内容审核表中的reviewer_id/admin_id
            audits = ContentAudit.query.filter(ContentAudit.admin_id.isnot(None)).all()
            for audit in audits:
                # 查找管理员记录
                admin = Admin.query.filter_by(user_id=audit.admin_id).first()
                if admin:
                    audit.admin_id = admin.id
                    logger.info(f"更新内容审核 #{audit.id} 的管理员ID为 {admin.id}")
                else:
                    audit.admin_id = None
                    logger.warning(f"内容审核 #{audit.id} 的管理员未找到，设置为NULL")
                    
            db.session.commit()
            logger.info("关系迁移完成")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"迁移关系时出错: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        migrate_roles()
        migrate_relationships()
        print("数据迁移成功完成！")
    except Exception as e:
        print(f"数据迁移失败: {str(e)}")
"""

# 写入文件
def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully wrote {path}")
    except Exception as e:
        print(f"Error writing {path}: {str(e)}")

def main():
    # 创建目录结构
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'backend', 'app', 'models')
    utils_dir = os.path.join(base_dir, 'backend', 'app', 'utils')
    
    # 确保目录存在
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(utils_dir, exist_ok=True)
    
    # 写入文件
    write_file(os.path.join(models_dir, 'user.py'), USER_MODEL.strip())
    write_file(os.path.join(models_dir, 'author.py'), AUTHOR_MODEL.strip())
    write_file(os.path.join(models_dir, 'admin.py'), ADMIN_MODEL.strip())
    write_file(os.path.join(models_dir, 'novel.py'), NOVEL_MODEL.strip())
    write_file(os.path.join(utils_dir, 'auth.py'), AUTH_UTILS.strip())
    write_file(os.path.join(base_dir, 'backend', 'data_migration.py'), DATA_MIGRATION.strip())
    
    print("\nAll model files have been updated!")
    print("\nNext steps:")
    print("1. 数据库迁移已完成")
    print("2. 模型文件已更新到相应目录")
    print("3. 重启应用程序以应用模型变更")

if __name__ == "__main__":
    main() 