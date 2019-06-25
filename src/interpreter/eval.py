import collections
import copy
from itertools import islice
from typing import Deque, Dict, Any, Tuple, List

import attr

from .types import NodeType, Node, ValueType, Value, LambdaValue, Cons
from . import builtin_handlers


class RuntimeError(Exception):
    pass


BUILTINS = {
    # arithmetic
    '+', '-', '/', '//', '*', '%', '**', 'abs', 
    # boolean
    '=', '&&', '||', '!', '<', '>', '<=', '>=',
    # bitwise
    '^', '&', '|',
    # list
    'cons', 'car', 'cdr', 'set-car', 'set-cdr', 'concat', 'length', 'filter',
    'map', 'reduce',
}


def to_list(values: List[Value]) -> Value:
    result = Value(ValueType.NIL)
    for v in reversed(values):
        result = Value(ValueType.CONS, Cons(car=v, cdr=result))
    return result


@attr.s(auto_attribs=True, slots=True)
class Environment:
    scopes: Deque[Dict[str, Value]] = attr.ib(factory=collections.deque)

    def set(self, key: str, value: Value) -> None:
        for scope in reversed(self.scopes):
            if key in scope:
                scope[key] = value
                return
        raise RuntimeError(
            f'Variable {key} not defined in scopes: {self.scopes}',
        )

    def def_(self, key: str, value: Value) -> None:
        self.scopes[-1][key] = value
        print(f'After defining {key}: {self.scopes}')

    def lookup(self, key: str) -> Value:
        for scope in reversed(self.scopes):
            if key in scope:
                return scope[key]
        raise RuntimeError(
            f'Variable {key} not defined in scopes: {self.scopes}',
        )

    def copy(self) -> 'Environment':
        copied_scopes = collections.deque(
            copy.deepcopy(scope) for scope in self.scopes
        )
        return self.__class__(copied_scopes)

    def push_empty_scope(self) -> None:
        self.push_scopes([{}])

    def push_scopes(self, contents: List[Dict[str, Value]] = None) -> None:
        self.scopes.extend(contents)

    def pop_scopes(self, count) -> None:
        split_index = len(self.scopes) - count
        result = collections.deque(islice(self.scopes, None, split_index))
        self.scopes = collections.deque(islice(self.scopes, split_index))
        return result

    def _is_builtin(self, node) -> bool:
        return node.variant == NodeType.VARIABLE and node.value in BUILTINS

    def _handle_builtin(self, name: str, args: List[Value]) -> Value:
        return builtin_handlers.handle(name, args)

    def eval_node(self, node: Node, toplevel: bool = False) -> Value:
        if node.variant == NodeType.NUMBER:
            return Value(ValueType.NUMBER, node.value)
        elif node.variant == NodeType.STRING:
            return Value(ValueType.STRING, node.value)
        elif node.variant == NodeType.BOOLEAN:
            return Value(ValueType.BOOLEAN, node.value)
        elif node.variant == NodeType.VARIABLE:
            return self.lookup(node.value)
        elif node.variant == NodeType.BLOCK:
            self.push_empty_scope()
            for statement in node.value:
                value = self.eval_node(statement)
            if not toplevel:
                self.pop_scopes(1)
            return value
        elif node.variant == NodeType.APPLY:
            fn_node, *fn_arg_nodes = node.value
            fn_args = [self.eval_node(a) for a in fn_arg_nodes]
            if self._is_builtin(fn_node):
                return self._handle_builtin(fn_node.value, fn_args)
            fn = self.eval_node(fn_node)
            fn_scopes = fn.value.scopes
            fn_scopes_count = len(fn_scopes)
            arg_scope = {k: v for k, v in zip(fn.value.args, fn_args)}
            self.push_scopes(fn_scopes + [arg_scope])
            return_value = self.eval_node(fn.value.body)
            # arg scope
            self.pop_scopes(1)
            # The rest of the scopes
            fn.value.scopes = self.pop_scopes(fn_scopes_count)
            return return_value
        elif node.variant == NodeType.LIST:
            # order of evaluation matters
            list_value = [self.eval_node(v) for v in node.value]
            return to_list(list_value)
        elif node.variant == NodeType.IF:
            cond, if_true, if_false = node.value
            cond_result = self.eval_node(cond)
            if cond_result.type_ != ValueType.BOOLEAN or \
                    not isinstance(cond_result.value, bool):
                raise RuntimeError(
                    f'Condition returned non-bool value: {cond_result}'
                )
            return self.eval_node(if_true if cond_result.value else if_false)
        elif node.variant == NodeType.LAMBDA:
            args, body = node.value
            result_args = [arg.value for arg in args.value]
            # at lambda creation time, no variables bound; body is totally
            # unevaluated
            return Value(ValueType.LAMBDA, LambdaValue(
                args=result_args, body=body, scopes=[]
            ))
        elif node.variant in (NodeType.SET, NodeType.DEF):
            key_node, value_node = node.value
            assert key_node.variant == NodeType.VARIABLE
            value = self.eval_node(value_node)
            method = self.set if node.variant == NodeType.SET else self.def_
            method(key_node.value, value)
            return value
        else:
            raise NotImplemented(node.variant)

