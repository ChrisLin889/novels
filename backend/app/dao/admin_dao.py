from typing import List, Dict, Optional, Tuple
from app import db
from app.models.admin import SensitiveWord, ContentAudit, UserAction, CrawledNovel, CrawledChapter
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import Comment
from sqlalchemy import desc, func, and_
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
            role: Filter by user role
            
        Returns:
            Tuple of (users, total_count)
        """
        query = User.query
        
        if role:
            query = query.filter(User.role == role)
            
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
            Created UserAction
        """
        # Update user status
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
            
        user.status = 'banned'
        if duration:
            user.ban_until = datetime.utcnow() + timedelta(days=duration)
        
        # Create action record
        action = UserAction(
            admin_id=admin_id,
            target_user_id=user_id,
            action_type='ban',
            reason=reason,
            duration=duration
        )
        
        # Save changes
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
            Created UserAction
        """
        # Update user status
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
            
        user.status = 'active'
        user.ban_until = None
        
        # Create action record
        action = UserAction(
            admin_id=admin_id,
            target_user_id=user_id,
            action_type='unban',
            reason=reason
        )
        
        # Save changes
        db.session.add(action)
        db.session.commit()
        
        return action
    
    @staticmethod
    def get_user_actions(user_id: Optional[int] = None, 
                         page: int = 1, 
                         per_page: int = 20) -> Tuple[List[UserAction], int]:
        """
        Get user management actions with pagination
        
        Args:
            user_id: Filter by target user ID
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
            content_type: Type of content ("novel", "chapter", "comment")
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (content_list, total_count)
        """
        query = ContentAudit.query.filter(
            and_(
                ContentAudit.content_type == content_type,
                ContentAudit.status == 'pending'
            )
        )
        
        total = query.count()
        audits = query.order_by(ContentAudit.created_at) \
                     .offset((page - 1) * per_page) \
                     .limit(per_page) \
                     .all()
        
        # Fetch the actual content objects
        content_list = []
        for audit in audits:
            content_obj = None
            
            if content_type == 'novel':
                content_obj = Novel.query.get(audit.content_id)
            elif content_type == 'chapter':
                content_obj = Chapter.query.get(audit.content_id)
            elif content_type == 'comment':
                content_obj = Comment.query.get(audit.content_id)
                
            if content_obj:
                # Combine audit info with content info
                content_data = content_obj.to_dict()
                content_data['audit_id'] = audit.id
                content_data['audit_status'] = audit.status
                content_data['audit_created_at'] = audit.created_at.isoformat()
                content_list.append(content_data)
        
        return content_list, total
    
    @staticmethod
    def audit_content(audit_id: int, admin_id: int, status: str, reason: Optional[str] = None) -> ContentAudit:
        """
        Approve or reject content
        
        Args:
            audit_id: ID of the audit record
            admin_id: ID of admin performing the action
            status: New status ("approved" or "rejected")
            reason: Reason for rejection
            
        Returns:
            Updated ContentAudit
        """
        audit = ContentAudit.query.get(audit_id)
        if not audit:
            raise ValueError(f"Audit with ID {audit_id} not found")
            
        # Update audit status
        audit.status = status
        audit.audited_by = admin_id
        audit.reason = reason
        
        # If rejected, we may need to hide the content
        if status == 'rejected':
            if audit.content_type == 'novel':
                novel = Novel.query.get(audit.content_id)
                if novel:
                    novel.status = 'hidden'
            elif audit.content_type == 'chapter':
                chapter = Chapter.query.get(audit.content_id)
                if chapter:
                    chapter.status = 'hidden'
            elif audit.content_type == 'comment':
                comment = Comment.query.get(audit.content_id)
                if comment:
                    comment.status = 'hidden'
        
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
            word: The sensitive word
            level: Sensitivity level (1=warn, 2=block, 3=ban)
            category: Category of the word
            admin_id: ID of admin adding the word
            
        Returns:
            Created SensitiveWord
        """
        # Check if word already exists
        existing = SensitiveWord.query.filter(SensitiveWord.word == word).first()
        if existing:
            # Update existing
            existing.level = level
            existing.category = category
            db.session.commit()
            return existing
            
        # Create new entry
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
    
    # ====== Crawler Management ======
    
    @staticmethod
    def get_crawled_novels(status: Optional[str] = None, 
                           page: int = 1, 
                           per_page: int = 20) -> Tuple[List[CrawledNovel], int]:
        """
        Get crawled novels with pagination
        
        Args:
            status: Filter by status (pending, approved, rejected)
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (novels, total_count)
        """
        query = CrawledNovel.query
        
        if status:
            query = query.filter(CrawledNovel.status == status)
            
        total = query.count()
        novels = query.order_by(desc(CrawledNovel.created_at)) \
                     .offset((page - 1) * per_page) \
                     .limit(per_page) \
                     .all()
                     
        return novels, total
    
    @staticmethod
    def get_crawled_chapters(novel_id: int) -> List[CrawledChapter]:
        """
        Get chapters for a crawled novel
        
        Args:
            novel_id: ID of the crawled novel
            
        Returns:
            List of CrawledChapter
        """
        chapters = CrawledChapter.query.filter(
            CrawledChapter.novel_id == novel_id
        ).order_by(
            CrawledChapter.chapter_number
        ).all()
        
        return chapters
    
    @staticmethod
    def approve_crawled_novel(novel_id: int) -> bool:
        """
        Approve a crawled novel and move it to production
        
        Args:
            novel_id: ID of the crawled novel
            
        Returns:
            True if successful
        """
        crawled_novel = CrawledNovel.query.get(novel_id)
        if not crawled_novel or crawled_novel.status != 'pending':
            return False
            
        # Create a new novel in production table
        novel = Novel(
            title=crawled_novel.title,
            author=crawled_novel.author,
            category=crawled_novel.category,
            cover=crawled_novel.cover,
            intro=crawled_novel.intro,
            status='ongoing'
        )
        
        db.session.add(novel)
        db.session.flush()  # Get the new novel ID
        
        # Get all chapters for this novel
        crawled_chapters = CrawledChapter.query.filter(
            CrawledChapter.novel_id == novel_id
        ).order_by(
            CrawledChapter.chapter_number
        ).all()
        
        # Create production chapters
        for crawled_chapter in crawled_chapters:
            chapter = Chapter(
                novel_id=novel.id,
                chapter_number=crawled_chapter.chapter_number,
                title=crawled_chapter.title,
                content=crawled_chapter.content,
                word_count=len(crawled_chapter.content)
            )
            db.session.add(chapter)
        
        # Update crawled novel status
        crawled_novel.status = 'approved'
        
        db.session.commit()
        return True
    
    @staticmethod
    def reject_crawled_novel(novel_id: int, reason: str) -> bool:
        """
        Reject a crawled novel
        
        Args:
            novel_id: ID of the crawled novel
            reason: Reason for rejection
            
        Returns:
            True if successful
        """
        crawled_novel = CrawledNovel.query.get(novel_id)
        if not crawled_novel or crawled_novel.status != 'pending':
            return False
            
        # Update status
        crawled_novel.status = 'rejected'
        
        # Create an audit record
        audit = ContentAudit(
            content_type='crawled_novel',
            content_id=novel_id,
            status='rejected',
            reason=reason
        )
        
        db.session.add(audit)
        db.session.commit()
        return True 