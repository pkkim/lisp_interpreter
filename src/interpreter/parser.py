from collections import deque
from typing import Optional, Deque, List, Any

import attr

from .types import Token, TokenType, Value, ValueType, TokenTree, ParseError


def parse(token) -> Value:
    if isinstance(token, TokenTree):
        return Value.list_to_cons([parse(elem) for elem in token.value])
    elif isinstance(token, Token):
        if token.variant == TokenType.NUMBER:
            return Value(ValueType.NUMBER, token.value)
        elif token.variant == TokenType.STRING and token.value in {
            'true', 'false'
        }:
            return Value(ValueType.BOOLEAN, token.value == 'true')
        elif token.variant in (TokenType.STRING, TokenType.OPERATOR):
            return Value(ValueType.STRING, token.value)
    raise ParseError(f'Could not parse value: {token}')
