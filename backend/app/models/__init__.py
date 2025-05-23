"""
Initialize models package for InterPrep-AI Next Generation.
"""
from ..extensions import db

# Import all models to make them available when importing the models package
from .user import User, UserProfile
from .question import Question, Submission, Favorite, PracticeHistory
from .learning import LearningCategory, LearningTopic, LearningContent, LearningProgress

# Export all models
__all__ = [
    'User',
    'UserProfile',
    'Question',
    'Submission',
    'Favorite',
    'PracticeHistory',
    'LearningCategory',
    'LearningTopic',
    'LearningContent',
    'LearningProgress'
]
