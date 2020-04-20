import pytest


def test_new_employee(new_employee):
    """
    GIVEN an employee model
    WHEN that employee is created
    THEN employee has necessary attributes
    """
    assert new_employee.email == "test_employee@yahoo.com"
