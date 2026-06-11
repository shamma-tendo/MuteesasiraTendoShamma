
#   BILL SPLIT CALCULATOR
#   Assignment 1 — Python Programming Class
#   By: muteesasira tendo shamma 2400707480


def get_positive_number(prompt, allow_zero=False):
    """Keep asking until the user gives us a valid positive number."""
    while True:
        try:
            value = float(input(prompt))
            if allow_zero and value < 0:
                print("   Oops! Please enter a number that's 0 or above.\n")
            elif not allow_zero and value <= 0:
                print("   Oops! Please enter a number greater than zero.\n")
            else:
                return value
        except ValueError:
            print("   That doesn't look like a number. Try again!\n")


def get_tip_percentage():
    """Let the user pick a tip percentage or enter a custom one."""
    print("\n  How much tip would you like to leave? (as a percentage of the total bill)")
    print("     [1] 10%  — Decent")
    print("     [2] 15%  — Good")
    print("     [3] 20%  — Generous")
    print("     [4] Custom — You decide!")

    while True:
        choice = input("\n  Enter choice (1/2/3/4): ").strip()
        if choice == "1":
            return 10.0
        elif choice == "2":
            return 15.0
        elif choice == "3":
            return 20.0
        elif choice == "4":
            custom = get_positive_number("  Enter your custom tip %: ", allow_zero=True)
            return custom
        else:
            print("   Please pick 1, 2, 3, or 4 only!")


def print_receipt(bill_amount, num_people, tip_percent, tip_amount, total_bill, per_person):
    """Print a beautifully formatted receipt using f-strings!"""
    width = 44
    divider   = "─" * width
    thick_div = "═" * width

    print(f"\n  {'╔' + thick_div + '╗'}")
    print(f"  ║{' BILL SPLIT RECEIPT':^{width}}║")
   
    print(f"  ╠{thick_div}╣")
    print(f"  ║  {'Original Bill:':<28} UGX{bill_amount:>10.2f}  ║")
    print(f"  ║  {'Tip Percentage:':<28} {tip_percent:>9.1f}%  ║")
    print(f"  ║  {'Tip Amount:':<28} UGX{tip_amount:>10.2f}  ║")
    print(f"  ║  {divider}  ║")
    print(f"  ║  {'TOTAL BILL (bill + tip):':<28} UGX{total_bill:>10.2f}  ║")
    print(f"  ╠{thick_div}╣")
    print(f"  ║  {'Number of People:':<28} {int(num_people):>10}  ║")
    print(f"  ║                                            ║")
    print(f"  ║  {' EACH PERSON PAYS:':<28} UGX{per_person:>10.2f}  ║")
    print(f"  ╚{thick_div}╝")
    print(f"\n   Split evenly among {int(num_people)} {'person' if num_people == 1 else 'people'}.")
    print(f"  Tip: Don't forget to actually pay your share! \n")


def main():
    
    print("   WELCOME TO THE BILL SPLIT CALCULATOR  ")
    print("="*50)
    print("   Let's figure out who owes what — fairly!\n")

    # Step 1: Get inputs
    bill_amount = get_positive_number("   Enter the total bill amount (UGX): ")
    num_people  = get_positive_number("   How many people are splitting? ")

    # Make sure people count is a whole number
    num_people = int(num_people)
    if num_people < 1:
        print("   Need at least 1 person!")
        return

    tip_percent = get_tip_percentage()

    #  Step 2: Calculate everything 
    tip_amount = bill_amount * (tip_percent / 100)
    total_bill = bill_amount + tip_amount
    per_person = total_bill / num_people

    #  Step 3: Show the receipt 
    print_receipt(bill_amount, num_people, tip_percent,
                  tip_amount, total_bill, per_person)


# Run the program!
if __name__ == "__main__":
    main()