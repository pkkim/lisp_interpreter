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
    BOOLEAN = 'boolean'  # only 'true' and 'false'

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


class ValueType(Enum):
    NUMBER = 'number'
    STRING = 'string'
    LIST = 'list'
    LAMBDA = 'lambda'
    BOOLEAN = 'boolean'


@attr.s(auto_attribs=True, slots=True)
class Value:
    type_: ValueType
    # for LAMBDA, it's a tuple with first arg the representation of the lambda,
    # and the second is the list of scopes
    # In turn, the first argument is the list of arguments, and the second is
    # the body.
    value: Any
