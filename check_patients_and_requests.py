"""
Script to check patients and emergency requests
"""

from app import app, db
from models import EmergencyRequest, Patient

def check_data():
    with app.app_context():
        print("\n=== REGISTERED PATIENTS ===")
        patients = Patient.query.all()
        if patients:
            for p in patients:
                print(f"ID: {p.id}, Name: '{p.name}', Email: {p.email}")
        else:
            print("No patients found in database")
        
        print("\n=== EMERGENCY REQUESTS WITHOUT PATIENT_ID ===")
        requests = EmergencyRequest.query.filter_by(patient_id=None).all()
        if requests:
            for r in requests:
                print(f"ID: {r.id}, Patient Name: '{r.patient_name}', Blood: {r.blood_type}, Hospital: {r.hospital}")
        else:
            print("No requests without patient_id")
        
        print("\n=== EMERGENCY REQUESTS WITH PATIENT_ID ===")
        requests_with_id = EmergencyRequest.query.filter(EmergencyRequest.patient_id.isnot(None)).all()
        if requests_with_id:
            for r in requests_with_id:
                print(f"ID: {r.id}, Patient Name: '{r.patient_name}', Linked to Patient ID: {r.patient_id}")
        else:
            print("No requests with patient_id")

if __name__ == '__main__':
    check_data()
