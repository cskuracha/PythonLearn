import math

import pytest
import source.shapes as shapes

class TestCircle:

    def setup_method(self, method):
        print(f"Setting up {method}")
        self.Circle = shapes.Circle(10)

    def teardown_method(self, method):
        print(f"Tearing down {method}")
    def test_area(self):
        assert self.Circle.area() == math.pi * self.Circle.radius ** 2

    def test_perimeter(self):
        result = self.Circle.perimeter()
        expected = 2 * math.pi * self.Circle.radius
        assert result == expected