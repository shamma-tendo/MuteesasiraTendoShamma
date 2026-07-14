# app.py - Main Application
from flask import Flask, render_template, request, redirect, url_for, flash
from sis_app.database import (
    init_db,
    add_student,
    get_all_students,
    get_student_by_name,
    get_student_by_id,
    update_student,
    delete_student
)
from sis_app.models import db, Student

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize database
init_db(app)

@app.route('/')
def home():
    total_students = Student.query.filter_by(is_active=True).count()
    return render_template('home.html', total_students=total_students)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_data = {
            'student_name': request.form.get('student_name', '').strip(),
            'registration_number': request.form.get('registration_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'programme': request.form.get('programme', '').strip()
        }
        
        if not all(student_data.values()):
            flash('All fields are required!', 'error')
            return render_template('register.html', form_data=student_data)
        
        success, message, student = add_student(student_data)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('student_profile', name=student.student_name))
        else:
            flash(message, 'error')
            return render_template('register.html', form_data=student_data)
    
    return render_template('register.html', form_data=None)

@app.route('/student/<name>')
def student_profile(name):
    students = get_student_by_name(name)
    if students:
        return render_template('confirmation.html', student=students[0])
    else:
        flash('Student not found!', 'error')
        return redirect(url_for('register'))


@app.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = get_student_by_id(student_id)
    if not student or not student.is_active:
        flash('Student not found!', 'error')
        return redirect(url_for('students_list'))

    if request.method == 'POST':
        form_data = {
            'student_name': request.form.get('student_name', '').strip(),
            'registration_number': request.form.get('registration_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'programme': request.form.get('programme', '').strip()
        }

        if not all(form_data.values()):
            flash('All fields are required!', 'error')
            return render_template('edit_student.html', student=form_data)

        success, message, updated = update_student(student_id, form_data)
        if success:
            flash(message, 'success')
            return redirect(url_for('students_list'))
        else:
            flash(message, 'error')
            return render_template('edit_student.html', student=form_data)

    return render_template('edit_student.html', student=student)


@app.route('/student/<int:student_id>/delete', methods=['POST'])
def delete_student_route(student_id):
    success, message, deleted = delete_student(student_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('students_list'))

@app.route('/students')
def students_list():
    all_students = get_all_students()
    return render_template('students_list.html', students=all_students)

@app.route('/search', methods=['GET'])
def search_students():
    search_term = request.args.get('q', '').strip()
    if search_term:
        students = get_student_by_name(search_term)
        return render_template('students_list.html', students=students, search_term=search_term)
    return redirect(url_for('students_list'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)