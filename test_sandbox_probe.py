"""Synthetic transport tests, not evidence of live Salesforce enforcement."""
import io
import unittest
from unittest.mock import Mock
from urllib.error import HTTPError

from sandbox_probe import NoRedirects, ProbeError, SandboxClient, probe, validate_origin

ORIGIN = 'https://example--dev.sandbox.my.salesforce.com'


class SandboxProbeTests(unittest.TestCase):
    def client(self, org=None, metadata=None):
        client = SandboxClient(ORIGIN, 'synthetic-token', 'v61.0')
        client.get = Mock(side_effect=[org if org is not None else {
            'done': True, 'totalSize': 1, 'records': [{'IsSandbox': True}]},
            metadata if metadata is not None else {
                'name': 'Metric__c', 'queryable': True, 'fields': [{'name': 'Version__c'}]}])
        return client

    def test_success_is_only_metadata_evidence(self):
        client = self.client()
        result = probe(client, 'Metric__c', ['Version__c'])
        self.assertEqual(result['status'], 'sandbox_metadata_verified')
        self.assertFalse(result['metric_value_verified'])
        self.assertFalse(result['business_records_read'])
        self.assertEqual(client.get.call_count, 2)

    def test_unverified_org_stops_before_describe(self):
        for org in ({}, {'done': False}, {'done': True, 'totalSize': 1,
                     'records': [{'IsSandbox': False}]},
                    {'done': True, 'totalSize': 1, 'records': [{'IsSandbox': 'true'}]}):
            client = self.client(org=org)
            with self.assertRaises(ProbeError):
                probe(client, 'Metric__c', ['Version__c'])
            self.assertEqual(client.get.call_count, 1)

    def test_origin_rejects_production_and_url_tricks(self):
        for origin in ('http://example--dev.sandbox.my.salesforce.com',
                       'https://example.my.salesforce.com', ORIGIN + '.evil.com',
                       ORIGIN + '/path', ORIGIN + '?token=x', ORIGIN + ':443',
                       ORIGIN.replace('https://', 'https://user@')):
            with self.subTest(origin=origin), self.assertRaises(ProbeError):
                validate_origin(origin)

    def test_missing_or_mismatched_metadata_fails(self):
        for metadata in ({}, {'name': 'Other__c', 'queryable': True},
                         {'name': 'Metric__c', 'queryable': False},
                         {'name': 'Metric__c', 'queryable': True, 'fields': []},
                         {'name': 'Metric__c', 'queryable': True, 'fields': [None]}):
            with self.assertRaises(ProbeError):
                probe(self.client(metadata=metadata), 'Metric__c', ['Version__c'])

    def test_invalid_binding_never_connects(self):
        for name, fields in (('../Account', ['Name']), ('Account', []),
                             ('Account', ['Name', 'Name']), ('Account', ['Name FROM User'])):
            client = self.client()
            with self.assertRaises(ProbeError):
                probe(client, name, fields)
            client.get.assert_not_called()

    def test_redirect_refused(self):
        with self.assertRaises(ProbeError):
            NoRedirects().redirect_request(None, None, 302, '', {}, 'https://evil.com')

    def test_transport_get_timeout_and_auth(self):
        client = SandboxClient(ORIGIN, 'synthetic-token', 'v61.0')
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = b'{}'
        client.opener = Mock()
        client.opener.open.return_value = response
        self.assertEqual(client.get('/sobjects/Account/describe'), {})
        args, kwargs = client.opener.open.call_args
        self.assertEqual(args[0].method, 'GET')
        self.assertEqual(kwargs['timeout'], 20)
        self.assertEqual(args[0].get_header('Authorization'), 'Bearer synthetic-token')

    def test_http_error_body_not_exposed(self):
        client = SandboxClient(ORIGIN, 'synthetic-token', 'v61.0')
        client.opener = Mock()
        client.opener.open.side_effect = HTTPError(ORIGIN, 403, 'secret', {}, io.BytesIO(b'secret'))
        with self.assertRaisesRegex(ProbeError, 'HTTP 403') as ctx:
            client.get('/query')
        self.assertNotIn('secret', str(ctx.exception))

    def test_invalid_token_and_version(self):
        for token, version in (('', 'v61.0'), ('a\nb', 'v61.0'), ('x', '../query')):
            with self.assertRaises(ProbeError):
                SandboxClient(ORIGIN, token, version)


if __name__ == '__main__':
    unittest.main()
