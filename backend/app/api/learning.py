"""
Learning resources routes for InterPrep-AI Next Generation.
"""
from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# from . import learning_bp
from ..models import LearningCategory, LearningTopic, LearningContent, LearningProgress
from ..extensions import db

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all learning categories."""
    categories = LearningCategory.query.order_by(LearningCategory.order).all()
    result = [category.to_dict() for category in categories]
    return jsonify(result), 200

@learning_bp.route('/topics', methods=['GET'])
@jwt_required()
def get_topics():
    """Get learning topics, optionally filtered by category."""
    category_id = request.args.get('category_id')
    
    # Base query
    query = LearningTopic.query
    
    # Apply filter if category_id is provided
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Get topics ordered by order field
    topics = query.order_by(LearningTopic.order).all()
    
    # Format response
    result = [topic.to_dict() for topic in topics]
    
    return jsonify(result), 200

@learning_bp.route('/topics/<int:topic_id>/content', methods=['GET'])
@jwt_required()
def get_topic_content(topic_id):
    """Get content for a specific topic."""
    current_user_id = get_jwt_identity()
    
    # Check if topic exists
    topic = LearningTopic.query.get(topic_id)
    if not topic:
        return jsonify({'message': 'Topic not found'}), 404
    
    # Get content ordered by order field
    content_items = LearningContent.query.filter_by(topic_id=topic_id).order_by(LearningContent.order).all()
    
    # Format response with progress information
    result = []
    for item in content_items:
        # Get progress for this content item
        progress = LearningProgress.query.filter_by(
            user_id=current_user_id,
            content_id=item.id
        ).first()
        
        # Format content item with progress
        content_data = item.to_dict()
        content_data['completed'] = progress.completed if progress else False
        content_data['last_accessed'] = progress.last_accessed.isoformat() if progress and progress.last_accessed else None
        
        result.append(content_data)
    
    return jsonify(result), 200

@learning_bp.route('/content/<int:content_id>', methods=['GET'])
@jwt_required()
def get_content(content_id):
    """Get specific learning content."""
    current_user_id = get_jwt_identity()
    
    # Get content
    content = LearningContent.query.get(content_id)
    if not content:
        return jsonify({'message': 'Content not found'}), 404
    
    try:
        # Record or update progress
        progress = LearningProgress.query.filter_by(
            user_id=current_user_id,
            content_id=content_id
        ).first()
        
        if progress:
            # Update last_accessed timestamp
            progress.last_accessed = db.func.now()
        else:
            # Create new progress entry
            progress = LearningProgress(
                user_id=current_user_id,
                content_id=content_id
            )
            db.session.add(progress)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log error but continue (non-critical)
        print(f"Error recording learning progress: {str(e)}")
    
    # Format response
    content_data = content.to_dict()
    content_data['completed'] = progress.completed if progress else False
    content_data['last_accessed'] = progress.last_accessed.isoformat() if progress and progress.last_accessed else None
    
    return jsonify(content_data), 200

@learning_bp.route('/progress', methods=['POST'])
@jwt_required()
def update_progress():
    """Update learning progress."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['content_id', 'completed']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    content_id = data['content_id']
    completed = data['completed']
    
    # Check if content exists
    content = LearningContent.query.get(content_id)
    if not content:
        return jsonify({'message': 'Content not found'}), 404
    
    try:
        # Find or create progress
        progress = LearningProgress.query.filter_by(
            user_id=current_user_id,
            content_id=content_id
        ).first()
        
        if progress:
            # Update progress
            progress.completed = completed
            progress.last_accessed = db.func.now()
        else:
            # Create new progress entry
            progress = LearningProgress(
                user_id=current_user_id,
                content_id=content_id,
                completed=completed
            )
            db.session.add(progress)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progress updated successfully',
            'content_id': content_id,
            'completed': completed,
            'last_accessed': progress.last_accessed.isoformat() if progress.last_accessed else None
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating progress: {str(e)}'}), 500


@learning_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_learning_stats():
    """Dummy learning stats endpoint for dashboard."""
    return jsonify({
        "overall_progress": 65,
        "completed_content": 13,
        "total_content": 20,
        "category_progress": [
            {"id": 1, "name": "Arrays", "percentage": 80},
            {"id": 2, "name": "Dynamic Programming", "percentage": 50},
            {"id": 3, "name": "Graphs", "percentage": 70}
        ]
    }), 200

@learning_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Return recommended topics (placeholder)."""
    return jsonify([
        {"id": 1, "name": "Arrays", "reason": "High importance in interviews"},
        {"id": 2, "name": "Graphs", "reason": "You recently practiced it"},
        {"id": 3, "name": "Dynamic Programming", "reason": "Low completion rate"}
    ]), 200