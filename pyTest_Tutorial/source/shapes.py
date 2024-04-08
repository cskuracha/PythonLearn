import math
class Shapes:

    def area(self):
        pass

    def perimeter(self):
        pass

class Circle(Shapes):

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shapes):

    def __init__(self, length, width):
        self.length = length
        self.width = width

    def __eq__(self, other):
        """Function to check if other is a rectangle"""
        if not isinstance(other, Rectangle):
            return False
        return self.width == other.width and self.length == other.length
    def area(self):
        return self.length * self.width

    def perimeter(self):
        return (self.length * 2) + (self.width * 2)

class Square(Rectangle):
    def __init__(self, side_length):
        super().__init__(side_length, side_length)