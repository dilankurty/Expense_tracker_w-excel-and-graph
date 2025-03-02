# Prog02: Create a program that ask user to input 2 numbers. 
# Print "Equal" when the numbers are the same.

while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        if num1 == num2:
            print("EQUAL")

        else:
            print("Not equal")
    
        break

    except ValueError:
        print("Please enter a valid number.")
        continue