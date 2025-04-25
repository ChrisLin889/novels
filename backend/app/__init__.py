from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
    
    # Set database URI based on environment
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'DATABASE_URL',
            'mysql+pymysql://root:ok123456@localhost/novel_db'
        )
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_dev_key')
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.api.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    from app.api.novel import novel_bp
    app.register_blueprint(novel_bp, url_prefix='/api/novel')
    
    from app.api.data_import import import_bp
    app.register_blueprint(import_bp, url_prefix='/api/import')
    
    from app.api.interaction import interaction_bp
    app.register_blueprint(interaction_bp, url_prefix='/api/interaction')
    
    from app.api.search import search_bp
    app.register_blueprint(search_bp, url_prefix='/api/search')
    
    from app.api.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    from app.api.author import author_bp
    app.register_blueprint(author_bp, url_prefix='/api/author')
    
    from app.api.notification import notification_bp
    app.register_blueprint(notification_bp, url_prefix='/api/notification')
    
    @app.route('/')
    def index():
        return {'message': 'Novel API is running!'}
    
    return app 