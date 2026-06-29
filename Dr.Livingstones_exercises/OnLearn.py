# ============================================
# Question 5: Online Learning Platform
# ============================================

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_logged_in = False
    
    def login(self):
        self.is_logged_in = True
        return f"{self.username} logged in"
    
    def logout(self):
        self.is_logged_in = False
        return f"{self.username} logged out"

class StudentUser(User):
    def __init__(self, username, email):
        super().__init__(username, email)
        self.courses = []
        self.grades = {}
    
    def enroll(self, course):
        self.courses.append(course)
        return f"{self.username} enrolled in {course}"
    
    def view_grades(self):
        return f"{self.username}'s grades: {self.grades}"

class InstructorUser(User):
    def __init__(self, username, email):
        super().__init__(username, email)
        self.courses_created = []
    
    def create_course(self, course_name):
        self.courses_created.append(course_name)
        return f"{self.username} created course: {course_name}"
    
    def grade_assignment(self, student, assignment, grade):
        student.grades[assignment] = grade
        return f"{student.username} got {grade} on {assignment}"

class StudentInstructor(StudentUser, InstructorUser):
    """Multiple inheritance: user who is both student and instructor"""
    def __init__(self, username, email):
        StudentUser.__init__(self, username, email)
        InstructorUser.__init__(self, username, email)
    
    def login(self):
        # MRO: StudentInstructor -> StudentUser -> InstructorUser -> User
        return User.login(self)
    
    def get_role(self):
        return "I'm both a student and an instructor!"

# Demonstration
si = StudentInstructor("johndoe", "john@edu.com")
print(si.login())
print(si.enroll("Python 101"))
print(si.create_course("Data Science"))
print(si.view_grades())
print(si.get_role())
print(StudentInstructor.__mro__)