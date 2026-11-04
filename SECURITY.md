# Security scope

This is an offline synthetic prototype. It has no server, authentication implementation, secret store, network client, or production authorization boundary. Scope strings and approval references are fixture inputs, not trusted credentials.

Do not connect this code directly to production or expose its functions as an untrusted-input API. The current implementation assumes well-shaped local dictionaries and can raise exceptions for malformed data. Source and bridge strings are not verified evidence.

Future integration must establish authenticated identity propagation, source and metadata authorization, tenant-safe caching, bounded operations, freshness, revocation, and sanitized audit evidence. See [architecture](docs/ARCHITECTURE.md) and [platform acceptance](docs/PLATFORM-FIT-REVIEW.md).

For a suspected issue, contact the repository owner privately through an established channel. Share a minimal synthetic reproduction; never include tokens, credentials, customer records, or sensitive logs in an issue or PR. No dedicated security response service or SLA is represented here.
