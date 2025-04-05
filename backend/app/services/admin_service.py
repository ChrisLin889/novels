from typing import List, Dict, Optional, Tuple
from app.dao.admin_dao import AdminDAO
from app.models.admin import SensitiveWord, ContentAudit, UserAction, CrawledNovel, CrawledChapter
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import Comment, UserTip
from datetime import datetime
import re
from sqlalchemy import func
from app import db

class AdminService:
    """
    Service for handling admin operations
    """
    
    # ====== User Management ======
    
    @staticmethod
    def get_users(page: int = 1, per_page: int = 20, role: Optional[str] = None) -> Dict:
        """
        Get users with pagination
        
        Args:
            page: Page number
            per_page: Items per page
            role: Filter by user role
            
        Returns:
            Dict with users and pagination info
        """
        users, total = AdminDAO.get_users(page, per_page, role)
        
        return {
            'users': [user.to_dict() for user in users],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def manage_user(admin_id: int, user_id: int, action: str, reason: str, duration: Optional[int] = None) -> Dict:
        """
        Manage a user (ban, unban)
        
        Args:
            admin_id: ID of admin performing the action
            user_id: ID of user to manage
            action: Action to take ("ban" or "unban")
            reason: Reason for action
            duration: Ban duration in days (for "ban" action)
            
        Returns:
            Action result
        """
        if action == 'ban':
            user_action = AdminDAO.ban_user(admin_id, user_id, reason, duration)
            return {
                'success': True,
                'message': f"User {user_id} has been banned",
                'action_id': user_action.id
            }
        elif action == 'unban':
            user_action = AdminDAO.unban_user(admin_id, user_id, reason)
            return {
                'success': True,
                'message': f"User {user_id} has been unbanned",
                'action_id': user_action.id
            }
        else:
            return {
                'success': False,
                'message': f"Unknown action: {action}"
            }
    
    @staticmethod
    def get_user_actions(user_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get user management actions with pagination
        
        Args:
            user_id: Filter by target user ID
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with actions and pagination info
        """
        actions, total = AdminDAO.get_user_actions(user_id, page, per_page)
        
        return {
            'actions': [action.to_dict() for action in actions],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def update_user_role(admin_id: int, user_id: int, role: str) -> Dict:
        """
        Update a user's role
        
        Args:
            admin_id: ID of admin performing the action
            user_id: ID of user to update
            role: New role for the user
            
        Returns:
            Dict with result
        """
        # Verify admin permissions
        admin = User.query.get(admin_id)
        if not admin or admin.role != 'admin':
            return {
                'success': False,
                'message': 'Admin privileges required'
            }
        
        # Verify target user exists
        user = User.query.get(user_id)
        if not user:
            return {
                'success': False,
                'message': f'User with ID {user_id} not found'
            }
        
        # Verify role is valid
        valid_roles = ['user', 'author', 'admin']
        if role not in valid_roles:
            return {
                'success': False,
                'message': f'Invalid role: {role}'
            }
        
        # Update user role
        user.role = role
        db.session.commit()
        
        # Create action record
        action = UserAction(
            admin_id=admin_id,
            target_user_id=user_id,
            action_type='update_role',
            reason=f'Role updated to {role}'
        )
        db.session.add(action)
        db.session.commit()
        
        return {
            'success': True,
            'message': f'User role updated to {role}',
            'user': user.to_dict()
        }
    
    # ====== Content Management ======
    
    @staticmethod
    def get_pending_content(content_type: str, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get pending content for moderation
        
        Args:
            content_type: Type of content ("novel", "chapter", "comment")
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with content and pagination info
        """
        content, total = AdminDAO.get_pending_content(content_type, page, per_page)
        
        return {
            'content': content,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'content_type': content_type
        }
    
    @staticmethod
    def audit_content(audit_id: int, admin_id: int, status: str, reason: Optional[str] = None) -> Dict:
        """
        Approve or reject content
        
        Args:
            audit_id: ID of the audit record
            admin_id: ID of admin performing the action
            status: New status ("approved" or "rejected")
            reason: Reason for rejection
            
        Returns:
            Dict with result
        """
        try:
            audit = AdminDAO.audit_content(audit_id, admin_id, status, reason)
            return {
                'success': True,
                'message': f"Content {audit.content_id} has been {status}",
                'audit': audit.to_dict()
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    # ====== Sensitive Words Management ======
    
    @staticmethod
    def filter_sensitive_content(content: str) -> Tuple[bool, List[Dict], str]:
        """
        Check content for sensitive words
        
        Args:
            content: Content to check
            
        Returns:
            Tuple of (has_sensitive, word_matches, filtered_content)
        """
        # Get all sensitive words
        words, _ = AdminDAO.get_sensitive_words(per_page=1000)
        
        # Check for matches
        matches = []
        filtered_content = content
        has_sensitive = False
        
        for word_obj in words:
            word = word_obj.word
            pattern = r'\b' + re.escape(word) + r'\b'
            
            if re.search(pattern, content, re.IGNORECASE):
                has_sensitive = True
                matches.append({
                    'word': word,
                    'level': word_obj.level,
                    'category': word_obj.category
                })
                
                # Replace based on sensitivity level
                if word_obj.level >= 2:  # Block or ban level
                    replacement = '*' * len(word)
                    filtered_content = re.sub(pattern, replacement, filtered_content, flags=re.IGNORECASE)
        
        return has_sensitive, matches, filtered_content
    
    @staticmethod
    def get_sensitive_words(category: Optional[str] = None, page: int = 1, per_page: int = 50) -> Dict:
        """
        Get sensitive words with pagination
        
        Args:
            category: Filter by category
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with words and pagination info
        """
        words, total = AdminDAO.get_sensitive_words(category, page, per_page)
        
        return {
            'words': [word.to_dict() for word in words],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def manage_sensitive_word(word: str, level: int, category: str, admin_id: int, action: str, word_id: Optional[int] = None) -> Dict:
        """
        Add or delete a sensitive word
        
        Args:
            word: The sensitive word
            level: Sensitivity level
            category: Word category
            admin_id: ID of admin performing the action
            action: "add" or "delete"
            word_id: ID of word to delete (for delete action)
            
        Returns:
            Dict with result
        """
        if action == 'add':
            word_obj = AdminDAO.add_sensitive_word(word, level, category, admin_id)
            return {
                'success': True,
                'message': f"Word '{word}' added to sensitive words list",
                'word': word_obj.to_dict()
            }
        elif action == 'delete':
            success = AdminDAO.delete_sensitive_word(word_id)
            return {
                'success': success,
                'message': "Word deleted" if success else "Word not found"
            }
        else:
            return {
                'success': False,
                'message': f"Unknown action: {action}"
            }
    
    # ====== Crawler Management ======
    
    @staticmethod
    def get_crawled_novels(status: Optional[str] = None, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get crawled novels with pagination
        
        Args:
            status: Filter by status
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with novels and pagination info
        """
        novels, total = AdminDAO.get_crawled_novels(status, page, per_page)
        
        return {
            'novels': [novel.to_dict() for novel in novels],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_crawled_chapters(novel_id: int) -> Dict:
        """
        Get chapters for a crawled novel
        
        Args:
            novel_id: ID of the crawled novel
            
        Returns:
            Dict with chapters
        """
        chapters = AdminDAO.get_crawled_chapters(novel_id)
        
        return {
            'novel_id': novel_id,
            'chapters': [chapter.to_dict() for chapter in chapters],
            'total': len(chapters)
        }
    
    @staticmethod
    def manage_crawled_novel(novel_id: int, action: str, reason: Optional[str] = None) -> Dict:
        """
        Approve or reject a crawled novel
        
        Args:
            novel_id: ID of the crawled novel
            action: "approve" or "reject"
            reason: Reason for rejection
            
        Returns:
            Dict with result
        """
        if action == 'approve':
            success = AdminDAO.approve_crawled_novel(novel_id)
            return {
                'success': success,
                'message': "Novel approved and moved to production" if success else "Failed to approve novel"
            }
        elif action == 'reject':
            success = AdminDAO.reject_crawled_novel(novel_id, reason)
            return {
                'success': success,
                'message': "Novel rejected" if success else "Failed to reject novel"
            }
        else:
            return {
                'success': False,
                'message': f"Unknown action: {action}"
            }
    
    # ====== Statistics ======
    
    @staticmethod
    def get_dashboard_stats() -> Dict:
        """
        Get statistics for admin dashboard
        
        Returns:
            Dict with statistics
        """
        # Get today's date range
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # User statistics
        total_users = User.query.count()
        new_users_today = User.query.filter(User.created_at >= today_start).count()
        active_users_today = User.query.filter(User.updated_at >= today_start).count()
        banned_users = User.query.filter(User.status == 1).count()
        
        # Content statistics
        total_novels = Novel.query.count()
        total_chapters = Chapter.query.count()
        pending_moderation = ContentAudit.query.filter_by(status='pending').count()
        rejected_content = ContentAudit.query.filter_by(status='rejected').count()
        
        # Activity statistics
        comments_today = Comment.query.filter(Comment.created_at >= today_start).count()
        readings_today = db.session.query(func.sum(Novel.view_count)).filter(
            Novel.updated_at >= today_start
        ).scalar() or 0
        tips_today = db.session.query(func.sum(UserTip.amount)).filter(
            UserTip.created_at >= today_start
        ).scalar() or 0
        
        return {
            'user_stats': {
                'total_users': total_users,
                'new_users_today': new_users_today,
                'active_users_today': active_users_today,
                'banned_users': banned_users
            },
            'content_stats': {
                'total_novels': total_novels,
                'total_chapters': total_chapters,
                'pending_moderation': pending_moderation,
                'rejected_content': rejected_content
            },
            'activity_stats': {
                'comments_today': comments_today,
                'readings_today': readings_today,
                'tips_today': tips_today
            }
        } 