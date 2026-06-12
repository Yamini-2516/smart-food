from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Booking, Meal, User
from datetime import datetime, date

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/', methods=['POST'])
@jwt_required()
def book_meal():
    """Book a meal"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if not all(k in data for k in ['meal_id', 'booking_date']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    meal = Meal.query.get(data['meal_id'])
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    # Check if already booked
    existing = Booking.query.filter_by(
        user_id=user_id,
        meal_id=data['meal_id'],
        booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    ).first()
    
    if existing:
        return jsonify({'error': 'Meal already booked'}), 409
    
    booking = Booking(
        user_id=user_id,
        meal_id=data['meal_id'],
        booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d').date(),
        confirmed=data.get('confirmed', False)
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Meal booked successfully',
        'booking': booking.to_dict()
    }), 201

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get booking details"""
    user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.user_id != user_id:
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(booking.to_dict()), 200

@booking_bp.route('/user/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """Get user's bookings"""
    user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'bookings': [b.to_dict() for b in bookings]
    }), 200

@booking_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """Update booking"""
    user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.user_id != user_id:
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if 'status' in data:
        booking.status = data['status']
    if 'confirmed' in data:
        booking.confirmed = data['confirmed']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Booking updated',
        'booking': booking.to_dict()
    }), 200

@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel booking"""
    user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.user_id != user_id:
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
    
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled'}), 200

@booking_bp.route('/confirm/<int:booking_id>', methods=['PUT'])
@jwt_required()
def confirm_eating(booking_id):
    """Mark as 'I will eat today' confirmation"""
    user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking or booking.user_id != user_id:
        return jsonify({'error': 'Booking not found'}), 404
    
    booking.confirmed = True
    db.session.commit()
    
    return jsonify({
        'message': 'Meal confirmed',
        'booking': booking.to_dict()
    }), 200
