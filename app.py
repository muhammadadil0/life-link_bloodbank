"""
LifeLink Blood Bank Management System - Main Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf.csrf import CSRFProtect
import os
from config import get_config
from routes import init_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Donor, Patient
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)

# Load configuration
config = get_config(None) # Changed to None as per new_code
app.config.from_object(config)

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

# Initialize routes
init_app(app)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# Context processors
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session and 'user_type' in session:
        if session['user_type'] == 'donor':
            user = Donor.query.get(session['user_id'])
        elif session['user_type'] == 'patient':
            user = Patient.query.get(session['user_id'])
    return dict(current_user=user)

@app.context_processor
def inject_config():
    """Inject configuration into all templates"""
    return dict(
        app_name=app.config.get('APP_NAME', 'LifeLink Blood Bank'),
        app_version=app.config.get('APP_VERSION', '1.0.0')
    )

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)

@socketio.on('send_message')
def handle_send_message(data):
    from models import ChatMessage, db, Donor, Patient
    sender_id = data['sender_id']
    sender_type = data['sender_type']
    receiver_id = data['receiver_id']
    receiver_type = data['receiver_type']
    message = data['message']
    room = data['room']
    print(f"[DEBUG] handle_send_message: sender_id={sender_id}, sender_type={sender_type}, receiver_id={receiver_id}, receiver_type={receiver_type}, message={message}, room={room}")
    chat = ChatMessage(sender_id=sender_id, sender_type=sender_type, receiver_id=receiver_id, receiver_type=receiver_type, message=message)
    db.session.add(chat)
    db.session.commit()
    # Get sender and receiver names
    sender_name = None
    receiver_name = None
    if sender_type == 'donor':
        sender = Donor.query.get(sender_id)
        sender_name = sender.name if sender else 'Donor'
    elif sender_type == 'patient':
        sender = Patient.query.get(sender_id)
        sender_name = sender.name if sender else 'Patient'
    if receiver_type == 'donor':
        receiver = Donor.query.get(receiver_id)
        receiver_name = receiver.name if receiver else 'Donor'
    elif receiver_type == 'patient':
        receiver = Patient.query.get(receiver_id)
        receiver_name = receiver.name if receiver else 'Patient'
    emit('receive_message', {
        'sender_id': sender_id,
        'sender_type': sender_type,
        'sender_name': sender_name,
        'receiver_id': receiver_id,
        'receiver_type': receiver_type,
        'receiver_name': receiver_name,
        'message': message,
        'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M')
    }, room=room)

# Create the application instance
# app = create_app() # This line is removed as per new_code

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True) 