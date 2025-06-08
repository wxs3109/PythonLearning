class Person:
    species = "Human"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # ✅ Class method: knows the class, often used for alternative constructors
    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = 2024
        age = current_year - birth_year
        return cls(name, age) # cls is the class itself

    # ✅ Static method: utility function, no access to class or instance
    @staticmethod
    def is_adult(age):
        return age >= 18


# Using class method to create an object
person1 = Person.from_birth_year("Alice", 2000)
print(person1.name)       # Alice
print(person1.age)        # 24
print(person1.species)    # Human

# Using static method for a utility check
print(Person.is_adult(20))  # True
print(Person.is_adult(15))  # False
