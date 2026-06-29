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


