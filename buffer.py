"""The buffer module implements a Buffer class for iterating through a list."""

class Buffer(object):
    """A Buffer tracks an index into a list and provides elements sequentially.

    The tracked index (initialized to 0) is incremented with each call to pop().
    Attempts to access an element for an index that is out of range return None.

    >>> buf = Buffer(['print', '2'])
    >>> buf.current
    'print'
    >>> buf.previous  # value is None for index -1
    >>> print(buf)
    [  >> print, 2 ]
    >>> buf.pop()
    'print'
    >>> print(buf)
    [ print >> 2 ]
    >>> buf.pop()
    '2'
    >>> buf.current  # value is None for index 2
    >>> buf.previous
    '2'
    >>> print(buf)
    [ print, 2 >>  ]
    """
    def __init__(self, elements, index=0):
        self.contents = list(elements)
        self.index = index

    def pop(self):
        """Remove the first element of the buffer and return it."""
        if self.index > self._maxindex():
            raise IndexError("Nothing left to pop")
        self.index += 1
        return self.previous

    @property
    def previous(self):
        """Return the previous element, or None if none exists."""
        if self.index == 0 or self._maxindex() < self.index - 1:
            return None
        return self.contents[self.index - 1]

    @property
    def current(self):
        """Return the current element, or None if none exists."""
        if self._maxindex() < self.index:
            return None
        return self.contents[self.index]

    def _maxindex(self):
        return len(self.contents) - 1

    def __str__(self):
        """Return a list-like string, marking the current element with >>."""
        s = '[ '
        s += ', '.join(map(str, self.contents[:self.index]))
        s += ' >> '
        s += ', '.join(map(str, self.contents[self.index:]))
        s += ' ]'
        return s

    def __repr__(self):
        return 'Buffer({0}, {1})'.format(repr(self.contents), repr(self.index))
