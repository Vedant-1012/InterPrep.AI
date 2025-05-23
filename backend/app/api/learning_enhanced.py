"""
Enhanced learning interface module for InterPrep-AI Next Generation.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.learning_service import LearningService

# Create blueprint
learning_enhanced_bp = Blueprint('learning_enhanced', __name__, url_prefix='/api/learning-enhanced')

@learning_enhanced_bp.route('/path', methods=['GET'])
@jwt_required()
def get_learning_path():
    """Get a personalized learning path."""
    current_user_id = get_jwt_identity()
    
    try:
        # Get learning path from service
        path = LearningService.get_learning_path(current_user_id)
        
        return jsonify(path), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting learning path: {str(e)}'}), 500

@learning_enhanced_bp.route('/topic/<int:topic_id>', methods=['GET'])
@jwt_required()
def get_topic_content(topic_id):
    """Get content for a specific topic with user progress."""
    current_user_id = get_jwt_identity()
    
    try:
        # Get topic content from service
        content = LearningService.get_topic_content(current_user_id, topic_id)
        
        return jsonify(content), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting topic content: {str(e)}'}), 500

@learning_enhanced_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_learning_stats():
    """Get user's learning statistics."""
    current_user_id = get_jwt_identity()
    
    try:
        # Get learning stats from service
        stats = LearningService.get_user_learning_stats(current_user_id)
        
        return jsonify(stats), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting learning stats: {str(e)}'}), 500

@learning_enhanced_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get recommended topics for the user."""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    limit = int(request.args.get('limit', 3))
    
    try:
        # Get recommendations from service
        recommendations = LearningService.recommend_next_topics(current_user_id, limit=limit)
        
        return jsonify(recommendations), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting recommendations: {str(e)}'}), 500
