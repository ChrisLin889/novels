from typing import Dict, Any, List, Optional
from app.dao.notification_dao import NotificationDAO

class NotificationService:
    """
    通知服务
    """
    
    @staticmethod
    def create_sensitive_word_notification(user_id: int, content_type: str, 
                                          content_id: int, matches: List[Dict]) -> Dict:
        """
        创建敏感词警告通知
        
        Args:
            user_id: 用户ID
            content_type: 内容类型 (novel, chapter, comment)
            content_id: 内容ID
            matches: 敏感词匹配列表
            
        Returns:
            Dict with operation result
        """
        # 根据内容类型生成不同通知
        content_type_map = {
            'novel': '小说',
            'chapter': '章节',
            'comment': '评论'
        }
        
        content_name = content_type_map.get(content_type, '内容')
        
        # 构建通知标题和内容
        title = f"您的{content_name}中包含敏感词"
        
        # 获取敏感词和级别
        words_info = []
        for match in matches:
            level_desc = "低级" if match['level'] == 1 else "中级" if match['level'] == 2 else "高级"
            words_info.append(f"{match['word']}（{level_desc}）")
        
        words_text = "、".join(words_info)
        content = f"系统检测到您的{content_name}（ID: {content_id}）中包含以下敏感词：{words_text}。请注意遵守社区规范，谨慎用词。"
        
        try:
            notification = NotificationDAO.create_notification(
                user_id=user_id,
                title=title,
                content=content,
                notification_type='sensitive_word',
                related_object_type=content_type,
                related_object_id=content_id
            )
            
            return {
                'success': True, 
                'message': '已发送敏感词警告通知',
                'notification_id': notification.id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_user_notifications(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        获取用户通知列表
        
        Args:
            user_id: 用户ID
            page: 页码
            per_page: 每页数量
            
        Returns:
            Dict with notifications and pagination info
        """
        try:
            notifications, total = NotificationDAO.get_user_notifications(user_id, page, per_page)
            
            return {
                'success': True,
                'notifications': [notification.to_dict() for notification in notifications],
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'unread_count': NotificationDAO.get_unread_count(user_id)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def mark_notification_read(user_id: int, notification_id: int) -> Dict[str, Any]:
        """
        将通知标记为已读
        
        Args:
            user_id: 用户ID
            notification_id: 通知ID
            
        Returns:
            Dict with operation result
        """
        try:
            result = NotificationDAO.mark_as_read(notification_id, user_id)
            return {
                'success': result,
                'message': '通知已标记为已读' if result else '通知不存在或不属于该用户'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def mark_all_read(user_id: int) -> Dict[str, Any]:
        """
        将用户所有通知标记为已读
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict with operation result
        """
        try:
            result = NotificationDAO.mark_all_as_read(user_id)
            return {
                'success': result,
                'message': '所有通知已标记为已读'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)} 