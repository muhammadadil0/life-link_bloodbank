"""
Database initialization and management for LifeLink Blood Bank Management System
"""

import sqlite3
import os
from datetime import datetime
from models import BloodType, EmergencyUrgency, UserType

class DatabaseManager:
    """Database manager for SQLite operations"""
    
    def __init__(self, db_path='blood_bank.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                user_type TEXT NOT NULL,
                blood_type TEXT,
                age INTEGER,
                city TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                is_verified BOOLEAN DEFAULT 0
            )
        ''')
        
        # Create donors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                total_donations INTEGER DEFAULT 0,
                last_donation_date TIMESTAMP,
                next_eligible_date TIMESTAMP,
                is_available BOOLEAN DEFAULT 1,
                emergency_contact TEXT,
                medical_conditions TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create emergency_requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                blood_type TEXT NOT NULL,
                units_needed INTEGER NOT NULL,
                urgency TEXT NOT NULL,
                hospital TEXT NOT NULL,
                contact TEXT NOT NULL,
                city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                is_fulfilled BOOLEAN DEFAULT 0,
                fulfilled_at TIMESTAMP,
                fulfilled_by INTEGER,
                FOREIGN KEY (fulfilled_by) REFERENCES users (id)
            )
        ''')
        
        # Create blood_donations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blood_donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_id INTEGER NOT NULL,
                blood_type TEXT NOT NULL,
                units INTEGER NOT NULL,
                donation_date TIMESTAMP NOT NULL,
                location TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_verified BOOLEAN DEFAULT 0,
                verified_by INTEGER,
                verified_at TIMESTAMP,
                FOREIGN KEY (donor_id) REFERENCES users (id),
                FOREIGN KEY (verified_by) REFERENCES users (id)
            )
        ''')
        
        # Create notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_user(self, user_data):
        """Insert a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, email, phone, user_type, blood_type, age, city, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['name'],
            user_data['email'],
            user_data['phone'],
            user_data['user_type'],
            user_data.get('blood_type'),
            user_data.get('age'),
            user_data.get('city'),
            user_data.get('address')
        ))
        
        user_id = cursor.lastrowid
        
        # If user is a donor, create donor record
        if user_data['user_type'] == 'donor':
            cursor.execute('''
                INSERT INTO donors (user_id)
                VALUES (?)
            ''', (user_id,))
        
        conn.commit()
        conn.close()
        
        return user_id
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users WHERE email = ?
        ''', (email,))
        
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def get_all_donors(self):
        """Get all donors"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.*, d.total_donations, d.last_donation_date, d.next_eligible_date, 
                   d.is_available, d.emergency_contact, d.medical_conditions
            FROM users u
            LEFT JOIN donors d ON u.id = d.user_id
            WHERE u.user_type = 'donor' AND u.is_active = 1
        ''')
        
        donors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return donors
    
    def insert_emergency_request(self, request_data):
        """Insert a new emergency request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO emergency_requests (patient_name, blood_type, units_needed, urgency, hospital, contact, city)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            request_data['patient_name'],
            request_data['blood_type'],
            request_data['units_needed'],
            request_data['urgency'],
            request_data['hospital'],
            request_data['contact'],
            request_data.get('city')
        ))
        
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return request_id
    
    def get_active_emergency_requests(self):
        """Get all active emergency requests"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM emergency_requests 
            WHERE is_active = 1 
            ORDER BY created_at DESC
        ''')
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return requests
    
    def update_emergency_request(self, request_id, data):
        """Update emergency request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE emergency_requests 
            SET is_fulfilled = ?, fulfilled_at = ?, fulfilled_by = ?
            WHERE id = ?
        ''', (
            data.get('is_fulfilled', False),
            data.get('fulfilled_at'),
            data.get('fulfilled_by'),
            request_id
        ))
        
        conn.commit()
        conn.close()
    
    def insert_donation(self, donation_data):
        """Insert a new blood donation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO blood_donations (donor_id, blood_type, units, donation_date, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            donation_data['donor_id'],
            donation_data['blood_type'],
            donation_data['units'],
            donation_data['donation_date'],
            donation_data['location']
        ))
        
        donation_id = cursor.lastrowid
        
        # Update donor's donation count and dates
        cursor.execute('''
            UPDATE donors 
            SET total_donations = total_donations + 1,
                last_donation_date = ?,
                next_eligible_date = datetime(?, '+56 days')
            WHERE user_id = ?
        ''', (
            donation_data['donation_date'],
            donation_data['donation_date'],
            donation_data['donor_id']
        ))
        
        conn.commit()
        conn.close()
        
        return donation_id
    
    def get_donations_by_donor(self, donor_id):
        """Get all donations by a donor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM blood_donations 
            WHERE donor_id = ? 
            ORDER BY donation_date DESC
        ''', (donor_id,))
        
        donations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return donations
    
    def insert_notification(self, notification_data):
        """Insert a new notification"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, notification_type)
            VALUES (?, ?, ?, ?)
        ''', (
            notification_data['user_id'],
            notification_data['title'],
            notification_data['message'],
            notification_data['notification_type']
        ))
        
        notification_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return notification_id
    
    def get_notifications_by_user(self, user_id, limit=50):
        """Get notifications for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM notifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        notifications = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return notifications
    
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications 
            SET is_read = 1 
            WHERE id = ?
        ''', (notification_id,))
        
        conn.commit()
        conn.close()
    
    def get_unread_notification_count(self, user_id):
        """Get count of unread notifications for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM notifications 
            WHERE user_id = ? AND is_read = 0
        ''', (user_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count

# Global database manager instance
db_manager = DatabaseManager() 