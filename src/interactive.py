import readline

import click

from interpreter import lexer, parser, evaluator


def run_code(env, code):
    lexed = lexer.lex(code)
    nodes = parser.Parser().parse(lexed)
    for node in nodes:
        value = env.eval_node(node)
    return value


def run_repl(environment):
    while True:
        code = input('>> ')
        if not code:
            continue
        try:
            value = run_code(environment, code)
            print(value.value)
        except Exception as e:
            print('error:', e)


@click.command()
@click.option('--builtins', type=click.File('r'),
        default='src/interpreter/builtins.lisp')
def main(builtins):
    env = evaluator.Environment()
    env.begin_toplevel()
    if builtins:
        run_code(env, builtins.read())
    run_repl(env)
        

if __name__ == '__main__':
    main()
