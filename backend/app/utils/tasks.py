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