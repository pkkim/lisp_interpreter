import pytest
from unittest import TestCase

from interpreter.eval import Environment
from interpreter.types import (
    Node as N, NodeType as NT, Value as V, ValueType as VT,
    LambdaValue, Cons,
)


testdata = [
    ('number', N(NT.NUMBER, 3), V(VT.NUMBER, 3)),
    ('string', N(NT.STRING, 'foo'), V(VT.STRING, 'foo')),
    ('block', N(NT.BLOCK, [
        N(NT.NUMBER, 3), N(NT.STRING, 'foo'), N(NT.STRING, 'bar'),
    ]), V(VT.STRING, 'bar')),
    (
        'list',
        N(NT.LIST, [
            N(NT.STRING, 'x'),
            N(NT.NUMBER, 5.5),
            N(NT.LIST, [N(NT.STRING, 'y')]),
        ]),
        V(VT.CONS, Cons(
          V(VT.STRING, 'x'),
          V(VT.CONS, Cons(
            V(VT.NUMBER, 5.5),
            V(VT.CONS, Cons(
             V(VT.CONS, Cons(
               V(VT.STRING, 'y')))))))))
    ),
    (
        'if',
        N(NT.IF, [
            N(NT.BOOLEAN, True), N(NT.NUMBER, 4), N(NT.NUMBER, 6),
        ]),
        V(VT.NUMBER, 4)
    ),
    (
        'apply inlined lambda',
        N(NT.APPLY, [
            N(NT.LAMBDA, [
                N(NT.LIST, []),
                N(NT.NUMBER, 8),
            ])
        ]),
        V(VT.NUMBER, 8)
    ),
    (
        'set and retrieve number',
        N(NT.BLOCK, [
            N(NT.DEF, [N(NT.VARIABLE, 'x'), N(NT.NUMBER, 4)]),
            N(NT.VARIABLE, 'x'),
        ]),
        V(VT.NUMBER, 4)
    ),
    (
        'apply stored lambda',
        N(NT.BLOCK, [
            # (set f (lambda (x) (x)))
            N(NT.DEF, [N(NT.VARIABLE, 'f'), N(NT.LAMBDA, [
                N(NT.LIST, [N(NT.VARIABLE, 'x')]),
                N(NT.VARIABLE, 'x'),
            ])]),
            # (f 4)
            N(NT.APPLY, [
                N(NT.VARIABLE, 'f'),
                N(NT.STRING, 'arg')
            ])
        ]),
        V(VT.STRING, 'arg'),
    ),
    (
        'addition',
        N(NT.APPLY, [
            N(NT.VARIABLE, '+'),
            N(NT.NUMBER, 3),
            N(NT.NUMBER, 4),
        ]),
        V(VT.NUMBER, 7),
    ),
    # ('\'();', [
    #     T(TT.QUOTE), T(TT.OPEN_PAREN), T(TT.CLOSE_PAREN), 
    #     T(TT.SEMICOLON),
    # ]),
    # ('  ', []),
    # (' 3.5 abc', [T(TT.NUMBER, 3.5), T(TT.STRING, 'abc')]),
    # ('abc;(', [
    #     T(TT.STRING, 'abc'), T(TT.SEMICOLON), T(TT.OPEN_PAREN),
    # ]),
]


@pytest.mark.parametrize('name,test_case,expected', testdata)
def tests(name, test_case, expected):
    environment = Environment()
    actual_result = environment.eval_node(test_case)
    assert actual_result == expected
