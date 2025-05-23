"""
Question management routes for InterPrep-AI Next Generation.
"""
from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import numpy as np

# from . import questions_bp
from ..models import Question, Favorite, PracticeHistory
from ..extensions import db
from ..ai.gemini import generate_question, generate_similar_question
from ..ai.embeddings import embed_text
from ..ai.search import search_similar_questions

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('', methods=['GET'])
@jwt_required()
def get_questions():
    """Get questions with filters."""
    # Get query parameters
    topic = request.args.get('topic')
    difficulty = request.args.get('difficulty')
    company = request.args.get('company')
    search_query = request.args.get('query')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Base query
    query = Question.query
    
    # Apply filters
    if topic:
        query = query.filter(Question.topic == topic)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if company:
        query = query.filter(Question.company == company)
    
    # If search query is provided, use vector search
    if search_query:
        # Get question IDs from vector search
        question_ids = search_similar_questions(search_query, limit=limit)
        if question_ids:
            query = query.filter(Question.id.in_(question_ids))
    
    # Apply pagination
    questions = query.limit(limit).offset(offset).all()
    
    # Format response
    result = [q.to_dict() for q in questions]
    
    return jsonify(result), 200

@questions_bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question(question_id):
    """Get question details."""
    current_user_id = get_jwt_identity()
    
    # Get question
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'message': 'Question not found'}), 404
    
    # Record in practice history
    try:
        # Check if already in history
        history = PracticeHistory.query.filter_by(
            user_id=current_user_id,
            question_id=question_id
        ).first()
        
        if history:
            # Update viewed_at timestamp
            history.viewed_at = db.func.now()
        else:
            # Create new history entry
            history = PracticeHistory(
                user_id=current_user_id,
                question_id=question_id
            )
            db.session.add(history)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log error but continue (non-critical)
        print(f"Error recording practice history: {str(e)}")
    
    # Check if question is favorited
    is_favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        question_id=question_id
    ).first() is not None
    
    # Get question data
    question_data = question.to_dict()
    question_data['is_favorite'] = is_favorite
    
    return jsonify(question_data), 200

@questions_bp.route('/generate', methods=['POST'])
@jwt_required()
def create_question():
    """Generate a new question."""
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['topic', 'difficulty']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        # Generate question using AI
        topic = data['topic']
        difficulty = data['difficulty']
        company = data.get('company')
        
        # Call AI service to generate question
        question_data = generate_question(topic, difficulty, company)
        
        # Create question in database
        question = Question(
            title=question_data['title'],
            content=question_data['content'],
            difficulty=difficulty,
            topic=topic,
            company=company,
            source_type='generated'
        )
        
        # Generate and store embedding
        embedding = embed_text(question.title + " " + question.content)
        if embedding is not None:
            question.embedding = embedding.tolist()
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify(question.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error generating question: {str(e)}'}), 500

@questions_bp.route('/<int:question_id>/similar', methods=['POST'])
@jwt_required()
def generate_similar(question_id):
    """Generate a similar question."""
    # Get original question
    original_question = Question.query.get(question_id)
    if not original_question:
        return jsonify({'message': 'Question not found'}), 404
    
    try:
        # Generate similar question using AI
        question_data = generate_similar_question(
            original_question.title,
            original_question.content,
            original_question.difficulty,
            original_question.topic
        )
        
        # Create question in database
        question = Question(
            title=question_data['title'],
            content=question_data['content'],
            difficulty=original_question.difficulty,
            topic=original_question.topic,
            company=original_question.company,
            source_type='generated'
        )
        
        # Generate and store embedding
        embedding = embed_text(question.title + " " + question.content)
        if embedding is not None:
            question.embedding = embedding.tolist()
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify(question.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error generating similar question: {str(e)}'}), 500

@questions_bp.route('/<int:question_id>/favorite', methods=['POST'])
@jwt_required()
def add_favorite(question_id):
    """Add question to favorites."""
    current_user_id = get_jwt_identity()
    
    # Check if question exists
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'message': 'Question not found'}), 404
    
    # Check if already favorited
    existing = Favorite.query.filter_by(
        user_id=current_user_id,
        question_id=question_id
    ).first()
    
    if existing:
        return jsonify({'message': 'Question already in favorites'}), 409
    
    try:
        # Add to favorites
        favorite = Favorite(
            user_id=current_user_id,
            question_id=question_id
        )
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Question added to favorites',
            'favorite_id': favorite.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error adding to favorites: {str(e)}'}), 500

@questions_bp.route('/<int:question_id>/favorite', methods=['DELETE'])
@jwt_required()
def remove_favorite(question_id):
    """Remove question from favorites."""
    current_user_id = get_jwt_identity()
    
    # Find favorite
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        question_id=question_id
    ).first()
    
    if not favorite:
        return jsonify({'message': 'Question not in favorites'}), 404
    
    try:
        # Remove from favorites
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({'message': 'Question removed from favorites'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error removing from favorites: {str(e)}'}), 500

__all__ = ['questions_bp']