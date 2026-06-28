class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name    = name
        self.email   = email

    def login(self):
        print(f"{self.name} logged in ({self.email})")

    def logout(self):
        print(f"{self.name} logged out")

    def display_profile(self):
        print(f"[User] ID:{self.user_id} Name:{self.name}")


class Student(User):                      # single inheritance
    def __init__(self, user_id, name, email, reg_no, course):
        super().__init__(user_id, name, email)
        self.reg_no = reg_no
        self.course = course

    def display_profile(self):             # override
        super().display_profile()
        print(f"  Reg:{self.reg_no} | Course:{self.course}")


class Supervisor(User):                  # single inheritance
    def __init__(self, user_id, name, email, company, emp_id):
        super().__init__(user_id, name, email)
        self.company = company
        self.emp_id  = emp_id

    def display_profile(self):
        super().display_profile()
        print(f"  Company:{self.company} | EmpID:{self.emp_id}")


class StudentRepresentative(Student, Supervisor):  # multiple
    def __init__(self, user_id, name, email,
                 reg_no, course, company, emp_id):
        
        # Explicitly initialise both parents
        Student.__init__(self, user_id, name, email, reg_no, course)
        Supervisor.__init__(self, user_id, name, email, company, emp_id)

    def display_profile(self):             # own override
        print("=== Student Representative ===")
        Student.display_profile(self)
        print(f"  Company:{self.company} | EmpID:{self.emp_id}")


# --- demo ---
sr = StudentRepresentative(
    "U001", "Amara", "amara@uni.ac",
    "REG-42", "Software Eng", "TechCorp", "TC-88"
)
sr.login()
sr.display_profile()
sr.logout()

# MRO
print(StudentRepresentative.mro())