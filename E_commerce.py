
# REAL WORLD E-COMMERCE SYSTEM
# Assignment2: Showcasing Control Structures
#MUTEESASIRA TENDO SHAMMA 2400707480 

# USER DATABASE (LOGIN SYSTEM)
users = {
    "admin": {"password": "1234", "role": "admin"},
    "customer1": {"password": "1111", "role": "customer"},
    "cashier1": {"password": "2222", "role": "cashier"}
}


# PRODUCT INVENTORY (STOCK LIST)
products = {
    "Lenovo": {"price": 2000000, "stock": 15},
    "Dell": {"price": 8000000, "stock": 8},
    "Asus": {"price": 1000000, "stock": 22},
    "HP": {"price": 5000000, "stock": 12},
    "MacBook": {"price": 15000000, "stock": 5},
    "Acer": {"price": 7000000, "stock": 18},
    "Surface": {"price": 12000000, "stock": 9},
    "Razer": {"price": 2500000, "stock": 11}
}


# COUPON CODES
coupons = {
    "SAVE10": 0.10,
    "SAVE20": 0.20,
    "SAVE30": 0.30
}


# DISPLAY PRODUCTS IN TABLE FORMAT
def display_products_table():
    print("\n" + "="*70)
    print(f"{'Product Name':<20} {'Unit Price (UGX)':<25} {'Stock Available':<15}")
    print("="*70)
    for item, details in products.items():
        print(f"{item:<20} {details['price']:<25,} {details['stock']:<15}")
    print("="*70 + "\n")


# LOGIN SYSTEM (3 ATTEMPTS)

def login():
    print("\n========== WELCOME TO GADGET WORLD ==========")
    print("Please log in to continue.\n")
    attempts = 3

    while attempts > 0:
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Check if user exists and password matches
        if username in users and users[username]["password"] == password:
            print("\nLogin successful!")
            return username
        else:
            attempts -= 1
            print(f"Invalid login. Attempts remaining: {attempts}")

    print("Too many failed attempts. Try again later.")
    return None



# TAX CALCULATION (BASED ON LOCATION)
def get_tax_rate(location):
    # nested condition for tax rates based on location where transaction occurs
    if location == "kampala":
        return 0.10
    elif location == "jinja":
        return 0.15
    else:
        return 0.20



# DISCOUNT BASED ON SUBTOTAL
def get_discount_rate(subtotal):
    # nested conditions for discount levels
    if subtotal >= 1000:
        return 0.15
    elif subtotal >= 500:
        return 0.10
    else:
        return 0.05


# PURCHASE FUNCTION (CUSTOMER)
def make_purchase():
    display_products_table()

    item = input("Enter product name: ")

    # check if product exists
    if item not in products:
        print("Product not found!")
        return

    quantity = int(input("Enter quantity: "))
    
    # check if enough stock is available
    if quantity > products[item]["stock"]:
        print(f"Not enough stock! Available: {products[item]['stock']}")
        return
    
    subtotal = products[item]["price"] * quantity

    # discount logic
    discount_rate = get_discount_rate(subtotal)
    discount = subtotal * discount_rate

    # coupon system
    coupon = input("Enter coupon code (or NONE): ")

    if coupon in coupons:
        coupon_discount = subtotal * coupons[coupon]
        print("Valid coupon applied!")
    else:
        coupon_discount = 0
        print("Invalid or no coupon applied!")

    location = input("Enter your location: ")
    tax_rate = get_tax_rate(location)

    # final calculations
    taxed_amount = (subtotal - discount - coupon_discount) * tax_rate
    final_price = subtotal - discount - coupon_discount + taxed_amount

    print("\n------ BILL SUMMARY ------")
    print(f"Subtotal: {subtotal}")
    print(f"Discount: {discount}")
    print(f"Coupon Discount: {coupon_discount}")
    print(f"Tax: {taxed_amount}")
    print(f"FINAL PRICE: {final_price}")



# ADMIN PANEL
def admin_panel():
    print("\n--- ADMIN DASHBOARD ---")
    print("1. View Products")
    print("2. Add Product")
    print("3. Logout")

    choice = input("Choose option: ")

    if choice == "1":
        display_products_table()

    elif choice == "2":
        name = input("Enter product name: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter initial stock quantity: "))
        products[name] = {"price": price, "stock": stock}
        print("Product added successfully!")

    else:
        print("Logging out...")



# INVENTORY MANAGEMENT (CASHIER)
def manage_inventory():
    display_products_table()
    item = input("Enter product name to update stock: ")
    
    if item not in products:
        print("Product not found!")
        return
    
    print(f"Current stock for {item}: {products[item]['stock']}")
    action = input("Add or Reduce stock? (add/reduce): ").lower()
    
    if action == "add":
        quantity = int(input("Enter quantity to add: "))
        products[item]["stock"] += quantity
        print(f"Stock updated! New stock: {products[item]['stock']}")
    elif action == "reduce":
        quantity = int(input("Enter quantity to reduce: "))
        if quantity > products[item]["stock"]:
            print(f"Cannot reduce! Current stock is only {products[item]['stock']}")
        else:
            products[item]["stock"] -= quantity
            print(f"Stock updated! New stock: {products[item]['stock']}")
    else:
        print("Invalid action!")


# CASHIER PANEL
def cashier_panel():
    print("\n--- CASHIER PANEL ---")
    print("1. View Products")
    print("2. Process Purchase")
    print("3. Manage Inventory")
    print("4. Logout")

    choice = input("Choose option: ")

    if choice == "1":
        display_products_table()

    elif choice == "2":
        make_purchase()
    
    elif choice == "3":
        manage_inventory()

    else:
        print("Logging out...")



# CUSTOMER PANEL
def customer_panel():
    print("\n--- CUSTOMER DASHBOARD ---")
    print("1. View Products")
    print("2. Make Purchase")
    print("3. Logout")

    choice = input("Choose option: ")

    if choice == "1":
        display_products_table()

    elif choice == "2":
        make_purchase()

    else:
        print("Logging out...")



# MAIN SYSTEM CONTROLLER
user = login()

if user:
    role = users[user]["role"]

    # role-based access control
    if role == "admin":
        admin_panel()

    elif role == "cashier":
        cashier_panel()

    elif role == "customer":
        customer_panel()

    else:
        print("Unknown role! Access denied.")