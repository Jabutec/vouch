# Vouch

**Verify a business using its invoice, before you pay.**

Vouch takes a supplier invoice, works out who the supplier claims to be, runs a layered set of checks on that business, and returns a verification report: what is consistent, what is confirmed, what is missing, and what you should check yourself.

> **Status:** planning and scaffolding. Nothing is built yet. See [`docs/plan.md`](docs/plan.md).

## Why

Change-of-banking-details and fake-invoice fraud are a documented problem in South Africa. Most small businesses have no easy way to sanity-check a supplier before paying. Vouch is a learning project that explores how far a small, honest .NET service can get with that problem, using the stack South African organisations actually run: SQL Server, flat files, Excel and Sage/SAP-style data.

## How it reports

No single "trust score". Every claim is shown with how far it has been verified:

| Level | Meaning |
|---|---|
| 0. Consistent | The invoice agrees with itself and with expected formats |
| 1. Registered | An independent registry confirms the business exists |
| 2. In good standing | Statutory standing is evidenced (tax, COIDA, sector registrations) |
| 3. Safe to pay | The payment account is tied to the business and unchanged from history |

Statuses: **Pass, Warn, Fail, Unverified, Not applicable**. "Unverified" is a normal result, not a failure.

## Planned architecture

- **Vouch.Api**: ASP.NET Core Web API (`POST /verifications`, `GET /verifications/{id}`, evidence endpoint)
- **Vouch.Worker**: .NET Worker Service that watches a drop folder and parses PDF (text layer), CSV and Excel
- **Vouch.Core**: canonical invoice model, `IBusinessCheck` implementations, provider interfaces
- **Vouch.Infrastructure**: EF Core + SQL Server, parsers, provider adapters (mock first)
- **Vouch.Tests**: xUnit tests driven by the sample documents in `samples/`

One database (SQL Server), including an append-only audit table with a hash chain.

## Getting started

Prerequisites: .NET SDK (current LTS), Docker, Git.

```bash
# 1. Create the .NET solution and projects (one-off)
./scripts/scaffold.sh          # macOS / Linux / Git Bash
# or
./scripts/scaffold.ps1         # Windows PowerShell

# 2. Start SQL Server
cp .env.example .env           # then set a strong MSSQL_SA_PASSWORD
docker compose up -d
```

## Project principles

- Evidence over scraping: no scraping of government portals and no handling of anyone's credentials.
- Every external lookup sits behind an adapter with an offline mock.
- Results always carry their source and date.
- The tool flags and organises evidence; the user decides. It is not legal, tax or credit advice.

## Privacy

Invoices contain personal and banking information (POPIA applies). Process locally, store extracted fields and hashes rather than original files by default, and keep real invoices out of this repository. See [`docs/popia-note.md`](docs/popia-note.md).

## Roadmap

See [`docs/plan.md`](docs/plan.md). Work is split into weekend-sized chunks with a stop rule: when the sample documents produce the expected reports and the README is complete, the project is finished.

## License

To be decided.
