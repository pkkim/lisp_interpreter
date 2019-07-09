import pytest

from interpreter.builtin_handlers import handle
from interpreter.types import (
    Value as V, ValueType as VT,
    # LambdaValue, Cons,
)


numerical_testdata = [
    ('+', [], 0),
    ('+', [3, 3], 6),
    ('-', [3, 5], -2),
    ('/', [3, 2], 1.5),
    ('//', [3, 2], 1),
    ('//', [3, -2], -2),
    ('*', [3, -2, 2.5], -15),
    ('*', [], 1),
    ('%', [2, 5], 2),
    ('%', [5, 2], 1),
    ('**', [5, 2], 25),
    ('abs', [-4], 4),
]


@pytest.mark.parametrize('op,test_case,expected', numerical_testdata)
def test_numerical(op, test_case, expected):
    args = [V(VT.NUMBER, a) for a in test_case]
    actual_result = handle(op, args)
    assert actual_result == V(VT.NUMBER, expected)


boolean_testdata = [
    ('=', [V(VT.NUMBER, 5), V(VT.NUMBER, 5), V(VT.NUMBER, 5)], True),
    ('=', [V(VT.BOOLEAN, True), V(VT.NUMBER, 1)], False),
    ('!=', [V(VT.BOOLEAN, True), V(VT.BOOLEAN, False)], True),
]


@pytest.mark.parametrize('op,test_case,expected', boolean_testdata)
def test_boolean(op, test_case, expected):
    assert handle(op, test_case) == V(VT.BOOLEAN, expected)
