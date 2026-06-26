class BankAccount:
    def __init__(self, acc_no, balance=0):
        self.acc_no  = acc_no
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Balance: {self.balance}")

    def withdraw(self, amount):    # base rule: can't go below 0
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. Balance: {self.balance}")


class SavingsAccount(BankAccount):
    def __init__(self, acc_no, balance, interest_rate):
        super().__init__(acc_no, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):      # extra method, not in parent
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest applied: {interest:.2f}. Balance: {self.balance:.2f}")


class CurrentAccount(BankAccount):
    def __init__(self, acc_no, balance, overdraft_limit):
        super().__init__(acc_no, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):   # OVERRIDES — allows overdraft
        if amount > self.balance + self.overdraft_limit:
            print("Exceeds overdraft limit")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. Balance: {self.balance}")


# demo
sv = SavingsAccount("SA01", 1000, 0.05)
sv.apply_interest()

ca = CurrentAccount("CA01", 200, 500)
ca.withdraw(600)  # allowed via overdraft