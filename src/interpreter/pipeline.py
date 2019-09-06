import itertools

from interpreter import lexer, desugarizer, parser


def run_code(env, code):
    lexed = desugarizer.desugar(lexer.lex(code))
    nodes = [parser.parse(tree) for tree in lexed]
    for node in nodes:
        value = env.eval(node)
    return value
