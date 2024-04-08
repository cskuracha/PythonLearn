import pytest
import source.shapes as shapes

@pytest.mark.parametrize("side_length,expected_area",[(2,4),(3,9),(4,16),(5,25),(6,36),(7,49)])
def test_multiple_square_area(side_length, expected_area):
    assert shapes.Square(side_length).area() == expected_area

@pytest.mark.parametrize("side_length, expected_perimeter",[(2,8),(3,12),(4,16),(5,20)])
def test_multiple_square_perimeter(side_length, expected_perimeter):
    assert shapes.Square(side_length).perimeter() == expected_perimeter