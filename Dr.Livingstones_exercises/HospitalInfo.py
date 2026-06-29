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


