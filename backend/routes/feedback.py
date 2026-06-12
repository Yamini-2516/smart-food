from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Feedback, Meal, User
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/', methods=['POST'])
@jwt_required()
def submit_feedback():
    """Submit food feedback"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['meal_id', 'rating']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    meal = Meal.query.get(data['meal_id'])
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    feedback = Feedback(
        user_id=user_id,
        meal_id=data['meal_id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({
        'message': 'Feedback submitted',
        'feedback': feedback.to_dict()
    }), 201

@feedback_bp.route('/', methods=['GET'])
@jwt_required()
def get_feedback():
    """Get feedback (Admin) or user's feedback"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'admin':
        # Get all feedback
        feedbacks = Feedback.query.all()
    else:
        # Get user's feedback
        feedbacks = Feedback.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'feedback': [f.to_dict() for f in feedbacks]
    }), 200

@feedback_bp.route('/meal/<int:meal_id>', methods=['GET'])
def get_meal_feedback(meal_id):
    """Get feedback for a specific meal"""
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    feedbacks = Feedback.query.filter_by(meal_id=meal_id).all()
    
    # Calculate average rating
    if feedbacks:
        avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks)
    else:
        avg_rating = 0
    
    return jsonify({
        'meal_id': meal_id,
        'meal_name': meal.name,
        'average_rating': avg_rating,
        'total_feedbacks': len(feedbacks),
        'feedbacks': [f.to_dict() for f in feedbacks]
    }), 200

@feedback_bp.route('/<int:feedback_id>', methods=['GET'])
@jwt_required()
def get_feedback_detail(feedback_id):
    """Get specific feedback"""
    user_id = get_jwt_identity()
    feedback = Feedback.query.get(feedback_id)
    
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404
    
    user = User.query.get(user_id)
    if feedback.user_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(feedback.to_dict()), 200

@feedback_bp.route('/<int:feedback_id>', methods=['DELETE'])
@jwt_required()
def delete_feedback(feedback_id):
    """Delete feedback"""
    user_id = get_jwt_identity()
    feedback = Feedback.query.get(feedback_id)
    
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404
    
    if feedback.user_id != user_id:
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(feedback)
    db.session.commit()
    
    return jsonify({'message': 'Feedback deleted'}), 200
