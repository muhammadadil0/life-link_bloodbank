"""
Script to update old emergency requests with patient_id
This links emergency requests to patients by matching names
"""

from app import app, db
from models import EmergencyRequest, Patient

def update_requests():
    with app.app_context():
        # Find all requests without patient_id
        requests = EmergencyRequest.query.filter_by(patient_id=None).all()
        updated_count = 0
        
        print(f"Found {len(requests)} requests without patient_id")
        
        for req in requests:
            # Try to find matching patient by name
            patient = Patient.query.filter_by(name=req.patient_name).first()
            if patient:
                req.patient_id = patient.id
                updated_count += 1
                print(f"✓ Linked request '{req.patient_name}' to patient ID {patient.id}")
            else:
                print(f"✗ No patient found for request '{req.patient_name}'")
        
        # Save all changes
        db.session.commit()
        print(f"\n✅ Updated {updated_count} out of {len(requests)} requests")

if __name__ == '__main__':
    update_requests()
