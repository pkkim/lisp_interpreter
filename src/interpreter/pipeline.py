def run_code(env, code):
    lexed = lexer.lex(code)
    lexed_desugared = desugarizer.desugar(lexed)
    nodes = parser.Parser().parse(lexed_desugared)
    for node in nodes:
        value = env.eval_node(node)
    return value


