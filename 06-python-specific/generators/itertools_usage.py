# itertools_generators.py

import itertools

# ============================================================
# 🔧 What is itertools?
# ------------------------------------------------------------
# - Built-in Python module for efficient looping and generator tools
# - All functions return **iterators** (lazy, memory-efficient)
# - Works well with generators and large datasets
# ============================================================


# ============================================================
# 🧮 1. itertools.count()
# ------------------------------------------------------------
# - Infinite counter starting from a value
# - Use break to stop manually
# ============================================================

for i in itertools.count(10, step=2):  # 10, 12, 14, ...
    print("Count:", i)
    if i >= 20:
        break


# ============================================================
# 🔁 2. itertools.cycle()
# ------------------------------------------------------------
# - Cycles through a sequence infinitely
# ============================================================

counter = 0
for item in itertools.cycle(["A", "B", "C"]):
    print("Cycle:", item)
    counter += 1
    if counter >= 6:
        break


# ============================================================
# 🔄 3. itertools.repeat()
# ------------------------------------------------------------
# - Repeats a value (infinitely or fixed times)
# ============================================================

for item in itertools.repeat("Hello", 3):
    print("Repeat:", item)


# ============================================================
# 🧪 4. itertools.chain()
# ------------------------------------------------------------
# - Combine multiple iterables into one sequence
# ============================================================

a = [1, 2]
b = [3, 4]
c = (5, 6)

for x in itertools.chain(a, b, c):
    print("Chained:", x)


# ============================================================
# 🔍 5. itertools.islice()
# ------------------------------------------------------------
# - Slice an infinite or large generator like a list
# ============================================================

infinite_numbers = itertools.count(100)
sliced = itertools.islice(infinite_numbers, 5)  # Take first 5

for x in sliced:
    print("Sliced:", x)


# ============================================================
# 🧹 6. itertools.compress()
# ------------------------------------------------------------
# - Filters data by selectors (True/False)
# ============================================================

data = ['a', 'b', 'c', 'd']
selectors = [1, 0, 1, 0]

for x in itertools.compress(data, selectors):
    print("Compressed:", x)


# ============================================================
# ⚙️ 7. itertools.product()
# ------------------------------------------------------------
# - Cartesian product of input iterables
# ============================================================

for p in itertools.product([1, 2], ['a', 'b']):
    print("Product:", p)


# ============================================================
# ✅ Summary
# ------------------------------------------------------------
# - itertools provides high-performance building blocks
# - Use with generators to create powerful, memory-efficient pipelines
# ============================================================
