from app import db
from app.models.user import User
from app.models.author import Author, AuthorApplication
from app.models.admin import Admin
from app.services.permission_service import PermissionService
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class AuthorService:
    """
    处理作者相关服务，包括作者申请和管理
    """
    
    @staticmethod
    def submit_application(user_id: int, pen_name: str, bio: str, reason: str) -> Dict[str, Any]:
        """
        提交作者申请
        
        Args:
            user_id: 用户ID
            pen_name: 笔名
            bio: 作者简介
            reason: 申请理由
            
        Returns:
            Dict with success status and message
        """
        try:
            # 验证用户是否存在
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'message': '用户不存在'
                }
                
            # 检查用户是否已经是作者
            if PermissionService.has_role(user_id, 'author'):
                return {
                    'success': False, 
                    'message': '您已经是作者，无需再次申请'
                }
                
            # 检查是否有正在处理的申请
            pending_application = AuthorApplication.query.filter_by(
                user_id=user_id,
                status='pending'
            ).first()
            
            if pending_application:
                return {
                    'success': False,
                    'message': '您已有一个正在处理的申请，请等待审核结果'
                }
                
            # 创建新申请
            application = AuthorApplication(
                user_id=user_id,
                pen_name=pen_name,
                bio=bio,
                reason=reason,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(application)
            db.session.commit()
            
            return {
                'success': True,
                'message': '作者申请提交成功，请等待管理员审核',
                'application': application.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"提交作者申请出错: {str(e)}")
            return {
                'success': False,
                'message': f'提交申请时出错: {str(e)}'
            }
    
    @staticmethod
    def get_user_applications(user_id: int) -> Dict[str, Any]:
        """
        获取用户的作者申请历史
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict with success status and applications list
        """
        try:
            applications = AuthorApplication.query.filter_by(user_id=user_id).order_by(
                AuthorApplication.created_at.desc()
            ).all()
            
            return {
                'success': True,
                'applications': [app.to_dict() for app in applications]
            }
            
        except Exception as e:
            logger.error(f"获取用户申请历史出错: {str(e)}")
            return {
                'success': False,
                'message': f'获取申请历史时出错: {str(e)}'
            }
    
    @staticmethod
    def get_pending_applications(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        获取待处理的作者申请列表（管理员使用）
        
        Args:
            page: 页码
            per_page: 每页数量
            
        Returns:
            Dict with success status and applications list
        """
        try:
            query = AuthorApplication.query.filter_by(status='pending')
            applications = query.order_by(AuthorApplication.created_at.asc()).paginate(page=page, per_page=per_page)
            
            return {
                'success': True,
                'total': applications.total,
                'pages': applications.pages,
                'current_page': page,
                'applications': [app.to_dict() for app in applications.items]
            }
            
        except Exception as e:
            logger.error(f"获取待处理申请出错: {str(e)}")
            return {
                'success': False,
                'message': f'获取待处理申请时出错: {str(e)}'
            }
    
    @staticmethod
    def process_application(application_id: int, admin_id: int, action: str, comment: str = None) -> Dict[str, Any]:
        """
        处理作者申请（管理员使用）
        
        Args:
            application_id: 申请ID
            admin_id: 管理员ID
            action: 操作（approve/reject）
            comment: 管理员评论（可选）
            
        Returns:
            Dict with success status and message
        """
        try:
            # 验证管理员权限
            if not PermissionService.has_role(admin_id, 'admin'):
                return {
                    'success': False,
                    'message': '需要管理员权限'
                }
                
            # 获取申请记录
            application = AuthorApplication.query.get(application_id)
            if not application:
                return {
                    'success': False,
                    'message': '申请记录不存在'
                }
                
            # 检查申请状态
            if application.status != 'pending':
                return {
                    'success': False,
                    'message': f'该申请已经被{application.status}，无法再次处理'
                }
                
            # 获取管理员记录
            admin_record = Admin.query.filter_by(user_id=admin_id).first()
            if not admin_record:
                return {
                    'success': False,
                    'message': '管理员记录不存在'
                }
                
            # 更新申请状态
            if action == 'approve':
                application.status = 'approved'
                
                # 创建作者记录
                user = User.query.get(application.user_id)
                if not user:
                    return {
                        'success': False,
                        'message': '申请用户不存在'
                    }
                
                # 检查用户是否已经是作者
                if PermissionService.has_role(application.user_id, 'author'):
                    return {
                        'success': False,
                        'message': '该用户已经是作者'
                    }
                
                # 创建新的作者记录
                author = Author(
                    user_id=application.user_id,
                    pen_name=application.pen_name,
                    bio=application.bio,
                    verified=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.session.add(author)
                message = '申请已批准，用户已成为作者'
                
            elif action == 'reject':
                application.status = 'rejected'
                message = '申请已拒绝'
            else:
                return {
                    'success': False,
                    'message': '无效的操作'
                }
                
            # 更新申请记录
            application.admin_id = admin_record.id
            application.admin_comment = comment
            application.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': message,
                'application': application.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"处理作者申请出错: {str(e)}")
            return {
                'success': False,
                'message': f'处理申请时出错: {str(e)}'
            }
    
    @staticmethod
    def update_author_profile(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新作者资料
        
        Args:
            user_id: 用户ID
            data: 更新数据
            
        Returns:
            Dict with success status and message
        """
        try:
            # 检查用户是否为作者
            if not PermissionService.has_role(user_id, 'author'):
                return {
                    'success': False,
                    'message': '只有作者才能更新作者资料'
                }
                
            # 获取作者记录
            author = Author.query.filter_by(user_id=user_id).first()
            if not author:
                return {
                    'success': False,
                    'message': '作者记录不存在'
                }
                
            # 更新资料
            updated = False
            allowed_fields = ['pen_name', 'bio', 'contact_email']
            
            for field in allowed_fields:
                if field in data and data[field] is not None:
                    setattr(author, field, data[field])
                    updated = True
            
            if updated:
                author.updated_at = datetime.utcnow()
                db.session.commit()
                return {
                    'success': True,
                    'message': '作者资料更新成功',
                    'author': author.to_dict()
                }
            else:
                return {
                    'success': False,
                    'message': '没有提供有效的更新数据'
                }
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新作者资料出错: {str(e)}")
            return {
                'success': False,
                'message': f'更新作者资料时出错: {str(e)}'
            }
    
    @staticmethod
    def resign_author(user_id: int) -> Dict[str, Any]:
        """
        放弃作者身份
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict with success status and message
        """
        try:
            # 检查用户是否为作者
            if not PermissionService.has_role(user_id, 'author'):
                return {
                    'success': False,
                    'message': '您不是作者，无法放弃作者身份'
                }
                
            # 获取作者记录
            author = Author.query.filter_by(user_id=user_id).first()
            if not author:
                return {
                    'success': False,
                    'message': '作者记录不存在'
                }
                
            # 检查作者是否有作品
            novel_count = author.novels.count()
            if novel_count > 0:
                return {
                    'success': False,
                    'message': '您有正在连载的作品，请先处理您的作品'
                }
                
            # 删除作者记录
            db.session.delete(author)
            db.session.commit()
            
            return {
                'success': True,
                'message': '您已成功放弃作者身份'
            }
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"放弃作者身份出错: {str(e)}")
            return {
                'success': False,
                'message': f'放弃作者身份时出错: {str(e)}'
            } 