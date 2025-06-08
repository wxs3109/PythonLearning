# ============================================================
# 📘 Basic Exception Handling
# ============================================================

# 1. Basic try-except block
# Knowledge: Basic exception handling with try-except
# Task: Add code to handle division by zero
try:
    a = 1 // 0
except ZeroDivisionError:
    print("ZeroDivisionError")

# 2. Multiple exception handling
# Knowledge: Catching different types of exceptions
# Task: Handle both ValueError and TypeError
try:
    a = int("hello")
    b = "1" + 1
except ValueError:
    print("Cannot convert string to int")
except TypeError:
    print("Cannot add string and int")

# 3. Exception with else clause
# Knowledge: else clause runs when no exception occurs
# Task: Add else clause to print success message
try:
    a = 10 / 2
except Exception:
    print("Exception")
else:
    print("Success")

# 4. Finally block
# Knowledge: finally block always executes
# Task: Add finally block to clean up resources
try:
    a = 10 / 0
except Exception:
    print("Exception")
finally:
    print("Finally")

# 5. Raising exceptions
# Knowledge: How to raise custom exceptions
# Task: Create a function that raises ValueError for negative numbers
def check_positive(number):
    if number < 0:
        raise ValueError("Number must be positive")
    else:
        print("Number is positive")

try:
    check_positive(-1)
except ValueError as e:
    print(e)

# 6. Exception chaining
# Knowledge: Preserving exception context
# Task: Chain exceptions using 'raise from'
try:
    try:
        int("s")
    except ValueError as e:
        raise RuntimeError("cannot convert string to int") from e
except RuntimeError as e:
    print(e)

# 7. Assertions
# Knowledge: Using assertions for debugging
# Task: Add assertions to validate function inputs
import math

def calculate_square_root(number):
    assert number >= 0, "Number must be positive"
    return math.sqrt(number)

try:
    calculate_square_root(-1)
except AssertionError as e:
    print(e)
