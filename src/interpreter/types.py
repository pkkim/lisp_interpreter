from enum import Enum, auto
from typing import Any, List, Dict, Optional, Union

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
    OPERATOR = 'operator'


@attr.s(auto_attribs=True, slots=True)
class Token:
    variant: TokenType
    value: Any = None


@attr.s(auto_attribs=True, slots=True)
class TokenTree:
    value: List[Union[Token, 'TokenTree']] = attr.ib(factory=lambda: [])


class ValueType(Enum):
    # Node types:
    NUMBER = 'number'
    STRING = 'string'
    BOOLEAN = 'boolean'
    CONS = 'cons'

    # Non-node types
    LAMBDA = 'lambda'
    NIL = 'nil'
    QUOTED = 'quoted'


class LispTypeError(Exception):
    pass


@attr.s(auto_attribs=True, slots=True)
class Value:
    variant: ValueType
    # for LAMBDA, it's a tuple with first arg the representation of the lambda,
    # and the second is the local scope
    # In turn, the first argument is the list of arguments, and the second is
    # the body.
    value: Any = None

    def __eq__(self, other) -> bool:
        if self.variant != other.variant:
            return False

        if self.variant in {
            ValueType.NIL,
            ValueType.NUMBER,
            ValueType.STRING,
            ValueType.BOOLEAN,
        }:
            return self.value == other.value
        elif self.variant in {ValueType.CONS, ValueType.LAMBDA}:
            return self is other
        else:
            raise NotImplemented(f'Equality not defined for {self.variant}.')

    def __bool__(self) -> bool:
        if self.variant == ValueType.NUMBER:
            return self.value != 0
        elif self.variant == ValueType.STRING:
            return self.value != ''
        elif self.variant == ValueType.BOOLEAN:
            return self.value
        elif self.variant in (ValueType.CONS, ValueType.BOOLEAN):
            return True
        elif self.variant == ValueType.NIL:
            return False
        else:
            raise NotImplemented(f'Truthiness not defined for {self.variant}.')

    def _value_comparison(f):
        def wrapped(v1, v2):
            if v1.variant != v2.variant:
                raise LispTypeError(
                    f'Args to {f.__name__} must have same type but got: '
                    f'{v1}, {v2}' 
                )
            elif v1.variant in (ValueType.CONS, ValueType.BOOLEAN):
                raise LispTypeError(
                    f'Cannot compare values of type {v1.variant}.'
                )
            return f(v1, v2)
        return wrapped

    @_value_comparison
    def __lt__(self, other):
        return super().__lt__(self, other)

    @_value_comparison
    def __lte__(self, other):
        return super().__le__(self, other)

    @_value_comparison
    def __gt__(self, other):
        return super().__gt__(self, other)

    @_value_comparison
    def __gte__(self, other):
        return super().__gte__(self, other)

    @classmethod
    def list_to_cons(cls, values: List['Value']) -> 'Value':
        if not values:
            return cls(ValueType.NIL)
        result_cons = Cons()
        curr = result_cons
        for v in values[:-1]:
            curr.car = v
            curr.cdr = cls(ValueType.CONS, Cons())
            curr = curr.cdr.value
        curr.car = values[-1]
        return cls(ValueType.CONS, result_cons)

    def __iter__(self):
        if self.variant in (ValueType.CONS, ValueType.NIL):
            return Cons._Iterator(self)
        raise ValueError(
            f'Iteration only allowed on CONS and NIL values, but got '
            f'{self.variant}'
        )

    def __len__(self):
        result = 0
        for _ in self:
            result += 1
        return result


@attr.s(auto_attribs=True, slots=True)
class LambdaValue:
    """`value` of a lambda."""
    args: Value
    body: Value
    scope: Dict[str, Value]

    def __str__(self):
        arg_str = ' '.join([arg.value.car.value for arg in self.args])
        return f'<lambda: ({arg_str})>'


@attr.s(auto_attribs=True, slots=True)
class Cons:
    car: Any = attr.ib(factory=lambda: Value(ValueType.NIL))
    cdr: Any = attr.ib(factory=lambda: Value(ValueType.NIL))

    def __str__(self):
        return f'({self.car.value} : {self.cdr.value})'

    @attr.s(auto_attribs=True, slots=True)
    class _Iterator:
        cons: Value
        idx: int = 0
        current: Optional[Value] = None

        def __attrs_post_init__(self):
            self.current = self.cons

        def __next__(self):
            if self.current.variant == ValueType.NIL:
                raise StopIteration
            elif self.current.variant == ValueType.CONS:
                result = self.current
                self.current = self.current.value.cdr
                self.idx += 1
                return result
            # todo error handling??
            raise ValueError(
                f'Received non-cons at position {idx}: {self.current}'
            )
