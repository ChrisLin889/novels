from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/novel_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_dev_key')
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.api.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    from app.api.novel import novel_bp
    app.register_blueprint(novel_bp, url_prefix='/api/novel')
    
    from app.api.crawler import crawler_bp
    app.register_blueprint(crawler_bp, url_prefix='/api/crawler')
    
    from app.api.interaction import interaction_bp
    app.register_blueprint(interaction_bp, url_prefix='/api/interaction')
    
    @app.route('/')
    def index():
        return {'message': 'Novel API is running!'}
    
    return app 