# Prog06: Create a program that ask user to input 2 numbers. 
# Print the result when the first number is raised to the second number.

while True:
    try:
        num = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        print(num ** num2)
        break
    
    except ValueError:
        print("Please enter a valid number")
        continue