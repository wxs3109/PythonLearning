# ============================================================
# 📘 Python @ Symbol Usage
# ============================================================

# 1. Decorators
# Knowledge:
# - @ is used for decorator syntax
# - Decorators modify or enhance functions/classes
# - Can be stacked (multiple decorators)
# - Can accept arguments

# Basic decorator
def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} finished")
        return result
    return wrapper

@log_function
def add(a, b):
    return a + b

# Decorator with arguments
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

# 2. Property Decorators
# Knowledge:
# - @property for getter methods
# - @x.setter for setter methods
# - @x.deleter for deleter methods
# - Enables controlled attribute access

class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

    @name.deleter
    def name(self):
        del self._name

# 3. Class Decorators
# Knowledge:
# - Modify or enhance classes
# - Can add methods or attributes
# - Can modify class behavior

def add_method(cls):
    def new_method(self):
        return "This is a new method"
    cls.new_method = new_method
    return cls

@add_method
class MyClass:
    pass

# 4. Static and Class Methods
# Knowledge:
# - @staticmethod for utility functions
# - @classmethod for factory methods
# - Don't need instance/class reference

class MathUtils:
    @staticmethod
    def add(x, y):
        return x + y

    @classmethod
    def create_from_string(cls, string):
        x, y = map(int, string.split(','))
        return cls(x, y)

# 5. Abstract Methods
# Knowledge:
# - @abstractmethod for interface definition
# - Forces implementation in subclasses
# - Part of ABC (Abstract Base Classes)

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

# 6. Dataclass Decorator
# Knowledge:
# - @dataclass for automatic method generation
# - Reduces boilerplate code
# - Adds __init__, __repr__, etc.

from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

# 7. Context Manager Decorator
# Knowledge:
# - @contextmanager for context managers
# - Simplifies context manager creation
# - Handles setup and cleanup

from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Setting up resource")
    try:
        yield "resource"
    finally:
        print("Cleaning up resource")

# Example usage
if __name__ == "__main__":
    # Test decorator
    print(add(5, 3))
    
    # Test property
    person = Person("John")
    print(person.name)
    person.name = "Jane"
    print(person.name)
    
    # Test class decorator
    obj = MyClass()
    print(obj.new_method())
    
    # Test static and class methods
    print(MathUtils.add(5, 3))
    
    # Test dataclass
    p = Point(1.0, 2.0)
    print(p)
    
    # Test context manager
    with managed_resource() as resource:
        print(f"Using {resource}") 