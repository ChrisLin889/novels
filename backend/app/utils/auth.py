from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import User
from app.services.permission_service import PermissionService

def login_required(f):
    """
    检查用户是否登录的装饰器
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'Authentication required'}), 401
            
        # 将用户对象存储在 g 中，以便在视图函数中访问
        g.user = user
        g.user_id = user.id
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    """
    通用的角色检查装饰器，可用于任何角色
    
    Args:
        role: 所需角色 ('admin', 'author', 'user')
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_id = g.user_id
            
            # 使用 PermissionService 检查角色
            if not PermissionService.has_role(user_id, role):
                return jsonify({'message': f'{role.capitalize()} privileges required'}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 为常用角色提供便捷装饰器
def admin_required(f):
    """管理员权限检查装饰器"""
    return role_required('admin')(f)

def author_required(f):
    """作者权限检查装饰器"""
    return role_required('author')(f)

def resource_permission_required(resource_type):
    """
    检查用户对特定资源的权限
    
    Args:
        resource_type: 资源类型 ('novel', 'chapter', 等)
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_id = g.user_id
            
            # 从路由参数中获取资源ID
            resource_id = kwargs.get(f'{resource_type}_id')
            if not resource_id:
                return jsonify({'message': 'Resource not specified'}), 400
                
            # 检查资源权限
            if not PermissionService.check_resource_permission(user_id, resource_id, resource_type):
                return jsonify({'message': 'Permission denied for this resource'}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator