# Command Pattern

# strategy functions

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

class Calculator:
    def __init__(self, strategy):
        self.strategy = strategy

    def calculate(self, a, b):
        return self.strategy(a, b)

calculator = Calculator(add)
print(calculator.calculate(1, 2))