"""
Learning module service for InterPrep-AI Next Generation.
"""
from sqlalchemy import desc

from ..extensions import db
from ..models import LearningCategory, LearningTopic, LearningContent, LearningProgress

class LearningService:
    """Service for learning-related operations."""
    
    @staticmethod
    def get_categories():
        """Get all learning categories."""
        categories = LearningCategory.query.order_by(LearningCategory.order).all()
        return [c.to_dict() for c in categories]
    
    @staticmethod
    def get_topics(category_id):
        """Get topics by category."""
        topics = LearningTopic.query.filter_by(
            category_id=category_id
        ).order_by(LearningTopic.order).all()
        return [t.to_dict() for t in topics]
    
    @staticmethod
    def get_content(topic_id):
        """Get content by topic."""
        content = LearningContent.query.filter_by(
            topic_id=topic_id
        ).order_by(LearningContent.order).all()
        return [c.to_dict() for c in content]
    
    @staticmethod
    def get_user_progress(user_id):
        """Get user's learning progress."""
        # Get all progress records
        progress_records = LearningProgress.query.filter_by(user_id=user_id).all()
        
        # Get all topics
        all_topics = LearningTopic.query.all()
        
        # Calculate overall progress
        total_topics = len(all_topics)
        completed_topics = len([p for p in progress_records if p.completed])
        overall_progress = (completed_topics / total_topics) if total_topics > 0 else 0
        
        # Get progress by category
        categories = LearningCategory.query.all()
        category_progress = []
        
        for category in categories:
            # Get topics in this category
            category_topics = LearningTopic.query.filter_by(category_id=category.id).all()
            total_category_topics = len(category_topics)
            
            # Get completed topics in this category
            completed_category_topics = 0
            for topic in category_topics:
                progress = LearningProgress.query.filter_by(
                    user_id=user_id,
                    topic_id=topic.id,
                    completed=True
                ).first()
                if progress:
                    completed_category_topics += 1
            
            # Calculate category progress
            category_completion = (completed_category_topics / total_category_topics) if total_category_topics > 0 else 0
            
            category_progress.append({
                'category_id': category.id,
                'name': category.name,
                'total_topics': total_category_topics,
                'completed_topics': completed_category_topics,
                'progress': category_completion
            })
        
        # Get recent activity
        recent_progress = LearningProgress.query.filter_by(
            user_id=user_id
        ).order_by(desc(LearningProgress.last_accessed)).limit(5).all()
        
        recent_activity = []
        for progress in recent_progress:
            topic = LearningTopic.query.get(progress.topic_id)
            if topic:
                category = LearningCategory.query.get(topic.category_id)
                recent_activity.append({
                    'topic_id': progress.topic_id,
                    'topic_name': topic.name,
                    'category_name': category.name if category else None,
                    'progress_percentage': progress.progress_percentage,
                    'completed': progress.completed,
                    'last_accessed': progress.last_accessed.isoformat() if progress.last_accessed else None
                })
        
        return {
            'overall_progress': overall_progress,
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'category_progress': category_progress,
            'recent_activity': recent_activity
        }
    
    @staticmethod
    def update_progress(user_id, topic_id, progress_percentage, completed=None):
        """Update learning progress."""
        # Check if topic exists
        topic = LearningTopic.query.get(topic_id)
        if not topic:
            raise ValueError(f"Topic with ID {topic_id} not found")
        
        # Check if progress exists
        progress = LearningProgress.query.filter_by(
            user_id=user_id,
            topic_id=topic_id
        ).first()
        
        if progress:
            # Update existing progress
            progress.update_progress(progress_percentage, completed)
        else:
            # Create new progress
            progress = LearningProgress(
                user_id=user_id,
                topic_id=topic_id,
                progress_percentage=progress_percentage,
                completed=completed if completed is not None else False
            )
            db.session.add(progress)
        
        db.session.commit()
        return progress.to_dict()
