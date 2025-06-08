# yield from examples
# yield_from_example.py

# ============================================================
# 📘 What is `yield from`?
# ------------------------------------------------------------
# - `yield from` delegates part of a generator to another iterable or generator
# - It simplifies looping over sub-generators or nested iterables
# - Helps flatten nested generator calls
# ============================================================


# ============================================================
# 🧪 1. Basic Example with List
# ------------------------------------------------------------
# - `yield from` works like: for x in iterable: yield x
# ============================================================

def generator_one():
    yield from [1, 2, 3]
    yield from (4, 5)

for val in generator_one():
    print("Value:", val)
# Output: 1 2 3 4 5


# ============================================================
# 🔗 2. Delegating to Another Generator
# ------------------------------------------------------------
# - Call another generator using `yield from`
# - Cleaner than nesting multiple for-loops
# ============================================================

def sub_generator():
    yield "A"
    yield "B"

def main_generator():
    yield "Start"
    yield from sub_generator()  # Delegates to sub_generator
    yield "End"

for item in main_generator():
    print(item)
# Output: Start A B End


# ============================================================
# 🧪 3. Recursive Flattening Generator
# ------------------------------------------------------------
# - Recursively flatten nested lists using yield from
# ============================================================

def flatten(items):
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, [3, 4], 5], 6]
for x in flatten(nested):
    print("Flattened:", x)
# Output: 1 2 3 4 5 6


# ============================================================
# ✅ Summary
# ------------------------------------------------------------
# - `yield from <iterable>` is a shortcut for looping and yielding
# - Useful for flattening, delegating, and composing generators
# ============================================================
