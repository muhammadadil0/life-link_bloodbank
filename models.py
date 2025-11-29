"""
Database models for the LifeLink Blood Bank Management System
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    medical_conditions = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    medical_conditions = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(255), nullable=True)

class EmergencyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    units_needed = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.String(20), nullable=False)
    hospital = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # 'donor' or 'patient'
    receiver_id = db.Column(db.Integer, nullable=False)
    receiver_type = db.Column(db.String(20), nullable=False)  # 'donor' or 'patient'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 