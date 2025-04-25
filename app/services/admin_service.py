from typing import Dict, List, Optional

from app.models import Novel, Chapter, Comment, User
from app.dao.admin_dao import AdminDAO
from app.services.permission_service import PermissionService

class AdminService:
    @staticmethod
    def delete_novel(admin_id: int, novel_id: int) -> Dict:
        """软删除小说（移至回收站）"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查小说是否存在
        novel = Novel.query.get(novel_id)
        if not novel:
            return {
                'success': False,
                'message': f'ID为{novel_id}的小说不存在'
            }
        
        # 获取小说标题用于响应消息
        novel_title = novel.title
        
        # 软删除小说（移至回收站）
        result = AdminDAO.soft_delete_novel(novel_id)
        
        if result:
            return {
                'success': True,
                'message': f'小说"{novel_title}"（ID: {novel_id}）已移至回收站'
            }
        else:
            return {
                'success': False,
                'message': f'移动ID为{novel_id}的小说至回收站失败'
            }

    @staticmethod
    def delete_chapter(admin_id: int, chapter_id: int) -> Dict:
        """软删除章节（移至回收站）"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查章节是否存在
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {
                'success': False,
                'message': f'ID为{chapter_id}的章节不存在'
            }
        
        # 获取章节详情用于响应消息
        chapter_title = chapter.title
        
        # 软删除章节（移至回收站）
        result = AdminDAO.soft_delete_chapter(chapter_id)
        
        if result:
            return {
                'success': True,
                'message': f'章节"{chapter_title}"（ID: {chapter_id}）已移至回收站'
            }
        else:
            return {
                'success': False,
                'message': f'移动ID为{chapter_id}的章节至回收站失败'
            }

    @staticmethod
    def delete_comment(admin_id: int, comment_id: int) -> Dict:
        """软删除评论（移至回收站）"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查评论是否存在
        comment = Comment.query.get(comment_id)
        if not comment:
            return {
                'success': False,
                'message': f'ID为{comment_id}的评论不存在'
            }
        
        # 软删除评论（移至回收站）
        result = AdminDAO.soft_delete_comment(comment_id)
        
        if result:
            return {
                'success': True,
                'message': f'ID为{comment_id}的评论已移至回收站'
            }
        else:
            return {
                'success': False,
                'message': f'移动ID为{comment_id}的评论至回收站失败'
            }

    @staticmethod
    def get_recycled_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Dict:
        """获取回收站中的小说"""
        novels, total = AdminDAO.get_deleted_novels(page, per_page, title_filter)
        
        return {
            'novels': [novel.to_dict() for novel in novels],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

    @staticmethod
    def get_recycled_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Dict:
        """获取回收站中的章节"""
        chapters, total = AdminDAO.get_deleted_chapters(novel_id, page, per_page)
        
        chapters_with_novel = []
        for chapter in chapters:
            chapter_dict = chapter.to_dict()
            novel = Novel.query.get(chapter.novel_id)
            if novel:
                chapter_dict['novel_title'] = novel.title
            chapters_with_novel.append(chapter_dict)
        
        return {
            'chapters': chapters_with_novel,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

    @staticmethod
    def get_recycled_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                        page: int = 1, per_page: int = 20) -> Dict:
        """获取回收站中的评论"""
        comments, total = AdminDAO.get_deleted_comments(novel_id, chapter_id, page, per_page)
        
        comments_with_details = []
        for comment in comments:
            comment_dict = comment.to_dict()
            
            # 添加用户信息
            user = User.query.get(comment.user_id)
            if user:
                comment_dict['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar
                }
            
            # 添加小说标题
            if comment.novel_id:
                novel = Novel.query.get(comment.novel_id)
                if novel:
                    comment_dict['novel_title'] = novel.title
            
            # 添加章节标题
            if comment.chapter_id:
                chapter = Chapter.query.get(comment.chapter_id)
                if chapter:
                    comment_dict['chapter_title'] = chapter.title
            
            comments_with_details.append(comment_dict)
        
        return {
            'comments': comments_with_details,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

    @staticmethod
    def restore_novel(admin_id: int, novel_id: int) -> Dict:
        """从回收站还原小说"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查小说是否存在于回收站
        novel = Novel.query.get(novel_id)
        if not novel:
            return {
                'success': False,
                'message': f'ID为{novel_id}的小说不存在'
            }
        
        if not novel.is_deleted:
            return {
                'success': False,
                'message': f'ID为{novel_id}的小说不在回收站中'
            }
        
        # 获取小说标题用于响应消息
        novel_title = novel.title
        
        # 还原小说
        result = AdminDAO.restore_novel(novel_id)
        
        if result:
            return {
                'success': True,
                'message': f'小说"{novel_title}"（ID: {novel_id}）已从回收站还原'
            }
        else:
            return {
                'success': False,
                'message': f'还原ID为{novel_id}的小说失败'
            }

    @staticmethod
    def restore_chapter(admin_id: int, chapter_id: int) -> Dict:
        """从回收站还原章节"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查章节是否存在于回收站
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {
                'success': False,
                'message': f'ID为{chapter_id}的章节不存在'
            }
        
        if not chapter.is_deleted:
            return {
                'success': False,
                'message': f'ID为{chapter_id}的章节不在回收站中'
            }
        
        # 获取章节标题用于响应消息
        chapter_title = chapter.title
        
        # 还原章节
        result = AdminDAO.restore_chapter(chapter_id)
        
        if result:
            return {
                'success': True,
                'message': f'章节"{chapter_title}"（ID: {chapter_id}）已从回收站还原'
            }
        else:
            return {
                'success': False,
                'message': f'还原ID为{chapter_id}的章节失败'
            }

    @staticmethod
    def restore_comment(admin_id: int, comment_id: int) -> Dict:
        """从回收站还原评论"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查评论是否存在于回收站
        comment = Comment.query.get(comment_id)
        if not comment:
            return {
                'success': False,
                'message': f'ID为{comment_id}的评论不存在'
            }
        
        if not comment.is_deleted:
            return {
                'success': False,
                'message': f'ID为{comment_id}的评论不在回收站中'
            }
        
        # 还原评论
        result = AdminDAO.restore_comment(comment_id)
        
        if result:
            return {
                'success': True,
                'message': f'ID为{comment_id}的评论已从回收站还原'
            }
        else:
            return {
                'success': False,
                'message': f'还原ID为{comment_id}的评论失败'
            }

    @staticmethod
    def permanently_delete_novel(admin_id: int, novel_id: int) -> Dict:
        """永久删除回收站中的小说"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查小说是否存在于回收站
        novel = Novel.query.get(novel_id)
        if not novel:
            return {
                'success': False,
                'message': f'ID为{novel_id}的小说不存在'
            }
        
        if not novel.is_deleted:
            return {
                'success': False,
                'message': f'ID为{novel_id}的小说不在回收站中'
            }
        
        # 获取小说标题用于响应消息
        novel_title = novel.title
        
        # 永久删除小说
        result = AdminDAO.delete_novel_cascade(novel_id)
        
        if result:
            return {
                'success': True,
                'message': f'小说"{novel_title}"（ID: {novel_id}）已永久删除'
            }
        else:
            return {
                'success': False,
                'message': f'永久删除ID为{novel_id}的小说失败'
            }

    @staticmethod
    def permanently_delete_chapter(admin_id: int, chapter_id: int) -> Dict:
        """永久删除回收站中的章节"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查章节是否存在于回收站
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {
                'success': False,
                'message': f'ID为{chapter_id}的章节不存在'
            }
        
        if not chapter.is_deleted:
            return {
                'success': False,
                'message': f'ID为{chapter_id}的章节不在回收站中'
            }
        
        # 获取章节标题用于响应消息
        chapter_title = chapter.title
        
        # 永久删除章节
        result = AdminDAO.permanently_delete_chapter(chapter_id)
        
        if result:
            return {
                'success': True,
                'message': f'章节"{chapter_title}"（ID: {chapter_id}）已永久删除'
            }
        else:
            return {
                'success': False,
                'message': f'永久删除ID为{chapter_id}的章节失败'
            }

    @staticmethod
    def permanently_delete_comment(admin_id: int, comment_id: int) -> Dict:
        """永久删除回收站中的评论"""
        # 验证管理员权限
        if not PermissionService.has_role(admin_id, 'admin'):
            return {
                'success': False,
                'message': '需要管理员权限'
            }
        
        # 检查评论是否存在于回收站
        comment = Comment.query.get(comment_id)
        if not comment:
            return {
                'success': False,
                'message': f'ID为{comment_id}的评论不存在'
            }
        
        if not comment.is_deleted:
            return {
                'success': False,
                'message': f'ID为{comment_id}的评论不在回收站中'
            }
        
        # 永久删除评论
        result = AdminDAO.permanently_delete_comment(comment_id)
        
        if result:
            return {
                'success': True,
                'message': f'ID为{comment_id}的评论已永久删除'
            }
        else:
            return {
                'success': False,
                'message': f'永久删除ID为{comment_id}的评论失败'
            } 