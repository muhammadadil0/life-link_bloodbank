"""
Forms for LifeLink Blood Bank Management System
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, SelectField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo, ValidationError

class LoginForm(FlaskForm):
    """Login form"""
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    """User registration form"""
    user_type = SelectField('User Type', choices=[
        ('donor', 'Blood Donor'),
        ('patient', 'Patient/Family')
    ], validators=[DataRequired()])
    
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    phone = StringField('Phone Number', validators=[
        DataRequired(message='Phone number is required'),
        Length(min=10, max=15, message='Phone number must be between 10 and 15 characters')
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(message='Age is required'),
        NumberRange(min=18, max=65, message='Age must be between 18 and 65')
    ])
    
    blood_group = SelectField('Blood Group', choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], validators=[DataRequired()])
    
    city = StringField('City', validators=[
        DataRequired(message='City is required'),
        Length(min=2, max=50, message='City must be between 2 and 50 characters')
    ])
    
    address = TextAreaField('Address', validators=[
        Optional(),
        Length(max=200, message='Address must be less than 200 characters')
    ])
    
    emergency_contact = StringField('Emergency Contact', validators=[
        Optional(),
        Length(max=100, message='Emergency contact must be less than 100 characters')
    ])
    
    medical_conditions = TextAreaField('Medical Conditions (Optional)', validators=[
        Optional(),
        Length(max=500, message='Medical conditions must be less than 500 characters')
    ])
    
    agree_to_terms = BooleanField('I agree to the Terms and Conditions', validators=[
        DataRequired(message='You must agree to the terms and conditions')
    ])
    
    agree_to_privacy = BooleanField('I agree to the Privacy Policy', validators=[
        DataRequired(message='You must agree to the privacy policy')
    ])

class EmergencyRequestForm(FlaskForm):
    """Emergency blood request form"""
    patient_name = StringField('Patient Name', validators=[
        DataRequired(message='Patient name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    blood_type = SelectField('Blood Type Needed', choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], validators=[DataRequired()])
    
    units_needed = IntegerField('Units Needed', validators=[
        DataRequired(message='Number of units is required'),
        NumberRange(min=1, max=10, message='Units must be between 1 and 10')
    ])
    
    urgency = SelectField('Urgency Level', choices=[
        ('Critical', 'Critical - Immediate need'),
        ('Urgent', 'Urgent - Within 2 hours'),
        ('Normal', 'Normal - Within 24 hours')
    ], validators=[DataRequired()])
    
    hospital = StringField('Hospital/Medical Center', validators=[
        DataRequired(message='Hospital name is required'),
        Length(min=2, max=100, message='Hospital name must be between 2 and 100 characters')
    ])
    
    contact = StringField('Contact Number', validators=[
        DataRequired(message='Contact number is required'),
        Length(min=10, max=15, message='Contact number must be between 10 and 15 characters')
    ])
    
    city = StringField('City', validators=[
        DataRequired(message='City is required'),
        Length(min=2, max=50, message='City must be between 2 and 50 characters')
    ])
    
    additional_info = TextAreaField('Additional Information (Optional)', validators=[
        Optional(),
        Length(max=500, message='Additional information must be less than 500 characters')
    ])

class DonorProfileForm(FlaskForm):
    """Donor profile update form"""
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    phone = StringField('Phone Number', validators=[
        DataRequired(message='Phone number is required'),
        Length(min=10, max=15, message='Phone number must be between 10 and 15 characters')
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(message='Age is required'),
        NumberRange(min=18, max=65, message='Age must be between 18 and 65')
    ])
    
    blood_group = SelectField('Blood Group', choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], validators=[DataRequired()])
    
    city = StringField('City', validators=[
        DataRequired(message='City is required'),
        Length(min=2, max=50, message='City must be between 2 and 50 characters')
    ])
    
    address = TextAreaField('Address', validators=[
        Optional(),
        Length(max=200, message='Address must be less than 200 characters')
    ])
    
    emergency_contact = StringField('Emergency Contact', validators=[
        Optional(),
        Length(max=100, message='Emergency contact must be less than 100 characters')
    ])
    
    medical_conditions = TextAreaField('Medical Conditions (Optional)', validators=[
        Optional(),
        Length(max=500, message='Medical conditions must be less than 500 characters')
    ])
    
    is_available = BooleanField('Available for Donation')

class PasswordChangeForm(FlaskForm):
    """Password change form"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ])
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords must match')
    ])

class ForgotPasswordForm(FlaskForm):
    """Forgot password form"""
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])

class ResetPasswordForm(FlaskForm):
    """Reset password form"""
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords must match')
    ])

class SearchForm(FlaskForm):
    """Search form for donors"""
    query = StringField('Search', validators=[
        Optional(),
        Length(max=100, message='Search query must be less than 100 characters')
    ])
    
    blood_type = SelectField('Blood Type', choices=[
        ('', 'All Blood Types'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ])
    
    city = StringField('City', validators=[
        Optional(),
        Length(max=50, message='City must be less than 50 characters')
    ])
    
    availability = SelectField('Availability', choices=[
        ('', 'All'),
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ])

class ContactForm(FlaskForm):
    """Contact form"""
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    subject = StringField('Subject', validators=[
        DataRequired(message='Subject is required'),
        Length(min=2, max=100, message='Subject must be between 2 and 100 characters')
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=1000, message='Message must be between 10 and 1000 characters')
    ])

class FeedbackForm(FlaskForm):
    """Feedback/contact form"""
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    subject = StringField('Subject', validators=[
        DataRequired(message='Subject is required'),
        Length(min=2, max=100, message='Subject must be between 2 and 100 characters')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=1000, message='Message must be between 10 and 1000 characters')
    ])

# Custom validators
# Remove or comment out any code that uses BloodType, EmergencyUrgency, or UserType
# def validate_blood_type(form, field):
#     valid_blood_types = [bt.value for bt in BloodType]
#     if field.data not in valid_blood_types:
#         raise ValidationError('Invalid blood type.')
#
# def validate_urgency_level(form, field):
#     valid_urgency_levels = [ul.value for ul in EmergencyUrgency]
#     if field.data not in valid_urgency_levels:
#         raise ValidationError('Invalid urgency level.')
#
# def validate_user_type(form, field):
#     valid_user_types = [ut.value for ut in UserType]
#     if field.data not in valid_user_types:
#         raise ValidationError('Invalid user type.') 