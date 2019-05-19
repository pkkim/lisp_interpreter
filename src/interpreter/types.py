from enum import Enum
from typing import Any

import attr


class TokenType:
    # Syntactic elements
    OPEN_PAREN = 'open_paren'
    CLOSE_PAREN = 'close_paren'
    QUOTE = 'quote'
    SEMICOLON = 'semicolon'

    # Atomic types (a variable is an unquoted string; QUOTE + STRING -> normal
    # string; otherwise a STRING is a variable)
    NUMBER = 'number'
    STRING = 'string'


@attr.s(auto_attribs=True, slots=True)
class Token:
    variant: TokenType
    value: Any = None


class NodeType(Enum):
    NUMBER = 'number'
    VARIABLE = 'variable'
    STRING = 'string'
    LIST = 'list'
    BLOCK = 'block'
    IF = 'if'
    LAMBDA = 'lambda'
    SET = 'set'
    APPLY = 'apply'
    DEF = 'def'


@attr.s(auto_attribs=True, slots=True)
class Node:
    variant: NodeType
    value: Any

