"""
Authentication routes for LifeLink Blood Bank Management System
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Donor, Patient
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Admin hardcoded login
        if email == 'admin@gmail.com' and password == 'admin':
            session['user_id'] = 'admin'
            session['user_type'] = 'admin'
            session['user_name'] = 'Admin'
            return redirect(url_for('dashboard.admin_dashboard'))
        if not email or not password:
            flash('Please enter both email and password', 'error')
            return render_template('login.html')
        user = Donor.query.filter_by(email=email).first()
        user_type = 'donor'
        if not user:
            user = Patient.query.filter_by(email=email).first()
            user_type = 'patient'
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user_type
            session['user_name'] = user.name
            if user_type == 'donor':
                return redirect(url_for('dashboard.donor_dashboard'))
            else:
                return redirect(url_for('dashboard.patient_landing'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        user_type = request.form.get('userType')
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age = request.form.get('age')
        blood_group = request.form.get('bloodGroup')
        address = request.form.get('address')
        password = request.form.get('password')
        medical_conditions = request.form.get('medicalConditions')
        emergency_contact = request.form.get('emergencyContact')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        # Check required fields
        if not (user_type and full_name and email and phone and age and blood_group and address and password):
            flash('Please fill all required fields', 'error')
            return render_template('register.html')
        if Donor.query.filter_by(email=email).first() or Patient.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        hashed_password = generate_password_hash(password)
        if user_type == 'donor':
            donor = Donor(
                name=full_name,
                email=email,
                phone=phone,
                age=int(age),
                password=hashed_password,
                blood_type=blood_group,
                latitude=float(latitude) if latitude else None,
                longitude=float(longitude) if longitude else None,
                address=address,
                medical_conditions=medical_conditions,
                emergency_contact=emergency_contact
            )
            db.session.add(donor)
        else:
            patient = Patient(
                name=full_name,
                email=email,
                phone=phone,
                age=int(age),
                password=hashed_password,
                blood_type=blood_group,
                address=address,
                medical_conditions=medical_conditions,
                emergency_contact=emergency_contact
            )
            db.session.add(patient)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """User logout route"""
    session.clear()
    return redirect(url_for('main.home'))

@auth_bp.route('/forgot-password')
def forgot_password():
    """Forgot password route"""
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>')
def reset_password(token):
    """Reset password route"""
    return render_template('auth/reset_password.html', token=token) 