from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    data = request.get_json()
    
    # Validation
    if not data or not all(k in data for k in ['name', 'email', 'password', 'role']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout endpoint"""
    # In a real app, you'd blacklist the token
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    """Mock Google OAuth login"""
    data = request.get_json()
    
    # In production, verify the token with Google
    email = data.get('email')
    name = data.get('name')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    # Find or create user
    user = User.query.filter_by(email=email).first()
    
    if not user:
        user = User(
            name=name or email.split('@')[0],
            email=email,
            role='student'
        )
        user.set_password('google-oauth-user')  # Dummy password
        db.session.add(user)
        db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Google login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200
