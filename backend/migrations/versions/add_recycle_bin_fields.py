"""add recycle bin fields

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
    # 为小说表添加回收站字段
    op.add_column('novel', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('novel', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    
    # 为章节表添加回收站字段
    op.add_column('chapter', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('chapter', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    
    # 为评论表添加回收站字段
    op.add_column('comments', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('comments', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    
    # 添加索引以优化查询性能
    op.create_index('idx_novel_is_deleted', 'novel', ['is_deleted'])
    op.create_index('idx_chapter_is_deleted', 'chapter', ['is_deleted'])
    op.create_index('idx_comments_is_deleted', 'comments', ['is_deleted'])


def downgrade():
    # 删除索引
    op.drop_index('idx_novel_is_deleted', 'novel')
    op.drop_index('idx_chapter_is_deleted', 'chapter')
    op.drop_index('idx_comments_is_deleted', 'comments')
    
    # 删除列
    op.drop_column('novel', 'is_deleted')
    op.drop_column('novel', 'deleted_at')
    op.drop_column('chapter', 'is_deleted')
    op.drop_column('chapter', 'deleted_at')
    op.drop_column('comments', 'is_deleted')
    op.drop_column('comments', 'deleted_at') 