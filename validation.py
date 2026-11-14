"""Compatibility entry point; implementation lives in sgo.validation."""
import runpy
import sys

if __name__ == '__main__':
    runpy.run_module('sgo.validation', run_name='__main__')
else:
    from sgo import validation as _implementation
    sys.modules[__name__] = _implementation
