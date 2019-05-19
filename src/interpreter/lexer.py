import string
from typing import Optional, List

import attr

from .types import Token, TokenType


atomic_characters = set(string.ascii_letters + string.digits + '_')


syntactic_tokens = {
    '(': Token(TokenType.OPEN_PAREN),
    ')': Token(TokenType.CLOSE_PAREN),
    '\'': Token(TokenType.QUOTE),
    ';': Token(TokenType.SEMICOLON),
}


@attr.s(auto_attribs=True, slots=True)
class InvalidToken(Exception):
    value: str
    char: int = -1


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
    number_value = _number(state)
    if number_value:
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
        if c in atomic_characters:
            state = state + c
            continue

        # syntactic tokens
        token = syntactic_tokens.get(c, None)
        if token:
            try:
                finished_token = _token_from_state(state)
            except InvalidToken as e:
                e.char = i
                raise

            if finished_token:
                result.append(finished_token)
            result.append(token)
            continue
    return result
