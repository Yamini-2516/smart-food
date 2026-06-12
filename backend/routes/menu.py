from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Meal, User
from datetime import datetime, date

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu():
    """Get today's menu"""
    today = date.today()
    meals = Meal.query.filter_by(date=today, is_available=True).all()
    
    # Group by meal type
    menu = {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    }
    
    for meal in meals:
        menu[meal.meal_type].append(meal.to_dict())
    
    return jsonify({
        'date': today.isoformat(),
        'menu': menu
    }), 200

@menu_bp.route('/<int:meal_id>', methods=['GET'])
def get_meal_details(meal_id):
    """Get meal details"""
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    return jsonify(meal.to_dict()), 200

@menu_bp.route('/', methods=['POST'])
@jwt_required()
def add_meal():
    """Add meal (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    
    if not all(k in data for k in ['name', 'meal_type', 'price']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    meal = Meal(
        name=data['name'],
        meal_type=data['meal_type'],
        price=data['price'],
        description=data.get('description', ''),
        date=datetime.strptime(data.get('date', str(date.today())), '%Y-%m-%d').date()
    )
    
    db.session.add(meal)
    db.session.commit()
    
    return jsonify({
        'message': 'Meal added successfully',
        'meal': meal.to_dict()
    }), 201

@menu_bp.route('/<int:meal_id>', methods=['PUT'])
@jwt_required()
def update_meal(meal_id):
    """Update meal (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        meal.name = data['name']
    if 'price' in data:
        meal.price = data['price']
    if 'description' in data:
        meal.description = data['description']
    if 'is_available' in data:
        meal.is_available = data['is_available']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Meal updated',
        'meal': meal.to_dict()
    }), 200

@menu_bp.route('/<int:meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    """Delete meal (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    db.session.delete(meal)
    db.session.commit()
    
    return jsonify({'message': 'Meal deleted'}), 200

@menu_bp.route('/weekly', methods=['GET'])
def get_weekly_menu():
    """Get weekly menu"""
    from datetime import timedelta
    
    start_date = date.today()
    end_date = start_date + timedelta(days=7)
    
    meals = Meal.query.filter(
        Meal.date >= start_date,
        Meal.date <= end_date,
        Meal.is_available == True
    ).all()
    
    weekly_menu = {}
    for meal in meals:
        date_str = meal.date.isoformat()
        if date_str not in weekly_menu:
            weekly_menu[date_str] = {'breakfast': [], 'lunch': [], 'dinner': []}
        weekly_menu[date_str][meal.meal_type].append(meal.to_dict())
    
    return jsonify({
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'menu': weekly_menu
    }), 200
