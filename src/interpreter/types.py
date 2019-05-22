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

    # Not given by keywords, need to be figured out
    BLOCK = 'block'
    APPLY = 'apply'
    LIST = 'list'  # for quoted lists or the first arg to lambda

    # keywords
    IF = 'if'
    LAMBDA = 'lambda'
    SET = 'set'
    DEF = 'def'

    # builtins should only be distinguished at evaluation (need to prevent
    # assigning to them)
    # e.g. nil, car, cdr, cons, list


@attr.s(auto_attribs=True, slots=True)
class Node:
    variant: NodeType
    value: Any

