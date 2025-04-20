from typing import Optional, Dict, Any
from app.models.user import User
from app.models.admin import Admin
from app.models.author import Author

class PermissionService:
    """
    独立的权限管理服务，处理所有与用户权限相关的逻辑
    将权限逻辑从User模型和其他服务中分离
    """
    
    @staticmethod
    def get_user_role(user_id: int) -> Optional[str]:
        """
        获取用户角色
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户角色: 'admin', 'author', 'user' 或 None (如果用户不存在)
        """
        user = User.query.get(user_id)
        if not user:
            return None
            
        # 检查管理员角色
        admin = Admin.query.filter_by(user_id=user_id).first()
        if admin:
            return 'admin'
            
        # 检查作者角色
        author = Author.query.filter_by(user_id=user_id).first()
        if author:
            return 'author'
            
        # 默认角色
        return 'user'
    
    @staticmethod
    def has_role(user_id: int, required_role: str) -> bool:
        """
        检查用户是否拥有指定角色
        
        Args:
            user_id: 用户ID
            required_role: 所需角色 ('admin', 'author', 'user')
            
        Returns:
            是否拥有指定角色
        """
        user_role = PermissionService.get_user_role(user_id)
        if not user_role:
            return False
            
        # 角色层次: admin > author > user
        if required_role == 'admin':
            return user_role == 'admin'
        elif required_role == 'author':
            return user_role in ('admin', 'author')
        elif required_role == 'user':
            return True
        
        return False
    
    @staticmethod
    def check_resource_permission(user_id: int, resource_id: int, resource_type: str) -> bool:
        """
        检查用户是否有权限访问特定资源
        
        Args:
            user_id: 用户ID
            resource_id: 资源ID
            resource_type: 资源类型 (例如 'novel', 'chapter')
            
        Returns:
            是否有访问权限
        """
        user_role = PermissionService.get_user_role(user_id)
        
        # 管理员可以访问任何资源
        if user_role == 'admin':
            return True
            
        # 检查特定资源的所有权
        if resource_type == 'novel':
            from app.models.novel import Novel
            novel = Novel.query.get(resource_id)
            if novel and novel.author:
                author = Author.query.filter_by(user_id=user_id).first()
                return author and author.id == novel.author_id
        
        # 可以根据需要添加其他资源类型
        
        return False 