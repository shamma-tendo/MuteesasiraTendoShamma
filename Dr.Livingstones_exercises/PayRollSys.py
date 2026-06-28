class Employee:
    def __init__(self, name, emp_no):
        self.name   = name
        self.emp_no = emp_no

    def calculate_pay(self):
        raise NotImplementedError


class FullTimeEmployee(Employee):
    def __init__(self, name, emp_no, monthly_salary):
        super().__init__(name, emp_no)
        self.monthly_salary = monthly_salary

    def calculate_pay(self):
        return self.monthly_salary       # fixed
class PartTimeEmployee(Employee):
    def __init__(self, name, emp_no, hourly_rate, hours_worked):
        super().__init__(name, emp_no)
        self.hourly_rate  = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self):
        return self.hourly_rate * self.hours_worked


staff = [
    FullTimeEmployee("Jane", "E01", 3000),
    PartTimeEmployee("Mark", "E02", 15, 80),
]
for e in staff:
    print(f"{e.name}: ${e.calculate_pay()}")