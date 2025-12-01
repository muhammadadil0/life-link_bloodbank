"""
Dashboard routes for LifeLink Blood Bank Management System
"""

from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from models import Donor, EmergencyRequest, Patient

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/donor')
def donor_dashboard():
    """Donor dashboard route"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if session.get('user_type') != 'donor':
        flash('Access denied: Donor dashboard is for donors only.', 'error')
        return redirect(url_for('dashboard.patient_landing'))
    donor = Donor.query.get(session['user_id'])
    if not donor:
        flash('Donor not found.', 'error')
        return redirect(url_for('auth.login'))
    emergency_requests = EmergencyRequest.query.order_by(EmergencyRequest.created_at.desc()).all()
    return render_template('dashboard/donor.html', donor_data=donor, emergency_requests=emergency_requests)

@dashboard_bp.route('/dashboard/admin')
def admin_dashboard():
    """Admin dashboard route"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Mock admin access for testing - allow any logged in user to access admin dashboard
    # In production, this should check for actual admin privileges
    
    # Mock admin data for testing
    admin_stats = {
        'total_donors': 1250,
        'active_donors': 847,
        'total_emergencies': 156,
        'fulfilled_emergencies': 142,
        'pending_emergencies': 14,
        'total_donations': 3247,
        'lives_saved': 2847,
        'response_time_avg': '2.3 min',
        'success_rate': '98.7%'
    }
    
    recent_emergencies = [
        {
            'id': 1,
            'patient_name': 'Sarah Johnson',
            'blood_type': 'O+',
            'urgency': 'Critical',
            'hospital': 'City General Hospital',
            'status': 'Active',
            'created_at': '2 hours ago'
        },
        {
            'id': 2,
            'patient_name': 'Michael Chen',
            'blood_type': 'A+',
            'urgency': 'Urgent',
            'hospital': 'St. Mary\'s Medical Center',
            'status': 'Fulfilled',
            'created_at': '4 hours ago'
        },
        {
            'id': 3,
            'patient_name': 'Omar Abdullah',
            'blood_type': 'B+',
            'urgency': 'Normal',
            'hospital': 'Memorial Hospital',
            'status': 'Active',
            'created_at': '6 hours ago'
        }
    ]
    
    recent_donors = [
        {
            'id': 1,
            'name': 'John Smith',
            'blood_type': 'O+',
            'city': 'New York',
            'total_donations': 12,
            'last_donation': '2 weeks ago',
            'status': 'Available'
        },
        {
            'id': 2,
            'name': 'Fatima Ali',
            'blood_type': 'A+',
            'city': 'Los Angeles',
            'total_donations': 8,
            'last_donation': '1 month ago',
            'status': 'Available'
        },
        {
            'id': 3,
            'name': 'Ahmed Hassan',
            'blood_type': 'B+',
            'city': 'Chicago',
            'total_donations': 15,
            'last_donation': '3 weeks ago',
            'status': 'Unavailable'
        }
    ]
    
    return render_template('dashboard/admin.html', 
                         admin_stats=admin_stats,
                         recent_emergencies=recent_emergencies,
                         recent_donors=recent_donors)

@dashboard_bp.route('/dashboard/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # TODO: Replace all mock_db and BloodType usage with real database queries
    # Get user data from mock database
    # user_data = mock_db.get_donor_by_id(session.get('user_id', 1))
    return render_template('dashboard/profile.html', user={}) # TODO: Replace with real data

@dashboard_bp.route('/dashboard/settings')
def settings():
    """User settings page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard/settings.html')

@dashboard_bp.route('/dashboard/history')
def donation_history():
    """Donation history page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # TODO: Replace all mock_db and BloodType usage with real database queries
    # Get donation history from mock database
    # donations = mock_db.donations
    return render_template('dashboard/history.html', donations=[]) # TODO: Replace with real data

@dashboard_bp.route('/dashboard/patient')
def patient_landing():
    """Patient landing page route (new design)"""
    # Debug logging
    print(f"DEBUG: Session data: user_id={session.get('user_id')}, user_type={session.get('user_type')}")
    
    if 'user_id' not in session:
        print("DEBUG: No user_id in session, redirecting to login")
        return redirect(url_for('auth.login'))
    
    if session.get('user_type') != 'patient':
        print(f"DEBUG: User type is '{session.get('user_type')}', not 'patient'. Redirecting to donor dashboard")
        flash('Access denied: Patient dashboard is for patients only.', 'error')
        return redirect(url_for('dashboard.donor_dashboard'))
    
    print("DEBUG: User is patient, loading patient dashboard")
    from models import Donor
    active_donors = Donor.query.filter_by(is_available=True).all()
    active_donor_count = Donor.query.filter_by(is_available=True).count()
    return render_template('dashboard/patient_landing.html', donors=active_donors, active_donor_count=active_donor_count) 