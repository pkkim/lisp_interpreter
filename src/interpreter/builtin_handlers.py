import functools

from .types import Value, ValueType, Cons


BUILTINS = {
    # arithmetic
    # '/' is true division, '//' is floor division
    '+', '-', '/', '//', '*', '%', '**', 'abs',
    # boolean
    '=', '!=', '&&', '||', '!', '<', '>', '<=', '>=',
    # # bitwise
    # '^', '&', '|',
    # list
    'cons', 'car', 'cdr', 'set_car', 'set_cdr', 'concat', 'length', 'list',
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
def floor_div(args):
    return args[0].value // args[1].value


@handler('*', ValueType.NUMBER)
def mul(args):
    return functools.reduce(lambda x, y: x * y, (a.value for a in args), 1)

@handler('%', ValueType.NUMBER, exact=2)
def mod(args):
    return args[0].value % args[1].value


@handler('**', ValueType.NUMBER, exact=2)
def pow(args):
    return args[0].value ** args[1].value


@handler('abs', ValueType.NUMBER, exact=1)
def abs_(args):
    return abs(args[0].value)


@handler('=', ValueType.BOOLEAN, minimum=2)
def eq(args):
    first, *rest = args
    return all(first == other for other in rest)


@handler('!=', ValueType.BOOLEAN, minimum=2)
def eq(args):
    first, *rest = args
    return any(first != other for other in rest)


@handler('&&', ValueType.BOOLEAN)
def and_bool(args):
    return all(a for a in args)


@handler('||', ValueType.BOOLEAN)
def or_bool(args):
    return any(a for a in args)


@handler('!', ValueType.BOOLEAN, exact=1)
def not_bool(args):
    return not args[0]


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


@handler('cons', ValueType.CONS, exact=2)
def cons(args):
    return Cons(args[0], args[1])


@handler('car', exact=1)
def car(args):
    return args[0].value.car


@handler('cdr', exact=1)
def car(args):
    return args[0].value.cdr


@handler('set_car', exact=2)
def set_car(args):
    args[0].value.car = args[1]
    return args[1]


@handler('set_cdr')
def set_cdr(args):
    args[0].value.cdr = args[1]
    return args[1]


@handler('concat')
def concat(args):
    result = Value(ValueType.NIL)
    result_ptr = result
    for l in args:
        for cons in l:
            result_ptr.type_ = ValueType.CONS
            result_ptr.value = Cons(car=cons.value.car)
            result_ptr = result_ptr.value.cdr
    return result


@handler('length', ValueType.NUMBER, exact=1)
def length(args):
    return sum(1 for cons in args[0])


@handler('list')
def _list(args):
    result = Value(ValueType.NIL)
    result_ptr = result
    for v in args:
        result_ptr.type_ = ValueType.CONS
        result_ptr.value = Cons(car=v)
        result_ptr = result_ptr.value.cdr
    return result


assert BUILTINS == set(HANDLERS.keys()), BUILTINS - set(HANDLERS.keys())


def handle(name: str, args) -> Value:
    return HANDLERS[name](args)
