import collections
from typing import Optional, List

import attr

from .types import Token, TokenType, TokenTree, ParseError


def desugar(tokens: List[Token]) -> List[TokenTree]:
    if (tokens.count(Token(TokenType.OPEN_PAREN)) != 
            tokens.count(Token(TokenType.CLOSE_PAREN))):
        raise ParseError('Unbalanced parentheses')

    result = TokenTree()  # actually the value of this will be returned
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

        # handle commas
        if any(isinstance(t, Token) and t.variant == TokenType.THEN
                for t in curr.value):
            new_value = []
            new_value.append(Token(TokenType.STRING, 'block'))
            for t in curr.value:
                if isinstance(t, TokenTree) or t.variant != TokenType.THEN:
                    new_value.append(t)
            curr.value = new_value

        # handle quoting
        if any(isinstance(t, Token) and t.variant == TokenType.QUOTE
                for t in curr.value):
            sugar_level = 0
            new_value = []
            for t in curr.value:
                if isinstance(t, Token) and t.variant == TokenType.QUOTE:
                    sugar_level += 1
                else:
                    to_append = t
                    for _ in range(sugar_level):
                        to_append = TokenTree(
                            [Token(TokenType.STRING, 'quote'), to_append]
                        )
                    new_value.append(to_append)
                    sugar_level = 0
            curr.value = new_value

        for tr in curr.value:
            if isinstance(tr, TokenTree):
                q.append(tr)

    return result.value

