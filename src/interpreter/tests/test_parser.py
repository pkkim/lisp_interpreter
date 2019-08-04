from unittest import TestCase

from interpreter.parser import Parser
from interpreter.types import Node as N, NodeType as NT, Token as T, \
    TokenType as TT


def test_single():
    for test_case, expected in [
        # variable
        ([T(TT.STRING, 'x')], N(NT.VARIABLE, 'x')),
        # number
        ([T(TT.NUMBER, 5)], N(NT.NUMBER, 5)),
        # quoted string
        ([T(TT.QUOTE), T(TT.STRING, 'abc')], N(NT.STRING, 'abc')),
        # bool
        ([T(TT.STRING, 'true')], N(NT.BOOLEAN, True)),
        # quoted list
        ([
            T(TT.QUOTE), T(TT.OPEN_PAREN),
            T(TT.STRING, 'x'), T(TT.STRING, 'yz'), T(TT.NUMBER, 99),
            T(TT.CLOSE_PAREN),
        ], N(
            NT.LIST, [N(NT.STRING, 'x'), N(NT.STRING, 'yz'),
            N(NT.NUMBER, 99)],
        )),
        # lambda
        ([
            T(TT.OPEN_PAREN),
                T(TT.STRING, 'lambda'),
                T(TT.OPEN_PAREN),
                    T(TT.STRING, 'x'), T(TT.STRING, 'yz'), 
                T(TT.CLOSE_PAREN),
                T(TT.OPEN_PAREN),
                    T(TT.STRING, 'f'), T(TT.STRING, 'yz'),
                    T(TT.STRING, 'x'), 
                T(TT.CLOSE_PAREN),
            T(TT.CLOSE_PAREN),
        ], N(NT.LAMBDA, [
            N(NT.LIST, [N(NT.STRING, 'x'), N(NT.STRING, 'yz')]),
            N(NT.APPLY, [
                N(NT.VARIABLE, 'f'),
                N(NT.VARIABLE, 'yz'),
                N(NT.VARIABLE, 'x'),
            ])
        ])),
        ([
            T(TT.OPEN_PAREN),
                T(TT.STRING, 'lambda'),
                T(TT.OPEN_PAREN),
                    T(TT.STRING, 'x'), T(TT.STRING, 'yz'), 
                T(TT.CLOSE_PAREN),
                T(TT.NUMBER, 3),
            T(TT.CLOSE_PAREN),
        ], N(NT.LAMBDA, [
            N(NT.LIST, [N(NT.STRING, 'x'), N(NT.STRING, 'yz')]),
            N(NT.NUMBER, 3)
        ])),
        # nested quoted list
        ([
            T(TT.QUOTE), T(TT.OPEN_PAREN),
            T(TT.QUOTE), T(TT.STRING, 'x'), T(TT.STRING, 'yz'),
            T(TT.CLOSE_PAREN),
        ], N(
            NT.LIST, [N(NT.STRING, 'x'), N(NT.STRING, 'yz')],
        )),
        # if
        ([
            T(TT.OPEN_PAREN),
                T(TT.STRING, 'if'),
                T(TT.STRING, 'a'),
                T(TT.OPEN_PAREN),
                    T(TT.STRING, 'f'), T(TT.NUMBER, 34.3),
                T(TT.CLOSE_PAREN),
                T(TT.STRING, 'y'),
            T(TT.CLOSE_PAREN),
        ], N(
            NT.IF,
            [
                N(NT.VARIABLE, 'a'),
                N(NT.APPLY, [N(NT.VARIABLE, 'f'), N(NT.NUMBER, 34.3)]),
                N(NT.VARIABLE, 'y'),
            ],
        )),
        # block; set
        ([
            T(TT.OPEN_PAREN),
                T(TT.STRING, 'f'),
            T(TT.SEMICOLON),
                T(TT.OPEN_PAREN),
                    T(TT.STRING, 'set'),
                    T(TT.STRING, 'g'),
                    T(TT.QUOTE), T(TT.STRING, 'mystring'),
                T(TT.CLOSE_PAREN),
            T(TT.SEMICOLON),
                T(TT.OPEN_PAREN),
                    T(TT.STRING, 'def'),
                    T(TT.STRING, 'x'),
                    T(TT.OPEN_PAREN),
                        T(TT.STRING, 'zeroaryfn'),
                    T(TT.CLOSE_PAREN),
                T(TT.CLOSE_PAREN),
            T(TT.SEMICOLON),
                T(TT.NUMBER, 4),
            T(TT.CLOSE_PAREN),
        ], N(NT.BLOCK, [
            N(NT.VARIABLE, 'f'),
            N(NT.SET, [N(NT.VARIABLE, 'g'), N(NT.STRING, 'mystring')]),
            N(NT.DEF, [
                N(NT.VARIABLE, 'x'),
                N(NT.APPLY, [N(NT.VARIABLE, 'zeroaryfn')]),
            ]),
            N(NT.NUMBER, 4),
        ])),
        # TODO: nested quoted stuff, all the keywords besides lambd
        # ('\'();', [
        #     T(TT.QUOTE), T(TT.OPEN_PAREN), T(TT.CLOSE_PAREN), 
        #     T(TT.SEMICOLON),
        # ]),
        # (' 3.5 abc', [T(TT.NUMBER, 3.5), T(TT.STRING, 'abc')]),
        # ('abc;(', [
        #     T(TT.STRING, 'abc'), T(TT.SEMICOLON), T(TT.OPEN_PAREN),
        # ]),
    ]:
        actual = Parser().parse(test_case)
        assert actual == [expected]


def test_multiple():
    assert (Parser().parse([T(TT.STRING, 'x'), T(TT.STRING, 'x')]) ==
            [N(NT.VARIABLE, 'x'), N(NT.VARIABLE, 'x')])
