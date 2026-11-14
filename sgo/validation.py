"""Structural and semantic validation for this bounded, synthetic registry format.

JSON Schema plus bounded semantic checks; not a validator for vendor metadata.
"""
import re
from datetime import date
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads(Path(__file__).with_name("ontology.schema.json").read_text())
_SCHEMA_VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

def schema_errors(model):
    """Validate structure with JSON Schema draft 2020-12 and date formats."""
    return [f"{e.json_path}: {e.message}" for e in _SCHEMA_VALIDATOR.iter_errors(model)]


# Metric identity must remain bound to its intended source AND operation.
BINDINGS = {
    'booked_revenue': ('fixture:crm:contract_bookings', 'read_contract_bookings'),
    'recognized_revenue': ('fixture:erp:revenue_ledger', 'read_recognized_revenue'),
}
GRAIN = ['operator_id', 'contract_id', 'period', 'currency']


def validate_model(model):
    """Return path-qualified errors; never mutate the supplied JSON value."""
    errors = schema_errors(model)

    def error(path, message):
        errors.append(f'{path}: {message}')

    def text(record, key, path):
        value = record.get(key)
        if not isinstance(value, str) or not value.strip():
            error(f'{path}.{key}', 'expected nonempty string')
            return None
        return value

    def records(key):
        value = model.get(key)
        if not isinstance(value, list) or not value:
            error(key, 'expected nonempty array')
            return []
        result = []
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                error(f'{key}[{i}]', 'expected object')
            else:
                result.append((f'{key}[{i}]', item))
        return result

    if not isinstance(model, dict):
        return ['$: expected object']
    for key in ('id', 'version', 'namespace', 'status'):
        text(model, key, '$')
    if model.get('evidence') != 'synthetic_only':
        error('$.evidence', 'this fixture format requires synthetic_only')
    concepts = set()
    for path, concept in records('concepts'):
        identifier = text(concept, 'id', path)
        text(concept, 'definition', path)
        if identifier:
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', identifier):
                error(path + '.id', 'expected simple identifier')
            if identifier in concepts:
                error(path + '.id', 'duplicate concept')
            concepts.add(identifier)
    edges = set()
    for path, relation in records('relationships'):
        parts = [text(relation, key, path) for key in ('source', 'predicate', 'target')]
        for key, value in (('source', parts[0]), ('target', parts[2])):
            if value and value not in concepts:
                error(path + '.' + key, 'unknown concept')
        if all(parts):
            edge = tuple(parts)
            if edge in edges:
                error(path, 'duplicate relationship')
            edges.add(edge)
    metrics = set()
    for path, metric in records('metrics'):
        identifier = text(metric, 'id', path)
        for key in ('label', 'version', 'definition', 'source_binding'):
            text(metric, key, path)
        if identifier in metrics:
            error(path + '.id', 'duplicate metric')
        metrics.add(identifier)
        if metric.get('status') not in ('draft', 'review', 'approved', 'deprecated', 'revoked'):
            error(path + '.status', 'unknown lifecycle state')
        dates = []
        for key in ('valid_from', 'valid_to'):
            value = metric.get(key)
            try:
                if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                    raise ValueError
                dates.append(date.fromisoformat(value))
            except ValueError:
                error(path + '.' + key, 'expected valid YYYY-MM-DD date')
        if len(dates) == 2 and dates[0] > dates[1]:
            error(path, 'valid_from must not exceed valid_to')
        approval = metric.get('approval')
        if not isinstance(approval, dict):
            error(path + '.approval', 'expected object')
        elif metric.get('status') == 'approved':
            for key in ('steward', 'reference'):
                text(approval, key, path + '.approval')
            if approval.get('kind') != 'synthetic_fixture':
                error(path + '.approval.kind', 'expected synthetic_fixture')
        if metric.get('grain') != GRAIN:
            error(path + '.grain', 'expected operator/contract/period/currency grain')
        if metric.get('aggregation') != 'sum' or metric.get('unit') != 'currency_minor_units':
            error(path, 'expected sum in currency_minor_units')
        lineage = metric.get('lineage')
        if (not isinstance(lineage, list) or not lineage
                or not all(isinstance(v, str) and v.strip() for v in lineage)
                or metric.get('source_binding') not in lineage):
            error(path + '.lineage', 'expected nonempty references including source_binding')
        action = metric.get('action')
        if not isinstance(action, dict):
            error(path + '.action', 'expected object')
            continue
        if action.get('side_effect') != 'read':
            error(path + '.action.side_effect', 'only read supported')
        if action.get('required_scope') != 'finance:read':
            error(path + '.action.required_scope', 'expected finance:read')
        if action.get('implementation') != 'local_fixture_only':
            error(path + '.action.implementation', 'expected local_fixture_only')
        if identifier not in BINDINGS or (metric.get('source_binding'), action.get('operation_id')) != BINDINGS.get(identifier):
            error(path + '.action', 'metric/source/operation binding mismatch')
    return errors
