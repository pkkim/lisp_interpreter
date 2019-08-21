import readline
import traceback

import click

from interpreter import evaluator, pipeline


def run_repl(environment):
    while True:
        code = input('>> ')
        if not code:
            continue
        try:
            value = pipeline.run_code(environment, code)
            print(f'-> {value}')
        except Exception as e:
            traceback.print_exc()


@click.command()
@click.option('--builtins', type=click.File('r'),
        default='src/interpreter/builtins.lisp')
def main(builtins):
    env = evaluator.Environment()
    env.begin_toplevel()
    if builtins:
        pipeline.run_code(env, builtins.read())
    run_repl(env)
        

if __name__ == '__main__':
    main()
