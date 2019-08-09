import collections
from typing import Optional, List, Union

import attr

from .types import Token, TokenType


@attr.s(auto_attribs=True, slots=True)
class TokenTree:
    value: List[Union['TokenTree', Token]] = attr.ib(factory=lambda: [])


def desugar(tokens: List[Token]) -> TokenTree:
    result = TokenTree()
    curr = result
    parents = collections.deque()
    for token in tokens:
        if token.variant == TokenType.OPEN_PAREN:
            parents.append(curr)
            child = TokenTree()
            curr.value.append(child)
            curr = child
        elif token.variant == TokenType.CLOSE_PAREN:
            curr = parents.pop()
        else:
            curr.value.append(token)

    # traverse result and replace sugar
    q = collections.deque()
    q.append(result)
    while q:
        # TODO should catch syntax errors here
        curr = q.pop()
        print('curr:', curr)

        # handle semicolons
        if any(isinstance(t, Token) and t.variant == TokenType.SEMICOLON
                for t in curr.value):
            print('in if')
            new_value = []
            new_value.append(Token(TokenType.STRING, 'block'))
            for t in curr.value:
                if isinstance(t, TokenTree) or t.variant != TokenType.SEMICOLON:
                    new_value.append(t)
            curr.value = new_value

        # handle quoting
        if any(isinstance(t, Token) and t.variant == TokenType.QUOTE
                for t in curr.value):
            new_value = []
            i = 0
            while i < len(curr.value):
                t = curr.value[i]
                if isinstance(t, Token) and t.variant == TokenType.QUOTE:
                    replacement = TokenTree(
                        [Token(TokenType.STRING, 'quote'), curr.value[i+1]],
                    )
                    new_value.append(replacement)
                    i += 1
                else:
                    new_value.append(t)
                i += 1
            curr.value = new_value

        for tr in curr.value:
            if isinstance(tr, TokenTree):
                q.append(tr)

    assert len(result.value) == 1
    return result.value[0]

