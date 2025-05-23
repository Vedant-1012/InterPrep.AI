"""
User management routes for InterPrep-AI Next Generation.
"""
from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# from . import users_bp
from ..models import User, UserProfile, Favorite, PracticeHistory, Submission, Question, LearningContent, LearningProgress
from ..extensions import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Get user profile
    profile = user.profile
    
    # Combine user and profile data
    user_data = user.to_dict()
    if profile:
        user_data.update(profile.to_dict())
    
    return jsonify(user_data), 200

@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    profile = user.profile
    
    try:
        # Update user fields
        if 'email' in data:
            # Check if email already exists for another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({'message': 'Email already exists'}), 409
            user.email = data['email']
        
        # Update password if provided
        if 'password' in data:
            user.set_password(data['password'])
        
        # Update profile fields
        if profile:
            if 'full_name' in data:
                profile.full_name = data['full_name']
            if 'bio' in data:
                profile.bio = data['bio']
            if 'preferences' in data:
                profile.preferences = data['preferences']
            if 'settings' in data:
                profile.settings = data['settings']
        
        db.session.commit()
        
        # Return updated user data
        user_data = user.to_dict()
        if profile:
            user_data.update(profile.to_dict())
        
        return jsonify(user_data), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating user: {str(e)}'}), 500

# @users_bp.route('/me/stats', methods=['GET'])
# @jwt_required()
# def get_user_stats():
#     """Get user statistics with simplified response."""
#     try:
#         print("Starting stats endpoint")
#         current_user_id = get_jwt_identity()
#         print(f"User ID: {current_user_id}")
        
#         # Return exactly what the frontend expects
#         stats = {
#             'submissions': {
#                 'total': 0,
#                 'correct': 0,
#                 'incorrect': 0,
#                 'pending': 0
#             },
#             'favorites_count': 0,
#             'practice_count': 0,
#             'completed_count': 0
#         }
        
#         print("Returning stats")
#         return jsonify(stats), 200
#     except Exception as e:
#         print(f"Error in stats endpoint: {str(e)}")
#         return jsonify({
#             'message': 'Error retrieving stats',
#             'error': str(e)
#         }), 500

# @users_bp.route('/me/stats', methods=['GET'])
# @jwt_required()
# def get_user_stats():
#     """Super simple stats endpoint."""
#     print("STATS ENDPOINT CALLED")
#     # Return a direct response without any processing
#     return jsonify({
#         "submissions": {"total": 0, "correct": 0, "incorrect": 0, "pending": 0}, 
#         "favorites_count": 0, 
#         "practice_count": 0, 
#         "completed_count": 0
#     }), 200
@users_bp.route('/me/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Basic test to rule out jsonify issues."""
    return {
        "submissions": {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "pending": 0
        },
        "favorites_count": 0,
        "practice_count": 0,
        "completed_count": 0
    }, 200


@users_bp.route('/me/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    """Get user's favorite questions."""
    current_user_id = get_jwt_identity()
    
    # Get favorites with question data
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    
    # Format response
    result = []
    for favorite in favorites:
        question = favorite.question
        result.append({
            'favorite_id': favorite.id,
            'added_at': favorite.added_at.isoformat() if favorite.added_at else None,
            'question': question.to_dict() if question else None
        })
    
    return jsonify(result), 200

@users_bp.route('/me/history', methods=['GET'])
@jwt_required()
def get_user_history():
    """Get user's practice history."""
    current_user_id = get_jwt_identity()
    
    # Get practice history with question data
    history = PracticeHistory.query.filter_by(user_id=current_user_id).all()
    
    # Format response
    result = []
    for entry in history:
        question = entry.question
        result.append({
            'history_id': entry.id,
            'viewed_at': entry.viewed_at.isoformat() if entry.viewed_at else None,
            'completed': entry.completed,
            'question': question.to_dict() if question else None
        })
    
    return jsonify(result), 200