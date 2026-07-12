#create a method overloading and  overriding that completes a banking system
#the parent class must be transaction and the child class can be deposit ,withdrawal and transfer
#demonstrate an employer depositing, withdrawing and transfering funds




class Transaction:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance

    # Method to be OVERRIDDEN by child classes
    def execute(self):
        print("Executing a generic transaction...")

    # METHOD OVERLOADING using default parameters
    def get_summary(self, show_name=False, show_balance=False):
        if show_name and show_balance:
            return f"Account: {self.account_holder} | Balance: ${self.balance:,.2f}"
        elif show_name:
            return f"Account Holder: {self.account_holder}"
        elif show_balance:
            return f"Current Balance: UGX{self.balance:,.2f}"
        else:
            return "Transaction Summary"


# CHILD CLASS 1
class Deposit(Transaction):
    def __init__(self, account_holder, balance, amount):
        super().__init__(account_holder, balance)
        self.amount = amount

    # OVERRIDING parent's execute()
    def execute(self):
        self.balance += self.amount
        print(f"Deposit:    +UGX{self.amount:,.2f} → New Balance: UGX{self.balance:,.2f}")
        return self.balance


#  CHILD CLASS 2
class Withdrawal(Transaction):
    def __init__(self, account_holder, balance, amount):
        super().__init__(account_holder, balance)
        self.amount = amount

    # OVERRIDING parent's execute()
    def execute(self):
        if self.amount > self.balance:
            print(f" Withdrawal: Insufficient funds! Balance: UGX{self.balance:,.2f}")
            return self.balance
        self.balance -= self.amount
        print(f" Withdrawal: -UGX{self.amount:,.2f} → New Balance: UGX{self.balance:,.2f}")
        return self.balance


# CHILD CLASS 3
class Transfer(Transaction):
    def __init__(self, account_holder, balance, amount, recipient):
        super().__init__(account_holder, balance)
        self.amount = amount
        self.recipient = recipient

    # OVERRIDING parent's execute()
    def execute(self):
        if self.amount > self.balance:
            print(f" Transfer:   Insufficient funds! Balance: UGX{self.balance:,.2f}")
            return self.balance
        self.balance -= self.amount
        print(f" Transfer:   -UGX{self.amount:,.2f} to {self.recipient} → New Balance: UGX{self.balance:,.2f}")
        return self.balance


# DEMO: Employer Banking Scenario 
if __name__ == "__main__":
    
    print("       EMPLOYER BANKING SYSTEM DEMO")
   

    # Starting account info
    holder  = "John Smith (Employer)"
    balance = 5000.00

    # Overloading demo — same method, different arguments
    base = Transaction(holder, balance)
    print(base.get_summary())                          # no args
    print(base.get_summary(show_name=True))            # 1 arg
    print(base.get_summary(show_name=True,
                           show_balance=True))         # 2 args
   

    #  Deposit 3,000
    dep = Deposit(holder, balance, 3000)
    balance = dep.execute()

    #   Withdraw 1,500 (salary payment)
    wdr = Withdrawal(holder, balance, 1500)
    balance = wdr.execute()

    #  Transfer 2,000 to supplier
    txf = Transfer(holder, balance, 2000, "Supplier Co.")
    balance = txf.execute()

    #   Try to overdraw
    wdr2 = Withdrawal(holder, balance, 9999)
    balance = wdr2.execute()

    
    print(f"  Final Balance for {holder}: UGX{balance:,.2f}")
   