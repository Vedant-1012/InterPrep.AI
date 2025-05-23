"""
Practice module service for InterPrep-AI Next Generation.
"""
from datetime import datetime
from sqlalchemy import desc

from ..extensions import db
from ..models import Question, PracticeHistory, Submission
from ..ai.gemini import evaluate_solution

class PracticeService:
    """Service for practice-related operations."""
    
    @staticmethod
    def get_practice_session(user_id, topic=None, difficulty=None, company=None, limit=5):
        """Get a personalized practice session."""
        # Base query
        query = Question.query
        
        # Apply filters
        if topic:
            query = query.filter(Question.topic == topic)
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
        if company:
            query = query.filter(Question.company == company)
        
        # Get user's practice history
        history = PracticeHistory.query.filter_by(user_id=user_id).all()
        completed_ids = [h.question_id for h in history if h.completed]
        
        # Prioritize questions not completed yet
        if completed_ids:
            query = query.filter(~Question.id.in_(completed_ids))
        
        # Get questions
        questions = query.limit(limit).all()
        
        # If not enough questions, add some completed ones
        if len(questions) < limit and completed_ids:
            remaining = limit - len(questions)
            completed_questions = Question.query.filter(
                Question.id.in_(completed_ids)
            ).limit(remaining).all()
            questions.extend(completed_questions)
        
        # Convert to dictionaries
        return [q.to_dict() for q in questions]
    
    @staticmethod
    def get_user_progress(user_id):
        """Get user's practice progress statistics."""
        # Get practice history
        history = PracticeHistory.query.filter_by(user_id=user_id).all()
        
        # Get submissions
        submissions = Submission.query.filter_by(user_id=user_id).all()
        
        # Calculate statistics
        total_practiced = len(history)
        total_completed = len([h for h in history if h.completed])
        total_submissions = len(submissions)
        successful_submissions = len([s for s in submissions if s.status == 'accepted'])
        
        # Get topic distribution
        topics = {}
        for h in history:
            question = Question.query.get(h.question_id)
            if question:
                topic = question.topic
                if topic in topics:
                    topics[topic] += 1
                else:
                    topics[topic] = 1
        
        # Get difficulty distribution
        difficulties = {}
        for h in history:
            question = Question.query.get(h.question_id)
            if question:
                difficulty = question.difficulty
                if difficulty in difficulties:
                    difficulties[difficulty] += 1
                else:
                    difficulties[difficulty] = 1
        
        # Get recent activity
        recent_history = PracticeHistory.query.filter_by(
            user_id=user_id
        ).order_by(desc(PracticeHistory.last_practiced)).limit(5).all()
        
        recent_activity = []
        for h in recent_history:
            question = Question.query.get(h.question_id)
            if question:
                recent_activity.append({
                    'question_id': h.question_id,
                    'title': question.title,
                    'completed': h.completed,
                    'last_practiced': h.last_practiced.isoformat() if h.last_practiced else None,
                    'attempts': h.attempts
                })
        
        return {
            'total_practiced': total_practiced,
            'total_completed': total_completed,
            'completion_rate': (total_completed / total_practiced) if total_practiced > 0 else 0,
            'total_submissions': total_submissions,
            'successful_submissions': successful_submissions,
            'success_rate': (successful_submissions / total_submissions) if total_submissions > 0 else 0,
            'topics': topics,
            'difficulties': difficulties,
            'recent_activity': recent_activity
        }
    
    @staticmethod
    def record_practice_activity(user_id, question_id, completed=False):
        """Record practice activity."""
        # Check if question exists
        question = Question.query.get(question_id)
        if not question:
            raise ValueError(f"Question with ID {question_id} not found")
        
        # Check if history exists
        history = PracticeHistory.query.filter_by(
            user_id=user_id,
            question_id=question_id
        ).first()
        
        if history:
            # Update existing history
            history.update_practice(completed)
        else:
            # Create new history
            history = PracticeHistory(
                user_id=user_id,
                question_id=question_id,
                completed=completed
            )
            db.session.add(history)
        
        db.session.commit()
        return history.to_dict()
    
    @staticmethod
    def evaluate_practice_solution(user_id, question_id, code, language):
        """Evaluate a practice solution."""
        # Check if question exists
        question = Question.query.get(question_id)
        if not question:
            raise ValueError(f"Question with ID {question_id} not found")
        
        # Get question with solution
        question_data = question.to_dict_with_solution()
        
        # Evaluate solution using AI
        evaluation = evaluate_solution(
            question_data['content'],
            code,
            language,
            question_data['solution'],
            question_data['test_cases']
        )
        
        # Create submission record
        submission = Submission(
            user_id=user_id,
            question_id=question_id,
            code=code,
            language=language,
            status=evaluation['status'],
            runtime=evaluation.get('runtime'),
            memory=evaluation.get('memory'),
            feedback=evaluation.get('feedback')
        )
        db.session.add(submission)
        
        # Update practice history if solution is correct
        if evaluation['status'] == 'accepted':
            PracticeService.record_practice_activity(user_id, question_id, completed=True)
        
        db.session.commit()
        
        return {
            'submission_id': submission.id,
            'status': submission.status,
            'runtime': submission.runtime,
            'memory': submission.memory,
            'feedback': submission.feedback,
            'created_at': submission.created_at.isoformat() if submission.created_at else None
        }
