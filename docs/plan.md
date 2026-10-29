# Vouch plan (repo copy)

**One-liner:** verify a business using its invoice, before you pay.

**Goals:** learn .NET and the South African legacy stack (SQL Server, flat files, Excel, Sage/SAP-style data); finish one demonstrable portfolio project; keep the scope calm.

**Non-goals:** not a business, not a payment system, not an ERP, not legal/tax/credit advice.

## Build chunks

One new thing per chunk. If a chunk overruns, cut a feature rather than extending the schedule.

| Chunk | Focus | Done when |
|---|---|---|
| 0 | Repo, decisions, 30 sample documents with expected results | Sample set and `expected` files exist |
| 1 | SQL Server schema, EF Core migrations, canonical invoice model | Database starts with one command; seed data loads |
| 2 | Parsers (text PDF, CSV) and document checks | Samples parse; Level 0 checks pass their tests |
| 3 | Supplier type classification, registration and VAT checks with mock providers, manual evidence endpoint | Report shows Unverified correctly and updates after evidence is entered |
| 4 | History checks (first-seen, duplicate, bank change) and audit table with hash chain | Duplicate and changed-bank samples caught; chain verifier passes |
| 5 | Report output, Swagger or one Razor page, README, POPIA note | Someone else can run it from the README |

**Stop rule:** when all sample documents give the expected report and the README is complete, the project is finished.

## Optional extras (at most one at a time)

1. COIDA Letter of Good Standing and CIDB grading evidence records
2. A real registry or AVS adapter via a provider
3. Local model (Ollama) used only to write the report summary, never to decide
4. Domain and email footprint checks
5. Structured e-invoice input once South African rules settle
6. Excel export, or a small SOAP/flat-file export to practise older integration styles
