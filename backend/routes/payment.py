from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Payment, Booking, User, Meal
from datetime import datetime
import uuid

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/', methods=['POST'])
@jwt_required()
def process_payment():
    """Process payment for booking"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['booking_id', 'amount', 'payment_method']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    booking = Booking.query.get(data['booking_id'])
    
    if not booking or booking.user_id != user_id:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check if payment already exists
    existing_payment = Payment.query.filter_by(booking_id=data['booking_id']).first()
    if existing_payment:
        return jsonify({'error': 'Payment already processed'}), 409
    
    # Create payment record
    payment = Payment(
        user_id=user_id,
        booking_id=data['booking_id'],
        amount=data['amount'],
        payment_method=data['payment_method'],
        transaction_id=str(uuid.uuid4()),
        status='completed'  # In production, integrate with payment gateway
    )
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify({
        'message': 'Payment successful',
        'payment': payment.to_dict()
    }), 201

@payment_bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    """Get payment details"""
    user_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.user_id != user_id:
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(payment.to_dict()), 200

@payment_bp.route('/receipt/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_receipt(payment_id):
    """Get receipt after payment"""
    user_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.user_id != user_id:
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
    
    booking = Booking.query.get(payment.booking_id)
    meal = Meal.query.get(booking.meal_id)
    user = User.query.get(payment.user_id)
    
    receipt = {
        'receipt_id': f'RCP-{payment.id:05d}',
        'transaction_id': payment.transaction_id,
        'date': payment.created_at.isoformat(),
        'user': {
            'name': user.name,
            'email': user.email
        },
        'meal': {
            'name': meal.name,
            'type': meal.meal_type,
            'price': meal.price
        },
        'booking_date': booking.booking_date.isoformat(),
        'amount': payment.amount,
        'payment_method': payment.payment_method,
        'status': payment.status
    }
    
    return jsonify(receipt), 200

@payment_bp.route('/user/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """Get user's payment history"""
    user_id = get_jwt_identity()
    payments = Payment.query.filter_by(user_id=user_id).all()
    
    history = []
    for payment in payments:
        booking = Booking.query.get(payment.booking_id)
        meal = Meal.query.get(booking.meal_id)
        history.append({
            'payment_id': payment.id,
            'meal_name': meal.name,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'status': payment.status,
            'date': payment.created_at.isoformat()
        })
    
    return jsonify({'payments': history}), 200
