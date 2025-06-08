# Input and Output

#  input() is used to get input from the user
#  print() is used to print output to the user

name = input("Enter your name: ")
print("Hello, " + name + "!")

#  input() returns a string, so we need to convert it to an integer if we want to use it in a calculation
age = int(input("Enter your age: "))
print("You are " + str(age) + " years old.")