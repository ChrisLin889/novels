from typing import List, Dict, Optional, Tuple
from app.dao.admin_dao import AdminDAO
from app.models.admin import Admin, SensitiveWord, ContentAudit, UserAction
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import Comment
from app.services.permission_service import PermissionService
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
        更新用户角色
        
        Args:
            admin_id: 执行操作的管理员ID
            user_id: 目标用户ID
            role: 新角色
            
        Returns:
            操作结果
        """
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': 'Admin privileges required'
            }
        
        # 验证目标用户存在
        user = User.query.get(user_id)
        if not user:
            return {
                'success': False,
                'message': f'User with ID {user_id} not found'
            }
        
        # 验证角色有效
        valid_roles = ['user', 'author', 'admin']
        if role not in valid_roles:
            return {
                'success': False,
                'message': f'Invalid role: {role}'
            }
        
        try:
            # 获取管理员的 admin_id (而不是 user_id)
            admin = Admin.query.filter_by(user_id=admin_id).first()
            if not admin:
                return {
                    'success': False,
                    'message': f'Admin record not found for user_id {admin_id}'
                }
            actual_admin_id = admin.id
            
            # 根据角色更新相应的关联记录
            if role == 'admin':
                # 检查是否已经是管理员
                if not PermissionService.has_role(user_id, 'admin'):
                    # 创建管理员记录
                    admin = Admin(
                        user_id=user_id,
                        admin_level=1,
                        permissions={'content': True, 'user': True}
                    )
                    db.session.add(admin)
            elif role == 'author':
                # 检查是否已经是作者
                if not PermissionService.has_role(user_id, 'author'):
                    # 创建作者记录
                    from app.models.author import Author
                    author = Author(
                        user_id=user_id,
                        pen_name=user.username
                    )
                    db.session.add(author)
            elif role == 'user':
                # 如果是管理员，删除管理员记录
                if PermissionService.has_role(user_id, 'admin'):
                    Admin.query.filter_by(user_id=user_id).delete()
                
                # 如果是作者，删除作者记录
                if PermissionService.has_role(user_id, 'author'):
                    from app.models.author import Author
                    Author.query.filter_by(user_id=user_id).delete()
            
            # 创建操作记录
            action = UserAction(
                admin_id=actual_admin_id,  # 使用实际的admin_id而不是用户ID
                target_user_id=user_id,
                action_type='update_role',
                reason=f'Role updated to {role}'
            )
            db.session.add(action)
            db.session.commit()
            
            # 获取最新的用户信息
            updated_user = User.query.get(user_id)
            
            return {
                'success': True,
                'message': f'User role updated to {role}',
                'user': updated_user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error updating role: {str(e)}'
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
    def filter_and_notify_sensitive_content(content: str, user_id: int, 
                                           content_type: str, content_id: int) -> Tuple[bool, List[Dict], str]:
        """
        检查内容中的敏感词并发送通知
        
        Args:
            content: 要检查的内容
            user_id: 内容所有者ID
            content_type: 内容类型 (novel, chapter, comment)
            content_id: 内容ID
            
        Returns:
            Tuple of (has_sensitive, word_matches, filtered_content)
        """
        # 调用现有的敏感词过滤函数
        has_sensitive, matches, filtered_content = AdminService.filter_sensitive_content(content)
        
        # 如果检测到敏感词，发送通知
        if has_sensitive and matches:
            from app.services.notification_service import NotificationService
            NotificationService.create_sensitive_word_notification(
                user_id=user_id,
                content_type=content_type,
                content_id=content_id,
                matches=matches
            )
        
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
                'readings_today': readings_today
            }
        } 