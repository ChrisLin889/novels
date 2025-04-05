from app.models.user import User
from app import db
from typing import Dict, Any, List, Optional
from app.utils.security import validate_password
import bcrypt

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
    def register(username: str, password: str, phone: Optional[str] = None, 
                email: Optional[str] = None) -> Dict[str, Any]:
        """Register a new user"""
        # Input validation
        if not username or not password:
            return {'success': False, 'error': 'Missing required fields'}
        
        if not phone and not email:
            return {'success': False, 'error': 'Either phone or email is required'}
        
        # Password validation
        if not validate_password(password):
            return {'success': False, 'error': 'Password does not meet requirements'}
        
        # Check for existing users
        if phone and UserDAO.get_user_by_phone(phone):
            return {'success': False, 'error': 'Phone number already registered'}
        
        if email and UserDAO.get_user_by_email(email):
            return {'success': False, 'error': 'Email already registered'}
        
        # Create user
        try:
            user = UserDAO.create_user(username, password, phone, email)
            return {
                'success': True,
                'message': 'User registered successfully',
                'user': user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def login(identifier: str, password: str, is_email: bool = False) -> Dict[str, Any]:
        """Login a user with phone or email"""
        # Find user
        user = None
        if is_email:
            user = UserDAO.get_user_by_email(identifier)
        else:
            user = UserDAO.get_user_by_phone(identifier)
        
        # Check user exists
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Check account status (0 = active, 1 = banned)
        if user.status != 0:
            return {'success': False, 'error': 'Account is disabled'}
        
        # Verify password
        if not user.check_password(password):
            return {'success': False, 'error': 'Invalid password'}
        
        # Return user data
        return {
            'success': True,
            'user': user.to_dict(),
            'user_id': user.id,
            'role': user.role
        }
    
    @staticmethod
    def get_profile(user_id: int) -> Dict[str, Any]:
        """Get user profile by ID"""
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        return {
            'success': True,
            'user': user.to_dict()
        }
    
    @staticmethod
    def update_profile(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile information"""
        # Filter out sensitive fields
        safe_data = {k: v for k, v in data.items() 
                    if k in ['username', 'avatar']}
        
        user = UserDAO.update_user_profile(user_id, safe_data)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        return {
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }
    
    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password"""
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Verify current password
        if not user.check_password(current_password):
            return {'success': False, 'error': 'Current password is incorrect'}
        
        # Validate new password
        if not validate_password(new_password):
            return {'success': False, 'error': 'New password does not meet requirements'}
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Password changed successfully'
        }
    
    @staticmethod
    def check_permission(user_id: int, required_role: str) -> bool:
        """Check if user has required role"""
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return False
        
        # Admin has all permissions
        if user.role == 'admin':
            return True
        
        # Author can perform author actions
        if required_role == 'author' and user.role == 'author':
            return True
        
        # Regular user permissions
        if required_role == 'user':
            return True
        
        return False
    
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
    def update_user_role(admin_id: int, target_user_id: int, new_role: str) -> Dict[str, Any]:
        """Update a user's role (admin only)"""
        try:
            # Check if admin exists and has admin role
            admin = UserDAO.get_user_by_id(admin_id)
            if not admin or admin.role != 'admin':
                return {'success': False, 'error': 'Admin privileges required'}
            
            # Check if target user exists
            target_user = UserDAO.get_user_by_id(target_user_id)
            if not target_user:
                return {'success': False, 'error': 'User not found'}
            
            # Update role
            target_user.role = new_role
            db.session.commit()
            
            return {
                'success': True,
                'message': f'User role updated to {new_role}',
                'user': target_user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)} 