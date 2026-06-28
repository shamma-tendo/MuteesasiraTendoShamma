class User:
    def __init__(self, username):
        self.username = username

    def login(self):
        print(f"{self.username} logged in")


class Student(User):          # level 2
    def __init__(self, username, student_id):
        super().__init__(username)
        self.student_id = student_id

    def enrol(self, course):
        print(f"{self.username} enrolled in {course}")


class TeachingAssistant(Student):   # level 3
    def __init__(self, username, student_id, assigned_module):
        super().__init__(username, student_id)
        self.assigned_module = assigned_module
        def mark_assignment(self):
          print(f"{self.username} marking for {self.assigned_module}")


ta = TeachingAssistant("sam", "S99", "Data Structures")
ta.login()           # from User
ta.enrol("AI")       # from Student
#ta.mark_assignment() # own method