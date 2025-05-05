from app.models.novel import Novel, Chapter, novel_tag
from app.models.interaction import UserCollection, UserHistory, Comment
from app.models.user import User
from app.models.author import Author
from app.models.tag import Tag
from app import db
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import desc, func
from app.services.permission_service import PermissionService
from datetime import datetime
from app.dao.novel_dao import NovelDAO
from app.dao.interaction_dao import InteractionDAO
from app.services.admin_service import AdminService
from app.models.audit_status import AuditStatus
from app.config.settings import get_settings
from app.models.admin import Admin, ContentAudit

class NovelService:
    """
    Service for accessing and manipulating novel data
    Handles business logic, error handling, and response formatting
    """
    
    @staticmethod
    def get_novel_by_id(novel_id: int) -> Dict[str, Any]:
        """Get novel details by ID
        
        Args:
            novel_id: Novel ID
            
        Returns:
            Dictionary with novel info and success status
        """
        try:
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
                
            return {
                'success': True,
                'novel': novel.to_dict()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_list(category: Optional[str] = None, page: int = 1, 
                      per_page: int = 10, sort_by: str = 'updated_at',
                      status: Optional[str] = None, sort_order: str = 'desc') -> Dict[str, Any]:
        """Get paginated list of novels with optional filtering
        
        Args:
            category: Optional category filter
            page: Page number
            per_page: Items per page
            sort_by: Sort field
            status: Optional status filter
            sort_order: Sort direction (asc or desc)
            
        Returns:
            Dictionary with novel list and pagination info
        """
        try:
            # Create base query with filters - only show approved content
            query = NovelDAO.get_novel_list_query(category, status, AuditStatus.APPROVED)
            
            # Apply sorting
            query = NovelDAO.apply_sorting(query, sort_by, sort_order)
            
            # Execute paginated query
            novels = query.paginate(page=page, per_page=per_page)
            
            return {
                'success': True,
                'total': novels.total,
                'pages': novels.pages,
                'current_page': page,
                'novels': [novel.to_dict() for novel in novels.items]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def search_novels(keyword: str, page: int = 1, per_page: int = 10, 
                     category: Optional[str] = None) -> Dict[str, Any]:
        """Search novels by keyword with optional filtering
        
        Args:
            keyword: Search term
            page: Page number
            per_page: Items per page
            category: Optional category filter
            
        Returns:
            Dictionary with search results and pagination info
        """
        if not keyword:
            return {'success': False, 'error': 'Search keyword is required'}
        
        try:
            # Create search query
            query = NovelDAO.search_novels_query(keyword, category)
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            novels = query.order_by(desc(Novel.updated_at))\
                          .offset((page - 1) * per_page)\
                          .limit(per_page)\
                          .all()
                          
            return {
                'success': True,
                'novels': [novel.to_dict() for novel in novels],
                'total': total,
                'pages': (total + per_page - 1) // per_page,
                'current_page': page
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_detail(novel_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get detailed information about a novel including its chapters
        
        Args:
            novel_id: Novel ID
            user_id: Optional user ID to check if user is the author
            
        Returns:
            Dictionary with novel details and chapters list
        """
        try:
            # Get novel by ID
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Check if novel is pending/rejected and user is not author
            if novel.audit_status != AuditStatus.APPROVED:
                # Check if user is author
                is_author = False
                if user_id:
                    author = Author.query.filter_by(user_id=user_id).first()
                    if author and author.id == novel.author_id:
                        is_author = True
                        
                # Check if user is admin
                is_admin = False
                if user_id:
                    admin = Admin.query.filter_by(user_id=user_id).first()
                    if admin:
                        is_admin = True
                        
                # Return error if user is not author or admin
                if not is_author and not is_admin:
                    return {'success': False, 'error': 'Novel not found or pending approval'}
            
            # Increment view count
            NovelDAO.increment_view_count(novel_id)
            
            # Get chapters for the novel - include pending if user is author
            include_pending = False
            if user_id:
                author = Author.query.filter_by(user_id=user_id).first()
                if author and author.id == novel.author_id:
                    include_pending = True
                    
            chapters = NovelDAO.get_novel_chapters(novel_id, include_pending)
            
            # Get novel data
            novel_data = novel.to_dict()
            
            # Add chapter list without content
            chapters_data = [
                {
                    'id': chapter.id,
                    'novel_id': chapter.novel_id,
                    'chapter_number': chapter.chapter_number,
                    'title': chapter.title,
                    'word_count': chapter.word_count,
                    'created_at': chapter.created_at.isoformat() if chapter.created_at else None,
                    'audit_status': chapter.audit_status
                }
                for chapter in chapters
            ]
            
            return {
                'success': True,
                'novel': novel_data,
                'chapters': chapters_data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_popular_novels(page: int = 1, per_page: int = 10, category: Optional[str] = None) -> Dict[str, Any]:
        """Get popular novels with pagination and optional category filtering
        
        Args:
            page: Page number
            per_page: Items per page
            category: Optional category filter
            
        Returns:
            Dictionary with popular novels and pagination info
        """
        try:
            # Create query for popular novels
            query = NovelDAO.get_popular_novels_query(category)
                
            # Apply pagination
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return {
                'success': True,
                'novels': [novel.to_dict() for novel in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_latest_novels(limit: int = 10) -> Dict[str, Any]:
        """Get latest novels
        
        Args:
            limit: Number of novels to return
            
        Returns:
            Dictionary with latest novels
        """
        try:
            novels = NovelDAO.get_latest_novels(limit)
            return {
                'success': True,
                'novels': [novel.to_dict() for novel in novels]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_categories() -> Dict[str, Any]:
        """Get list of categories with novel counts
        
        Returns:
            Dictionary with categories and their counts
        """
        try:
            categories = NovelDAO.get_categories()
            return {'success': True, 'categories': categories}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_author_novels(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """获取用户作为作者创建的小说列表
        
        Args:
            user_id: 用户ID（不是作者ID）
            page: 页码
            per_page: 每页数量
            
        Returns:
            包含作者小说列表和分页信息的字典
        """
        try:
            # 获取用户作为作者创建的小说查询
            query = NovelDAO.get_novel_by_user_id_query(user_id)
            
            # 应用分页
            pagination = query.order_by(desc(Novel.updated_at))\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            # 转换小说为字典
            novels = [novel.to_dict() for novel in pagination.items]
            
            return {
                'success': True,
                'novels': novels,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_novel(title: str, category: str, intro: str, 
                 cover: str = 'default_cover.jpg', tags: list = None,
                 user_id: int = None) -> Dict[str, Any]:
        """Add new novel
        
        Args:
            title: Novel title
            category: Novel category
            intro: Novel introduction
            cover: Cover image path
            tags: List of tag names
            user_id: User ID of the author
            
        Returns:
            Dictionary with new novel ID and success status
        """
        try:
            # Check if user is an author
            if user_id:
                author = Author.query.filter_by(user_id=user_id).first()
                if not author:
                    return {
                        'success': False, 
                        'error': 'User is not registered as an author'
                    }
                    
                # Determine audit status based on settings and author status
                settings = get_settings()
                content_audit_enabled = settings.get('enable_content_audit', True)
                
                if content_audit_enabled and not author.exempt_from_audit:
                    audit_status = AuditStatus.PENDING
                else:
                    audit_status = AuditStatus.APPROVED
                    
                # Create new novel
                novel = Novel(
                    title=title,
                    author=author.pen_name,
                    author_id=author.id,
                    category=category,
                    cover=cover,
                    intro=intro,
                    audit_status=audit_status
                )
            else:
                # External author, no audit needed (legacy support)
                novel = Novel(
                    title=title,
                    author=title,  # Use title as author name for external novels
                    category=category,
                    cover=cover,
                    intro=intro,
                    audit_status=AuditStatus.APPROVED
                )
                
            # Add novel to database
            db.session.add(novel)
            db.session.flush()  # Get ID without committing
            
            # Add tags if provided
            if tags:
                for tag_name in tags:
                    # Get or create tag
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                        
                    # Add tag to novel
                    novel.tags.append(tag)
            
            # Create ContentAudit record if novel needs review
            if novel.audit_status == AuditStatus.PENDING:
                audit_record = ContentAudit(
                    content_type='novel',
                    content_id=novel.id,
                    status='pending',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(audit_record)
            
            # Commit changes
            db.session.commit()
            
            # Return success with novel ID and audit status
            result = {
                'success': True,
                'novel_id': novel.id,
                'audit_status': novel.audit_status
            }
            
            # Add message if pending review
            if novel.audit_status == AuditStatus.PENDING:
                result['message'] = '小说已提交，等待审核'
            
            return result
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_novel(novel_id: int, user_id: Optional[int] = None, title: Optional[str] = None, 
                    category: Optional[str] = None, intro: Optional[str] = None,
                    cover: Optional[str] = None, status: Optional[str] = None,
                    tags: Optional[list] = None) -> Dict[str, Any]:
        """Update novel information
        
        Args:
            novel_id: Novel ID
            user_id: User ID performing the update
            title: New title (optional)
            category: New category (optional)
            intro: New introduction (optional)
            cover: New cover image (optional)
            status: New status (optional)
            tags: New tags list (optional)
            
        Returns:
            Dictionary with update result
        """
        try:
            # Get novel
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Check permission: only the author can modify their novel
            if novel.author_id and user_id:
                author = Author.query.filter_by(user_id=user_id).first()
                if not author or novel.author_id != author.id:
                    return {'success': False, 'error': 'Permission denied'}
            
            # Create update data dictionary
            update_data = {
                'title': title,
                'category': category,
                'intro': intro,
                'cover': cover,
                'status': status
            }
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            # Determine if update requires approval
            settings = get_settings()
            content_audit_enabled = settings.get('enable_content_audit', True)
            author = Author.query.filter_by(id=novel.author_id).first()
            
            # Only mark for review if substantial updates (not just status change)
            substantial_updates = any(k in update_data for k in ['title', 'category', 'intro'])
            needs_review = (content_audit_enabled and author and not author.exempt_from_audit 
                          and substantial_updates)
            
            if needs_review:
                update_data['audit_status'] = AuditStatus.PENDING
            
            # Update novel using DAO
            NovelDAO.update_novel_fields(novel, update_data)
            
            # Update tags if provided
            if tags and isinstance(tags, list):
                # Remove old tags and add new ones
                novel.tags = []
                db.session.commit()
                NovelService.add_tags_to_novel(novel.id, tags)
            
            # Create ContentAudit record if update needs review
            if needs_review:
                audit_record = ContentAudit(
                    content_type='novel',
                    content_id=novel.id,
                    status='pending',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(audit_record)
                db.session.commit()
                
                result = {
                    'success': True,
                    'message': '小说已更新，等待审核',
                    'novel': novel.to_dict(),
                    'audit_status': AuditStatus.PENDING
                }
            else:
                result = {
                    'success': True,
                    'message': '小说已更新',
                    'novel': novel.to_dict()
                }
            
            return result
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_chapter(author_id: int, novel_id: int, title: str, 
                   content: str, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """Add new chapter to a novel
        
        Args:
            author_id: Author ID
            novel_id: Novel ID
            title: Chapter title
            content: Chapter content
            chapter_number: Chapter number (optional)
            
        Returns:
            Dictionary with new chapter info and success status
        """
        try:
            # Check if novel exists and belongs to author
            novel = Novel.query.filter_by(id=novel_id, author_id=author_id).first()
            if not novel:
                return {
                    'success': False,
                    'error': 'Novel not found or you are not the author'
                }
            
            # Get author to check exempt status
            author = Author.query.get(author_id)
            
            # Determine audit status based on settings and author status
            settings = get_settings()
            content_audit_enabled = settings.get('enable_content_audit', True)
            
            if content_audit_enabled and not author.exempt_from_audit:
                audit_status = AuditStatus.PENDING
            else:
                audit_status = AuditStatus.APPROVED
            
            # Calculate chapter number if not provided
            if chapter_number is None:
                last_chapter = Chapter.query.filter_by(novel_id=novel_id).order_by(
                    Chapter.chapter_number.desc()
                ).first()
                
                if last_chapter:
                    chapter_number = last_chapter.chapter_number + 1
                else:
                    chapter_number = 1
                
            # Calculate word count
            word_count = len(content)
            
            # Create new chapter
            chapter = Chapter(
                novel_id=novel_id,
                chapter_number=chapter_number,
                title=title,
                content=content,
                word_count=word_count,
                audit_status=audit_status
            )
            
            # Add chapter to database
            db.session.add(chapter)
            db.session.flush()  # Get ID without committing
            
            # Create ContentAudit record if chapter needs review
            if chapter.audit_status == AuditStatus.PENDING:
                audit_record = ContentAudit(
                    content_type='chapter',
                    content_id=chapter.id,
                    status='pending',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(audit_record)
            
            # Update novel updated_at timestamp
            novel.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Return success with chapter info
            result = {
                'success': True,
                'chapter': chapter.to_dict(),
                'audit_status': chapter.audit_status
            }
            
            # Add message if pending review
            if chapter.audit_status == AuditStatus.PENDING:
                result['message'] = '章节已提交，等待审核'
            
            return result
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_chapter(user_id: int, chapter_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update chapter information (author or admin only)"""
        # Verify chapter exists
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            return {'success': False, 'error': 'Chapter not found'}
        
        # Get novel to check ownership
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(user_id) == 'admin'
        
        # If not admin, verify user is the author of the novel
        author = None
        if not is_admin:
            author = Author.query.filter_by(user_id=user_id).first()
            if not author or novel.author_id != author.id:
                return {'success': False, 'error': 'Permission denied - only the novel author or admin can update chapters'}
        
        try:
            # Determine if update requires approval
            settings = get_settings()
            content_audit_enabled = settings.get('enable_content_audit', True)
            
            # Only set pending status if:
            # 1. Content audit is enabled
            # 2. User is not admin
            # 3. Author is not exempt from audit
            # 4. Content or title is being updated (substantial update)
            substantial_update = 'content' in data or 'title' in data
            needs_review = (content_audit_enabled and not is_admin and author and 
                          not author.exempt_from_audit and substantial_update)
            
            if needs_review:
                data['audit_status'] = AuditStatus.PENDING
            
            updated_chapter = NovelDAO.update_chapter_fields(chapter, data)
            
            # Create ContentAudit record if update needs review
            if needs_review:
                audit_record = ContentAudit(
                    content_type='chapter',
                    content_id=chapter.id,
                    status='pending',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(audit_record)
                db.session.commit()
                
                return {
                    'success': True,
                    'message': '章节已更新，等待审核',
                    'chapter': updated_chapter.to_dict(),
                    'audit_status': AuditStatus.PENDING
                }
            else:
                return {
                    'success': True,
                    'message': '章节已更新',
                    'chapter': updated_chapter.to_dict()
                }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_novel(user_id: int, novel_id: int) -> Dict[str, Any]:
        """Delete a novel (author or admin only)"""
        # Verify novel exists
        novel = NovelDAO.get_novel_by_id(novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(user_id) == 'admin'
        
        # Find author record for the user
        author = Author.query.filter_by(user_id=user_id).first()
        
        # Verify ownership: only the novel author or admin can delete novel
        if not is_admin and (not author or novel.author_id != author.id):
            return {'success': False, 'error': 'Permission denied - only the novel author or admin can delete this novel'}
        
        try:
            NovelDAO.delete_novel(novel_id)
            
            return {
                'success': True,
                'message': 'Novel deleted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_chapter(user_id: int, chapter_id: int) -> Dict[str, Any]:
        """Delete a chapter (author or admin only)
        
        Args:
            user_id: User ID of the requester
            chapter_id: Chapter ID to delete
            
        Returns:
            Dictionary with operation result
        """
        # Verify chapter exists
        chapter = NovelDAO.get_chapter_by_id(chapter_id)
        if not chapter:
            return {'success': False, 'error': 'Chapter not found'}
        
        # Get novel to check ownership
        novel = NovelDAO.get_novel_by_id(chapter.novel_id)
        if not novel:
            return {'success': False, 'error': 'Novel not found'}
        
        # Check if user is admin
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        is_admin = PermissionService.get_user_role(user_id) == 'admin'
        
        # If not admin, verify user is the author of the novel
        if not is_admin:
            author = Author.query.filter_by(user_id=user_id).first()
            if not author or novel.author_id != author.id:
                return {'success': False, 'error': 'Permission denied - only the novel author or admin can delete chapters'}
        
        novel_id = chapter.novel_id
        
        try:
            NovelDAO.delete_chapter(chapter_id)
            
            return {
                'success': True,
                'message': 'Chapter deleted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def refresh_cache() -> Dict[str, Any]:
        """
        This method previously refreshed Redis cache, now just returns success
        This method is kept for backwards compatibility
        """
        return {'success': True, 'message': 'No cache to refresh'}
    
    @staticmethod
    def get_chapter(chapter_id: int, include_content: bool = True, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get chapter details
        
        Args:
            chapter_id: Chapter ID
            include_content: Whether to include chapter content
            user_id: Optional user ID to check permissions
            
        Returns:
            Dictionary with chapter details
        """
        try:
            # Get chapter by ID
            chapter = NovelDAO.get_chapter_by_id(chapter_id)
            if not chapter:
                return {'success': False, 'error': 'Chapter not found'}
            
            # Check audit status
            if chapter.audit_status != AuditStatus.APPROVED:
                # If chapter is pending or rejected, only author or admin can view
                novel = NovelDAO.get_novel_by_id(chapter.novel_id)
                
                is_author = False
                is_admin = False
                
                if user_id:
                    # Check if user is the author
                    author = Author.query.filter_by(user_id=user_id).first()
                    if author and novel and author.id == novel.author_id:
                        is_author = True
                        
                    # Check if user is admin
                    admin = Admin.query.filter_by(user_id=user_id).first()
                    if admin:
                        is_admin = True
                        
                # Return error if user is not author or admin
                if not is_author and not is_admin:
                    return {'success': False, 'error': 'Chapter not found or pending approval'}
            
            # Get novel to check if it exists
            novel = NovelDAO.get_novel_by_id(chapter.novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Find previous and next chapter
            prev_chapter = Chapter.query.filter(
                Chapter.novel_id == chapter.novel_id,
                Chapter.chapter_number < chapter.chapter_number,
                Chapter.is_deleted == False
            ).order_by(Chapter.chapter_number.desc()).first()
            
            next_chapter = Chapter.query.filter(
                Chapter.novel_id == chapter.novel_id,
                Chapter.chapter_number > chapter.chapter_number,
                Chapter.is_deleted == False
            ).order_by(Chapter.chapter_number.asc()).first()
            
            # Format response data
            result = {
                'success': True,
                'chapter': chapter.to_dict(include_content),
                'novel_title': novel.title,
                'prev_chapter': prev_chapter.to_dict(False) if prev_chapter else None,
                'next_chapter': next_chapter.to_dict(False) if next_chapter else None
            }
            
            # Record reading history if user is logged in
            if user_id:
                InteractionDAO.record_reading_history(user_id, novel.id, chapter.id)
            
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_author_stats(user_id: int) -> Dict[str, Any]:
        """获取用户作为作者的统计数据
        
        Args:
            user_id: 用户ID（不是作者ID）
            
        Returns:
            包含作者统计数据的字典
        """
        try:
            # 获取用户作为作者创建的小说列表
            novels = NovelDAO.get_novel_by_user_id_query(user_id).all()
            
            # 统计数据
            novel_count = len(novels)
            novel_ids = [novel.id for novel in novels]
            
            # 总字数
            total_words = db.session.query(func.sum(Chapter.word_count))\
                .filter(Chapter.novel_id.in_(novel_ids))\
                .scalar() or 0
            
            # 总收藏数
            total_collections = db.session.query(func.sum(Novel.collection_count))\
                .filter(Novel.id.in_(novel_ids))\
                .scalar() or 0
            
            # 总浏览量
            total_views = db.session.query(func.sum(Novel.view_count))\
                .filter(Novel.id.in_(novel_ids))\
                .scalar() or 0
            
            # 总章节数
            total_chapters = Chapter.query.filter(Chapter.novel_id.in_(novel_ids)).count()
            
            stats = {
                'novel_count': novel_count,
                'total_words': total_words,
                'total_collections': total_collections,
                'total_views': total_views,
                'total_chapters': total_chapters
            }
            
            return {
                'success': True,
                'stats': stats
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_novel_chapters(novel_id: int) -> Dict[str, Any]:
        """Get all chapters for a novel
        
        Args:
            novel_id: Novel ID
            
        Returns:
            Dictionary with chapters list
        """
        try:
            # Check if novel exists
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # Get chapters - only show approved chapters
            chapters = NovelDAO.get_novel_chapters(novel_id, include_pending=False)
            
            return {
                'success': True,
                'chapters': [chapter.to_dict() for chapter in chapters]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_tags_to_novel(novel_id: int, tag_names: List[str]) -> Dict[str, Any]:
        """添加标签到小说
        
        Args:
            novel_id: 小说ID
            tag_names: 标签名称列表
            
        Returns:
            操作结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 处理标签
            added_tags = []
            for tag_name in tag_names:
                # 检查标签是否已存在
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    # 创建新标签
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()  # 获取新标签ID
                
                # 检查小说是否已有此标签
                if tag not in novel.tags:
                    novel.tags.append(tag)
                    added_tags.append(tag.to_dict())
            
            db.session.commit()
            
            return {
                'success': True, 
                'message': 'Tags added successfully',
                'added_tags': added_tags
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
            
    @staticmethod
    def remove_tag_from_novel(novel_id: int, tag_id: int) -> Dict[str, Any]:
        """从小说中移除标签
        
        Args:
            novel_id: 小说ID
            tag_id: 标签ID
            
        Returns:
            操作结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
                
            # 检查标签是否存在
            tag = Tag.query.get(tag_id)
            if not tag:
                return {'success': False, 'error': 'Tag not found'}
                
            # 检查小说是否有此标签
            if tag not in novel.tags:
                return {'success': False, 'error': 'Novel does not have this tag'}
                
            # 移除标签
            novel.tags.remove(tag)
            db.session.commit()
            
            return {'success': True, 'message': 'Tag removed successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_novel_tags(novel_id: int) -> Dict[str, Any]:
        """获取小说的所有标签
        
        Args:
            novel_id: 小说ID
            
        Returns:
            包含标签列表的结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 获取小说的所有标签
            tags = [tag.to_dict() for tag in novel.tags]
            
            return {
                'success': True, 
                'tags': tags
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    @staticmethod
    def get_all_tags() -> Dict[str, Any]:
        """获取所有标签列表
        
        Returns:
            包含所有标签的结果字典
        """
        try:
            tags = Tag.query.all()
            
            return {
                'success': True,
                'tags': [tag.to_dict() for tag in tags]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    @staticmethod
    def get_all_chapters(novel_id: int) -> Dict[str, Any]:
        """获取小说的所有章节（不分页）
        
        与get_novel_chapters不同，此方法返回小说的所有章节，不进行分页处理，
        适用于需要获取全部章节列表的场景，如下载或全文搜索。
        
        Args:
            novel_id: 小说ID
            
        Returns:
            包含所有章节列表的结果字典
        """
        try:
            # 检查小说是否存在
            novel = NovelDAO.get_novel_by_id(novel_id)
            if not novel:
                return {'success': False, 'error': 'Novel not found'}
            
            # 获取所有章节，按章节号排序
            chapters = NovelDAO.get_novel_chapters(novel_id)
            
            # 将章节信息转换为字典格式，不包含章节内容
            chapters_data = [chapter.to_dict(include_content=False) for chapter in chapters]
            
            return {
                'success': True,
                'novel_id': novel_id,
                'novel_title': novel.title,
                'total_chapters': len(chapters_data),
                'chapters': chapters_data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)} 