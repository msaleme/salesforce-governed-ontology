"""Installed CLI for the tour, registry validation and bring-your-own-data evaluation."""
import argparse
import json
import sys
from . import explore
from .byod import evaluate_file, load_json, validate_registry


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ('tour', 'scenario', 'validate'):
        return explore.main(argv)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('tour', help='Eight synthetic verdicts')
    sub.add_parser('scenario', help='One synthetic scenario (see sgo scenario --help)')
    sub.add_parser('validate', help='Validate the bounded fixture registry')
    byod = sub.add_parser('byod', help='Evaluate your own metric definitions and cases offline')
    byod.add_argument('path', help='JSON file with ontology and cases')
    schema = sub.add_parser('validate-registry', help='Schema and semantic checks for custom registries')
    schema.add_argument('path')
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate-registry':
            errors = validate_registry(load_json(args.path))
            result = {'valid': not errors, 'errors': errors}
            code = int(bool(errors))
        else:
            result = evaluate_file(args.path)
            code = int(result['passed'] != result['total'])
    except (OSError, UnicodeError, ValueError) as exc:
        result = {'status': 'invalid_input', 'error': str(exc)}
        code = 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return code
