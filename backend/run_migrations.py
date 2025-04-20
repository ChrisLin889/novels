import os
import sys
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Novel, Chapter, UserCollection, UserHistory, Comment, Author, Category, Tag

# 创建应用实例
app = create_app()

# 确保所有模型都已导入
with app.app_context():
    # 运行迁移
    print("开始执行数据库迁移...")
    try:
        # 直接执行迁移
        from flask_migrate import upgrade
        # 运行迁移
        upgrade()
        print("数据库迁移成功完成!")
    except Exception as e:
        print(f"迁移过程中出现错误: {e}")
        sys.exit(1)
    
    # 验证Category表是否创建成功
    try:
        categories = Category.query.all()
        print(f"成功查询到 {len(categories)} 个分类")
    except Exception as e:
        print(f"查询Category表失败: {e}")
        
    print("迁移过程完成.") 