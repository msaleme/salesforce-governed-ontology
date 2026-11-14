"""Compatibility entry point; implementation lives in sgo.demo."""
import runpy
import sys

if __name__ == '__main__':
    runpy.run_module('sgo.demo', run_name='__main__')
else:
    from sgo import demo as _implementation
    sys.modules[__name__] = _implementation
