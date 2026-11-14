"""Compatibility entry point; implementation lives in sgo.industry_proof."""
import runpy
import sys

if __name__ == '__main__':
    runpy.run_module('sgo.industry_proof', run_name='__main__')
else:
    from sgo import industry_proof as _implementation
    sys.modules[__name__] = _implementation
