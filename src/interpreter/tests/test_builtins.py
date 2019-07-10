import pytest

from interpreter.builtin_handlers import handle
from interpreter.types import (
    Value as V, ValueType as VT, Cons
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
    ('&&', [V(VT.BOOLEAN, True), V(VT.BOOLEAN, False)], False),
    ('&&', [V(VT.BOOLEAN, True), V(VT.NUMBER, 3)], True),
    ('&&', [V(VT.BOOLEAN, True), V(VT.NUMBER, 0)], False),
    ('&&', [V(VT.NUMBER, 0)], False),
    ('||', [V(VT.NUMBER, 0)], False),
    ('||', [V(VT.NUMBER, 0), V(VT.STRING, ''), V(VT.BOOLEAN, False)], False),
    ('||', [V(VT.NUMBER, 0), V(VT.STRING, ''), V(VT.BOOLEAN, True)], True),
    ('!', [V(VT.NUMBER, 0)], True),
    ('!', [V(VT.NUMBER, 1)], False),
    ('!', [V(VT.BOOLEAN, True)], False),
    ('<', [V(VT.NUMBER, 0), V(VT.NUMBER, 3)], True),
    ('<', [V(VT.NUMBER, 3), V(VT.NUMBER, 0)], False),
    ('<', [V(VT.NUMBER, 0), V(VT.NUMBER, 0)], False),
    ('>', [V(VT.NUMBER, 0), V(VT.NUMBER, 3)], False),
    ('>', [V(VT.NUMBER, 3), V(VT.NUMBER, 0)], True),
    ('>', [V(VT.NUMBER, 0), V(VT.NUMBER, 0)], False),
    ('<=', [V(VT.NUMBER, 0), V(VT.NUMBER, 3)], True),
    ('<=', [V(VT.NUMBER, 3), V(VT.NUMBER, 0)], False),
    ('<=', [V(VT.NUMBER, 0), V(VT.NUMBER, 0)], True),
    ('>=', [V(VT.NUMBER, 0), V(VT.NUMBER, 3)], False),
    ('>=', [V(VT.NUMBER, 3), V(VT.NUMBER, 0)], True),
    ('>=', [V(VT.NUMBER, 0), V(VT.NUMBER, 0)], True),
]


@pytest.mark.parametrize('op,test_case,expected', boolean_testdata)
def test_boolean(op, test_case, expected):
    assert handle(op, test_case) == V(VT.BOOLEAN, expected)


@pytest.mark.parametrize('op,test_case,expected', [
    ('cons', [V(VT.NUMBER, 4), V(VT.NUMBER, 5)],
        V(VT.CONS, Cons(V(VT.NUMBER, 4), V(VT.NUMBER, 5)))),
    ('car', [V(VT.CONS, Cons(V(VT.NUMBER, 4), V(VT.NUMBER, 5)))],
        V(VT.NUMBER, 4)),
    ('cdr', [V(VT.CONS, Cons(V(VT.NUMBER, 4), V(VT.NUMBER, 5)))],
        V(VT.NUMBER, 5)),
])
def test_cons(op, test_case, expected):
    assert handle(op, test_case) == expected


@pytest.mark.parametrize('test_case', [
    ([]),
    ([[]]),
    ([[], []]),
    ([[V(VT.NUMBER, 34), V(VT.STRING, 'x')], [], [], [V(VT.BOOLEAN, True)]]),
])
def test_concat(test_case):
    conses = [V.list_to_cons(l) for l in test_case]
    expected = []
    for sublist in test_case:
        expected.extend(sublist)
    assert V.list_to_cons(expected) == handle('concat', conses)


def test_set_car_cdr():
    cons = V(VT.CONS, Cons(V(VT.NUMBER, 1), V(VT.NUMBER, 2)))
    handle('set_car', [cons, V(VT.BOOLEAN, True)])
    assert cons.value.car == V(VT.BOOLEAN, True)
    handle('set_cdr', [cons, V(VT.BOOLEAN, False)])
    assert cons.value.cdr == V(VT.BOOLEAN, False)
