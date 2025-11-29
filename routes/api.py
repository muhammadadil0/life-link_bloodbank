"""
API routes for LifeLink Blood Bank Management System
"""

from flask import Blueprint, jsonify, request, session
from functools import wraps
from flask import request, jsonify
from models import ChatMessage
from flask_login import login_required
from models import Donor

api_bp = Blueprint('api', __name__)

# Authentication decorator for API endpoints
def require_auth(f):
    """Decorator to require authentication for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/api/donors')
def get_donors():
    """Get all donors"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({
        'success': True,
        'donors': [],
        'count': 0
    })

@api_bp.route('/api/donors/<int:donor_id>')
def get_donor(donor_id):
    """Get specific donor by ID"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({'error': 'Donor not found'}), 404
    
    return jsonify({
        'success': True,
        'donor': {}
    })

@api_bp.route('/api/donors', methods=['POST'])
def create_donor():
    """Create new donor"""
    data = request.get_json()
    
    required_fields = ['name', 'email', 'phone', 'blood_type', 'age', 'city']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
        return jsonify({
            'success': True,
            'message': 'Donor created successfully',
            'donor': {}
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/api/emergency')
def get_emergency_requests():
    """Get all emergency requests"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({
        'success': True,
        'emergencies': [],
        'count': 0
    })

@api_bp.route('/api/emergency/<int:request_id>')
def get_emergency_request(request_id):
    """Get specific emergency request by ID"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({'error': 'Emergency request not found'}), 404
    
    return jsonify({
        'success': True,
        'emergency': {}
    })

@api_bp.route('/api/emergency', methods=['POST'])
def create_emergency_request():
    """Create new emergency request"""
    data = request.get_json()
    
    required_fields = ['patient_name', 'blood_type', 'units_needed', 'urgency', 'hospital', 'contact']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
        return jsonify({
            'success': True,
            'message': 'Emergency request created successfully',
            'emergency': {}
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/api/stats')
def get_stats():
    """Get system statistics"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({
        'success': True,
        'stats': {
            'total_donors': 0,
            'active_donors': 0,
            'total_emergencies': 0,
            'active_emergencies': 0,
            'fulfilled_emergencies': 0,
            'lives_saved': 0,  # Mock calculation
            'cities_covered': 0  # Mock data
        }
    })

@api_bp.route('/api/blood-types')
def get_blood_types():
    """Get available blood types"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({
        'success': True,
        'blood_types': []
    })

@api_bp.route('/api/urgency-levels')
def get_urgency_levels():
    """Get available urgency levels"""
    # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
    return jsonify({
        'success': True,
        'urgency_levels': []
    })

@api_bp.route('/api/search/donors')
def search_donors():
    query = request.args.get('q', '').strip().lower()
    blood_type = request.args.get('blood_type', '').strip()
    city = request.args.get('city', '').strip().lower()
    availability = request.args.get('availability', '').strip().lower()

    print(f"[DEBUG] Donor search: q='{query}', blood_type='{blood_type}', city='{city}', availability='{availability}'")

    donors_query = Donor.query
    if query:
        donors_query = donors_query.filter(Donor.name.ilike(f'%{query}%'))
    if blood_type:
        donors_query = donors_query.filter(Donor.blood_type == blood_type)
    if city:
        donors_query = donors_query.filter(Donor.address.ilike(f'%{city}%'))
    if availability == 'available':
        donors_query = donors_query.filter(Donor.is_available == True)
    elif availability == 'unavailable':
        donors_query = donors_query.filter(Donor.is_available == False)

    donors = donors_query.all()
    print(f"[DEBUG] Donor search results: {len(donors)} donors found")
    donor_list = [
        {
            'id': getattr(d, 'id', None),
            'name': getattr(d, 'name', ''),
            'email': getattr(d, 'email', ''),
            'phone': getattr(d, 'phone', ''),
            'age': getattr(d, 'age', ''),
            'blood_type': getattr(d, 'blood_type', ''),
            'address': getattr(d, 'address', ''),
            'is_available': getattr(d, 'is_available', False)
        } for d in donors
    ]
    return jsonify({'success': True, 'donors': donor_list, 'count': len(donor_list)})

@api_bp.route('/api/user/profile', methods=['GET', 'PUT'])
@require_auth
def user_profile():
    """Get or update user profile"""
    user_id = session.get('user_id')
    
    if request.method == 'GET':
        # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
        return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {}
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        # TODO: Replace all mock_db, BloodType, and EmergencyUrgency usage with real database queries
        return jsonify({'error': 'User not found'}), 404
        
        # Update user data (mock implementation)
        for key, value in data.items():
            if key in user:
                user[key] = value
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {}
        })

@api_bp.route('/api/notifications')
@require_auth
def get_notifications():
    """Get user notifications"""
    user_id = session.get('user_id')
    
    # Mock notifications
    return jsonify({
        'success': True,
        'notifications': [],
        'unread_count': 0
    }) 

@api_bp.route('/chat/history')
def chat_history():
    user1 = int(request.args.get('user1'))
    user2 = int(request.args.get('user2'))
    type1 = request.args.get('type1')
    type2 = request.args.get('type2')
    messages = ChatMessage.query.filter(
        (((ChatMessage.sender_id==user1) & (ChatMessage.sender_type==type1) & (ChatMessage.receiver_id==user2) & (ChatMessage.receiver_type==type2)) |
         ((ChatMessage.sender_id==user2) & (ChatMessage.sender_type==type2) & (ChatMessage.receiver_id==user1) & (ChatMessage.receiver_type==type1)))
    ).order_by(ChatMessage.timestamp).all()
    return jsonify([
        {
            'sender_id': m.sender_id,
            'sender_type': m.sender_type,
            'receiver_id': m.receiver_id,
            'receiver_type': m.receiver_type,
            'message': m.message,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M')
        } for m in messages
    ]) 