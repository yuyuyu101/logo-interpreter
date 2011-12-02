"""The logo_parser module implements a parser for Logo."""

from buffer import Buffer

def parse_line(line, chars=None, depth=0):
    """Convert a single line of Logo into a list of tokens or lists.

    >>> parse_line('print sum 10 difference 7 3')
    ['print', 'sum', '10', 'difference', '7', '3']
    >>> parse_line('print "this [is a [deep] list]')
    ['print', '"this', ['is', 'a', ['deep'], 'list']]
    """
    if chars == None:
        chars = Buffer(line.strip()[:])

    tokens = []
    while True:
        if chars.current == None: # End of the line
            if depth != 0:
                raise SyntaxError('Unmatched "[" at ' + str(chars))
            return tokens
        elif chars.current == ' ': # Skip over spaces
            chars.pop()
        elif chars.current == '[':
            chars.pop()
            tokens.append(parse_line(line, chars, depth + 1))
        elif chars.current == ']':
            if depth == 0:
                raise SyntaxError('Unexpected "]" at ' + str(chars))
            else:
                chars.pop()
                return tokens
        else:
            tokens.append(parse_token(chars))

LOGO_OPERATORS = set('+-*/=<>()'[:])
LOGO_DELIMITERS = set('[]\n '[:]).union(LOGO_OPERATORS)

def parse_symbol(chars):
    """Parse the next symbol from a buffer chars, starting at chars.current."""
    symbol = chars.pop()
    while chars.current is not None and chars.current not in LOGO_DELIMITERS:
        symbol += chars.pop()
    return symbol

def parse_token(chars):
    """Parse the next token from a buffer chars, starting at chars.current."""
    ch = chars.current
    if ch in LOGO_OPERATORS:
        if ch != '-' or chars.previous not in [' ', None]: # Negative numbers
            return chars.pop()
    return parse_symbol(chars)

