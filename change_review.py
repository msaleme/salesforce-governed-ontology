"""Offline registry change review, not an approval or migration executor."""
import argparse
import hashlib
import json
from pathlib import Path

from validation import validate_model


def fingerprint(model):
    """SHA-256 of Python sorted compact UTF-8 JSON; not RFC 8785/JCS."""
    payload = json.dumps(model, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=True, allow_nan=False).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def review_changes(before, after):
    """Compare two valid fixture registries without mutating either input.

    A version change is necessary for changed content, never sufficient approval.
    All changes require review. List ordering inside records is significant.
    """
    errors = {side: validate_model(model) for side, model in
              (('before', before), ('after', after))}
    if any(errors.values()):
        return {'status': 'invalid_registry', 'errors': errors}
    try:
        hashes = {'before': fingerprint(before), 'after': fingerprint(after)}
    except (TypeError, ValueError):
        return {'status': 'invalid_registry', 'errors': {'serialization': ['Expected finite JSON values']}}
    changes = []
    violations = []

    def add(path, kind, fields):
        changes.append({'path': path, 'kind': kind, 'fields': sorted(fields)})

    def compare_record(path, old, new, versioned=False):
        # Presence matters: an absent extension and explicit null are distinct.
        fields = {k for k in old.keys() | new.keys()
                  if k not in old or k not in new or fingerprint(old[k]) != fingerprint(new[k])}
        if not fields:
            return
        content = fields - {'version'}
        if versioned and content and old['version'] == new['version']:
            violations.append(path + ': content changed without a version change')
        if not content:
            kind = 'version_only'
        elif content <= {'label'}:
            kind = 'descriptive'
        else:
            # Unknown extension semantics cannot safely be declared compatible.
            kind = 'contract_review_required'
        add(path, kind, fields)

    collections = {'concepts', 'metrics', 'relationships'}
    compare_record('$', {k: v for k, v in before.items() if k not in collections},
                   {k: v for k, v in after.items() if k not in collections})
    for collection in ('concepts', 'metrics'):
        old = {r['id']: r for r in before[collection]}
        new = {r['id']: r for r in after[collection]}
        for key in sorted(old.keys() | new.keys()):
            path = collection + '.' + key
            if key not in old:
                add(path, 'added', new[key].keys())
            elif key not in new:
                add(path, 'removed', old[key].keys())
            else:
                compare_record(path, old[key], new[key], versioned=collection == 'metrics')
    # Include extension fields, not just edge identity, in comparisons.
    def edges(model):
        return {(r['source'], r['predicate'], r['target']): r for r in model['relationships']}
    old, new = edges(before), edges(after)
    for key in sorted(old.keys() | new.keys()):
        path = 'relationships.' + '/'.join(key)
        if key not in old:
            add(path, 'added', new[key].keys())
        elif key not in new:
            add(path, 'removed', old[key].keys())
        else:
            compare_record(path, old[key], new[key])
    if changes and before['version'] == after['version']:
        violations.append('$: registry changed without a version change')
    return {'status': 'version_policy_violation' if violations else
            ('review_required' if changes else 'unchanged'),
            'evidence': 'synthetic_only', 'fingerprints': hashes,
            'changes': changes, 'violations': violations}


def load_snapshot(path):
    """Reject ambiguous duplicate JSON keys instead of accepting the last value."""
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result

    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    args = parser.parse_args()
    try:
        result = review_changes(load_snapshot(args.before), load_snapshot(args.after))
    except (OSError, ValueError, RecursionError) as exc:
        # Do not echo arbitrary file contents or local paths in the report.
        result = {'status': 'invalid_input', 'error': type(exc).__name__}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['status'] == 'unchanged' else 1


if __name__ == '__main__':
    raise SystemExit(main())
