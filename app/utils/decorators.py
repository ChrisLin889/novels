from functools import wraps
from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models import User

def admin_required(fn):
    """
    确保当前用户是管理员的装饰器
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 从JWT获取用户ID
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': '此操作需要管理员权限'}), 403
        
        # 将用户ID存储在g对象中，以便在视图函数中访问
        g.user_id = user_id
        g.user = user
        
        return fn(*args, **kwargs)
    return wrapper 