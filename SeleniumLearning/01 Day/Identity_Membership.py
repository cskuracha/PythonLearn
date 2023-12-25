########### Identity Operators #####################
num1 = 10
num2 = 12
print(num1 is num2)
print(num1 is not num2)
num3 = num1
print(num1 is num3)
print(num1 is not num3)

################### Membership Operators ##########################

lst1 = [0,1,2,3,4,5,6,7,8,9]
x = 10
if x in lst1:
    print(f"{x} is in lst1")
elif x not in lst1:
    print(f"{x} is not in lst1")
