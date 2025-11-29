"""
Routes package for LifeLink Blood Bank Management System
"""

from flask import Blueprint

# Import route modules
from .auth import auth_bp
from .main import main_bp
from .dashboard import dashboard_bp
from .emergency import emergency_bp
from .api import api_bp

# Register blueprints
def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(emergency_bp)
    app.register_blueprint(api_bp) 