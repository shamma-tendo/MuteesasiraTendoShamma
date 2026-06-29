# ============================================
# Question 1: University Management System
# ============================================

class Person:
    """Base class for all people"""
    def __init__(self, name, national_id, email):
        self.name = name
        self.national_id = national_id
        self.email = email
    
    def display_info(self):
        return f"Name: {self.name}, ID: {self.national_id}, Email: {self.email}"

class Student(Person):
    """Single inheritance from Person"""
    def __init__(self, name, national_id, email, reg_no, program):
        super().__init__(name, national_id, email)  # super() calls parent
        self.reg_no = reg_no
        self.program = program
    
    def display_info(self):
        return super().display_info() + f", Reg: {self.reg_no}, Program: {self.program}"

class Staff(Person):
    """Single inheritance from Person"""
    def __init__(self, name, national_id, email, emp_no, department):
        super().__init__(name, national_id, email)
        self.emp_no = emp_no
        self.department = department
    
    def display_info(self):
        return super().display_info() + f", Emp: {self.emp_no}, Dept: {self.department}"

class TeachingAssistant(Student, Staff):
    """Multiple inheritance - combines Student and Staff"""
    def __init__(self, name, national_id, email, reg_no, program, emp_no, department):
        # Call both parent constructors
        Student.__init__(self, name, national_id, email, reg_no, program)
        Staff.__init__(self, name, national_id, email, emp_no, department)
    
    def display_info(self):
        # MRO: TeachingAssistant -> Student -> Staff -> Person
        return f"TA: {self.name}, Reg: {self.reg_no}, Emp: {self.emp_no}"

# Demonstration
ta = TeachingAssistant("Alice", "NID123", "alice@uni.edu", "R001", "CS", "E001", "CompSci")
print(ta.display_info())
print(TeachingAssistant.__mro__)  # Method Resolution Order


