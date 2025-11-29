"""
Configuration settings for LifeLink Blood Bank Management System
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database settings
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'lifelink.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email settings (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Application settings
    APP_NAME = 'LifeLink Blood Bank Management System'
    APP_VERSION = '1.0.0'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Pagination settings
    ITEMS_PER_PAGE = 20
    
    # File upload settings
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # API settings
    API_RATE_LIMIT = '100 per minute'
    
    # Emergency settings
    EMERGENCY_RESPONSE_TIME_LIMIT = 300  # 5 minutes in seconds
    MAX_EMERGENCY_REQUESTS_PER_USER = 5  # per day
    
    # Donation settings
    MIN_DONATION_INTERVAL_DAYS = 56  # 8 weeks
    MAX_DONATION_AGE = 65
    MIN_DONATION_AGE = 18
    
    # Notification settings
    ENABLE_EMAIL_NOTIFICATIONS = True
    ENABLE_SMS_NOTIFICATIONS = False  # Requires SMS service integration
    
    # Blood type compatibility (for matching)
    BLOOD_COMPATIBILITY = {
        'O-': ['O-', 'O+', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB+', 'AB-'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB+', 'AB-'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB+', 'AB-'],
        'AB+': ['AB+']
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for development
    
    # Mock data settings
    USE_MOCK_DATA = True
    
    # Logging settings
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Use SQLite for development as well
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'instance', 'lifelink.sqlite3')

class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Email settings
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Logging settings
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    def __init__(self):
        """Validate required environment variables"""
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for production environment")
        if not self.DATABASE_URL:
            raise ValueError("No DATABASE_URL set for production environment")

class TestingConfig(Config):
    """Testing configuration"""
    
    DEBUG = True
    TESTING = True
    
    # Testing-specific settings
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Mock data settings
    USE_MOCK_DATA = True
    
    # Logging settings
    LOG_LEVEL = 'DEBUG'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration class by name"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default']) 