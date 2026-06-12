from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, WasteData, Booking, Payment
from datetime import datetime, date, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to check admin access"""
    from functools import wraps
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/waste', methods=['POST'])
@admin_required
def add_waste_entry():
    """Add food waste entry"""
    data = request.get_json()
    
    if not all(k in data for k in ['waste_date', 'waste_kg']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    waste_entry = WasteData(
        waste_date=datetime.strptime(data['waste_date'], '%Y-%m-%d').date(),
        waste_kg=data['waste_kg'],
        notes=data.get('notes', '')
    )
    
    db.session.add(waste_entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Waste entry added',
        'entry': waste_entry.to_dict()
    }), 201

@admin_bp.route('/waste', methods=['GET'])
@admin_required
def get_waste_data():
    """Get waste data"""
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    
    waste_data = WasteData.query.filter(
        WasteData.waste_date >= start_date,
        WasteData.waste_date <= end_date
    ).all()
    
    total_waste = sum(w.waste_kg for w in waste_data)
    
    return jsonify({
        'start_date': start_date,
        'end_date': end_date,
        'total_waste_kg': total_waste,
        'entries': len(waste_data),
        'waste_data': [w.to_dict() for w in waste_data]
    }), 200

@admin_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get analytics dashboard data"""
    # Total users
    total_users = User.query.count()
    student_count = User.query.filter_by(role='student').count()
    guest_count = User.query.filter_by(role='guest').count()
    
    # Total bookings
    total_bookings = Booking.query.count()
    confirmed_bookings = Booking.query.filter_by(confirmed=True).count()
    cancelled_bookings = Booking.query.filter_by(status='cancelled').count()
    
    # Total payments
    total_payments = Payment.query.count()
    completed_payments = Payment.query.filter_by(status='completed').count()
    total_revenue = sum(p.amount for p in Payment.query.all())
    
    # Last 7 days bookings
    last_week = date.today() - timedelta(days=7)
    week_bookings = Booking.query.filter(Booking.booking_date >= last_week).count()
    
    # Waste tracking
    waste_entries = WasteData.query.filter(WasteData.waste_date >= last_week).all()
    total_waste = sum(w.waste_kg for w in waste_entries)
    
    return jsonify({
        'users': {
            'total': total_users,
            'students': student_count,
            'guests': guest_count
        },
        'bookings': {
            'total': total_bookings,
            'confirmed': confirmed_bookings,
            'cancelled': cancelled_bookings,
            'last_week': week_bookings
        },
        'payments': {
            'total': total_payments,
            'completed': completed_payments,
            'total_revenue': total_revenue
        },
        'waste': {
            'last_week_total_kg': total_waste,
            'entries': len(waste_entries)
        }
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users"""
    users = User.query.all()
    return jsonify({
        'total': len(users),
        'users': [u.to_dict() for u in users]
    }), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user (Admin only)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted'}), 200

@admin_bp.route('/daily-report', methods=['GET'])
def get_daily_report():
    """Get daily report"""
    report_date = request.args.get('date', date.today().isoformat())
    report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
    
    # Bookings for the day
    day_bookings = Booking.query.filter_by(booking_date=report_date).all()
    confirmed = sum(1 for b in day_bookings if b.confirmed)
    
    # Payments for the day
    day_payments = Payment.query.filter(
        db.func.date(Payment.created_at) == report_date
    ).all()
    total_collected = sum(p.amount for p in day_payments)
    
    # Waste for the day
    waste = WasteData.query.filter_by(waste_date=report_date).first()
    waste_kg = waste.waste_kg if waste else 0
    
    return jsonify({
        'date': report_date.isoformat(),
        'bookings': {
            'total': len(day_bookings),
            'confirmed': confirmed
        },
        'payments': {
            'total': len(day_payments),
            'total_collected': total_collected
        },
        'waste_kg': waste_kg
    }), 200
