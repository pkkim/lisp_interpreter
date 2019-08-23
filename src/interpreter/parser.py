from collections import deque
from typing import Optional, Deque, List, Any

import attr

from .types import Token, TokenType, Value, ValueType, TokenTree, ParseError


# @attr.s(auto_attribs=True, slots=True)
# class _Frame:
#     variant: Optional[NodeType] = None
#     nodes: List[Node] = attr.ib(factory=list)

#     @property
#     def quoted(self) -> bool:
#         return self.variant == NodeType.LIST


def parse2(token) -> Value:
    if isinstance(token, TokenTree):
        return Value.list_to_cons([parse2(elem) for elem in token.value])
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


# @attr.s(auto_attribs=True, slots=True)
# class Parser:
#     frames: Deque[_Frame] = attr.ib(factory=lambda: deque([_Frame()]))
#     quote_next: bool = False

#     def current_frame(self) -> _Frame:
#         return self.frames[-1]

#     def finalize_current_frame(self) -> Node:
#         frame = self.current_frame()
#         value = frame.nodes
#         node_type = frame.variant
#         if frame.variant == NodeType.IF:
#             if len(value) == 2:
#                 # No "else" explicitly given, so make it a no-op
#                 value = value + [Node(NodeType.BLOCK, [])]
#             expected_length = 3
#         elif frame.variant in {NodeType.LAMBDA, NodeType.SET, NodeType.DEF}:
#             expected_length = 2
#         elif frame.variant == NodeType.BLOCK:
#             expected_length = None
#         elif frame.variant == NodeType.LIST:
#             expected_length = None
#         else:
#             node_type = NodeType.APPLY
#             expected_length = None

#         return Node(node_type, value)

#     def process_string(self, token: T) -> None:
#         current_frame = self.current_frame()
#         current_frame_quoted = current_frame.quoted
#         quoted = self.quote_next or current_frame_quoted

#         if quoted:
#             current_frame.nodes.append(Node(NodeType.STRING, token.value))
#             return
#         elif token.value in ('true', 'false'):
#             current_frame.nodes.append(
#                 Node(NodeType.BOOLEAN, token.value == 'true')
#             )
#             return

#         # otherwise, it's a real keyword
#         if token.value == 'if':
#             self.current_frame().variant = NodeType.IF
#         elif token.value == 'lambda':
#             self.current_frame().variant = NodeType.LAMBDA
#         elif token.value == 'set':
#             self.current_frame().variant = NodeType.SET
#         elif token.value == 'def':
#             self.current_frame().variant = NodeType.DEF
#         else:
#             self.current_frame().nodes.append(
#                 Node(NodeType.VARIABLE, token.value)
#             )

#     def process_token(self, token: T) -> None:
#         quote_next = False
#         if token.variant == TT.OPEN_PAREN:
#             quoted = self.quote_next
#             self.frames.append(_Frame(NodeType.LIST if quoted else None))
#         elif token.variant == TT.CLOSE_PAREN:
#             node = self.finalize_current_frame()
#             try:
#                 self.frames.pop()
#             except IndexError:
#                 raise ParseError('Too many right parentheses')
#             self.frames[-1].nodes.append(node)
#         elif token.variant == TT.QUOTE:
#             quote_next = True
#         elif token.variant == TT.SEMICOLON:
#             self.frames[-1].variant = NodeType.BLOCK
#         elif token.variant == TT.NUMBER:
#             # quoted numbers are just numbers
#             self.frames[-1].nodes.append(Node(NodeType.NUMBER, token.value))
#         elif token.variant == TT.STRING:
#             self.process_string(token)
#         elif token.variant == TT.OPERATOR:
#             self.frames[-1].nodes.append(Node(NodeType.VARIABLE, token.value))

#         self.quote_next = quote_next

#     def parse(self, tokens: List[T]) -> List[Node]:
#         for token in tokens:
#             self.process_token(token)
#         if len(self.frames) > 1:
#             raise ParseError('Too many left parentheses')
#         return self.current_frame().nodes
