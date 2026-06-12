import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smart-food-secret-key-2024'
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/smartfood.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'smart-food-jwt-secret-2024'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # CORS
    CORS_ORIGINS = ['http://localhost:8000', 'http://localhost:3000', 'http://127.0.0.1:8000']
    
    # Pricing
    PRICES = {
        'breakfast': 40,
        'lunch': 70,
        'dinner': 70
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
