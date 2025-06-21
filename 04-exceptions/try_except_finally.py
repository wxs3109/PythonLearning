# Try-Except-Finally

class MyException(Exception):
    pass





try:
    print("try block")
    raise MyException("This is a test error")
except MyException as e:
    print(f"MyException: {e}")
finally:
    print("finally block")

print("after try-except-finally")