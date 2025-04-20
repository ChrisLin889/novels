from app import create_app, db
from app.models.tag import Tag
from app.models.category import Category

app = create_app()

with app.app_context():
    tags = Tag.query.all()
    print(f"找到 {len(tags)} 个标签:")
    for t in tags:
        category_name = t.category.name if t.category else "无分类"
        print(f"- ID: {t.id}, 名称: {t.name}, 分类: {category_name}, 描述: {t.description}") 