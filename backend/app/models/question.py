"""
Question models for InterPrep-AI Next Generation.
"""
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

from ..extensions import db

class Question(db.Model):
    """Question model for storing coding questions."""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    topic = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    code_template = db.Column(db.Text, nullable=True)
    solution = db.Column(db.Text, nullable=True)
    test_cases = db.Column(JSON, nullable=True)
    hints = db.Column(JSON, nullable=True)
    
    # Relationships
    submissions = db.relationship('Submission', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    practice_history = db.relationship('PracticeHistory', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, title, content, difficulty, topic, company=None, code_template=None, solution=None, test_cases=None, hints=None):
        self.title = title
        self.content = content
        self.difficulty = difficulty
        self.topic = topic
        self.company = company
        self.code_template = code_template
        self.solution = solution
        self.test_cases = test_cases or []
        self.hints = hints or []
    
    def to_dict(self):
        """Convert question to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'company': self.company,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'code_template': self.code_template,
            'hints': self.hints
        }
    
    def to_dict_with_solution(self):
        """Convert question to dictionary with solution."""
        data = self.to_dict()
        data['solution'] = self.solution
        data['test_cases'] = self.test_cases
        return data
    
    def __repr__(self):
        return f'<Question {self.title}>'


class Submission(db.Model):
    """Submission model for storing user submissions."""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # accepted, wrong_answer, time_limit_exceeded, etc.
    runtime = db.Column(db.Integer, nullable=True)  # in milliseconds
    memory = db.Column(db.Integer, nullable=True)  # in kilobytes
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, question_id, code, language, status, runtime=None, memory=None, feedback=None):
        self.user_id = user_id
        self.question_id = question_id
        self.code = code
        self.language = language
        self.status = status
        self.runtime = runtime
        self.memory = memory
        self.feedback = feedback
    
    def to_dict(self):
        """Convert submission to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'code': self.code,
            'language': self.language,
            'status': self.status,
            'runtime': self.runtime,
            'memory': self.memory,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Submission {self.id}>'


class Favorite(db.Model):
    """Favorite model for storing user favorites."""
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id
    
    def to_dict(self):
        """Convert favorite to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Favorite {self.id}>'


class PracticeHistory(db.Model):
    """Practice history model for tracking user practice."""
    __tablename__ = 'practice_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    last_practiced = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.Column(db.Integer, default=1)
    
    def __init__(self, user_id, question_id, completed=False):
        self.user_id = user_id
        self.question_id = question_id
        self.completed = completed
    
    def update_practice(self, completed=None):
        """Update practice history."""
        if completed is not None:
            self.completed = completed
        self.last_practiced = datetime.utcnow()
        self.attempts += 1
    
    def to_dict(self):
        """Convert practice history to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'completed': self.completed,
            'last_practiced': self.last_practiced.isoformat() if self.last_practiced else None,
            'attempts': self.attempts
        }
    
    def __repr__(self):
        return f'<PracticeHistory {self.id}>'
