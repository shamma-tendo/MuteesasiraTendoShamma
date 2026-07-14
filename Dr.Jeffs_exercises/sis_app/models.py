# models.py - Database Models
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Student {self.student_name} - {self.registration_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'registration_number': self.registration_number,
            'email': self.email,
            'programme': self.programme,
            'registration_date': self.registration_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }