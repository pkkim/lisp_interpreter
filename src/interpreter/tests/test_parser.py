from unittest import TestCase

from interpreter.parser import Parser
from interpreter.types import Node as N, NodeType as NT, Token as T, \
    TokenType as TT


class TestParser(TestCase):

    def tests(self):
        for test_case, expected in [
            # variable
            ([T(TT.STRING, 'x')], N(NT.VARIABLE, 'x')),
            # number
            ([T(TT.NUMBER, 5)], N(NT.NUMBER, 5)),
            # quoted string
            ([T(TT.QUOTE), T(TT.STRING, 'abc')], N(NT.STRING, 'abc')),
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
            ]))
            # TODO: nested quoted stuff, all the keywords besides lambd
            # ('\'();', [
            #     T(TT.QUOTE), T(TT.OPEN_PAREN), T(TT.CLOSE_PAREN), 
            #     T(TT.SEMICOLON),
            # ]),
            # ('  ', []),
            # (' 3.5 abc', [T(TT.NUMBER, 3.5), T(TT.STRING, 'abc')]),
            # ('abc;(', [
            #     T(TT.STRING, 'abc'), T(TT.SEMICOLON), T(TT.OPEN_PAREN),
            # ]),
        ]:
            actual = Parser().parse(test_case)
            assert actual == expected
