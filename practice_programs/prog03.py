# Prog03: Create a program that ask user to input 2 numbers. Print the sum of the two numbers.

while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        print(num1 + num2)
        break

    except ValueError:
        print("Please enter a valid number.")
        continue