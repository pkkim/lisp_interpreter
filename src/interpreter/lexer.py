import string
from typing import Optional, List

import attr

from .types import Token, TokenType


atomic_characters = set(string.ascii_letters + string.digits + '_.')

operator_characters = '+-*/%^&<>=|'


syntactic_tokens = {
    '(': Token(TokenType.OPEN_PAREN),
    ')': Token(TokenType.CLOSE_PAREN),
    '\'': Token(TokenType.QUOTE),
    ',': Token(TokenType.THEN),
}


@attr.s(auto_attribs=True, slots=True, frozen=True)
class InvalidToken(Exception):
    value: str
    char: int = -1


def _operator(s: str):
    if not all(c in operator_characters for c in s):
        return None
    return s


def _number(s: str):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None


def _token_from_state(state: str) -> Optional[Token]:
    if state == '':
        return None
    operator_value = _operator(state)
    if operator_value is not None:
        return Token(TokenType.OPERATOR, operator_value)
    number_value = _number(state)
    if number_value is not None:
        return Token(TokenType.NUMBER, number_value)
    else:
        if state[0].isnumeric():
            raise InvalidToken(state)
        return Token(TokenType.STRING, state)


def lex(s: str) -> List[Token]:
    i = 0
    result = []

    state = ''
    in_number = False
    for i, c in enumerate(s):
        # The operator is continuing
        if c in operator_characters:
            state = state + c
            continue

        # The token is continuing
        if c in atomic_characters:
            state = state + c
            continue

        # Wrap up the current token
        finished_token = _token_from_state(state)

        if finished_token:
            result.append(finished_token)
            state = ''

        # syntactic tokens
        token = syntactic_tokens.get(c, None)
        if token:
            result.append(token)
            continue

    # Wrap up the current token
    try:
        finished_token = _token_from_state(state)
    except InvalidToken as e:
        raise InvalidToken(e.value, char=i) from e
    if finished_token:
        result.append(finished_token)

    return result
