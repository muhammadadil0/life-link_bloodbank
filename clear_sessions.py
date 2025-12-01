"""
Clear all Flask sessions
"""

from app import app
import os

with app.app_context():
    # Get the session directory
    session_dir = app.config.get('SESSION_FILE_DIR', '/tmp/flask_session')
    
    if os.path.exists(session_dir):
        for file in os.listdir(session_dir):
            file_path = os.path.join(session_dir, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        print("✅ All sessions cleared")
    else:
        print("No session directory found")

if __name__ == '__main__':
    print("Clearing Flask sessions...")
