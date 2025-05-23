"""
Authentication routes for InterPrep-AI Next Generation.
"""
from flask import Blueprint,request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import check_password_hash

# from . import auth_bp
from ..models import User, UserProfile
from ..extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({
            'message': 'Missing required fields',
            'details': 'Username, email, and password are required'
        }), 400
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'message': 'Username already exists',
            'details': 'Please choose a different username'
        }), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'message': 'Email already exists',
            'details': 'An account with this email already exists'
        }), 409
    
    # Create new user
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(user)
        db.session.flush()  # Flush to get the user ID
        
        # User profile is now automatically created in the User model
        # No need to create it separately here
        
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error registering user',
            'details': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get JWT tokens."""
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['username', 'password']):
        return jsonify({
            'message': 'Missing username or password',
            'details': 'Both username and password are required'
        }), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({
            'message': 'Invalid username or password',
            'details': 'Please check your credentials and try again'
        }), 401
    
    # Update last login timestamp
    user.update_last_login()
    
    # Generate tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'message': 'Token refreshed',
        'access_token': access_token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client-side token removal)."""
    # Note: JWT tokens can't be invalidated server-side without additional infrastructure
    # Client should remove tokens from storage
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({
            'message': 'User not found',
            'details': 'The user associated with this token no longer exists'
        }), 404
    
    return jsonify({
        'message': 'User retrieved successfully',
        'user': user.to_dict()
    }), 200
