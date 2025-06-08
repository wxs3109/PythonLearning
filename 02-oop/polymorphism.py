# Polymorphism
# polymorphism.py

# ============================================================
# 🧬 Basic Polymorphism
# ------------------------------------------------------------
# - Define a base class (e.g., Animal) with a method like make_sound()
# - Define multiple subclasses (e.g., Dog, Cat) that override this method
# - Create a list of mixed Animal objects (Dog, Cat)
# - Loop through the list and call make_sound() on each
# - Demonstrate that the same method call behaves differently
# ============================================================

from abc import ABC, abstractmethod


class Animal:
    def make_sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def make_sound(self):
        print("Dog makes a sound")

class Cat(Animal):
    def make_sound(self):
        print("Cat makes a sound")

animals = [Dog(), Dog(), Cat()]
for animal in animals:
    animal.make_sound()

# ============================================================
# 🎭 Polymorphism via Duck Typing
# ------------------------------------------------------------
# - Define two unrelated classes that both have the same method (e.g., draw())
# - Write a function that calls that method on any object
# - Pass different objects into the function
# - Show that Python doesn’t require inheritance — “if it quacks like a duck…”
# ============================================================

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Drawable):
    def draw(self):
        print("Drawing a circle")

class Square(Drawable):
    def draw(self):
        print("Drawing a square")

def draw_shape(shape):
    shape.draw()

draw_shape(Circle())
draw_shape(Square())

# ============================================================
# 🔁 Polymorphism in Function Parameters
# ------------------------------------------------------------
# - Create a function that accepts an object (e.g., animal_action(obj))
# - Inside, call the common method (e.g., obj.make_sound())
# - Pass in various objects with that method
# - Demonstrate flexibility in code reusability
# ============================================================

class Animal:
    def make_sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def make_sound(self):
        print("Dog makes a sound")

class Cat(Animal):
    def make_sound(self):
        print("Cat makes a sound")

class Tofu:
    def is_delicious(self):
        print("Tofu is delicious")

def animal_action(animal):
    animal.make_sound()

animals = [Dog(), Cat(), Tofu()]
for animal in animals:
    if hasattr(animal, "make_sound"):
        animal_action(animal)
    else:
        print("This is not an animal")

# ============================================================
# 🧱 Polymorphism + Inheritance + Abstract Base Class
# ------------------------------------------------------------
# - Use abc.ABC to define an abstract base class with an abstract method
# - Subclasses implement the abstract method
# - Show polymorphic behavior by calling the method on instances of subclasses
# - Optional: raise NotImplementedError if base method is used directly
# ============================================================
