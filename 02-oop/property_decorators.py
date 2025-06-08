# Property Decorators
# property_decorators.py

# ============================================================
# 🧼 Introduction to @property
# ------------------------------------------------------------
# - Use @property to define a method that behaves like an attribute
# - Create a class (e.g., Circle) with a private attribute (e.g., __radius)
# - Create a getter method using @property to access the radius
# - Create a setter method using @<name>.setter to validate and set the radius
# - Demonstrate using it like a regular attribute: obj.radius = 5
# ============================================================

class Circle:
    def __init__(self, radius):
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius

circle = Circle(10)
print(circle.radius)


# ============================================================
# 📐 Read-only Property
# ------------------------------------------------------------
# - Create a read-only property (e.g., area or diameter)
# - Use @property without a setter
# - Show that trying to assign a value to it raises an AttributeError
# ============================================================

class Circle:
    def __init__(self, radius):
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, value):
        if value > 0:
            self.__radius = value
        else:
            raise ValueError("Radius must be positive")
    
    @property
    def area(self):
        return math.pi * self.__radius ** 2

circle = Circle(10)
circle.radius = -5
print(circle.area)


# ============================================================
# 🧪 Example with Validation
# ------------------------------------------------------------
# - In the setter, raise ValueError if input is invalid (e.g., negative radius)
# - Demonstrate the validation in action
# - Optionally, add type checking using isinstance()
# ============================================================

class Circle:

# ============================================================
# 📦 Internal Use of @property in __init__
# ------------------------------------------------------------
# - In the constructor (__init__), assign values using the property setter
# - This ensures validation logic is reused consistently
# ============================================================
