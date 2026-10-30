# Vouch

**Verify a business using its invoice, before you pay.**

Drop in a supplier invoice and Vouch works out who the supplier claims to be, runs a layered set of checks on that business, and returns a verification report: what is consistent, what is confirmed, what is missing, and what to check yourself.

> **Status:** Stage 1 (core and tests). See [`docs/plan.md`](docs/plan.md).

## Why

Change-of-banking-details and fake-invoice fraud are a documented problem in South Africa, and most small businesses have no easy way to sanity-check a supplier before paying. Vouch is a learning project: a small, honest .NET product built in stages, using the kind of stack South African organisations actually run (SQL Server, flat files, Excel).

## How it reports

No single "trust score". Every claim shows how far it has been verified:

| Level | Meaning |
|---|---|
| 0. Consistent | The invoice agrees with itself and with expected formats |
| 1. Registered | An independent registry confirms the business exists |
| 2. In good standing | Statutory standing is evidenced (tax, COIDA, sector registrations) |
| 3. Safe to pay | The payment account is tied to the business and unchanged from history |

Statuses: **Pass, Warn, Fail, Unverified, Not applicable**. "Unverified" is a normal result, not a failure.

## Built in stages

Each stage ends with something that works. Stopping after any stage is a legitimate finish.

| Stage | Adds | Projects |
|---|---|---|
| 1. Core | Parsing, checks, report, tests against `samples/`, optional tiny CLI | `Vouch.Core`, `Vouch.Tests` |
| 2. API | ASP.NET Core Web API, validation, Swagger, integration tests | `Vouch.Api` |
| 3. Database | EF Core + SQL Server, migrations, history checks (duplicate, first-seen, bank change) | `Vouch.Infrastructure` |
| 4. Production habits | Logging, health checks, config and secrets, Dockerfile, CI, rate limiting, optional API key | n/a |
| 5. Extras | Folder-intake worker, audit hash chain, front end, real registry adapters | `Vouch.Worker` |

## Getting started

Prerequisites: .NET 10 SDK and Git. Docker is only needed from stage 3.

```powershell
# create the solution and the stage 1 projects (re-run with -Stage 2, 3, 5 later)
powershell -ExecutionPolicy Bypass -File scripts\scaffold.ps1

dotnet build
dotnet test
```

On macOS, Linux or Git Bash: `./scripts/scaffold.sh` (pass a stage number as the first argument for later stages).

From stage 3: `cp .env.example .env`, set a strong `MSSQL_SA_PASSWORD`, then `docker compose up -d` (and `docker compose stop` when you are not working on the database).

## Principles

- Evidence over scraping: no scraping of government portals and no handling of anyone's credentials.
- Every external lookup sits behind an adapter with an offline mock.
- Results always carry their source and date.
- The tool flags and organises evidence; the user decides. It is not legal, tax or credit advice.

## Privacy

Invoices contain personal and banking information (POPIA applies). Store extracted fields and hashes rather than original files by default, and keep real invoices out of this repository. See [`docs/popia-note.md`](docs/popia-note.md).

## License

To be decided.
