from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db, User, Meal, Booking, Payment, Feedback, WasteData
from datetime import datetime, timedelta
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app_env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[app_env])

# Initialize extensions
db.init_app(app)
JWTManager(app)
CORS(app, origins=app.config['CORS_ORIGINS'])

# Register blueprints
from routes.auth import auth_bp
from routes.menu import menu_bp
from routes.booking import booking_bp
from routes.payment import payment_bp
from routes.feedback import feedback_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(menu_bp, url_prefix='/api/menu')
app.register_blueprint(booking_bp, url_prefix='/api/booking')
app.register_blueprint(payment_bp, url_prefix='/api/payment')
app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

# Initialize database
@app.before_request
def create_tables():
    db.create_all()

# Add sample data on first run
@app.before_request
def init_sample_data():
    if Meal.query.first() is None:
        # Add sample meals
        meals = [
            Meal(name='Breakfast Special - Idli & Sambar', meal_type='breakfast', price=40, description='South Indian special'),
            Meal(name='Breakfast - Poha & Tea', meal_type='breakfast', price=40, description='Light breakfast'),
            Meal(name='Lunch - Paneer Butter Masala', meal_type='lunch', price=70, description='Creamy paneer curry'),
            Meal(name='Lunch - Dal Makhani & Rice', meal_type='lunch', price=70, description='Lentil preparation'),
            Meal(name='Dinner - Chicken Tikka Masala', meal_type='dinner', price=70, description='Spiced chicken curry'),
            Meal(name='Dinner - Vegetable Biryani', meal_type='dinner', price=70, description='Fragrant rice dish'),
        ]
        for meal in meals:
            db.session.add(meal)
        
        # Add sample users
        users = [
            User(name='Student One', email='student@example.com', role='student'),
            User(name='Guest User', email='guest@example.com', role='guest'),
            User(name='Admin User', email='admin@example.com', role='admin'),
        ]
        for user in users:
            user.set_password('password123')
            db.session.add(user)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
