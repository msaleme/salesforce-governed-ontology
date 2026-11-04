"""Opt-in Salesforce sandbox metadata probe; never reads business records."""
import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_BYTES = 2_000_000


class ProbeError(Exception):
    """Safe operator-facing failure without response bodies or credentials."""


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProbeError('Redirect refused; use the exact sandbox My Domain URL.')


def validate_origin(origin):
    parsed = urlsplit(origin)
    if (parsed.scheme != 'https' or parsed.username or parsed.password
            or parsed.port is not None or parsed.path not in ('', '/')
            or parsed.query or parsed.fragment
            or not re.fullmatch(r'[a-z0-9-]+--[a-z0-9-]+\.sandbox\.my\.salesforce\.com',
                                parsed.hostname or '')):
        raise ProbeError('Expected an HTTPS sandbox My Domain origin without port or path.')
    return 'https://' + parsed.hostname


def api_name(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,254}', value):
        raise ProbeError('Invalid object or field API name.')
    return value


class SandboxClient:
    def __init__(self, origin, token, version):
        self.origin = validate_origin(origin)
        if not re.fullmatch(r'v[0-9]{2,3}\.0', version):
            raise ProbeError('API version must look like vXX.0; select a version supported by your org.')
        if not token or any(c.isspace() for c in token):
            raise ProbeError('Set SF_ACCESS_TOKEN to a valid session token locally.')
        self.token = token
        self.prefix = '/services/data/' + version
        self.opener = build_opener(NoRedirects())

    def get(self, path):
        request = Request(self.origin + self.prefix + path,
                          headers={'Authorization': 'Bearer ' + self.token,
                                   'Accept': 'application/json'}, method='GET')
        try:
            with self.opener.open(request, timeout=20) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ProbeError('Response exceeded the bounded metadata limit.')
            result = json.loads(data)
            if not isinstance(result, dict):
                raise ProbeError('Expected a JSON object response.')
            return result
        except HTTPError as exc:
            raise ProbeError(f'Salesforce HTTP {exc.code}; response body suppressed.') from None
        except (URLError, TimeoutError, OSError):
            raise ProbeError('Salesforce transport failed; connection details suppressed.') from None
        except (ValueError, UnicodeError):
            raise ProbeError('Salesforce returned invalid JSON.') from None


def probe(client, object_name, fields):
    object_name = api_name(object_name)
    if not fields or len(fields) != len(set(fields)):
        raise ProbeError('Supply at least one unique field API name.')
    fields = [api_name(field) for field in fields]
    # This fixed query reads org classification only, not customer/business rows.
    org = client.get('/query?' + urlencode({'q': 'SELECT IsSandbox FROM Organization LIMIT 1'}))
    records = org.get('records')
    if (org.get('done') is not True or org.get('totalSize') != 1
            or not isinstance(records, list) or len(records) != 1
            or not isinstance(records[0], dict) or records[0].get('IsSandbox') is not True):
        raise ProbeError('Sandbox identity could not be verified; metadata read stopped.')
    metadata = client.get('/sobjects/' + object_name + '/describe')
    if metadata.get('name') != object_name or metadata.get('queryable') is not True:
        raise ProbeError('Requested object is absent, mismatched, or not queryable.')
    descriptions = metadata.get('fields')
    if not isinstance(descriptions, list) or any(not isinstance(f, dict) for f in descriptions):
        raise ProbeError('Malformed field metadata.')
    available = {f.get('name') for f in descriptions if isinstance(f.get('name'), str)}
    if not set(fields).issubset(available):
        raise ProbeError('One or more requested fields are absent from this identity\'s describe response.')
    return {
        'status': 'sandbox_metadata_verified',
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'sandbox_verified': True,
        'requested_field_count': len(fields),
        'business_records_read': False,
        'metric_value_verified': False,
        'authorization_boundary_verified': False,
        'note': 'Metadata visibility is not proof of row/field access enforcement or approved business meaning.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instance-url', required=True)
    parser.add_argument('--api-version', required=True)
    parser.add_argument('--object', required=True, dest='object_name')
    parser.add_argument('--field', action='append', required=True, dest='fields')
    args = parser.parse_args()
    try:
        client = SandboxClient(args.instance_url, os.environ.get('SF_ACCESS_TOKEN', ''), args.api_version)
        print(json.dumps(probe(client, args.object_name, args.fields), indent=2))
    except (ProbeError, ValueError):
        # Never expose an unexpected exception's payload or a token-bearing URL.
        exc = sys.exc_info()[1]
        print(json.dumps({'status': 'failed', 'reason': str(exc) if isinstance(exc, ProbeError)
                         else 'Invalid connection configuration.'}), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
