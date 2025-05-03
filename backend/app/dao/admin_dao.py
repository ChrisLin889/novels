from typing import List, Dict, Optional, Tuple
from app import db
from app.models.admin import SensitiveWord, ContentAudit, UserAction, Admin
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import Comment
from app.models.author import Author
from app.services.permission_service import PermissionService
from sqlalchemy import desc, func
from datetime import datetime, timedelta

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
        
        # 获取管理员的 admin_id (而不是 user_id)
        admin = Admin.query.filter_by(user_id=admin_id).first()
        if not admin:
            raise ValueError(f"Admin record not found for user_id {admin_id}")
        actual_admin_id = admin.id
            
        # Update user status
        user.status = 1  # Banned
        user.banned_until = datetime.utcnow().replace(
            hour=23, minute=59, second=59
        ) + timedelta(days=duration) if duration else None
        
        # Create action record
        action = UserAction(
            admin_id=actual_admin_id,  # 使用实际的admin_id而不是用户ID
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
        
        # 获取管理员的 admin_id (而不是 user_id)
        admin = Admin.query.filter_by(user_id=admin_id).first()
        if not admin:
            raise ValueError(f"Admin record not found for user_id {admin_id}")
        actual_admin_id = admin.id
            
        # Update user status
        user.status = 0  # Active
        user.banned_until = None
        
        # Create action record
        action = UserAction(
            admin_id=actual_admin_id,  # 使用实际的admin_id而不是用户ID
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
    
    # ====== Recycle Bin ======
    
    @staticmethod
    def soft_delete_novel(novel_id: int) -> bool:
        """
        Soft delete a novel (move to recycle bin)
        
        Args:
            novel_id: ID of novel to soft delete
            
        Returns:
            Success status
        """
        novel = Novel.query.get(novel_id)
        if not novel:
            return False
        
        try:
            # Soft delete novel
            novel.is_deleted = True
            novel.deleted_at = datetime.now()
            
            # Also soft delete related chapters
            Chapter.query.filter_by(novel_id=novel_id).update({
                'is_deleted': True,
                'deleted_at': datetime.now()
            })
            
            # Also soft delete related comments
            Comment.query.filter_by(novel_id=novel_id).update({
                'is_deleted': True,
                'deleted_at': datetime.now()
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error soft deleting novel: {str(e)}")
            return False

    @staticmethod
    def soft_delete_chapter(chapter_id: int) -> bool:
        """
        Soft delete a chapter (move to recycle bin)
        
        Args:
            chapter_id: ID of chapter to soft delete
            
        Returns:
            Success status
        """
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return False
        
        try:
            # Soft delete chapter
            chapter.is_deleted = True
            chapter.deleted_at = datetime.now()
            
            # Also soft delete related comments
            Comment.query.filter_by(chapter_id=chapter_id).update({
                'is_deleted': True,
                'deleted_at': datetime.now()
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error soft deleting chapter: {str(e)}")
            return False

    @staticmethod
    def soft_delete_comment(comment_id: int) -> bool:
        """
        Soft delete a comment (move to recycle bin)
        
        Args:
            comment_id: ID of comment to soft delete
            
        Returns:
            Success status
        """
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        
        try:
            comment.is_deleted = True
            comment.deleted_at = datetime.now()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error soft deleting comment: {str(e)}")
            return False

    @staticmethod
    def get_deleted_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Tuple[List[Novel], int]:
        """
        Get all novels in recycle bin
        
        Args:
            page: Page number
            per_page: Items per page
            title_filter: Optional title filter
            
        Returns:
            Tuple of (novels, total_count)
        """
        query = Novel.query.filter_by(is_deleted=True)
        
        if title_filter:
            query = query.filter(Novel.title.ilike(f'%{title_filter}%'))
        
        total = query.count()
        novels = query.order_by(desc(Novel.deleted_at)).paginate(page=page, per_page=per_page).items
        
        return novels, total

    @staticmethod
    def get_deleted_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Tuple[List[Chapter], int]:
        """
        Get all chapters in recycle bin
        
        Args:
            novel_id: Optional novel ID filter
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (chapters, total_count)
        """
        query = Chapter.query.filter_by(is_deleted=True)
        
        if novel_id:
            query = query.filter_by(novel_id=novel_id)
        
        total = query.count()
        chapters = query.order_by(desc(Chapter.deleted_at)).paginate(page=page, per_page=per_page).items
        
        return chapters, total

    @staticmethod
    def get_deleted_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                         page: int = 1, per_page: int = 20) -> Tuple[List[Comment], int]:
        """
        Get all comments in recycle bin
        
        Args:
            novel_id: Optional novel ID filter
            chapter_id: Optional chapter ID filter
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (comments, total_count)
        """
        query = Comment.query.filter_by(is_deleted=True)
        
        if novel_id:
            query = query.filter_by(novel_id=novel_id)
        
        if chapter_id:
            query = query.filter_by(chapter_id=chapter_id)
        
        total = query.count()
        comments = query.order_by(desc(Comment.deleted_at)).paginate(page=page, per_page=per_page).items
        
        return comments, total

    @staticmethod
    def restore_novel(novel_id: int) -> bool:
        """
        Restore a novel and its related content from recycle bin
        
        Args:
            novel_id: ID of novel to restore
            
        Returns:
            Success status
        """
        novel = Novel.query.get(novel_id)
        if not novel or not novel.is_deleted:
            return False
        
        try:
            # Restore novel
            novel.is_deleted = False
            novel.deleted_at = None
            
            # Restore related chapters
            Chapter.query.filter_by(novel_id=novel_id, is_deleted=True).update({
                'is_deleted': False,
                'deleted_at': None
            })
            
            # Restore related comments
            Comment.query.filter_by(novel_id=novel_id, is_deleted=True).update({
                'is_deleted': False,
                'deleted_at': None
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error restoring novel: {str(e)}")
            return False

    @staticmethod
    def restore_chapter(chapter_id: int) -> bool:
        """
        Restore a chapter and its related comments from recycle bin
        
        Args:
            chapter_id: ID of chapter to restore
            
        Returns:
            Success status
        """
        chapter = Chapter.query.get(chapter_id)
        if not chapter or not chapter.is_deleted:
            return False
        
        try:
            # Restore chapter
            chapter.is_deleted = False
            chapter.deleted_at = None
            
            # Also restore related comments
            Comment.query.filter_by(chapter_id=chapter_id, is_deleted=True).update({
                'is_deleted': False,
                'deleted_at': None
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error restoring chapter: {str(e)}")
            return False

    @staticmethod
    def restore_comment(comment_id: int) -> bool:
        """
        Restore a comment from recycle bin
        
        Args:
            comment_id: ID of comment to restore
            
        Returns:
            Success status
        """
        comment = Comment.query.get(comment_id)
        if not comment or not comment.is_deleted:
            return False
        
        try:
            comment.is_deleted = False
            comment.deleted_at = None
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error restoring comment: {str(e)}")
            return False

    @staticmethod
    def permanently_delete_novel(novel_id: int) -> bool:
        """
        Permanently delete a novel and all its chapters and comments (cascade delete)
        
        Args:
            novel_id: ID of novel to delete permanently
            
        Returns:
            Success status
        """
        novel = Novel.query.get(novel_id)
        if not novel:
            return False
        
        try:
            # Delete all comments related to this novel
            Comment.query.filter_by(novel_id=novel_id).delete()
            
            # Delete novel (will cascade delete chapters via foreign key constraints)
            db.session.delete(novel)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error permanently deleting novel: {str(e)}")
            return False

    @staticmethod
    def permanently_delete_chapter(chapter_id: int) -> bool:
        """
        Permanently delete a chapter and its related comments
        
        Args:
            chapter_id: ID of chapter to delete permanently
            
        Returns:
            Success status
        """
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return False
        
        try:
            # Delete all comments related to this chapter
            Comment.query.filter_by(chapter_id=chapter_id).delete()
            
            # Delete chapter
            db.session.delete(chapter)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error permanently deleting chapter: {str(e)}")
            return False

    @staticmethod
    def permanently_delete_comment(comment_id: int) -> bool:
        """
        Permanently delete a comment
        
        Args:
            comment_id: ID of comment to delete permanently
            
        Returns:
            Success status
        """
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        
        try:
            db.session.delete(comment)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error permanently deleting comment: {str(e)}")
            return False 