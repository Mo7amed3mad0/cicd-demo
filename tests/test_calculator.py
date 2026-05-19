"""
Unit Tests for Calculator App
Pytest-based tests - CI/CD Pipeline Demo
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from calculator import add, subtract, multiply, divide, power


class TestAdd:
    def test_add_positive_numbers(self):
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert add(-1, -4) == -5

    def test_add_zero(self):
        assert add(0, 5) == 5

    def test_add_floats(self):
        assert add(1.5, 2.5) == 4.0


class TestSubtract:
    def test_subtract_basic(self):
        assert subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        assert subtract(3, 7) == -4

    def test_subtract_zero(self):
        assert subtract(5, 0) == 5


class TestMultiply:
    def test_multiply_positive(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0

    def test_multiply_negative(self):
        assert multiply(-3, 4) == -12


class TestDivide:
    def test_divide_basic(self):
        assert divide(10, 2) == 5.0

    def test_divide_float_result(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)


class TestPower:
    def test_power_basic(self):
        assert power(2, 8) == 256

    def test_power_zero_exp(self):
        assert power(5, 0) == 1

    def test_power_negative_base(self):
        assert power(-2, 3) == -8
