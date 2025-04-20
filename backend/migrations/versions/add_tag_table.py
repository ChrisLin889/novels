"""add tag table

Revision ID: 20251001002
Revises: 20251001001
Create Date: 2025-10-01 00:00:02

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '20251001002'
down_revision = '20251001001'
branch_labels = None
depends_on = None


def upgrade():
    # 创建tag表
    op.create_table('tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # 创建novel_tag关联表
    op.create_table('novel_tag',
        sa.Column('novel_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['novel_id'], ['novel.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('novel_id', 'tag_id')
    )
    
    # 添加初始数据
    op.bulk_insert(
        sa.table('tag',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('category_id', sa.Integer),
            sa.column('description', sa.Text),
        ),
        [
            {'id': 1, 'name': '奇幻', 'category_id': 5, 'description': '包含幻想元素的作品'},
            {'id': 2, 'name': '冒险', 'category_id': 5, 'description': '主角踏上冒险旅程的作品'},
            {'id': 3, 'name': '浪漫', 'category_id': 5, 'description': '包含浪漫情节的作品'},
            {'id': 4, 'name': '悬疑', 'category_id': 5, 'description': '包含悬疑元素的作品'},
            {'id': 5, 'name': '英雄', 'category_id': 6, 'description': '有英雄人物的作品'},
            {'id': 6, 'name': '反派', 'category_id': 6, 'description': '有精彩反派的作品'},
            {'id': 7, 'name': '幽默', 'category_id': 7, 'description': '幽默风格的作品'},
            {'id': 8, 'name': '黑暗', 'category_id': 7, 'description': '黑暗风格的作品'},
        ]
    )


def downgrade():
    op.drop_table('novel_tag')
    op.drop_table('tag') 