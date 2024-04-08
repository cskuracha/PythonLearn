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