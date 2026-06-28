# Base class
class Vehicle:
    def __init__(self, reg_no, rentalPrice):
        self.reg_no = reg_no
        self.rentalPrice = rentalPrice
        self.running = False

    def start(self):
        self.running = True
        return f"{self.reg_no} started"

    def stop(self):
        self.running = False
        return f"{self.reg_no} stopped"

    # Method to calculate rental cost (can be inherited by subclasses)
    def rental_cost(self, days):
        return self.rentalPrice * days

    # Base display method (will be overridden by subclasses)
    def display(self):
        return f"Reg No: {self.reg_no}, Rental Price: UGX {self.rentalPrice}/day"


# Subclass Car
class Car(Vehicle):
    def __init__(self, reg_no, rentalPrice, seatingCapacity):  # ✅ Fixed: added reg_no and rentalPrice as parameters
        super().__init__(reg_no, rentalPrice)                   # ✅ Fixed: correctly passing to Vehicle
        self.seatingCapacity = seatingCapacity

    # Overriding display to include seating capacity
    def display(self):
        return super().display() + f", Seating Capacity: {self.seatingCapacity} seats"


# Subclass Motorcycle
class Motorcycle(Vehicle):
    def __init__(self, reg_no, rentalPrice, engineCapacity):   # ✅ Fixed: added reg_no and rentalPrice as parameters
        super().__init__(reg_no, rentalPrice)                   # ✅ Fixed: was missing entirely
        self.engineCapacity = engineCapacity

    # Overriding display to include engine capacity
    def display(self):
        return super().display() + f", Engine Capacity: {self.engineCapacity}cc"


# ── Demonstration ─────────────────────────────────────────────────

print("=== Vehicle Rental Company ===")

# Car
c = Car("UA2001", 25000, 5)
print("\n-- Car --")
print(c.display())
print(c.start())
print(f"Rental cost for 3 days: UGX {c.rental_cost(3)}")
print(c.stop())

# Motorcycle
m = Motorcycle("UMA129", 2500, 400)
print("\n-- Motorcycle --")
print(m.display())
print(m.start())
print(f"Rental cost for 5 days: UGX {m.rental_cost(5)}")
print(m.stop())

# Polymorphism demonstration — same method call, different output
print("\n-- Polymorphism: display() called on each vehicle --")
vehicles = [c, m]
for v in vehicles:
    print(v.display())