# Decision log

## ADR-001: Name (2026-10-29)
Product name **Vouch** (the accounting term for checking against evidence). **InvoiceCheck** remains the name of the first module (invoice analysis).

## ADR-002: Scope (2026-10-29)
Pre-payment verification of a business from its invoice. Learning and portfolio project, not a business. A stop rule defines "done".

## ADR-003: Single database (2026-10-29)
SQL Server only, including an append-only `AuditEvent` table with a hash chain. DynamoDB, Redis and SignalR from earlier drafts are dropped unless a later need is demonstrated.

## ADR-004: Evidence over scraping (2026-10-29)
External lookups sit behind adapters with offline mocks. Government portals without a public API are handled by "verify here" links and manually recorded evidence. No scraping, no handling of credentials.

## ADR-005: No single trust score (2026-10-29)
Reports show verification levels (0 to 3) and per-check statuses with source and date, including "Unverified" as a normal outcome.
