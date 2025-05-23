# """
# API blueprints initialization for InterPrep-AI Next Generation.
# """
# from flask import Blueprint

# # Create blueprints
# auth_bp = Blueprint('auth', __name__)
# questions_bp = Blueprint('questions', __name__)
# submissions_bp = Blueprint('submissions', __name__)
# learning_bp = Blueprint('learning', __name__)
# users_bp = Blueprint('users', __name__)
# practice_bp = Blueprint('practice', __name__)

# # Import routes to register them with blueprints
# from . import auth, questions, submissions, learning, users, practice
# from .practice import practice_bp

# # Export all blueprints
# __all__ = [
#     'auth_bp',
#     'questions_bp',
#     'submissions_bp',
#     'learning_bp',
#     'users_bp',
#     'practice_bp'
# ]


"""
API blueprints initialization for InterPrep-AI Next Generation.
"""
from flask import Blueprint

# Import routes to register them with blueprints
from . import auth, questions, submissions, learning, users, practice

# Import only the blueprints (not re-creating them)
from .auth import auth_bp
from .questions import questions_bp
from .submissions import submissions_bp
from .learning import learning_bp
from .users import users_bp
from .practice import practice_bp

# Export all blueprints
__all__ = [
    'auth_bp',
    'questions_bp',
    'submissions_bp',
    'learning_bp',
    'users_bp',
    'practice_bp'
]