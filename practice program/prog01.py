# Prog01: Create a program that ask user to input 2 numbers. Print the bigger number.

while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if num1 > num2:
            print(f"The bigger number is {num1}")

        elif num2 > num1:
            print(f"The bigger number is {num2}")

        else:
            print("Both numbers are EQUAL")

        break

    except ValueError:
        print("Please enter a valid number")
        continue

