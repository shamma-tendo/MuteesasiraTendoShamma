class Driver:
    def __init__(self, name, vehicle_reg, rating):
        self.name        = name
        self.vehicle_reg = vehicle_reg
        self.rating      = rating

    def calculate_earnings(self):
        raise NotImplementedError("Each driver type must define earnings")

    def display(self):
        print(f"{self.name} | {self.vehicle_reg} | ★{self.rating}")


class TaxiDriver(Driver):
    def __init__(self, name, reg, rating, trips, rate_per_trip):
        super().__init__(name, reg, rating)
        self.trips         = trips
        self.rate_per_trip = rate_per_trip
        
    def calculate_earnings(self):
        return self.trips * self.rate_per_trip
    
class DeliveryDriver(Driver):
    def __init__(self, name, reg, rating, deliveries, rate):
        super().__init__(name, reg, rating)
        self.deliveries = deliveries
        self.rate       = rate

    def calculate_earnings(self):
        return self.deliveries * self.rate


drivers = [
    TaxiDriver("Ali", "T-001", 4.8, 12, 8),
    DeliveryDriver("Nia", "D-002", 4.9, 20, 5),
]
for d in drivers:
    d.display()
    print(f"Earnings: ${d.calculate_earnings()}\n")