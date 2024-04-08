import pytest

import source.functions as functions

def test_add():
    """pyTest test to add functions"""
    result = functions.add(1,2)
    assert result == 3

def test_add_strings():
    """pytest test to test add two strings"""
    result = functions.add("Chaitanya ", "Sagar")
    assert result == "Chaitanya Sagar"

def test_divide():
    """pytest test to divide functions"""
    result = functions.div(10,5)
    assert result == 2

def test_divide_by_zero():
    """pytest test to divide functions with division by zero"""
    with pytest.raises(ZeroDivisionError):
        functions.div(10, 0)

def test_divide_by_zero_for_div_by_zero():
    """pytest test to divided functions with division by zero"""
    with pytest.raises(ValueError): # Since function div_by_zero() raises ValueError when second num is zero
        functions.div_by_zero(10, 0)