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


# ============================================
# Question 2: Smart City Transport System
# ============================================

class Vehicle:
    def __init__(self, reg_no, manufacturer, speed):
        self.reg_no = reg_no
        self.manufacturer = manufacturer
        self.speed = speed
    
    def start(self):
        return f"{self.reg_no} starting..."
    
    def stop(self):
        return f"{self.reg_no} stopping..."

class Bus(Vehicle):
    def __init__(self, reg_no, manufacturer, speed, route_no, capacity):
        super().__init__(reg_no, manufacturer, speed)
        self.route_no = route_no
        self.capacity = capacity
    
    def start(self):
        return f"Bus {self.route_no}: " + super().start()

class ElectricVehicle(Vehicle):
    def __init__(self, reg_no, manufacturer, speed, battery_percent):
        super().__init__(reg_no, manufacturer, speed)
        self.battery_percent = battery_percent
        self.charging = False
    
    def charge(self):
        self.charging = True
        self.battery_percent = 100
        return "Charging complete!"
    
    def start(self):
        if self.battery_percent < 5:
            return "Battery low! Charge first."
        return super().start()

class ElectricBus(Bus, ElectricVehicle):
    """Multiple inheritance: combines Bus and ElectricVehicle"""
    def __init__(self, reg_no, manufacturer, speed, route_no, capacity, battery_percent):
        Bus.__init__(self, reg_no, manufacturer, speed, route_no, capacity)
        ElectricVehicle.__init__(self, reg_no, manufacturer, speed, battery_percent)
    
    def start(self):
        # MRO: ElectricBus -> Bus -> ElectricVehicle -> Vehicle
        return ElectricVehicle.start(self)  # Use EV's start method

# Demonstration
ebus = ElectricBus("E123", "Tesla", 60, "R42", 50, 80)
print(ebus.start())
print(ebus.charge())
print(ElectricBus.__mro__)


# ============================================
# Question 3: Hospital Information System
# ============================================

class Employee:
    def __init__(self, emp_id, name, contact):
        self.emp_id = emp_id
        self.name = name
        self.contact = contact
    
    def display(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Contact: {self.contact}"

class Doctor(Employee):
    def __init__(self, emp_id, name, contact, specialization, fee):
        super().__init__(emp_id, name, contact)
        self.specialization = specialization
        self.consultation_fee = fee
    
    def display(self):
        return super().display() + f", Spec: {self.specialization}, Fee: ${self.consultation_fee}"

class Researcher(Employee):
    def __init__(self, emp_id, name, contact, research_area, publications):
        super().__init__(emp_id, name, contact)
        self.research_area = research_area
        self.publications = publications
    
    def display(self):
        return super().display() + f", Area: {self.research_area}, Pubs: {self.publications}"

class DoctorResearcher(Doctor, Researcher):
    """Multiple inheritance - resolves attribute conflicts"""
    def __init__(self, emp_id, name, contact, specialization, fee, research_area, publications):
        # Call both parents - note attribute sharing (name, emp_id, contact)
        Doctor.__init__(self, emp_id, name, contact, specialization, fee)
        Researcher.__init__(self, emp_id, name, contact, research_area, publications)
    
    def display(self):
        # MRO: DoctorResearcher -> Doctor -> Researcher -> Employee
        return Doctor.display(self) + f", {Researcher.display(self).split(', ')[-1]}"

# Demonstration
dr = DoctorResearcher("D001", "Dr. Smith", "123-456", "Cardiology", 200, "Heart Research", 15)
print(dr.display())
print(DoctorResearcher.__mro__)


# ============================================
# Question 4: E-Commerce Platform
# ============================================

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price
    
    def get_price(self):
        return self.price

class Discountable:
    def __init__(self, discount_percent=0):
        self.discount_percent = discount_percent
    
    def apply_discount(self, price):
        return price * (1 - self.discount_percent / 100)

class Taxable:
    def __init__(self, tax_rate=0):
        self.tax_rate = tax_rate
    
    def apply_tax(self, price):
        return price * (1 + self.tax_rate / 100)

class TaxableDiscountableProduct(Product, Discountable, Taxable):
    """Multiple inheritance: combines Product, Discountable, Taxable"""
    def __init__(self, product_id, name, price, discount_percent=0, tax_rate=0):
        Product.__init__(self, product_id, name, price)
        Discountable.__init__(self, discount_percent)
        Taxable.__init__(self, tax_rate)
    
    def get_final_price(self):
        # Method composition: discount first, then tax
        discounted = self.apply_discount(self.price)
        final = self.apply_tax(discounted)
        return final

# Demonstration
item = TaxableDiscountableProduct("P001", "Laptop", 1000, 10, 18)
print(f"Original: ${item.price}")
print(f"Final price: ${item.get_final_price():.2f}")


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