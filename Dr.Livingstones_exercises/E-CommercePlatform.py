class Product:
    def __init__(self, name, price):
        self.name  = name
        self.price = price

    def get_total_cost(self):
        return self.price           # base: just the price


class PhysicalProduct(Product):
    def __init__(self, name, price, shipping_cost):
        super().__init__(name, price)
        self.shipping_cost = shipping_cost

    def get_total_cost(self):
        return self.price + self.shipping_cost
class DigitalProduct(Product):
    def __init__(self, name, price, download_link):
        super().__init__(name, price)
        self.download_link = download_link

    def get_total_cost(self):
        return self.price              # no shipping

    def display(self):
        print(f"Download: {self.download_link}")


cart = [
    PhysicalProduct("Book", 15, 3.50),
    DigitalProduct("eBook", 9, "https://dl.example.com/eb"),
]
for p in cart:
    print(f"{p.name} → total: ${p.get_total_cost()}")
