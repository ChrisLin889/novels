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

class UserDAO:
    """
    Data Access Object for User model
    Only handles interactions with the user table
    """
    @staticmethod
    def create_user(username: str, password: str, phone: Optional[str] = None, 
                   email: Optional[str] = None, role: str = 'user') -> User:
        """Create a new user and save to database"""
        user = User(
            username=username,
            phone=phone,
            email=email,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Retrieve user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_phone(phone: str) -> Optional[User]:
        """Retrieve user by phone number"""
        return User.query.filter_by(phone=phone).first()
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Retrieve user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def update_user_profile(user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """Update user profile information"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Update user attributes
        for key, value in data.items():
            if hasattr(user, key) and key not in ['id', 'password_hash', 'created_at', 'updated_at']:
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    @staticmethod
    def change_user_status(user_id: int, status: bool) -> Optional[User]:
        """Enable or disable a user account"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Convert boolean to integer: True = enabled (0), False = disabled (1)
        user.status = 0 if status else 1
        db.session.commit()
        return user
    
    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of all users"""
        users = User.query.paginate(page=page, per_page=per_page)
        return {
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'users': [user.to_dict() for user in users.items]
        }


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
        role = user.get_role()
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
            'role': user.get_role(),
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
        Check if user has permission
        
        Args:
            user_id: User ID
            required_role: Required role (if any)
            resource_id: Resource ID (if any)
            resource_type: Resource type (if any)
            
        Returns:
            Boolean indicating if user has permission
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        # Admin has all permissions
        if user.is_admin():
            return True
        
        # Role-specific checks
        if required_role == 'author' and user.is_author():
            # If resource is specified, check if user is the author
            if resource_type == 'novel' and resource_id:
                novel = Novel.query.get(resource_id)
                if novel and novel.author_id:
                    # 检查小说的作者ID是否匹配用户的作者ID
                    author = Author.query.filter_by(user_id=user.id).first()
                    return author and novel.author_id == author.id
                
            # Just checking for author role
            return True
        
        # Regular user permissions
        # Check if user owns the resource
        if resource_type and resource_id:
            # Novel ownership check is already covered by author check
            pass
                
        # No specific permission required
        return required_role is None
    
    @staticmethod
    def update_user_role(admin_id: int, target_user_id: int, new_role: str) -> Dict[str, Any]:
        """
        Update user role (admin only)
        
        Args:
            admin_id: Admin user ID
            target_user_id: Target user ID
            new_role: New role
            
        Returns:
            Dict with success status and message
        """
        # 验证管理员权限
        admin_user = User.query.get(admin_id)
        if not admin_user or not admin_user.is_admin():
            return {'success': False, 'message': 'Unauthorized'}
            
        target_user = User.query.get(target_user_id)
        if not target_user:
            return {'success': False, 'message': 'User not found'}
            
        # 根据角色创建或删除对应表记录
        if new_role == 'author':
            # 删除admin角色(如果有)
            admin = Admin.query.filter_by(user_id=target_user_id).first()
            if admin:
                db.session.delete(admin)
                
            # 创建author角色(如果没有)
            author = Author.query.filter_by(user_id=target_user_id).first()
            if not author:
                author = Author(
                    user_id=target_user_id,
                    pen_name=target_user.username,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(author)
        
        elif new_role == 'admin':
            # 删除author角色(如果有)
            author = Author.query.filter_by(user_id=target_user_id).first()
            if author:
                db.session.delete(author)
                
            # 创建admin角色(如果没有)
            admin = Admin.query.filter_by(user_id=target_user_id).first()
            if not admin:
                admin = Admin(
                    user_id=target_user_id,
                    admin_level=1,
                    permissions={'content': True, 'user': True},
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(admin)
        
        elif new_role == 'user':
            # 删除author和admin角色(如果有)
            author = Author.query.filter_by(user_id=target_user_id).first()
            if author:
                db.session.delete(author)
                
            admin = Admin.query.filter_by(user_id=target_user_id).first()
            if admin:
                db.session.delete(admin)
        
        db.session.commit()
        
        return {
            'success': True,
            'message': f'User role updated to {new_role}',
            'user_id': target_user.id
        }
    
    @staticmethod
    def manage_user_status(admin_id: int, target_user_id: int, status: bool) -> Dict[str, Any]:
        """Enable or disable a user account (admin only)"""
        # Verify admin permissions
        if not UserService.check_permission(admin_id, 'admin'):
            return {'success': False, 'error': 'Admin privileges required'}
        
        # Update user status
        user = UserDAO.change_user_status(target_user_id, status)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        action = 'enabled' if status else 'disabled'
        return {
            'success': True,
            'message': f'User account {action} successfully',
            'user': user.to_dict()
        }
    
    @staticmethod
    def list_users(admin_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of all users (admin only)"""
        # Verify admin permissions
        if not UserService.check_permission(admin_id, 'admin'):
            return {'success': False, 'error': 'Admin privileges required'}
        
        # Get users
        result = UserDAO.get_all_users(page, per_page)
        return {
            'success': True,
            **result
        }
    
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
        # Get user
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Verify current password
        if not user.check_password(current_password):
            return {'success': False, 'error': 'Current password is incorrect'}
        
        # Validate new password
        if len(new_password) < 6:
            return {'success': False, 'error': 'Password must be at least 6 characters long'}
            
        # Set new password
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Password changed successfully'
        }