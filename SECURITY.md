# Security scope

The core CLI is offline. It has no server, authentication implementation, secret store or production authorization boundary. Scope strings and approval references are supplied inputs, not trusted credentials. The separate opt-in sandbox metadata probe is a network client; the tour and BYOD commands do not invoke it.

Do not connect this code directly to production or expose its functions as an untrusted-input API. The CLI validates file structure and semantic constraints, but this is not a resource-isolation service. Very large/deep inputs can exhaust memory or parser limits. Source and bridge strings are not verified evidence. BYOD reports include supplied definitions and expectations, so treat its output as private when the inputs are private.

Future integration must establish authenticated identity propagation, source and metadata authorization, tenant-safe caching, bounded operations, freshness, revocation, and sanitized audit evidence. See [architecture](docs/ARCHITECTURE.md) and [platform acceptance](docs/ASSURANCE.md).

For a suspected issue, contact the repository owner privately through an established channel. Share a minimal synthetic reproduction; never include tokens, credentials, customer records, or sensitive logs in an issue or PR. No dedicated security response service or SLA is represented here.
