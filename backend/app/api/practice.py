print("🔥 practice.py loaded")

"""
Enhanced practice interface module for InterPrep-AI Next Generation.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.practice_service import PracticeService

# Create blueprint
practice_bp = Blueprint('practice', __name__)

@practice_bp.route('/session', methods=['GET'])
@jwt_required()
def get_practice_session():
    """Get a personalized practice session."""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    topic = request.args.get('topic')
    difficulty = request.args.get('difficulty')
    company = request.args.get('company')
    limit = int(request.args.get('limit', 5))
    
    try:
        # Get practice session from service
        questions = PracticeService.get_practice_session(
            current_user_id,
            topic=topic,
            difficulty=difficulty,
            company=company,
            limit=limit
        )
        
        return jsonify(questions), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting practice session: {str(e)}'}), 500

@practice_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_practice_progress():
    """Get user's practice progress statistics."""
    current_user_id = get_jwt_identity()
    
    try:
        # Get progress from service
        progress = PracticeService.get_user_progress(current_user_id)
        
        return jsonify(progress), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting practice progress: {str(e)}'}), 500

@practice_bp.route('/activity', methods=['POST'])
@jwt_required()
def record_practice_activity():
    """Record practice activity."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['question_id']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        # Record activity from service
        history = PracticeService.record_practice_activity(
            current_user_id,
            data['question_id'],
            completed=data.get('completed', False)
        )
        
        return jsonify(history), 200
    
    except Exception as e:
        return jsonify({'message': f'Error recording practice activity: {str(e)}'}), 500

@practice_bp.route('/evaluate', methods=['POST'])
@jwt_required()
def evaluate_solution():
    """Evaluate a practice solution."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['question_id', 'code', 'language']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        # Evaluate solution from service
        result = PracticeService.evaluate_practice_solution(
            current_user_id,
            data['question_id'],
            data['code'],
            data['language']
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'message': f'Error evaluating solution: {str(e)}'}), 500

@practice_bp.route('/debug', methods=['GET'])
def debug_route():
    print("✅ /debug endpoint hit")
    return jsonify({"msg": "Practice blueprint is working!"}), 200