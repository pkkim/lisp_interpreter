from unittest import TestCase

from interpreter.lexer import lex
from interpreter.lexer import Token as T, TokenType as TT


class TestLexer(TestCase):

    def tests(self):
        for test_case, expected in [
            ('', []),
            ('\'();', [
                T(TT.QUOTE), T(TT.OPEN_PAREN), T(TT.CLOSE_PAREN), 
                T(TT.SEMICOLON),
            ]),
            ('  ', []),
            (' 3.5 abc', [T(TT.NUMBER, 3.5), T(TT.STRING, 'abc')]),
            ('abc;(', [
                T(TT.STRING, 'abc'), T(TT.SEMICOLON), T(TT.OPEN_PAREN),
            ]),
        ]:
            actual = lex(test_case)
            assert actual == expected
