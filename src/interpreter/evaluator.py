import collections
from itertools import islice
from typing import Deque, Dict, Any, Tuple, List

import attr

from .types import ValueType, Value, LambdaValue, Cons, RuntimeError
from . import builtin_handlers


def _assert(condition, message):
    if not condition:
        raise RuntimeError(message)


def _assert_arity(name, args, count):
    _assert(
        len(args) == count,
        f'{name} takes {count} argument(s) but got {args}',
    )


def to_list(values: List[Value]) -> Value:
    result = Value(ValueType.NIL)
    for v in reversed(values):
        result = Value(ValueType.CONS, Cons(car=v, cdr=result))
    return result


KEYWORDS = {'block', 'if', 'list', 'lambda', 'set', 'def', 'eval'}


KEYWORD_VALUES = {'nil'}


@attr.s(auto_attribs=True, slots=True)
class Environment:
    scopes: Deque[Dict[str, Value]] = attr.ib(factory=collections.deque)

    def set(self, key: str, value: Value) -> None:
        for scope in reversed(self.scopes):
            if key in scope:
                scope[key] = value
                return
        raise RuntimeError(f'Variable {key} not defined')

    def def_(self, key: str, value: Value) -> None:
        self.scopes[-1][key] = value

    def lookup(self, key: str) -> Value:
        for scope in reversed(self.scopes):
            if key in scope:
                return scope[key]
        raise RuntimeError(f'Variable {key} not defined')

    def push_empty_scope(self) -> None:
        self.push_scope({})

    def push_scope(self, contents: Dict[str, Value]) -> None:
        self.scopes.append(contents)

    def pop_scope(self) -> Dict[str, Any]:
        return self.scopes.pop()

    def _is_keyword(self, node: Value) -> bool:
        return (node.variant == ValueType.STRING and node.value in KEYWORDS)

    def _handle_keyword(self, name: str, args) -> Value:
        # the args are not yet evaluated.
        
        if name == 'block':
            self.push_empty_scope()
            for statement in args:
                value = self.eval(statement.value.car)
            self.pop_scope()
            return value
        elif name == 'if':
            cond, if_true, if_false = args
            cond_result = self.eval(cond.value.car)
            _assert(
                cond_result.variant == ValueType.BOOLEAN and \
                        isinstance(cond_result.value, bool),
                f'Condition returned non-bool value: {cond_result}'
            )
            return self.eval(
                if_true.value.car
                if cond_result.value
                else if_false.value.car
            )
        elif name == 'list':
            # order of evaluation matters
            list_value = [self.eval(v.value.car) for v in args]
            result = to_list(list_value)
            return result
        elif name == 'lambda':
            _assert_arity('lambda', args, 2)
            fn_args, body = args
            # at lambda creation time, no variables bound; body is totally
            # unevaluated
            return Value(ValueType.LAMBDA, LambdaValue(
                args=fn_args.value.car, body=body.value.car, scope={}
            ))
        elif name in ('set', 'def'):
            _assert_arity(name, args, 2)
            key_node, value_node = args
            assert key_node.value.car.variant == ValueType.STRING
            value = self.eval(value_node.value.car)
            method = self.set if name == 'set' else self.def_
            method(key_node.value.car.value, value)
            return value
        elif name == 'eval':
            _assert_arity('eval', args, 1)
            arg, = args
            _assert(
                (arg.value.car.variant == ValueType.CONS) and
                (arg.value.car.value.car.value == 'quote'),
                f'argument to eval must be of form (quote X) but got {arg}',
            )
            return self.eval(arg.value.car.value.cdr.value.car)
        else:
            raise RuntimeError(f'Keyword not supported: {name}')

    def _is_builtin(self, node: Value) -> bool:
        return (node.variant == ValueType.STRING and
                node.value in builtin_handlers.BUILTINS)

    def _handle_builtin(self, name: str, args: List[Value]) -> Value:
        return builtin_handlers.handle(name, args)

    def begin_toplevel(self):
        self.push_empty_scope()

    def eval(self, node: Value) -> Value:
        if node.variant in {ValueType.NUMBER, ValueType.BOOLEAN}:
            return node
        elif node.variant == ValueType.STRING:
            return self.lookup(node.value)
        elif node.variant == ValueType.CONS:
            # An application
            x = iter(node)
            fn_node = next(x).value.car
            try:
                fn_args = next(x)
            except StopIteration:
                fn_args = Value(ValueType.NIL)

            if fn_node.value == 'quote':
                # Quote prevents further evaluation
                _assert_arity('quote', fn_args, 1)
                return node

            # Each keyword requires its arguments to be evaluated differently,
            # so they must be passed to the keyword handlers unevaluated.
            if self._is_keyword(fn_node):
                return self._handle_keyword(fn_node.value, fn_args)

            # From here, treat the args as a list, because the Cons cell is a
            # bear to work with...
            args = [self.eval(arg.value.car) for arg in fn_args]
            if self._is_builtin(fn_node):
                return self._handle_builtin(fn_node.value, args)
            else:
                fn = self.eval(fn_node)
                fn_scope = fn.value.scope
                arg_scope = {
                    k.value.car.value: v for k, v in zip(fn.value.args, args)
                }
                self.push_scope(fn_scope)
                self.push_scope(arg_scope)
                return_value = self.eval(fn.value.body)
                # Set new scope on function
                updated_arg_scope = self.pop_scope()
                if return_value.variant == ValueType.LAMBDA:
                    return_value.value.scope = updated_arg_scope
                updated_fn_scope = self.pop_scope()
                fn.value.scope = updated_fn_scope
                return return_value
