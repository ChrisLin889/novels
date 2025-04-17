from app import db, create_app
from app.models.user import User
from app.models.author import Author
from app.models.admin import Admin, ContentAudit
from app.models.novel import Novel
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_roles():
    """将现有用户的角色迁移到新的表结构"""
    app = create_app()
    with app.app_context():
        # 检查是否已经有作者或管理员记录
        existing_authors = Author.query.count()
        existing_admins = Admin.query.count()
        
        if existing_authors > 0 or existing_admins > 0:
            logger.info("已存在作者或管理员记录，跳过迁移")
            return
            
        # 找出所有有role信息的用户（从备份表中获取）
        try:
            # 尝试从user_backup表读取角色信息
            authors = db.session.execute("SELECT id, username, created_at, updated_at FROM user_backup WHERE role = 'author'").fetchall()
            admins = db.session.execute("SELECT id, username, created_at, updated_at FROM user_backup WHERE role = 'admin'").fetchall()
            
            logger.info(f"找到 {len(authors)} 个作者和 {len(admins)} 个管理员需要迁移")
            
            # 创建作者记录
            for author_data in authors:
                user = User.query.get(author_data.id)
                if user:
                    author = Author(
                        user_id=user.id,
                        pen_name=user.username,
                        created_at=user.created_at,
                        updated_at=user.updated_at
                    )
                    db.session.add(author)
                    logger.info(f"为用户 {user.username} 创建作者记录")
            
            # 创建管理员记录
            for admin_data in admins:
                user = User.query.get(admin_data.id)
                if user:
                    admin = Admin(
                        user_id=user.id,
                        admin_level=1,
                        permissions={'content': True, 'user': True},
                        created_at=user.created_at,
                        updated_at=user.updated_at
                    )
                    db.session.add(admin)
                    logger.info(f"为用户 {user.username} 创建管理员记录")
            
            db.session.commit()
            logger.info("用户角色迁移完成")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"迁移过程中出错: {str(e)}")
            raise
            
def migrate_relationships():
    """更新关系表的外键引用"""
    app = create_app()
    with app.app_context():
        try:
            # 更新小说表中的author_id
            novels = Novel.query.filter(Novel.author_id.isnot(None)).all()
            for novel in novels:
                # 查找作者记录
                author = Author.query.filter_by(user_id=novel.author_id).first()
                if author:
                    novel.author_id = author.id
                    logger.info(f"更新小说 '{novel.title}' 的作者ID为 {author.id}")
                else:
                    novel.author_id = None
                    logger.warning(f"小说 '{novel.title}' 的作者未找到，设置为NULL")
                    
            # 更新内容审核表中的reviewer_id/admin_id
            audits = ContentAudit.query.filter(ContentAudit.admin_id.isnot(None)).all()
            for audit in audits:
                # 查找管理员记录
                admin = Admin.query.filter_by(user_id=audit.admin_id).first()
                if admin:
                    audit.admin_id = admin.id
                    logger.info(f"更新内容审核 #{audit.id} 的管理员ID为 {admin.id}")
                else:
                    audit.admin_id = None
                    logger.warning(f"内容审核 #{audit.id} 的管理员未找到，设置为NULL")
                    
            db.session.commit()
            logger.info("关系迁移完成")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"迁移关系时出错: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        migrate_roles()
        migrate_relationships()
        print("数据迁移成功完成！")
    except Exception as e:
        print(f"数据迁移失败: {str(e)}")