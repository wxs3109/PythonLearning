# Abstraction

# abc is a module that provides the abstract base class for creating abstract classes
from abc import ABC, abstractmethod, abstractproperty

# abstract class is a class that cannot be instantiated, but can be subclassed
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def make_sound(self):
        print("Dog makes a sound")

class Cat(Animal):
    def make_sound(self):
        print("Cat makes a sound")

dog = Dog()
dog.make_sound()

cat = Cat()
cat.make_sound()

# animal = Animal() # This will  raise an error because Animal is an abstract class
# print(animal.make_sound())
# animal = Animal()
# animal.make_sound()

# abstract properties are properties that are not implemented in the abstract class, but must be implemented in the subclass
class Animal(ABC):
    @abstractproperty       
    def make_sound(self):
        pass

class Dog(Animal):
    @property
    def make_sound(self):
        return "Dog makes a sound"

dog = Dog()
print(dog.make_sound)