"""
Submission management routes for InterPrep-AI Next Generation.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# from . import submissions_bp
from ..models import Submission, Question, PracticeHistory
from ..extensions import db
from ..ai.gemini import evaluate_solution

submissions_bp = Blueprint('submissions', __name__) 

@submissions_bp.route('', methods=['POST'])
@jwt_required()
def submit_solution():
    """Submit a solution for evaluation."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['question_id', 'code', 'language']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if question exists
    question_id = data['question_id']
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'message': 'Question not found'}), 404
    
    try:
        # Create submission
        submission = Submission(
            user_id=current_user_id,
            question_id=question_id,
            code=data['code'],
            language=data['language'],
            status='pending'
        )
        db.session.add(submission)
        db.session.flush()  # Get submission ID
        
        # Evaluate solution using AI
        evaluation_result = evaluate_solution(
            question.content,
            data['code'],
            data['language']
        )
        
        # Update submission with evaluation results
        submission.status = evaluation_result['status']
        submission.feedback = evaluation_result['feedback']
        
        # Mark question as completed in practice history
        history = PracticeHistory.query.filter_by(
            user_id=current_user_id,
            question_id=question_id
        ).first()
        
        if history:
            history.completed = True
        
        db.session.commit()
        
        # Return submission with evaluation
        result = submission.to_dict()
        result.update(evaluation_result)
        
        return jsonify(result), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error submitting solution: {str(e)}'}), 500

@submissions_bp.route('', methods=['GET'])
@jwt_required()
def get_submissions():
    """Get user's submissions."""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    question_id = request.args.get('question_id')
    status = request.args.get('status')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Base query
    query = Submission.query.filter_by(user_id=current_user_id)
    
    # Apply filters
    if question_id:
        query = query.filter_by(question_id=question_id)
    if status:
        query = query.filter_by(status=status)
    
    # Apply sorting and pagination
    submissions = query.order_by(Submission.submitted_at.desc()).limit(limit).offset(offset).all()
    
    # Format response
    result = []
    for submission in submissions:
        submission_data = submission.to_dict()
        submission_data['question'] = submission.question.to_dict() if submission.question else None
        result.append(submission_data)
    
    return jsonify(result), 200

@submissions_bp.route('/<int:submission_id>', methods=['GET'])
@jwt_required()
def get_submission(submission_id):
    """Get submission details."""
    current_user_id = get_jwt_identity()
    
    # Get submission
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'message': 'Submission not found'}), 404
    
    # Check if submission belongs to current user
    if submission.user_id != current_user_id:
        return jsonify({'message': 'Unauthorized access to submission'}), 403
    
    # Format response
    submission_data = submission.to_dict()
    submission_data['question'] = submission.question.to_dict() if submission.question else None
    
    return jsonify(submission_data), 200
