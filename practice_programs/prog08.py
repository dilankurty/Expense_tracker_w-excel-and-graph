# Prog08: Create a program that ask user to input 10 numbers. Print how many are odd numbers.

nums = []

for i in range(10):
    while True:
        try:
            num = int(input(f"Enter number {i+1}: "))
            nums.append (num)
            break
        except ValueError:
            print("Please enter an integer.")
            continue   

odd_nums = []
for num in nums:
    if num%2 != 0:
        odd_nums.append(num)
print(f"Odd numbers: {len(odd_nums)}")