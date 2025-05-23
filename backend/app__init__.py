"""
Flask application initialization for InterPrep-AI Next Generation.
"""
import os
from flask import Flask
from flask_cors import CORS

from .config import config
from .extensions import init_extensions, db
from .models import *

def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Configure CORS properly
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    register_blueprints(app)
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'UserProfile': UserProfile,
            'Question': Question,
            'Submission': Submission,
            'Favorite': Favorite,
            'PracticeHistory': PracticeHistory,
            'LearningCategory': LearningCategory,
            'LearningTopic': LearningTopic,
            'LearningContent': LearningContent,
            'LearningProgress': LearningProgress
        }
    
    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    # Import blueprints
    from .api import auth_bp, questions_bp, submissions_bp, learning_bp, users_bp, practice_bp
    
    # Register blueprints with URL prefixes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(submissions_bp, url_prefix='/api/submissions')
    app.register_blueprint(learning_bp, url_prefix='/api/learning')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(practice_bp, url_prefix='/api/practice')
