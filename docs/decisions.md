# Decision log

## ADR-001: Name (2026-10-29)
Product name **Vouch** (the accounting term for checking against evidence). **InvoiceCheck** remains the name of the first module (invoice analysis).

## ADR-002: Scope (2026-10-29)
Pre-payment verification of a business from its invoice. Learning and portfolio project, not a business. Reports use verification levels instead of a single trust score.

## ADR-003: Database (2026-10-29, superseded by ADR-006)
Originally: SQL Server only, with an audit hash chain; DynamoDB, Redis and SignalR dropped.

## ADR-004: Evidence over scraping (2026-10-29)
External lookups sit behind adapters with offline mocks. Government portals without a public API are handled by "verify here" links and manually recorded evidence. No scraping, no handling of credentials.

## ADR-005: Pure core (2026-10-30)
`Vouch.Core` has no file, network or database access. Checks are small classes behind one interface. Storage is behind `IHistoryStore`, so it can be in-memory first and SQL Server later.

## ADR-006: Build in stages, full backend (2026-10-30)
After considering a small CLI-only utility and a browser-only (Blazor WebAssembly) tool, the decision is to build the full backend (API, EF Core, SQL Server) in stages, so the .NET backend is learned properly. Each stage is shippable and stopping after any stage is a valid finish. SQL Server returns at stage 3.

## ADR-007: No-signup experience (2026-10-30)
The product goal stays "drop an invoice, get a report, no account". Processing is ephemeral by default. Optional history uses a browser-held API key rather than user accounts (stage 4).
