# ============================================================
# 📘 Custom Exceptions and Error Handling
# ============================================================

# 1. Basic Custom Exception
# Knowledge: Creating custom exception classes
# Task: Create a custom exception for invalid age
class InvalidAgeError(Exception):
    def __init__(self, age):
        super().__init__(f"Invalid age: {age}, must be between 0 and 120")

# 2. Exception with Additional Data
# Knowledge: Adding custom attributes to exceptions
# Task: Create an exception that carries additional data
class ValidationError(Exception):
    def __init__(self, message, field, value):
        self.field = field
        self.value = value
        super().__init__(f"{message} (field: {field}, value: {value})")

# 3. Exception Hierarchy
# Knowledge: Creating a hierarchy of custom exceptions
# Task: Create a base exception and specific subclasses
class DatabaseError(Exception):
    pass

class ConnectionError(DatabaseError):
    pass

class QueryError(DatabaseError):
    pass

# 4. Exception with Custom Methods
# Knowledge: Adding methods to custom exceptions
# Task: Create an exception with helper methods
class ConfigurationError(Exception):
    def __init__(self, message, config_file):
        self.config_file = config_file
        super().__init__(message)
    
    def get_config_path(self):
        return self.config_file
    
    def is_critical(self):
        return "critical" in str(self).lower()

# 5. Exception Factory
# Knowledge: Creating exceptions dynamically
# Task: Create a function that generates appropriate exceptions
def create_validation_error(field, value, rules):
    # Your code here
    pass
