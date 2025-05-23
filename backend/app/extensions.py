"""
Flask extensions initialization for InterPrep-AI Next Generation.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_extensions(app):
    """Initialize Flask extensions with the app."""
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate.init_app(app, db)
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Note: CORS is now initialized directly in app/__init__.py
    # to avoid redundant configuration
