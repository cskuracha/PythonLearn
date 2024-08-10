import re

text = """
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890
abcdef

.[{()^$|?*+

scaler.com

321-555-4321
123.555.1234

Mr. Varma
Mr Anant
Ms Nandini
Mrs. Singh
Mr. T

test@test.com
test_123@test_123.com

"""
pattern = "\d{3}[.-]\d{3}[.-]\d{4}"
print(re.match(pattern, text))
print(re.search(pattern, text))
print(re.findall(pattern, text))
num = re.finditer(pattern, text)
for i,n in enumerate(num):
    print(i, n.group())

email_pattern = "\w+@\w+\.\w{2,3}"
email = re.finditer(email_pattern, text)
for i,e in enumerate(email):
    print(e.group())