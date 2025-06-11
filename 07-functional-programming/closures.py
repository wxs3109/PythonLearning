# Closures
# what is a closure?
# a closure is a function that remembers the environment in which it was created
# a closure is a function that has access to the variables in the scope in which it was created
# a closure is a function that has access to the variables in the scope in which it was created


def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function


def multiplyer(factor):
    def multiply(number):
        return factor * number
    return multiply

closure = outer_function(10)
print(closure(5))

double = multiplyer(2)
triple = multiplyer(3)

print(double(5))
print(triple(5))





