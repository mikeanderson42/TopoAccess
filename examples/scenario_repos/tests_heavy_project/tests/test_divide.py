import pytest

from calc.divide import divide


def test_divide():
    assert divide(6, 3) == 2


def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
