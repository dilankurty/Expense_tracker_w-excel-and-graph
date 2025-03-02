# Prog05: Create a program that ask user to input 2 numbers. 
# Print the quotient of the two numbers with the decimal point

while True:
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        if num2 == 0:
            print("Cannot divide by zero.")
            continue 

        elif num2 != 0:
            print(num1 / num2)
            break
        
    except ValueError:
        print("Please enter a valid number.")
        continue