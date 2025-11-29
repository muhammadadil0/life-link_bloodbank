"""
Utility functions for LifeLink Blood Bank Management System
"""

import re
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models import BloodType, EmergencyUrgency

def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) >= 10

def validate_blood_type(blood_type: str) -> bool:
    """Validate blood type"""
    valid_types = [bt.value for bt in BloodType]
    return blood_type in valid_types

def validate_urgency_level(urgency: str) -> bool:
    """Validate urgency level"""
    valid_levels = [ul.value for ul in EmergencyUrgency]
    return urgency in valid_levels

def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    today = datetime.now()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

def is_eligible_for_donation(age: int, last_donation_date: Optional[datetime] = None) -> Dict[str, bool]:
    """Check if donor is eligible for donation"""
    min_age = 18
    max_age = 65
    min_interval_days = 56  # 8 weeks
    
    # Check age eligibility
    age_eligible = min_age <= age <= max_age
    
    # Check time since last donation
    time_eligible = True
    if last_donation_date:
        days_since_last = (datetime.now() - last_donation_date).days
        time_eligible = days_since_last >= min_interval_days
    
    return {
        'eligible': age_eligible and time_eligible,
        'age_eligible': age_eligible,
        'time_eligible': time_eligible
    }

def get_next_eligible_date(last_donation_date: datetime) -> datetime:
    """Calculate next eligible donation date"""
    return last_donation_date + timedelta(days=56)

def get_blood_compatibility(blood_type: str) -> List[str]:
    """Get compatible blood types for donation"""
    compatibility_map = {
        'O-': ['O-', 'O+', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB+', 'AB-'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB+', 'AB-'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB+', 'AB-'],
        'AB+': ['AB+']
    }
    return compatibility_map.get(blood_type, [])

def format_time_ago(date: datetime) -> str:
    """Format time difference as human-readable string"""
    now = datetime.now()
    diff = now - date
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    # Remove dangerous characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    return text

def validate_password_strength(password: str) -> Dict[str, bool]:
    """Validate password strength"""
    checks = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }
    checks['strong'] = all(checks.values())
    return checks

def generate_password(length: int = 12) -> str:
    """Generate a secure random password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula"""
    import math
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def format_phone_number(phone: str) -> str:
    """Format phone number for display"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone

def get_urgency_color(urgency: str) -> str:
    """Get CSS color class for urgency level"""
    color_map = {
        'Critical': 'text-red-600 bg-red-100',
        'Urgent': 'text-orange-600 bg-orange-100',
        'Normal': 'text-green-600 bg-green-100'
    }
    return color_map.get(urgency, 'text-gray-600 bg-gray-100')

def get_blood_type_color(blood_type: str) -> str:
    """Get CSS color class for blood type"""
    color_map = {
        'O+': 'text-red-600 bg-red-100',
        'O-': 'text-red-700 bg-red-200',
        'A+': 'text-blue-600 bg-blue-100',
        'A-': 'text-blue-700 bg-blue-200',
        'B+': 'text-green-600 bg-green-100',
        'B-': 'text-green-700 bg-green-200',
        'AB+': 'text-purple-600 bg-purple-100',
        'AB-': 'text-purple-700 bg-purple-200'
    }
    return color_map.get(blood_type, 'text-gray-600 bg-gray-100')

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def is_valid_file_extension(filename: str, allowed_extensions: set) -> bool:
    """Check if file has valid extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename to prevent conflicts"""
    import uuid
    name, ext = original_filename.rsplit('.', 1)
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{unique_id}.{ext}"

def send_email_notification(to_email: str, subject: str, message: str) -> bool:
    """Send email notification (mock implementation)"""
    # In production, implement actual email sending
    print(f"Email to {to_email}: {subject} - {message}")
    return True

def send_sms_notification(phone: str, message: str) -> bool:
    """Send SMS notification (mock implementation)"""
    # In production, implement actual SMS sending
    print(f"SMS to {phone}: {message}")
    return True

def log_activity(user_id: int, action: str, details: str = None) -> None:
    """Log user activity (mock implementation)"""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] User {user_id}: {action}"
    if details:
        log_entry += f" - {details}"
    print(log_entry)  # In production, write to log file or database 