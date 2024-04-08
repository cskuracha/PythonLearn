import source.shapes as shapes


def test_area():
    rectangle = shapes.Rectangle(10, 20)
    assert rectangle.area() == 10 * 20


def test_perimeter():
    rectangle = shapes.Rectangle(10, 20)
    assert rectangle.perimeter() == (10 * 2) + (20 * 2)


def test_area_with_fixtures(my_rectangle):
    assert my_rectangle.area() == 10 * 20


def test_perimeter_with_fixtures(my_rectangle):
    assert my_rectangle.perimeter() == (10 * 2) + (20 * 2)


def test_not_equal(my_rectangle, other_rectangle):
    assert my_rectangle != other_rectangle
