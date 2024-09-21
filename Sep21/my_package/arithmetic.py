def add(a,b):
    """
    Adding two number
    :param a:
    :param b:
    :return: a + b
    """
    return a + b

def subtract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    if b == 0:
        return 0
    return a / b

def average(a,b):
    return (a + b) /2

def power(a,b):
    return a ** b


if __name__ == "__main__":
    print(add(2,3))
    print(subtract(2, 3))
    print(multiply(2, 3))

