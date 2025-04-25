from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 导入模型类
from .novel import Novel
from .chapter import Chapter
from .comment import Comment
from .user import User 