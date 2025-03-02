# Prog10: Create a program that print all the numbers starting from 0 to 100 except numbers ending in zero.
num = []
for i in range(101):
    if i%10 != 0:
        num.append(i)

print(num)