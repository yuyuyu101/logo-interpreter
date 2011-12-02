"""The logo_primitives module contains definitions of Logo primitive procedures.

Note: Some additional primitive procedures are defined in logo.py.
"""

import operator as op
import logo
from buffer import Buffer

try:
    import turtle
except Exception as e:
    print('Cannot import turtle graphics:', e)

def logo_print(x):
    """Implements Logo "print" primitive."""
    logo.logo_type(x)
    print('')

def logo_show(x):
    """Implements Logo "show" primitive."""
    if type(x) == list:
        print('[', end='')
    logo.logo_type(x)
    if type(x) == list:
        print(']', end='')
    print('')

def repeat(n, exp, env):
    """Implements "repeat", which evaluates an exp, n times."""
    for _ in range(int(n)):
        logo.eval_line(Buffer(exp), env)
    return None

def logo_word(x, y):
    """Implements "word", which applies string addition and evaluation."""
    if type(x) == list or type(y) == list:
        raise logo.LogoError('Cannot take a sentence input.')
    return x + y

def logo_sentence(x, y):
    """Implements "sentence", which builds a list (sentence) from two lists,
    converting non-list inputs to lists first."""
    if type(x) != list:
        x = [x]
    if type(y) != list:
        y = [y]
    return x + y

def logo_list(x, y):
    """Implements "list", which constructs a list (sentence) from two
    elements."""
    return [x, y]

def logo_fput(x, y):
    """Implements "fput", which constructs a list (sentence) from an element
    and the rest of the list."""
    if type(y) != list:
        raise logo.LogoError('Second input must be a sentence.')
    return [x] + y

def numeric(f):
    """Return a Logo primitive that has numeric inputs and output."""
    def coerced(*args):
        result = f(*map(to_num, args))
        if result is not None:
            return str(result) 
    return coerced

def logical(f):
    """Return a Logo primitive that has boolean inputs and output."""
    def coerced(*args):
        return str(f(*tuple(map(to_bool, args))))
    return coerced

def to_num(s):
    """Coerce string s to a number."""
    try:
        return int(s)
    except (TypeError, ValueError):
        try:
            return float(s)
        except (TypeError, ValueError):
            raise logo.error(str(s) + ' is not a number')

def to_bool(s):
    """Coerce string s to a bool."""
    if s == 'True':
        return True
    if s == 'False':
        return False
    raise logo.error(str(s) + ' is not a boolean value')

def equal(x, y):
    """Return True if x and y are equal."""
    if x == y:
        return 'True'
    try:
        return str(float(x) == float(y))
    except (TypeError, ValueError):
        return 'False'

def load(make_primitive):
    """Extend the set of primitive Logo procedures."""
    make_primitive('first', 1, lambda l: l[0])
    make_primitive(['butfirst', 'bf'], 1, lambda l: l[1:])
    make_primitive('last', 1, lambda l: l[-1])
    make_primitive(['butlast', 'bl'], 1, lambda l: l[:-1])

    make_primitive('sum', 2, numeric(op.add))
    make_primitive('difference', 2, numeric(op.sub))
    make_primitive('product', 2, numeric(op.mul))
    make_primitive(['div', 'quotient'], 2, numeric(op.truediv))

    make_primitive(['equalp', 'eq', 'equal?'], 2, equal)
    make_primitive(['lessp', 'lt', 'less?'], 2, numeric(op.lt))
    make_primitive(['greaterp', 'gp', 'greater?'], 2, numeric(op.gt))
    make_primitive(['emptyp', 'empty?'], 1, lambda x: str(len(x) == 0))
    make_primitive(['listp', 'list?'], 1, lambda x: str(type(x) == list))
    make_primitive(['wordp', 'word?'], 1, lambda x: str(type(x) == str))

    make_primitive('or', 2, logical(lambda x, y: bool(x or y)))
    make_primitive('and', 2, logical(lambda x, y: bool(x and y)))
    make_primitive('not', 1, logical(lambda x: not x))

    make_primitive('print', 1, logo_print)
    make_primitive('show', 1, logo_show)

    make_primitive('repeat', 2, repeat, needs_env=True)

    make_primitive('word', 2, logo_word)
    make_primitive(['sentence', 'se'], 2, logo_sentence)
    make_primitive('list', 2, logo_list)
    make_primitive('fput', 2, logo_fput)

    load_turtle_graphics(make_primitive)

def turtle_speed(n):
    """Set turtle graphics to draw every n frames (default: 1)."""
    turtle.tracer(n, 0)

def load_turtle_graphics(make_primitive):
    """Extend the set of primitive Logo procedures with turtle graphics.

    See http://docs.python.org/py3k/library/turtle.html for details on what
    these procedures do.
    """
    make_primitive(['forward', 'fd'], 1, numeric(turtle.fd))
    make_primitive(['backward', 'back', 'bk'], 1, numeric(turtle.bk))
    make_primitive(['right', 'rt'], 1, numeric(turtle.rt))
    make_primitive(['left', 'lt'], 1, numeric(turtle.lt))
    make_primitive('circle', 1, numeric(turtle.circle))
    make_primitive(['setpos', 'setposition', 'goto'], 2, numeric(turtle.goto))
    make_primitive(['seth', 'setheading'], 1, numeric(turtle.seth))
    make_primitive(['penup', 'pu'], 0, turtle.up)
    make_primitive(['pendown', 'pd'], 0, turtle.down)
    make_primitive(['showturtle', 'st'], 0, turtle.showturtle)
    make_primitive(['hideturtle', 'ht'], 0, turtle.hideturtle)
    make_primitive('clear', 0, turtle.clear)
    make_primitive('color', 1, turtle.color)  # accepts strings, e.g., 'red'
    make_primitive('begin_fill', 0, turtle.begin_fill)
    make_primitive('end_fill', 0, turtle.end_fill)
    make_primitive('exitonclick', 0, turtle.exitonclick)
    make_primitive('speed', 1, turtle_speed)
