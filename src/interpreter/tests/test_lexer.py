import pytest

from interpreter.desugarizer import TokenTree, desugar
from interpreter.lexer import lex, Token as T, TokenType as TT


testdata = [
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
] 


@pytest.mark.parametrize('test_case,expected', testdata)
def test_lexer(test_case, expected):
    actual = lex(test_case)
    assert actual == expected


desugar_testdata = [
    ("(a; b; '(c 4); 'd)", TokenTree([
        T(TT.STRING, 'block'),
        T(TT.STRING, 'a'),
        T(TT.STRING, 'b'),
        TokenTree([
            T(TT.STRING, 'quote'),
            TokenTree([
                T(TT.STRING, 'c'),
                T(TT.NUMBER, 4),
            ]),
        ]),
        TokenTree([
            T(TT.STRING, 'quote'),
            T(TT.STRING, 'd'),
        ])
    ])),
]


@pytest.mark.parametrize('test_case,expected', desugar_testdata)
def test_desugar(test_case, expected):
    lexed = lex(test_case)
    actual = desugar(lexed)
    print(actual)
    assert actual == expected

