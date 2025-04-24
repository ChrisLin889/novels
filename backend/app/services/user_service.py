from app.models.user import User
from app import db
from typing import Dict, Any, List, Optional, Union
from app.utils.security import validate_password
import bcrypt
from app.models.author import Author
from app.models.admin import Admin
from app.models.novel import Novel
from app.models.interaction import UserCollection, UserHistory, UserFollowing
from datetime import datetime
import re
import random
import string
from app.services.permission_service import PermissionService
from app.dao.user_dao import UserDAO

class UserService:
    """
    Service layer for user-related operations
    Implements business logic and interacts with DAO
    """
    
    @staticmethod
    def register(username: str, password: str, email: Optional[str] = None, phone: Optional[str] = None) -> Dict:
        """
        Register a new user
        
        Args:
            username: Username
            password: Plain password
            email: Email address (optional)
            phone: Phone number (optional)
            
        Returns:
            Dict with success status and message
        """
        # Check if username exists
        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            return {'success': False, 'message': 'Username already exists'}
            
        # Check if email exists if provided
        if email:
            existing_email = User.query.filter(User.email == email).first()
            if existing_email:
                return {'success': False, 'message': 'Email already exists'}
                
        # Check if phone exists if provided
        if phone:
            existing_phone = User.query.filter(User.phone == phone).first()
            if existing_phone:
                return {'success': False, 'message': 'Phone already exists'}
        
        # Validate password strength
        if len(password) < 6:
            return {'success': False, 'message': 'Password must be at least 6 characters long'}
            
        # Create new user
        new_user = User(
            username=username,
            email=email,
            phone=phone,
            status=0  # 0 = active
        )
        
        # Set password (with hash)
        new_user.set_password(password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'User registered successfully',
            'user_id': new_user.id
        }
    
    @staticmethod
    def login(username_or_email: str, password: str, is_email: bool = False) -> Dict:
        """
        Login user
        
        Args:
            username_or_email: Username, email or phone
            password: Plain password
            is_email: Boolean indicating if the input is an email
            
        Returns:
            Dict with login result
        """
        print(f"Login attempt - identifier: {username_or_email}, is_email: {is_email}")
        
        # Validate input
        if not username_or_email or not password:
            print("Missing username/email or password")
            return {
                'success': False,
                'error': 'Username/email/phone and password are required'
            }
        
        # Try to find user based on provided identifier
        if is_email:
            user = User.query.filter(User.email == username_or_email).first()
            print(f"Searching by email: {username_or_email}, found: {user is not None}")
        else:
            # Try by phone number or username
            user = User.query.filter(
                (User.phone == username_or_email) | 
                (User.username == username_or_email)
            ).first()
            print(f"Searching by phone/username: {username_or_email}, found: {user is not None}")
        
        # Verify user exists
        if not user:
            print("User not found")
            return {
                'success': False,
                'error': 'User not found'
            }
        
        # Print user details for debugging
        print(f"User details - ID: {user.id}, Username: {user.username}, Password hash: {user.password_hash[:20]}...")
        
        # Check password
        password_match = user.debug_check_password(password)
        print(f"Password check result: {password_match}")
        
        if not password_match:
            return {
                'success': False,
                'error': 'Invalid password'
            }
        
        # Check if user is active
        if user.status != 0:  # 0 = active, 1 = banned
            print("User account is disabled")
            return {
                'success': False,
                'error': 'Your account is disabled'
            }
        
        # Update last login
        user.updated_at = datetime.now()
        db.session.commit()
        
        # Determine user role and get additional data
        user_data = {
            'id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'avatar': user.avatar,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            'status': 'active' if user.status == 0 else 'inactive'
        }
        
        # Get the user's role
        role = PermissionService.get_user_role(user.id)
        user_data['role'] = role
        
        # Add role-specific data
        if role == 'author':
            author = Author.query.filter_by(user_id=user.id).first()
            if author:
                user_data['author'] = {
                    'id': author.id,
                    'pen_name': author.pen_name,
                    'bio': author.bio,
                    'verified': author.verified,
                    'works_count': author.works_count,
                    'fans_count': author.fans_count
                }
        elif role == 'admin':
            admin = Admin.query.filter_by(user_id=user.id).first()
            if admin:
                user_data['admin'] = {
                    'id': admin.id,
                    'admin_level': admin.admin_level,
                    'department': admin.department,
                    'permissions': admin.permissions
                }
        
        # Return user info (excluding sensitive data)
        return {
            'success': True,
            'user_id': user.id,
            'role': role,
            'user': user_data
        }
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data dict or None if not found
        """
        user = User.query.get(user_id)
        if not user:
            return None
            
        # Get user collections and following stats
        collection_count = UserCollection.query.filter(
            UserCollection.user_id == user_id
        ).count()
        
        following_count = UserFollowing.query.filter(
            UserFollowing.follower_id == user_id
        ).count()
        
        followers_count = UserFollowing.query.filter(
            UserFollowing.followed_id == user_id
        ).count()
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'role': PermissionService.get_user_role(user.id),
            'avatar': user.avatar,
            'created_at': user.created_at.isoformat(),
            'status': 'active' if user.status == 0 else 'banned',
            'stats': {
                'collection_count': collection_count,
                'following_count': following_count,
                'followers_count': followers_count
            }
        }
    
    @staticmethod
    def update_profile(user_id: int, data: Dict[str, Any]) -> Dict:
        """
        Update user profile
        
        Args:
            user_id: User ID
            data: Dict with profile data to update
            
        Returns:
            Dict with success status and message
        """
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        # Update allowed fields
        allowed_fields = ['avatar', 'email', 'phone']
        updated = False
        
        for field in allowed_fields:
            if field in data and data[field] is not None:
                # Validate unique fields
                if field == 'email' and data['email']:
                    existing = User.query.filter(User.email == data['email']).first()
                    if existing and existing.id != user_id:
                        return {'success': False, 'error': 'Email already in use'}
                
                if field == 'phone' and data['phone']:
                    existing = User.query.filter(User.phone == data['phone']).first()
                    if existing and existing.id != user_id:
                        return {'success': False, 'error': 'Phone already in use'}
                
                setattr(user, field, data[field])
                updated = True
        
        if 'password' in data and data['password']:
            # Update password
            if len(data['password']) < 6:
                return {'success': False, 'error': 'Password must be at least 6 characters long'}
                
            user.set_password(data['password'])
            updated = True
            
        if updated:
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return {
                'success': True, 
                'message': 'Profile updated successfully',
                'user': UserService.get_user_by_id(user_id)
            }
        else:
            return {'success': False, 'error': 'No fields to update'}
    
    @staticmethod
    def get_profile(user_id: int) -> Dict:
        """
        Get user profile information
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with success status and user data
        """
        user_data = UserService.get_user_by_id(user_id)
        if not user_data:
            return {'success': False, 'error': 'User not found'}
            
        return {
            'success': True,
            'user': user_data
        }
    
    @staticmethod
    def get_security_info(user_id: int) -> Dict:
        """
        Get user security info (for verification purposes)
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with masked email and phone
        """
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'message': 'User not found'}
            
        # Mask email and phone
        masked_email = None
        if user.email:
            parts = user.email.split('@')
            if len(parts) > 1:
                username = parts[0]
                domain = parts[1]
                if len(username) > 2:
                    masked_email = username[0] + '*' * (len(username) - 2) + username[-1] + '@' + domain
                else:
                    masked_email = '*' * len(username) + '@' + domain
                    
        masked_phone = None
        if user.phone and len(user.phone) > 4:
            masked_phone = user.phone[:3] + '*' * (len(user.phone) - 7) + user.phone[-4:]
        
        return {
            'success': True,
            'email': masked_email,
            'phone': masked_phone,
            'has_email': user.email is not None,
            'has_phone': user.phone is not None
        }
    
    @staticmethod
    def check_permission(user_id: int, required_role: str = None, resource_id: int = None, resource_type: str = None) -> bool:
        """
        检查用户是否拥有特定权限
        
        Args:
            user_id: 用户ID
            required_role: 所需角色 (admin, author)
            resource_id: 资源ID (可选)
            resource_type: 资源类型 (可选)
            
        Returns:
            是否拥有权限
        """
        # 如果只检查角色
        if required_role and not resource_id:
            return PermissionService.has_role(user_id, required_role)
            
        # 如果需要检查资源权限
        if resource_id and resource_type:
            return PermissionService.check_resource_permission(user_id, resource_id, resource_type)
            
        # 默认为拥有权限，但要求登录
        return User.query.get(user_id) is not None
    
    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> Dict:
        """
        Change user password
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            Dict with success status and message
        """
        user = User.query.get(user_id)
        if not user:
            return {
                'success': False,
                'error': 'User not found'
            }
        
        # Verify current password
        if not user.check_password(current_password):
            return {
                'success': False,
                'error': 'Current password is incorrect'
            }
        
        # Validate new password
        if len(new_password) < 6:
            return {
                'success': False,
                'error': 'New password must be at least 6 characters long'
            }
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Password changed successfully'
        }
    
    @staticmethod
    def deactivate_account(user_id: int, password: str) -> Dict:
        """
        Deactivate a user account. This will completely delete the user record.
        
        Args:
            user_id: User ID
            password: Password for verification
            
        Returns:
            Dict with success status and message
        """
        user = User.query.get(user_id)
        if not user:
            return {
                'success': False,
                'error': 'User not found'
            }
        
        # Verify password
        if not user.check_password(password):
            return {
                'success': False,
                'error': 'Password is incorrect'
            }
        
        # 使用 PermissionService 获取用户角色，而不是直接访问 user.role
        user_role = PermissionService.get_user_role(user_id)
        
        # Check if user is an admin (cannot deactivate admin accounts through this method)
        if user_role == 'admin':
            return {
                'success': False,
                'error': 'Admin accounts cannot be deactivated through this method'
            }
            
        # Check if user is an author
        if user_role == 'author':
            # 注意：如果只想注销作者身份但保留用户账户，应使用作者模块的 /api/author/resign API
            # 这里的操作会完全删除用户账户
            author = Author.query.filter_by(user_id=user_id).first()
            if author:
                # Clear author relationship but keep the novels
                db.session.delete(author)
        
        # 处理作者申请记录 - 应该在删除用户前处理
        from app.models.author import AuthorApplication
        AuthorApplication.query.filter_by(user_id=user_id).delete()
        
        # 处理操作记录 - 需要在删除用户前处理
        from app.models.admin import UserAction
        # 删除此用户作为目标的记录
        UserAction.query.filter_by(target_user_id=user_id).delete()
        
        # Delete user interactions (collections, history, following)
        UserCollection.query.filter_by(user_id=user_id).delete()
        UserHistory.query.filter_by(user_id=user_id).delete()
        UserFollowing.query.filter_by(follower_id=user_id).delete()
        UserFollowing.query.filter_by(followed_id=user_id).delete()
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Account successfully deactivated'
        }