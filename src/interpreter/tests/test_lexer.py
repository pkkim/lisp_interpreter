from unittest import TestCase

from interpreter.lexer import lex
from interpreter.lexer import Token as T, TokenType as TT


class TestLexer(TestCase):

    def tests(self):
        for test_case, expected in [
            ('', []),
            ('\'', [T(TT.QUOTE)]),
            ('()', [T(TT.OPEN_PAREN), T(TT.CLOSE_PAREN)])
        ]:
            actual = lex(test_case)
            assert actual == expected
