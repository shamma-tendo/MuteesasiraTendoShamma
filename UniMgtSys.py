# Base class
class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    # Method to display person information
    def display(self):
        return f"Name: {self.name}, ID: {self.id}"


# Subclass Student inherits from Person
class Student(Person):
    def __init__(self, name, id, major):
        super().__init__(name, id)   
        self.major = major

    # Overriding display method
    def display(self):
        return super().display() + f", Major: {self.major}"


# Subclass Lecturer inherits from Person (renamed from Staff per instructions)
class Lecturer(Person):
    def __init__(self, name, id, dept):
        super().__init__(name, id)   
        self.dept = dept

    # Overriding display method
    def display(self):
        return super().display() + f", Department: {self.dept}"


# Demonstration
student1 = Student("Alice", "S001", "Computer Science")
student2 = Student("Bob", "S002", "Mathematics")

lecturer1 = Lecturer("Dr. Smith", "L001", "Computer Science")
lecturer2 = Lecturer("Dr. Jones", "L002", "Mathematics")

print("=== University Management System ===")
print("\n-- Students --")
print(student1.display())
print(student2.display())

print("\n-- Lecturers --")
print(lecturer1.display())
print(lecturer2.display())