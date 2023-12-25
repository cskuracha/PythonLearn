num1 = 10
num2 = 12

# Greater than
#print(num1 >num2)
if num1 > num2:
    print("Num1 is greater")
else:
    print("Num2 is greater")

# Less than
if num1 < num2:
    print("Num1 is lesser")
else:
    print("Num2 is lesser")

# Equal
if num1 == num2:
    print("Num1 is equal to Num2")
else:
    print("Num1 and Num2 are not equal")

# Not Equal
if num1 != num2:
    print("Num1 is not equal to Num2")
else:
    print("Num1 is equal to Num2")

# Greater Than or equal
if num1 >= num2:
    print("Num1 is greater or equal")
else:
    print("Num2 is greater")

# Less than or equal
if num1 <= num2:
    print("Num1 is less or equal")
else:
    print("Num2 is lesser")

while num1 <= num2:
    print(num1)
    num1 += 1
