class Staff:
    def __init__(self, name, staff_id):
        self.name     = name
        self.staff_id = staff_id

    def clock_in(self):          # shared by ALL subclasses
        print(f"{self.name} ({self.staff_id}) clocked in")


class Doctor(Staff):
    def __init__(self, name, staff_id, specialty):
        super().__init__(name, staff_id)
        self.specialty = specialty

    def consult(self, patient):
        print(f"Dr {self.name} consulting {patient} [{self.specialty}]")

class Nurse(Staff):
    def __init__(self, name, staff_id, ward):
        super().__init__(name, staff_id)
        self.ward = ward

    def administer(self, medication):
        print(f"{self.name} (Ward {self.ward}) giving {medication}")


class Pharmacist(Staff):
    def __init__(self, name, staff_id, license_no):
        super().__init__(name, staff_id)
        self.license_no = license_no

    def dispense(self, drug):
        print(f"{self.name} [Lic:{self.license_no}] dispensing {drug}")

# Everyone shares clock_in
team = [
    Doctor("Patel", "D01", "Cardiology"),
    Nurse("Grace", "N01", "ICU"),
    Pharmacist("Bayo", "P01", "PH-887"),
]
for m in team: m.clock_in()