from app.models.user import User
from app import db
from typing import Dict, Any, List, Optional, Union


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