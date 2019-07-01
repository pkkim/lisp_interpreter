import pytest

from interpreter.types import (
    Value as V, ValueType as VT, LambdaValue, Cons,
)


list_testdata = [
    ('one', [V(VT.NUMBER, 1)]),
    ('multiple', [V(VT.NUMBER, 4), V(VT.STRING, 'h')]),
]


@pytest.mark.parametrize('op,test_case', list_testdata)
def test_list(op, test_case):
    cons = V.list_to_cons(test_case)
    for x in cons:
        print('x:', x)
    # for from_cons, from_list in zip(cons, test_case):
    #     print('point 2')
    #     assert from_cons == from_list
