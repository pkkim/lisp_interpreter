import collections
import copy
from itertools import islice
from typing import Deque, Dict, Any, Tuple, List

import attr

from .types import NodeType, Node, ValueType, Value

class RuntimeError(Exception):
    pass


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

    def eval_function(self, args, body) -> Any:
        raise NotImplemented

    def eval_node(self, node: Node) -> Any:
        if node.variant == NodeType.NUMBER:
            return Value(ValueType.NUMBER, node.value)
        elif node.variant == NodeType.STRING:
            return Value(ValueType.STRING, node.value)
        elif node.variant == NodeType.VARIABLE:
            return self.lookup(node.value)
        elif node.variant == NodeType.BLOCK:
            self.push_empty_scope()
            for statement in node.value:
                value = self.eval_node(statement)
            self.pop_scopes(1)
            return value
        elif node.variant == NodeType.APPLY:
            fn_name, *fn_args = node.value
            fn_value = self.lookup(fn_name)
            (fn_arg_names, fn_body), fn_scopes = fn_value.value
            fn_scopes_count = len(fn_scopes)
            arg_scope = {k.value: v for k, v in zip(fn_arg_names.value, fn_args)}
            self.push_scopes(fn_scopes + [arg_scope])
            return_value = self.eval_node(fn_body)
            new_env.pop_scopes(1)  # arg scope
            fn_value.value[1] = self.pop_scopes(fn_scopes_count)
            return return_value
        elif node.variant == NodeType.LIST:
            # order of evaluation matters
            list_value = [self.eval_node(v) for v in node.value]
            return Value(ValueType.LIST, list_value)
        else:
            raise NotImplemented(node.variant)

