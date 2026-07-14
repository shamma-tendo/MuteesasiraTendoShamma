# database.py - Database Operations
from flask_sqlalchemy import SQLAlchemy
from sis_app.models import db, Student

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
        
        if Student.query.count() == 0:
            add_sample_data()

def add_sample_data():
    sample_students = [
        Student(
            student_name='John Doe',
            registration_number='STU2024001',
            email='john.doe@university.edu',
            programme='Computer Science'
        ),
        Student(
            student_name='Jane Smith',
            registration_number='STU2024002',
            email='jane.smith@university.edu',
            programme='Information Technology'
        )
    ]
    
    for student in sample_students:
        db.session.add(student)
    db.session.commit()
    print("📚 Sample data added!")

def get_all_students():
    return Student.query.filter_by(is_active=True).all()

def get_student_by_name(name):
    return Student.query.filter(
        Student.student_name.contains(name),
        Student.is_active == True
    ).all()

def get_student_by_registration(registration_number):
    return Student.query.filter_by(registration_number=registration_number).first()

def add_student(student_data):
    try:
        existing = get_student_by_registration(student_data['registration_number'])
        if existing:
            return False, "Registration number already exists!", None
        
        existing_email = Student.query.filter_by(email=student_data['email']).first()
        if existing_email:
            return False, "Email already registered!", None
        
        new_student = Student(
            student_name=student_data['student_name'],
            registration_number=student_data['registration_number'],
            email=student_data['email'],
            programme=student_data['programme']
        )
        
        db.session.add(new_student)
        db.session.commit()
        return True, "Student registered successfully!", new_student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None


def get_student_by_id(student_id):
    return Student.query.get(student_id)


def update_student(student_id, student_data):
    try:
        student = get_student_by_id(student_id)
        if not student or not student.is_active:
            return False, "Student not found!", None

        # Check for registration number conflict
        if student.registration_number != student_data.get('registration_number'):
            conflict = Student.query.filter_by(registration_number=student_data.get('registration_number')).first()
            if conflict and conflict.id != student.id:
                return False, "Registration number already exists!", None

        # Check for email conflict
        if student.email != student_data.get('email'):
            conflict_email = Student.query.filter_by(email=student_data.get('email')).first()
            if conflict_email and conflict_email.id != student.id:
                return False, "Email already registered!", None

        student.student_name = student_data.get('student_name', student.student_name)
        student.registration_number = student_data.get('registration_number', student.registration_number)
        student.email = student_data.get('email', student.email)
        student.programme = student_data.get('programme', student.programme)

        db.session.commit()
        return True, "Student updated successfully!", student

    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None


def delete_student(student_id):
    try:
        student = get_student_by_id(student_id)
        if not student or not student.is_active:
            return False, "Student not found!", None

        # Soft-delete
        student.is_active = False
        db.session.commit()
        return True, "Student deleted successfully!", student

    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None