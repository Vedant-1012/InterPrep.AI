from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from ..extensions import db

class LearningCategory(db.Model):
    """Learning category model for organizing learning content."""
    __tablename__ = 'learning_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50), nullable=True)
    
    topics = db.relationship('LearningTopic', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, name, description=None, order=0, icon=None):
        self.name = name
        self.description = description
        self.order = order
        self.icon = icon
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'icon': self.icon
        }
    
    def __repr__(self):
        return f'<LearningCategory {self.name}>'


class LearningTopic(db.Model):
    """Learning topic model for organizing learning content."""
    __tablename__ = 'learning_topics'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('learning_categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50), nullable=True)
    
    content = db.relationship('LearningContent', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    progress = db.relationship('LearningProgress', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, category_id, name, description=None, order=0, icon=None):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.order = order
        self.icon = icon
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'icon': self.icon
        }
    
    def __repr__(self):
        return f'<LearningTopic {self.name}>'


class LearningContent(db.Model):
    """Learning content model for storing learning materials."""
    __tablename__ = 'learning_content'
    
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('learning_topics.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # text, code, image, video
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    content_metadata = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, topic_id, title, content_type, content, order=0, metadata=None):
        self.topic_id = topic_id
        self.title = title
        self.content_type = content_type
        self.content = content
        self.order = order
        self.content_metadata = metadata or {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'title': self.title,
            'content_type': self.content_type,
            'content': self.content,
            'order': self.order,
            'metadata': self.content_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<LearningContent {self.title}>'


class LearningProgress(db.Model):
    """Learning progress model for tracking user progress."""
    __tablename__ = 'learning_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('learning_topics.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    progress_percentage = db.Column(db.Float, default=0.0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, topic_id, completed=False, progress_percentage=0.0):
        self.user_id = user_id
        self.topic_id = topic_id
        self.completed = completed
        self.progress_percentage = progress_percentage
    
    def update_progress(self, progress_percentage, completed=None):
        self.progress_percentage = progress_percentage
        if completed is not None:
            self.completed = completed
        self.last_accessed = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'completed': self.completed,
            'progress_percentage': self.progress_percentage,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }
    
    def __repr__(self):
        return f'<LearningProgress {self.id}>'