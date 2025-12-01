"""
Emergency routes for LifeLink Blood Bank Management System
"""

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from models import db, EmergencyRequest, Donor

emergency_bp = Blueprint('emergency', __name__, url_prefix='/emergency')

@emergency_bp.route('/')
def emergency_list():
    """Emergency requests listing page"""
    # If user is a patient, show only their requests
    if session.get('user_type') == 'patient' and session.get('user_id'):
        emergency_requests = EmergencyRequest.query.filter_by(patient_id=session['user_id']).order_by(EmergencyRequest.created_at.desc()).all()
    else:
        # For donors and non-logged-in users, show all requests
        emergency_requests = EmergencyRequest.query.order_by(EmergencyRequest.created_at.desc()).all()
    
    total_donors = Donor.query.count()
    active_donors = Donor.query.filter_by(is_available=True).count()
    return render_template('emergency.html', emergency_requests=emergency_requests, total_donors=total_donors, active_donors=active_donors)

@emergency_bp.route('/create', methods=['GET', 'POST'])
def create_emergency():
    """Create new emergency request"""
    # Require login to create emergency request
    if 'user_id' not in session:
        flash('Please login to create an emergency request.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        blood_type = request.form.get('blood_type')
        units_needed = request.form.get('units_needed')
        urgency = request.form.get('urgency')
        hospital = request.form.get('hospital')
        contact = request.form.get('contact')
        city = request.form.get('city')
        if not (patient_name and blood_type and units_needed and urgency and hospital and contact and city):
            flash('Please fill all required fields', 'error')
            return render_template('emergency_create.html')
        
        # Get patient_id if user is logged in as patient
        patient_id = None
        if session.get('user_type') == 'patient' and session.get('user_id'):
            patient_id = session['user_id']
        
        new_request = EmergencyRequest(
            patient_id=patient_id,
            patient_name=patient_name,
            blood_type=blood_type,
            units_needed=int(units_needed),
            urgency=urgency,
            hospital=hospital,
            contact=contact,
            city=city
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Emergency request created successfully!', 'success')
        return redirect(url_for('emergency.emergency_list'))
    return render_template('emergency_create.html')

@emergency_bp.route('/<int:request_id>')
def emergency_detail(request_id):
    """Emergency request detail page"""
    # TODO: Replace all mock_db, EmergencyUrgency, and BloodType usage with real database queries
    emergency_request = {} # Placeholder for emergency request data
    
    if not emergency_request:
        return render_template('404.html'), 404
    
    return render_template('emergency/detail.html', request=emergency_request)

@emergency_bp.route('/<int:request_id>/fulfill', methods=['POST'])
def fulfill_emergency(request_id):
    """Fulfill emergency request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'})
    
    # TODO: Replace all mock_db, EmergencyUrgency, and BloodType usage with real database queries
    emergency_request = {} # Placeholder for emergency request data
    
    if not emergency_request:
        return jsonify({'success': False, 'message': 'Emergency request not found'})
    
    # TODO: Replace all mock_db, EmergencyUrgency, and BloodType usage with real database queries
    emergency_request['is_fulfilled'] = True # Placeholder for fulfillment status
    emergency_request['fulfilled_by'] = session.get('user_id') # Placeholder for fulfilled by user
    
    return jsonify({
        'success': True,
        'message': 'Emergency request fulfilled successfully'
    })

@emergency_bp.route('/api/emergency/active')
def api_active_emergencies():
    """API endpoint for active emergency requests"""
    # TODO: Replace all mock_db, EmergencyUrgency, and BloodType usage with real database queries
    emergency_requests = [] # Placeholder for emergency requests
    return jsonify({
        'success': True,
        'emergencies': emergency_requests,
        'count': len(emergency_requests)
    })

@emergency_bp.route('/api/emergency/stats')
def api_emergency_stats():
    """API endpoint for emergency statistics"""
    # TODO: Replace all mock_db, EmergencyUrgency, and BloodType usage with real database queries
    all_requests = [] # Placeholder for all requests
    active_requests = [] # Placeholder for active requests
    fulfilled_requests = [] # Placeholder for fulfilled requests
    
    stats = {
        'total_requests': len(all_requests),
        'active_requests': len(active_requests),
        'fulfilled_requests': len(fulfilled_requests),
        'response_time_avg': '2.3 min',
        'success_rate': '98.7%'
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    }) 