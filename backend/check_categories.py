from app import create_app, db
from app.models.category import Category

app = create_app()

with app.app_context():
    categories = Category.query.all()
    print(f"找到 {len(categories)} 个分类:")
    for c in categories:
        print(f"- ID: {c.id}, 名称: {c.name}, 类型: {c.type}, 描述: {c.description}") 