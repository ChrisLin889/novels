from app.models import User

class PermissionService:
    @staticmethod
    def has_role(user_id: int, role: str) -> bool:
        """检查用户是否拥有指定角色"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        if role == 'admin':
            return user.role == 'admin'
        elif role == 'user':
            return user.role in ['user', 'admin']  # admin 也拥有 user 权限
        
        return False 