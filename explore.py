"""Compatibility entry point; implementation lives in sgo.explore."""
import runpy
import sys

if __name__ == '__main__':
    runpy.run_module('sgo.explore', run_name='__main__')
else:
    from sgo import explore as _implementation
    sys.modules[__name__] = _implementation
