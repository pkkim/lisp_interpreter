import readline

import click

from interpreter import lexer, parser, evaluator, pipeline


def run_repl(environment):
    while True:
        code = input('>> ')
        if not code:
            continue
        try:
            value = pipeline.run_code(environment, code)
            print(value.value)
        except Exception as e:
            print(f'error: {e.__class__}', e)


@click.command()
@click.option('--builtins', type=click.File('r'),
        default=None)
def main(builtins):
    env = evaluator.Environment()
    env.begin_toplevel()
    if builtins:
        run_code(env, builtins.read())
    run_repl(env)
        

if __name__ == '__main__':
    main()
