import itertools

from interpreter import lexer, desugarizer, parser, preprocessor


def run_code(env, code):
    code = preprocessor.remove_comments(code)
    lexed = desugarizer.desugar(lexer.lex(code))
    nodes = [parser.parse(tree) for tree in lexed]
    for node in nodes:
        value = env.eval(node)
    return value
