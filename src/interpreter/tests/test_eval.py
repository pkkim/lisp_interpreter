from unittest import TestCase

from interpreter.eval import Environment
from interpreter.types import (
    Node as N, NodeType as NT, Value as V, ValueType as VT,
)


class TestEval(TestCase):

    def tests(self):
        for test_case, expected in [
            (N(NT.NUMBER, 3), ([], V(VT.NUMBER, 3))),
            (N(NT.STRING, 'foo'), ([], V(VT.STRING, 'foo'))),
            (N(NT.BLOCK, [
                N(NT.NUMBER, 3), N(NT.STRING, 'foo'), N(NT.STRING, 'bar'),
            ]), ([], V(VT.STRING, 'bar'))),
            (
                N(NT.LIST, [
                    N(NT.STRING, 'x'),
                    N(NT.NUMBER, 5.5),
                    N(NT.LIST, [N(NT.STRING, 'y')]),
                ]),
                ([], V(VT.LIST, [
                    V(VT.STRING, 'x'),
                    V(VT.NUMBER, 5.5),
                    V(VT.LIST, [V(VT.STRING, 'y')])
                ]))
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
        ]:
            environment = Environment()
            actual_result = environment.eval_node(test_case)
            assert (list(environment.scopes), actual_result) == expected
