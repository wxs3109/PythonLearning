# Pytest Basic Tests
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(-1, -1) == -3

def test_add_strings():
    assert add("hello", "world") == "helloworld"


test_add()
test_add_strings()