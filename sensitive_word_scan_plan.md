# 敏感词自动扫描及通知方案

本文档详细描述了为系统添加敏感词自动扫描、替换和通知功能的实现方案。

## 1. 添加用户通知模型

```python
# backend/app/models/notification.py
from app import db
from datetime import datetime

class UserNotification(db.Model):
    """
    用户通知模型 - 用于存储系统向用户发送的通知
    """
    __tablename__ = 'user_notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(20), nullable=False)  # sensitive_word, system, admin, etc.
    related_object_type = db.Column(db.String(20), nullable=True)  # novel, chapter, comment
    related_object_id = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'notification_type': self.notification_type,
            'related_object_type': self.related_object_type,
            'related_object_id': self.related_object_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
```

## 2. 添加用户通知DAO和服务层

```python
# backend/app/dao/notification_dao.py
from app.models.notification import UserNotification
from app import db
from typing import List, Dict, Optional, Tuple
from sqlalchemy import desc

class NotificationDAO:
    """
    通知数据访问对象
    """
    
    @staticmethod
    def create_notification(user_id: int, title: str, content: str, 
                           notification_type: str, related_object_type: Optional[str] = None, 
                           related_object_id: Optional[int] = None) -> UserNotification:
        """
        创建一条用户通知
        """
        notification = UserNotification(
            user_id=user_id,
            title=title,
            content=content,
            notification_type=notification_type,
            related_object_type=related_object_type,
            related_object_id=related_object_id
        )
        
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def get_user_notifications(user_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[UserNotification], int]:
        """
        获取用户通知列表
        """
        query = UserNotification.query.filter_by(user_id=user_id)
        total = query.count()
        
        notifications = query.order_by(desc(UserNotification.created_at)) \
                        .offset((page - 1) * per_page) \
                        .limit(per_page) \
                        .all()
                        
        return notifications, total
    
    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> bool:
        """
        将通知标记为已读
        """
        notification = UserNotification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notification:
            return False
            
        notification.is_read = True
        db.session.commit()
        return True
    
    @staticmethod
    def mark_all_as_read(user_id: int) -> bool:
        """
        将用户所有通知标记为已读
        """
        UserNotification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()
        return True
    
    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """
        获取未读通知数量
        """
        return UserNotification.query.filter_by(user_id=user_id, is_read=False).count()
```

```python
# backend/app/services/notification_service.py
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
```

## 3. 修改敏感词过滤服务以集成通知功能

```python
# backend/app/services/admin_service.py 中增加或修改函数
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
```

## 4. 添加定时批量扫描服务

```python
# backend/app/utils/tasks.py
from app.models.novel import Novel, Chapter
from app.models.interaction import Comment
from app.services.admin_service import AdminService
from app import db
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def scan_and_update_content():
    """
    扫描并更新所有内容中的敏感词
    - 直接替换敏感词
    - 发送通知给内容所有者
    """
    try:
        results = {
            'novel': {'total': 0, 'updated': 0},
            'chapter': {'total': 0, 'updated': 0},
            'comment': {'total': 0, 'updated': 0}
        }
        
        # 扫描小说简介
        novels = Novel.query.all()
        results['novel']['total'] = len(novels)
        
        for novel in novels:
            has_sensitive, matches, filtered_content = AdminService.filter_sensitive_content(novel.intro)
            if has_sensitive:
                # 更新内容
                novel.intro = filtered_content
                results['novel']['updated'] += 1
                
                # 发送通知
                author = novel.author_id  # 假设这是作者的用户ID关联
                AdminService.filter_and_notify_sensitive_content(
                    content=novel.intro,
                    user_id=author,
                    content_type='novel',
                    content_id=novel.id
                )
        
        # 扫描章节内容
        chapters = Chapter.query.all()
        results['chapter']['total'] = len(chapters)
        
        for chapter in chapters:
            has_sensitive, matches, filtered_content = AdminService.filter_sensitive_content(chapter.content)
            if has_sensitive:
                # 更新内容
                chapter.content = filtered_content
                results['chapter']['updated'] += 1
                
                # 获取作者ID并发送通知
                novel = Novel.query.get(chapter.novel_id)
                if novel:
                    author = novel.author_id  # 假设这是作者的用户ID关联
                    AdminService.filter_and_notify_sensitive_content(
                        content=chapter.content,
                        user_id=author,
                        content_type='chapter',
                        content_id=chapter.id
                    )
        
        # 扫描评论内容
        comments = Comment.query.all()
        results['comment']['total'] = len(comments)
        
        for comment in comments:
            has_sensitive, matches, filtered_content = AdminService.filter_sensitive_content(comment.content)
            if has_sensitive:
                # 更新内容
                comment.content = filtered_content
                results['comment']['updated'] += 1
                
                # 发送通知给评论作者
                AdminService.filter_and_notify_sensitive_content(
                    content=comment.content,
                    user_id=comment.user_id,
                    content_type='comment',
                    content_id=comment.id
                )
        
        # 提交所有变更
        db.session.commit()
        
        # 记录结果
        logger.info(f"敏感词自动扫描完成: {results}")
        return {
            'success': True,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }
            
    except Exception as e:
        logger.error(f"敏感词自动扫描出错: {str(e)}")
        db.session.rollback()
        return {
            'success': False,
            'error': f"扫描过程中出错: {str(e)}",
            'timestamp': datetime.utcnow().isoformat()
        }
```

## 5. 添加定时任务调度器

```python
# backend/app/utils/scheduler.py
import schedule
import time
import threading
from app.utils.tasks import scan_and_update_content
import logging

logger = logging.getLogger(__name__)

def run_scheduler():
    """运行定时任务调度器"""
    # 每天凌晨3点执行敏感词自动扫描
    schedule.every().day.at("03:00").do(scan_and_update_content)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

def start_scheduler():
    """启动调度器线程"""
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logger.info("敏感词自动扫描调度器已启动")
```

## 6. 在应用启动时启动调度器

```python
# 在backend/app/__init__.py文件的create_app函数末尾添加
from app.utils.scheduler import start_scheduler

def create_app(config_name='default'):
    # ... 现有代码 ...
    
    # 启动调度器
    with app.app_context():
        start_scheduler()
    
    return app
```

## 7. 添加通知API接口

```python
# backend/app/api/notification.py
from flask import Blueprint, jsonify, request, g
from app.services.notification_service import NotificationService
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    """获取用户通知列表"""
    user_id = get_jwt_identity()
    
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    result = NotificationService.get_user_notifications(
        user_id=user_id,
        page=page,
        per_page=per_page
    )
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 400
    
    return jsonify(result), 200

@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """将通知标记为已读"""
    user_id = get_jwt_identity()
    
    result = NotificationService.mark_notification_read(
        user_id=user_id,
        notification_id=notification_id
    )
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 400
    
    return jsonify(result), 200

@notification_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_read():
    """将所有通知标记为已读"""
    user_id = get_jwt_identity()
    
    result = NotificationService.mark_all_read(user_id=user_id)
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 400
    
    return jsonify(result), 200
```

## 8. 添加管理员手动扫描接口

```python
# 在backend/app/api/admin.py中添加
@admin_bp.route('/content-scan', methods=['POST'])
@admin_required
def scan_content():
    """
    手动触发内容敏感词扫描和替换
    """
    from app.utils.tasks import scan_and_update_content
    
    # 执行扫描
    result = scan_and_update_content()
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 500
    
    return jsonify(result), 200
```

## 9. 修改前端API调用模块

```javascript
// frontend/src/api/notification.js
import request from '@/utils/request';

/**
 * 获取当前用户的通知列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @returns {Promise}
 */
export const getNotifications = async (params = {}) => {
  try {
    const response = await request({
      url: '/notification',
      method: 'get',
      params
    });
    return response;
  } catch (error) {
    console.error('获取通知列表失败:', error);
    throw error.response?.data?.error || '获取通知列表失败';
  }
};

/**
 * 将通知标记为已读
 * @param {number} notificationId - 通知ID
 * @returns {Promise}
 */
export const markNotificationRead = async (notificationId) => {
  try {
    const response = await request({
      url: `/notification/${notificationId}/read`,
      method: 'post'
    });
    return response;
  } catch (error) {
    console.error('标记通知已读失败:', error);
    throw error.response?.data?.error || '标记通知已读失败';
  }
};

/**
 * 将所有通知标记为已读
 * @returns {Promise}
 */
export const markAllNotificationsRead = async () => {
  try {
    const response = await request({
      url: '/notification/read-all',
      method: 'post'
    });
    return response;
  } catch (error) {
    console.error('标记所有通知已读失败:', error);
    throw error.response?.data?.error || '标记所有通知已读失败';
  }
};
```

## 10. 在前端添加管理员手动扫描功能

```javascript
// frontend/src/api/admin.js 添加
/**
 * 触发内容敏感词扫描和替换
 * @returns {Promise}
 */
export const scanContentForSensitiveWords = async () => {
  try {
    const response = await request({
      url: '/admin/content-scan',
      method: 'post'
    });
    return response;
  } catch (error) {
    console.error('内容扫描失败:', error);
    throw error.response?.data?.error || '内容扫描失败';
  }
};
```

```vue
<!-- 在frontend/src/views/admin/SensitiveWords.vue中添加扫描按钮 -->
<el-button type="warning" @click="handleContentScan" :loading="scanning">扫描并更新现有内容</el-button>

<!-- 添加相关方法 -->
<script>
// ...现有代码...

// 在setup函数中添加以下内容
const scanning = ref(false);

// 手动扫描内容
const handleContentScan = async () => {
  scanning.value = true;
  try {
    const result = await adminApi.scanContentForSensitiveWords();
    
    ElMessage.success(`扫描完成: 小说 ${result.results.novel.updated}/${result.results.novel.total}, `
                   + `章节 ${result.results.chapter.updated}/${result.results.chapter.total}, `
                   + `评论 ${result.results.comment.updated}/${result.results.comment.total}`);
    
  } catch (error) {
    ElMessage.error('扫描失败: ' + error);
  } finally {
    scanning.value = false;
  }
};

// 返回新增的属性和方法
return {
  // ...现有返回内容...
  scanning,
  handleContentScan
};
</script>
```

## 11. 为编写评论、添加小说、章节添加实时检查

修改相关服务层函数，添加实时敏感词检测功能：

```python
# 在app/services/interaction_service.py中修改add_comment方法

@staticmethod
def add_comment(user_id: int, novel_id: int, chapter_id: Optional[int], content: str) -> Dict[str, Any]:
    """Add a comment"""
    # Check if novel exists
    novel = Novel.query.get(novel_id)
    if not novel:
        return {'success': False, 'error': 'Novel not found'}
        
    # Check if chapter exists if provided
    if chapter_id is not None and chapter_id != 0:
        chapter = Chapter.query.get(chapter_id)
        if not chapter or chapter.novel_id != novel_id:
            return {'success': False, 'error': 'Invalid chapter'}
    
    # 敏感词过滤和检查
    from app.services.admin_service import AdminService
    has_sensitive, matches, filtered_content = AdminService.filter_and_notify_sensitive_content(
        content=content,
        user_id=user_id, 
        content_type='comment',
        content_id=0  # 先设为0，评论创建后再更新
    )
    
    # 使用过滤后的内容创建评论
    comment = InteractionDAO.add_comment(user_id, novel_id, chapter_id, filtered_content)
    user = User.query.get(user_id)
    
    # 如果有敏感词匹配，更新通知中的评论ID
    if has_sensitive and matches:
        # 这里可以更新之前创建的通知，添加评论ID
        pass
    
    return {
        'success': True,
        'message': 'Comment added',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'user': {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            },
            'has_sensitive': has_sensitive
        }
    }
```

类似地，修改小说和章节添加功能：

```python
# 在app/services/novel_service.py中修改add_novel和add_chapter方法

# 在add_novel方法中添加敏感词过滤
from app.services.admin_service import AdminService
has_sensitive, matches, filtered_intro = AdminService.filter_and_notify_sensitive_content(
    content=intro,
    user_id=user_id,
    content_type='novel',
    content_id=0  # 先设为0，小说创建后再更新
)

# 使用过滤后的简介创建小说
novel = NovelDAO.create_novel(
    title=title,
    author_id=author.id,
    author=author_name,
    category=category,
    intro=filtered_intro,  # 使用过滤后的内容
    cover=cover,
    status='ongoing'
)

# 在add_chapter方法中同样添加敏感词过滤
has_sensitive, matches, filtered_content = AdminService.filter_and_notify_sensitive_content(
    content=content,
    user_id=author_id,  # 这里应该是作者ID
    content_type='chapter',
    content_id=0  # 先设为0，章节创建后再更新
)

# 使用过滤后的内容创建章节
chapter = NovelDAO.create_chapter(novel_id, title, filtered_content, chapter_number)
```

## 12. 更新API文档

```markdown
# 通知模块 API 文档

## 1. 获取用户通知列表

- **URL**: `/api/notification`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 100)

- **成功响应** (200 OK):

```json
{
  "success": true,
  "notifications": [
    {
      "id": 1,
      "title": "您的评论中包含敏感词",
      "content": "系统检测到您的评论（ID: 123）中包含以下敏感词：敏感词1（低级）、敏感词2（中级）。请注意遵守社区规范，谨慎用词。",
      "notification_type": "sensitive_word",
      "related_object_type": "comment",
      "related_object_id": 123,
      "is_read": false,
      "created_at": "2025-04-10T15:30:00"
    }
  ],
  "total": 10,
  "page": 1,
  "per_page": 20,
  "total_pages": 1,
  "unread_count": 5
}
```

## 2. 将通知标记为已读

- **URL**: `/api/notification/{notification_id}/read`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `notification_id`: 通知ID

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "通知已标记为已读"
}
```

## 3. 将所有通知标记为已读

- **URL**: `/api/notification/read-all`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**: `Authorization: Bearer {token}`

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "所有通知已标记为已读"
}
```

# 敏感词管理 API 文档补充

## 1. 扫描内容中的敏感词

- **URL**: `/api/admin/content-scan`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **请求头**: `Authorization: Bearer {token}`
- **描述**: 扫描所有现有内容中的敏感词，自动替换并发送通知给内容所有者

- **成功响应** (200 OK):

```json
{
  "success": true,
  "results": {
    "novel": {
      "total": 100,
      "updated": 5
    },
    "chapter": {
      "total": 500,
      "updated": 15
    },
    "comment": {
      "total": 1000,
      "updated": 23
    }
  },
  "timestamp": "2025-04-10T15:30:00"
}
```
```

## 总结

本方案提供了以下功能：

1. **敏感词自动扫描**：每天自动扫描所有内容中的敏感词
2. **管理员手动扫描**：管理员可以随时触发手动扫描
3. **实时内容过滤**：创建评论、小说、章节时自动过滤敏感词
4. **用户通知**：发现敏感词时自动发送通知给内容所有者
5. **自动替换**：自动将敏感词替换为星号

该方案无需额外的内容审核步骤，自动执行敏感词过滤，同时通过通知机制让用户了解其内容被修改的原因。这样管理员只需要维护敏感词列表，无需手动审核每个内容。

需要添加的依赖库：
```
schedule==1.1.0  # 或最新版本
```

前端需要额外实现的功能：
1. 用户通知列表页面
2. 通知数量提示和已读标记功能
3. 管理后台的手动敏感词扫描功能


### 已完成实施:

1. ✅ 创建用户通知模型 (UserNotification)
2. ✅ 实现通知DAO和服务层
3. ✅ 修改敏感词过滤服务，添加通知功能
4. ✅ 添加批量扫描任务
5. ✅ 添加定时任务调度器
6. ✅ 更新requirements.txt，添加schedule依赖
7. ✅ 应用启动时启动调度器 (通过独立脚本启动)
8. ✅ 后端通知API接口注册 (导入notification蓝图)
9. ✅ 管理员手动扫描接口注册
10. ✅ 前端API调用模块 (notification.js, admin.js)
11. ✅ 前端管理员扫描界面 (SensitiveWords.vue)
12. ✅ 修改评论/小说/章节添加功能，添加实时敏感词检测 (interaction_service.py, novel_service.py)

### 待完成:

- 无

### 实施中遇到的问题:

1. 已创建独立脚本backend/scripts/setup_scheduler.py用于启动调度器，解决了无法在应用启动时自动启动的问题。
2. 蓝图注册和API endpoint添加已完成。