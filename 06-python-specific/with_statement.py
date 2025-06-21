# ============================================================
# 📘 Python with Statement Usage
# ============================================================

# 1. Basic File Operations
# Knowledge:
# - Automatically handles file closing
# - Ensures resources are properly released
# - Exception-safe file handling

# Reading a file
with open('example.txt', 'r') as file:
    content = file.read()
    # File automatically closes after the block

# Writing to a file
with open('output.txt', 'w') as file:
    file.write('Hello, World!')
    # File automatically closes after the block

# 2. Multiple Context Managers
# Knowledge:
# - Can use multiple with statements
# - Resources are released in reverse order
# - All resources are properly managed

with open('input.txt', 'r') as source, open('output.txt', 'w') as destination:
    content = source.read()
    destination.write(content)

# 3. Custom Context Managers
# Knowledge:
# - Create custom context managers using classes
# - Implement __enter__ and __exit__ methods
# - Handle setup and cleanup

class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self):
        print("Connecting to database...")
        # Simulate connection
        self.connection = "Connected"
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        self.connection = None
        if exc_type:
            print(f"An error occurred: {exc_val}")
            return False  # Re-raise the exception
        return True  # Suppress the exception

# Using custom context manager
with DatabaseConnection("my_db") as db:
    print(f"Using database: {db}")
    # Database automatically closes after the block

# 4. Context Manager Decorator
# Knowledge:
# - Use @contextmanager decorator
# - Simpler way to create context managers
# - Uses generator functions

from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield
    end = time.time()
    print(f"Operation took {end - start} seconds")

# Using context manager decorator
with timer():
    # Your code here
    import time
    time.sleep(1)

# 5. Error Handling in with
# Knowledge:
# - with blocks handle exceptions
# - Resources are still properly cleaned up
# - Can suppress or re-raise exceptions

class ErrorHandler:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"Handled ValueError: {exc_val}")
            return True  # Suppress the exception
        return False  # Re-raise other exceptions

# Example usage
with ErrorHandler():
    raise ValueError("This error will be handled")

# 6. Common Use Cases
# Knowledge:
# - File operations
# - Database connections
# - Network connections
# - Locks and synchronization
# - Temporary changes

# Example: Temporary directory
import tempfile
import os

with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Created temporary directory: {temp_dir}")
    # Directory is automatically deleted after the block

# Example: Lock
from threading import Lock

lock = Lock()
with lock:
    # Critical section
    print("This code is thread-safe")

# Example: Changing directory
import os

class ChangeDirectory:
    def __init__(self, path):
        self.path = path
        self.old_path = None

    def __enter__(self):
        self.old_path = os.getcwd()
        os.chdir(self.path)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_path)

# Using the context manager
with ChangeDirectory("/tmp"):
    print(f"Current directory: {os.getcwd()}")
    # Directory is automatically changed back after the block

# Example usage
if __name__ == "__main__":
    # Test custom context manager
    with DatabaseConnection("test_db") as db:
        print(f"Using database: {db}")
    
    # Test timer
    with timer():
        import time
        time.sleep(1)
    
    # Test error handling
    with ErrorHandler():
        raise ValueError("Test error") 