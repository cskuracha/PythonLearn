def add(num1, num2):
    """Function to return addition of two numbers"""
    return num1 + num2


def div(num1, num2):
    """Function to return division of two numbers"""
    return num1 / num2

def div_by_zero(num1, num2):
    """Function to return error when second number is zero else return division"""
    if num2 == 0:
        raise ValueError
    return num1 / num2