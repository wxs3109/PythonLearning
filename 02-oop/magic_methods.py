# magic_methods.py

# ============================================================
# ✨ Introduction to Magic Methods (a.k.a. dunder methods)
# ------------------------------------------------------------
# - Magic methods in Python start and end with double underscores (e.g., __init__, __str__)
# - They define how objects behave with built-in functions and operators
# - You’ll implement a custom class (e.g., Book or Vector) to demonstrate them
# ============================================================

class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price
    
    def __str__(self):
        return f"{self.title} by {self.author} (${self.price})"
    
    def __repr__(self): # different from __str__ in that it is used for debugging
        return f"Book('{self.title}', '{self.author}', {self.price})"
    
    def __len__(self):
        return len(self.title)

    def __eq__(self, other):
        print("__eq__ is called")
        return self.title == other.title and self.author == other.author and self.price == other.price

book = Book("The Great Gatsby", "F. Scott Fitzgerald", 10.99)
print(book)
print(repr(book))
print(len(book))



# ============================================================
# 🔧 __init__, __str__, __repr__
# ------------------------------------------------------------
# - __init__: constructor, initializes object attributes
# - __str__: defines user-friendly string, used by print()
# - __repr__: defines developer-friendly string, used in console/debugging
# - Show how print(obj) vs just obj in REPL behaves differently
# ============================================================


# ============================================================
# 🔢 __len__, __getitem__, __setitem__
# ------------------------------------------------------------
# - __len__: make object compatible with len()
# - __getitem__: access items via obj[index]
# - __setitem__: allow setting items via obj[index] = value
# - Implement these on a custom container-like class
# ============================================================

class BookStore:
    def __init__(self):
        self.books = []

    def __len__(self):
        return len(self.books)
    
    def __getitem__(self, index):
        return self.books[index]
    
    def __setitem__(self, index, value):
        self.books[index] = value

book_store = BookStore()
book_store.books.append(Book("The Great Gatsby", "F. Scott Fitzgerald", 10.99))
book_store.books.append(Book("1984", "George Orwell", 12.99))
book_store.books.append(Book("To Kill a Mockingbird", "Harper Lee", 11.99))

print(book_store[0])
print(book_store[1])
print(book_store[2])
print(len(book_store))

# ============================================================
# ➕ ➖ __add__, __sub__, __mul__, etc.
# ------------------------------------------------------------
# - Implement operator overloading (e.g., +, -, *, /) on a class like Vector or Point
# - Define __add__, __sub__, __mul__, __truediv__
# - Show how expressions like a + b call a.__add__(b)
# ============================================================

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other): # how to make sure other is a vector
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Vector can only be added to another vector")
    
    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)


# ============================================================
# ⚖️ __eq__, __lt__, __le__, __gt__, __ge__, __ne__
# ------------------------------------------------------------
# - Define comparison behavior for objects (==, <, <=, >, etc.)
# - Use __eq__ to compare object equality by value instead of identity
# - Implement ordering comparisons for a class (e.g., Student by score)
# ============================================================

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

student1 = Student("Alice", 85)
student2 = Student("Bob", 90)
print(student1 < student2)
print(student1 > student2)
print(student1 == student2)


# ============================================================
# 📦 __contains__, __iter__, __next__
# ------------------------------------------------------------
# - __contains__: allow use of `in` operator
# - __iter__ and __next__: make object iterable (like a custom range or list)
# - Use with a for-loop to demonstrate custom iteration
# ============================================================

class BookStore:
    def __init__(self):
        self.books = []

    def __contains__(self, book):
        return book in self.books

book_store = BookStore()
book_store.books.append(Book("The Great Gatsby", "F. Scott Fitzgerald", 10.99))
book_store.books.append(Book("1984", "George Orwell", 12.99))
book_store.books.append(Book("To Kill a Mockingbird", "Harper Lee", 11.99))

print("The Great Gatsby" in book_store)
print("1984" in book_store)
print("To Kill a Mockingbird" in book_store)

# ============================================================
# 🧹 __enter__, __exit__ (Context Managers)
# ------------------------------------------------------------
# - Implement with statement support (e.g., for file/resource handling)
# - Show how __enter__ and __exit__ work in a class using `with`
# - Optional: use `contextlib` for a simpler version
# ============================================================

# TODO
class BookStore:
    def __init__(self):
        self.books = []

    def __enter__(self):
        print("__enter__ is called")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("__exit__ is called") 
    