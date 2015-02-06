#
# Use with
# >>> from pythonfix import *  # pylint: disable=W0401
#

import sys

__all__ = []

def export(fun):
    __all__.append(fun.__name__)
    return fun

# pylint: disable=I0011,W0622
if sys.version_info < (2, 5):
    @export
    def any(iterable):
        for item in iterable:
            if item:
                return True
        return False
