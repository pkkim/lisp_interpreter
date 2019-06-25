import functools

from .types import Value, ValueType


BUILTINS = {
    # arithmetic
    # '/' is true division, '//' is floor division
    '+', '-', '/', '//', '*', '%', '**', 'abs',
    # boolean
    '=', '&&', '||', '!', '<', '>', '<=', '>=',
    # bitwise
    '^', '&', '|',
    # list
    'cons', 'car', 'cdr', 'set_car', 'set_cdr', 'concat', 'length', 'filter',
    'map', 'reduce', 'list',
}


HANDLERS = {}


def handler(name, value_type=None, minimum=None, maximum=None, exact=None):
    def wrapped(f):
        @functools.wraps(f)
        def g(args):
            argc = len(args)
            if exact is not None:
                assert argc == exact
            if minimum is not None:
                assert argc >= minimum
            if maximum is not None:
                assert argc <= maximum

            result = f(args)
            return Value(value_type, result) if value_type else result

        assert name in BUILTINS
        HANDLERS[name] = g
        return g
    return wrapped


@handler('+', ValueType.NUMBER)
def plus(args):
    return sum(a.value for a in args)


@handler('-', ValueType.NUMBER, exact=2)
def minus(args):
    return args[0].value - args[1].value


@handler('/', ValueType.NUMBER, exact=2)
def div(args):
    return args[0].value / args[1].value


@handler('//', ValueType.NUMBER, exact=2)
def div_int(args):
    return args[0].value // args[1].value


@handler('*', ValueType.NUMBER)
def mul(args):
    return functools.reduce(lambda x, y: x * y, (a.value for a in args))

@handler('%', ValueType.NUMBER, exact=2)
def mod(args):
    return args[0].value % args[1].value


@handler('**', ValueType.NUMBER, exact=2)
def pow(args):
    return args[0].value ** args[1].value


@handler('abs', ValueType.NUMBER, exact=1)
def abs(args):
    return abs(args[0].value)


@handler('=', ValueType.BOOLEAN, minimum=2)
def eq(args):
    first, *rest = args
    return all(first == other for other in rest)


@handler('&&', ValueType.BOOLEAN, minimum=2)
def and_bool(args):
    return all(a.value for a in args)


@handler('||', ValueType.BOOLEAN, minimum=2)
def or_bool(args):
    return any(a.value for a in args)


@handler('!', ValueType.BOOLEAN, exact=1)
def not_bool(args):
    return not args[0].value


@handler('<', ValueType.BOOLEAN, exact=2)
def lt(args):
    return args[0].value < args[1].value


@handler('>', ValueType.BOOLEAN, exact=2)
def gt(args):
    return args[0].value > args[1].value


@handler('<=', ValueType.BOOLEAN, exact=2)
def le(args):
    return args[0].value <= args[1].value


@handler('>=', ValueType.BOOLEAN, exact=2)
def ge(args):
    return args[0].value >= args[1].value


@handler('cons', exact=2)
def cons(args):
    return Cons(args[0], args[1])


@handler('car', exact=1)
def car(args):
    return args[0].car


@handler('cdr', exact=1)
def car(args):
    return args[0].cdr


@handler('set_car', exact=2)
def set_car(args):
    args[0].car = args[1]
    return args[1]


@handler('set_cdr')
def set_cdr(args):
    args[0].cdr = args[1]
    return args[1]


@handler('concat')
def concat(args):
    if all(l == Value(ValueType.NIL) for l in args):
        return Value(ValueType.NIL)

    result = Value(ValueType.CONS, Cons())
    result_ptr = result
    for l in args:
        current = l
        while current != Value(ValueType.NIL):
            result.value.car = current.value.car
            assert current.cdr.type_ in (ValueType.NIL, ValueType.CONS), (
                f'Argument to concat is not a list: {l}'
            )
            current = current.cdr
            result_ptr = result.cdr
    return result


# @handler('length', ValueType.NUMBER)
# @handler('filter', ValueType.NUMBER)
# @handler('map', ValueType.NUMBER)
# @handler('reduce', ValueType.NUMBER)
# @handler('list', ValueType.NUMBER)
# assert BUILTINS == set(HANDLERS.keys())


def handle(name: str, args) -> Value:
    return HANDLERS[name](args)
