"""add category table

Revision ID: 20251001001
Revises: 
Create Date: 2025-10-01 00:00:01

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '20251001001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 创建category表
    op.create_table('category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(['parent_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # 添加初始数据
    op.bulk_insert(
        sa.table('category',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('type', sa.String),
            sa.column('description', sa.Text),
        ),
        [
            # 小说分类
            {'id': 1, 'name': 'Fantasy', 'type': 'novel', 'description': '奇幻小说'},
            {'id': 2, 'name': 'Science Fiction', 'type': 'novel', 'description': '科幻小说'},
            {'id': 3, 'name': 'Romance', 'type': 'novel', 'description': '言情小说'},
            {'id': 4, 'name': 'Mystery', 'type': 'novel', 'description': '悬疑小说'},
            # 标签分类
            {'id': 5, 'name': '情节', 'type': 'tag', 'description': '与情节相关的标签'},
            {'id': 6, 'name': '角色', 'type': 'tag', 'description': '与角色相关的标签'},
            {'id': 7, 'name': '风格', 'type': 'tag', 'description': '与写作风格相关的标签'},
        ]
    )


def downgrade():
    op.drop_table('category') 