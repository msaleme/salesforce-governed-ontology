# Read-only sandbox readiness

This optional adapter verifies sandbox identity and requested object/field metadata using Salesforce REST. It does **not** execute a metric, implement a Salesforce semantic registry, call MuleSoft/Informatica, or establish an authorization boundary. Its tests use synthetic transport responses. No live org has been verified.

## Operator prerequisites

1. Designate a sandbox and approved internal evidence location with the platform owner.
2. Select existing semantic objects and field API names; do not deploy invented registry objects to fit the demo.
3. Use an approved short-lived sandbox session with the minimum available permissions. The probe only issues GET requests, but does not reduce the token's underlying privileges.
4. Choose a REST API version supported by the org. The example below is illustrative, not a compatibility claim.

Set a token locally without placing it in shell history. Never paste it into an issue, PR, or chat:

```bash
read -rsp 'Sandbox session token: ' SF_ACCESS_TOKEN
export SF_ACCESS_TOKEN
printf '\n'
python3 sandbox_probe.py \
  --instance-url https://YOURDOMAIN--SANDBOX.sandbox.my.salesforce.com \
  --api-version v61.0 \
  --object YOUR_APPROVED_OBJECT \
  --field YOUR_APPROVED_FIELD
unset SF_ACCESS_TOKEN
```

Replace all uppercase placeholders with approved names. Repeat `--field` for each required field. Standard, enhanced sandbox My Domain hostnames are supported; custom domains, production orgs and redirects are rejected. There is no automatic login, refresh, retry, credential persistence or network call in the offline test suite.

## Optional field-type contracts

After the platform owner supplies approved bindings, add repeatable
`--field-type YOUR_APPROVED_FIELD=string` arguments to the command above.
Each contract must name a field also supplied with `--field`; duplicate contracts
are rejected before any network request. Use the exact, case-sensitive REST
`describe` type, not a UI label. `string` is illustrative, not an approved binding.
No type coercion or compatibility inference is performed. Unknown type identifiers
are not treated as supported types: they must match the returned describe value.

A missing or mismatched type fails the probe. The sanitized receipt reports only
`field_type_contract_count` and `field_type_contracts_verified`, never the field
names or types. With no contracts, the count is zero and verification is false;
legacy name-only checks remain available. A subset of fields may be contracted,
so the count does not imply all requested fields have been type-checked.

Type agreement does not verify units, currency, precision/scale, reference targets,
nullability, accounting meaning or field access enforcement. Those remain separate
binding and live-read acceptance requirements. No actual org binding is included.

## What happens

1. Validate the hostname, API version and API-name syntax locally.
2. Send the fixed query `SELECT IsSandbox FROM Organization LIMIT 1`.
3. Stop unless a complete response explicitly identifies one sandbox organization.
4. GET the selected object's `describe` endpoint and verify its name, queryability and required field presence, plus any supplied exact field-type contracts.
5. Emit a timestamped summary without the hostname, org ID, token, object/field names or raw response. On failure, exit nonzero with a bounded diagnostic. HTTP response bodies are never printed.

Network requests have a 20-second timeout and a 2 MB response cap. Redirects are refused before a second request can forward credentials. TLS verification uses Python's normal trust store. A local machine controlling the token or trusted proxy remains within the operator's trust boundary.

## Interpretation and troubleshooting

- `sandbox_metadata_verified`: connection and selected metadata visibility passed for this identity only.
- HTTP 401: obtain a new approved session locally; no automatic refresh is attempted.
- HTTP 403: verify assigned access with the platform owner; do not broaden permissions just to make the probe green.
- Missing fields: check the actual API names and the current identity's metadata visibility.
- Sandbox identity unavailable: the probe stops before describe, including when Organization query access is unavailable.

A describe response is **not** a proof of field-level or row-level enforcement. No customer or business records are requested. Do not treat visibility of a field as permission to retrieve its values.

## Evidence gates for the real metric

The remaining dependencies are the [platform-fit packet](ASSURANCE.md): named owner/steward, approved definition version and dimensions, actual Informatica asset, fixed MuleSoft read operation and schemas, approved test records, and two differently restricted identities.

After those inputs exist, implement the fixed read binding and capture permitted/denied reads, revoked-definition rejection, stale/partial response handling and identity isolation. Keep live receipts in the approved private location, not this public repo. The offline ontology fixtures must not silently become live business approvals.

## Current evidence

- Implemented: bounded REST transport, sandbox-classification check and metadata-binding preflight.
- Verified locally: synthetic success/failure and transport regression controls, run by `python3 scripts/verify.py`.
- Not verified: live connectivity, real semantic bindings, metric values, identity propagation, restricted-principal denial, or vendor integration.
