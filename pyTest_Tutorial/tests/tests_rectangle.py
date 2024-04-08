import pytest
import source.shapes as shapes

class TestRectangle:

    def test_area(self):
        rectangle = shapes.Rectangle(10, 20)
        assert rectangle.area() == 10 * 20

    def test_perimeter(self):
        rectangle = shapes.Rectangle(10, 20)
        assert rectangle.perimeter() == (10 * 2) + (20 * 2)

    @pytest.fixture
    def my_rectangle(self):
        return shapes.Rectangle(10, 20)

    def test_area_with_fixtures(self, my_rectangle):
        assert my_rectangle.area() == 10 * 20

    def test_perimeter_with_fixtures(self, my_rectangle):
        assert my_rectangle.perimeter() == (10 * 2) + (20 * 2)

    @pytest.fixture
    def other_rectangle(self):
        return shapes.Rectangle(5, 6)

    def test_not_equal(self, my_rectangle, other_rectangle):
        assert my_rectangle != other_rectangle