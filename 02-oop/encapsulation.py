# Encapsulation

# encapsulation.py

# ============================================================
# 🧱 Basic Encapsulation Concept
# ------------------------------------------------------------
# - Create a class (e.g., BankAccount)
# - Define a "private" attribute using double underscore, like __balance
# - Provide public methods to deposit and withdraw money
# - Try accessing __balance directly (should fail)
# - Access it via public methods instead
# ============================================================

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance 

    def deposit(self, amount):
        self.__balance += amount

    # getter method
    def get_balance(self):
        return self.__balance

bank_account = BankAccount(100)
bank_account.deposit(50)
#print(bank_account.__balance) # this will raise an error because __balance is private
print(bank_account.get_balance())


# ============================================================
# 🔐 Getters and Setters
# ------------------------------------------------------------
# - Add get_balance() and set_balance() methods
# - In set_balance(), prevent setting negative balances
# - Demonstrate using these methods to read/write balance
# ============================================================

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance 

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance

    def set_balance(self, amount):
        if amount > 0:
            self.__balance = amount
bank_account = BankAccount(100)
bank_account.set_balance(-50)
print(bank_account.get_balance())


# ============================================================
# 🧼 Using @property and @<property>.setter
# ------------------------------------------------------------
# - Replace get_balance and set_balance with @property
# - Add validation logic in the setter
# - Show clean syntax: obj.balance instead of obj.get_balance()
# ============================================================

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance 

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        if amount > 0:
            self.__balance = amount
    
bank_account = BankAccount(100)
bank_account.balance = -50
print(bank_account.balance)



# ============================================================
# 🚫 Attempt Direct Access
# ------------------------------------------------------------
# - Try printing __balance directly from outside the class
# - Catch the error and explain why it fails (name mangling)
# - Optionally, demonstrate how to access it via _ClassName__balance (not recommended)
# ============================================================




