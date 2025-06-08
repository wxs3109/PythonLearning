# Inheritance
# inheritance.py

# ============================================================
# 🧬 Basic Inheritance
# ------------------------------------------------------------
# - Define a base class (e.g., Animal) with a method like make_sound()
# - Define a subclass (e.g., Dog) that inherits from Animal
# - Override the make_sound() method in the subclass
# - Create instances of both and call the method to show behavior
# ============================================================

class Animal:
    def make_sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def make_sound(self):
        print("Dog makes a sound")

dog = Dog()
dog.make_sound()

# ============================================================
# 🧰 Inheriting Attributes and Methods
# ------------------------------------------------------------
# - In base class, add an __init__() method that initializes some attributes
# - In subclass, use super().__init__() to call the parent constructor
# - Add extra attributes in subclass constructor
# - Create instance of subclass and access both inherited and subclass attributes
# ============================================================

class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

dog = Dog("Buddy", "Golden Retriever")
print(dog.name)
print(dog.breed)

# ============================================================
# 🔁 Method Overriding
# ------------------------------------------------------------
# - Override a method from the base class in the subclass
# - Demonstrate calling the overridden method
# - Optionally, call the base class version from subclass using super()
# ============================================================

class Animal:
    def make_sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def make_sound(self):
        print("Dog makes a sound")

dog = Dog()
dog.make_sound()

# ============================================================
# 🧪 isinstance() and issubclass()
# ------------------------------------------------------------
# - Use isinstance() to check if an object is an instance of a class or its parent
# - Use issubclass() to check class relationships
# ============================================================
print(isinstance(dog, Animal))

# ============================================================
# 🧱 Multiple Inheritance (Optional)
# ------------------------------------------------------------
# - Define two base classes with different methods
# - Create a subclass that inherits from both
# - Show that it can access methods from both parents
# - Be aware of method resolution order (MRO)
# ============================================================

class Robot:
    def __init__(self, name):
        self.name = name

    def transform(self):
        print(f"{self.name} is transforming")

# dog inherits from robot and animal
class Dog(Robot, Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def make_sound(self):
        print("Dog makes a sound")

    def transform(self):
        print(f"{self.name} is transforming into a dog")

dog = Dog("Buddy", "Golden Retriever")