from typing import List, Dict, Optional, Tuple
from app import db
from app.models.admin import SensitiveWord, ContentAudit, UserAction, Admin
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import Comment
from app.models.author import Author
from app.services.permission_service import PermissionService
from sqlalchemy import desc, func
from datetime import datetime

class AdminDAO:
    """
    Data Access Object for admin operations
    """
    
    # ====== User Management ======
    
    @staticmethod
    def get_users(page: int = 1, per_page: int = 20, role: Optional[str] = None) -> Tuple[List[User], int]:
        """
        Get users with pagination
        
        Args:
            page: Page number
            per_page: Items per page
            role: Optional role filter
            
        Returns:
            Tuple of (users, total_count)
        """
        query = User.query
        
        if role:
            if role == 'admin':
                # 获取所有管理员ID
                admin_user_ids = db.session.query(Admin.user_id).all()
                admin_user_ids = [id[0] for id in admin_user_ids]
                query = query.filter(User.id.in_(admin_user_ids))
            elif role == 'author':
                # 获取所有作者ID
                author_user_ids = db.session.query(Author.user_id).all()
                author_user_ids = [id[0] for id in author_user_ids]
                query = query.filter(User.id.in_(author_user_ids))
            elif role == 'user':
                # 普通用户 = 既不是管理员也不是作者
                admin_user_ids = db.session.query(Admin.user_id).all()
                admin_user_ids = [id[0] for id in admin_user_ids]
                author_user_ids = db.session.query(Author.user_id).all()
                author_user_ids = [id[0] for id in author_user_ids]
                special_user_ids = admin_user_ids + author_user_ids
                query = query.filter(~User.id.in_(special_user_ids))
            
        total = query.count()
        users = query.order_by(desc(User.created_at)) \
                    .offset((page - 1) * per_page) \
                    .limit(per_page) \
                    .all()
                    
        return users, total
    
    @staticmethod
    def ban_user(admin_id: int, user_id: int, reason: str, duration: Optional[int] = None) -> UserAction:
        """
        Ban a user
        
        Args:
            admin_id: ID of admin performing the action
            user_id: ID of user to ban
            reason: Reason for ban
            duration: Ban duration in days (None for permanent)
            
        Returns:
            UserAction record
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
            
        # Update user status
        user.status = 1  # Banned
        user.banned_until = datetime.utcnow().replace(
            hour=23, minute=59, second=59
        ) + datetime.timedelta(days=duration) if duration else None
        
        # Create action record
        action = UserAction(
            admin_id=admin_id,
            target_user_id=user_id,
            action_type='ban',
            reason=reason,
            duration=duration
        )
        
        db.session.add(action)
        db.session.commit()
        return action
    
    @staticmethod
    def unban_user(admin_id: int, user_id: int, reason: str) -> UserAction:
        """
        Unban a user
        
        Args:
            admin_id: ID of admin performing the action
            user_id: ID of user to unban
            reason: Reason for unban
            
        Returns:
            UserAction record
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
            
        if user.status != 1:  # Not banned
            raise ValueError(f"User {user_id} is not banned")
            
        # Update user status
        user.status = 0  # Active
        user.banned_until = None
        
        # Create action record
        action = UserAction(
            admin_id=admin_id,
            target_user_id=user_id,
            action_type='unban',
            reason=reason
        )
        
        db.session.add(action)
        db.session.commit()
        return action
    
    @staticmethod
    def get_user_actions(user_id: Optional[int] = None, 
                         page: int = 1, 
                         per_page: int = 20) -> Tuple[List[UserAction], int]:
        """
        Get user actions history
        
        Args:
            user_id: Optional user ID to filter by
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (actions, total_count)
        """
        query = UserAction.query
        
        if user_id:
            query = query.filter(UserAction.target_user_id == user_id)
            
        total = query.count()
        actions = query.order_by(desc(UserAction.created_at)) \
                      .offset((page - 1) * per_page) \
                      .limit(per_page) \
                      .all()
                      
        return actions, total
    
    # ====== Content Management ======
    
    @staticmethod
    def get_pending_content(content_type: str, page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int]:
        """
        Get pending content for moderation
        
        Args:
            content_type: Type of content (novel, chapter, comment)
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (content_items, total_count)
        """
        # First get all pending audit records for this content type
        audits = ContentAudit.query.filter(
            ContentAudit.content_type == content_type,
            ContentAudit.status == 'pending'
        ).order_by(
            desc(ContentAudit.created_at)
        ).offset((page - 1) * per_page) \
         .limit(per_page) \
         .all()
        
        # Now fetch the actual content based on content type and IDs
        result = []
        if content_type == 'novel':
            for audit in audits:
                novel = Novel.query.get(audit.content_id)
                if novel:
                    item = novel.to_dict()
                    item['audit_id'] = audit.id
                    result.append(item)
        elif content_type == 'chapter':
            for audit in audits:
                chapter = Chapter.query.get(audit.content_id)
                if chapter:
                    item = chapter.to_dict()
                    item['audit_id'] = audit.id
                    result.append(item)
        elif content_type == 'comment':
            for audit in audits:
                comment = Comment.query.get(audit.content_id)
                if comment:
                    item = comment.to_dict()
                    item['audit_id'] = audit.id
                    result.append(item)
        
        # Count total pending items for this content type
        total = ContentAudit.query.filter(
            ContentAudit.content_type == content_type,
            ContentAudit.status == 'pending'
        ).count()
        
        return result, total
    
    @staticmethod
    def audit_content(audit_id: int, admin_id: int, status: str, reason: Optional[str] = None) -> ContentAudit:
        """
        Approve or reject content
        
        Args:
            audit_id: ID of the audit record
            admin_id: ID of admin performing the action
            status: New status (approved or rejected)
            reason: Optional reason for rejection
            
        Returns:
            Updated ContentAudit record
        """
        audit = ContentAudit.query.get(audit_id)
        if not audit or audit.status != 'pending':
            raise ValueError(f"Audit record {audit_id} not found or not pending")
            
        # Update audit record
        audit.status = status
        audit.admin_id = admin_id
        audit.reason = reason if status == 'rejected' else None
        audit.updated_at = datetime.utcnow()
        
        # If rejected, update the content status
        if status == 'rejected':
            if audit.content_type == 'novel':
                novel = Novel.query.get(audit.content_id)
                if novel:
                    novel.status = 'rejected'
            elif audit.content_type == 'chapter':
                chapter = Chapter.query.get(audit.content_id)
                if chapter:
                    chapter.status = 'rejected'
            elif audit.content_type == 'comment':
                comment = Comment.query.get(audit.content_id)
                if comment:
                    comment.status = 'rejected'
        
        db.session.commit()
        return audit
    
    # ====== Sensitive Words Management ======
    
    @staticmethod
    def get_sensitive_words(category: Optional[str] = None, 
                            page: int = 1, 
                            per_page: int = 50) -> Tuple[List[SensitiveWord], int]:
        """
        Get sensitive words with pagination
        
        Args:
            category: Filter by category
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (words, total_count)
        """
        query = SensitiveWord.query
        
        if category:
            query = query.filter(SensitiveWord.category == category)
            
        total = query.count()
        words = query.order_by(SensitiveWord.word) \
                     .offset((page - 1) * per_page) \
                     .limit(per_page) \
                     .all()
                     
        return words, total
    
    @staticmethod
    def add_sensitive_word(word: str, level: int, category: str, admin_id: int) -> SensitiveWord:
        """
        Add a new sensitive word
        
        Args:
            word: The word to add
            level: Sensitivity level (1=warn, 2=block, 3=ban)
            category: Category (political, violence, sex, etc.)
            admin_id: ID of admin adding the word
            
        Returns:
            Created SensitiveWord
        """
        sensitive_word = SensitiveWord(
            word=word,
            level=level,
            category=category,
            added_by=admin_id
        )
        
        db.session.add(sensitive_word)
        db.session.commit()
        return sensitive_word
    
    @staticmethod
    def delete_sensitive_word(word_id: int) -> bool:
        """
        Delete a sensitive word
        
        Args:
            word_id: ID of word to delete
            
        Returns:
            True if deleted, False if not found
        """
        word = SensitiveWord.query.get(word_id)
        if not word:
            return False
            
        db.session.delete(word)
        db.session.commit()
        return True 