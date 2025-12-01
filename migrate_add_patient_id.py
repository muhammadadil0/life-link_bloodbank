"""
Migration script to add patient_id column to emergency_request table
Run this once to update your existing database
"""

from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Add patient_id column to emergency_request table
            with db.engine.connect() as conn:
                # Check if column already exists
                result = conn.execute(text("PRAGMA table_info(emergency_request)"))
                columns = [row[1] for row in result]
                
                if 'patient_id' not in columns:
                    print("Adding patient_id column to emergency_request table...")
                    conn.execute(text("ALTER TABLE emergency_request ADD COLUMN patient_id INTEGER"))
                    conn.commit()
                    print("✅ Migration completed successfully!")
                else:
                    print("✅ patient_id column already exists. No migration needed.")
        except Exception as e:
            print(f"❌ Migration failed: {e}")

if __name__ == '__main__':
    migrate()
