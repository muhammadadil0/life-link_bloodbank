"""
Check what type a user is in the database
"""

from app import app, db
from models import Donor, Patient

def check_user(email):
    with app.app_context():
        # Check if user is a donor
        donor = Donor.query.filter_by(email=email).first()
        if donor:
            print(f"✓ Found as DONOR:")
            print(f"  Name: {donor.name}")
            print(f"  Email: {donor.email}")
            print(f"  Blood Type: {donor.blood_type}")
            return
        
        # Check if user is a patient
        patient = Patient.query.filter_by(email=email).first()
        if patient:
            print(f"✓ Found as PATIENT:")
            print(f"  Name: {patient.name}")
            print(f"  Email: {patient.email}")
            print(f"  Blood Type: {patient.blood_type}")
            return
        
        print(f"✗ User with email '{email}' not found")

if __name__ == '__main__':
    email = input("Enter email to check: ")
    check_user(email)
