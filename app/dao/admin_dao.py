from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import desc

from app.models import db, Novel, Chapter, Comment

class AdminDAO:
    @staticmethod
    def soft_delete_novel(novel_id: int) -> bool:
        """软删除小说（移至回收站）"""
        novel = Novel.query.get(novel_id)
        if not novel:
            return False
        
        try:
            # 软删除小说
            novel.is_deleted = True
            novel.deleted_at = datetime.now()
            
            # 同时软删除相关章节
            Chapter.query.filter_by(novel_id=novel_id).update({
                'is_deleted': True,
                'deleted_at': datetime.now()
            })
            
            # 同时软删除相关评论
            Comment.query.filter_by(novel_id=novel_id).update({
                'is_deleted': True,
                'deleted_at': datetime.now()
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"软删除小说时出错: {str(e)}")
            return False

    @staticmethod
    def soft_delete_chapter(chapter_id: int) -> bool:
        """软删除章节（移至回收站）"""
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return False
        
        try:
            # 软删除章节
            chapter.is_deleted = True
            chapter.deleted_at = datetime.now()
            
            # 同时软删除相关评论
            Comment.query.filter_by(chapter_id=chapter_id).update({
                'is_deleted': True,
                'deleted_at': datetime.now()
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"软删除章节时出错: {str(e)}")
            return False

    @staticmethod
    def soft_delete_comment(comment_id: int) -> bool:
        """软删除评论（移至回收站）"""
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
            print(f"软删除评论时出错: {str(e)}")
            return False

    @staticmethod
    def get_deleted_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Tuple[List[Novel], int]:
        """获取回收站中的所有小说"""
        query = Novel.query.filter_by(is_deleted=True)
        
        if title_filter:
            query = query.filter(Novel.title.ilike(f'%{title_filter}%'))
        
        total = query.count()
        novels = query.order_by(desc(Novel.deleted_at)).paginate(page=page, per_page=per_page).items
        
        return novels, total

    @staticmethod
    def get_deleted_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Tuple[List[Chapter], int]:
        """获取回收站中的所有章节"""
        query = Chapter.query.filter_by(is_deleted=True)
        
        if novel_id:
            query = query.filter_by(novel_id=novel_id)
        
        total = query.count()
        chapters = query.order_by(desc(Chapter.deleted_at)).paginate(page=page, per_page=per_page).items
        
        return chapters, total

    @staticmethod
    def get_deleted_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                         page: int = 1, per_page: int = 20) -> Tuple[List[Comment], int]:
        """获取回收站中的所有评论"""
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
        """从回收站还原小说及其关联内容"""
        novel = Novel.query.get(novel_id)
        if not novel or not novel.is_deleted:
            return False
        
        try:
            # 还原小说
            novel.is_deleted = False
            novel.deleted_at = None
            
            # 还原相关章节
            Chapter.query.filter_by(novel_id=novel_id, is_deleted=True).update({
                'is_deleted': False,
                'deleted_at': None
            })
            
            # 还原相关评论
            Comment.query.filter_by(novel_id=novel_id, is_deleted=True).update({
                'is_deleted': False,
                'deleted_at': None
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"还原小说时出错: {str(e)}")
            return False

    @staticmethod
    def restore_chapter(chapter_id: int) -> bool:
        """从回收站还原章节及其关联评论"""
        chapter = Chapter.query.get(chapter_id)
        if not chapter or not chapter.is_deleted:
            return False
        
        try:
            # 还原章节
            chapter.is_deleted = False
            chapter.deleted_at = None
            
            # 同时还原相关评论
            Comment.query.filter_by(chapter_id=chapter_id, is_deleted=True).update({
                'is_deleted': False,
                'deleted_at': None
            })
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"还原章节时出错: {str(e)}")
            return False

    @staticmethod
    def restore_comment(comment_id: int) -> bool:
        """从回收站还原评论"""
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
            print(f"还原评论时出错: {str(e)}")
            return False

    @staticmethod
    def delete_novel_cascade(novel_id: int) -> bool:
        """永久删除小说及其所有章节和评论（级联删除）"""
        novel = Novel.query.get(novel_id)
        if not novel:
            return False
        
        try:
            # 删除该小说下的所有评论
            Comment.query.filter_by(novel_id=novel_id).delete()
            
            # 删除小说（会通过外键约束级联删除章节）
            db.session.delete(novel)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"删除小说时出错: {str(e)}")
            return False

    @staticmethod
    def permanently_delete_chapter(chapter_id: int) -> bool:
        """永久删除回收站中的章节（同时删除关联评论）"""
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return False
        
        try:
            # 删除该章节下的所有评论
            Comment.query.filter_by(chapter_id=chapter_id).delete()
            
            # 删除章节
            db.session.delete(chapter)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"永久删除章节时出错: {str(e)}")
            return False

    @staticmethod
    def permanently_delete_comment(comment_id: int) -> bool:
        """永久删除回收站中的评论"""
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        
        try:
            db.session.delete(comment)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"永久删除评论时出错: {str(e)}")
            return False 