# Vouch plan

**One-liner:** verify a business using its invoice, before you pay.

**Goals:** learn the .NET backend properly (C#, ASP.NET Core, EF Core, SQL Server, testing, CI), on the stack South African organisations run; finish a demonstrable portfolio project; keep each step small.

**Non-goals:** not a business, not a payment system, not an ERP, not legal/tax/credit advice.

## Stages

One new thing at a time. If a stage overruns, cut a feature rather than extend the schedule. Stopping after any stage is a legitimate finish.

### Stage 1: Core (no database, no Docker)
- Canonical `Invoice` model, amount and date parsing (including `R20000`, `R 40 000,00`, `R 6,000.00`)
- PDF text extraction (PdfPig) and a parser from text to `Invoice`
- Document checks: required fields, arithmetic, VAT rate, CIPC/VAT/bank formats, name and email consistency, red-flag wording
- Report model with statuses and verification levels
- xUnit tests driven by `samples/*.expected.json`
- **Done when:** the 10 samples give the expected statuses.

### Stage 2: API
- `POST /verifications`, `GET /verifications/{id}` (in-memory store at first)
- Validation, ProblemDetails errors, Swagger, integration tests
- **Done when:** a sample PDF uploaded through Swagger returns the right report.

### Stage 3: Database
- EF Core + SQL Server (Docker), migrations
- `IHistoryStore` behind an interface; history checks: duplicate invoice, first-seen supplier, bank change
- **Done when:** samples 08 and 09 are caught after 01 is stored.

### Stage 4: Production habits
- Serilog logging, health checks, configuration and secrets, API Dockerfile, GitHub Actions CI, rate limiting
- Optional: browser-held API key (no signup form) tying history to a key
- **Done when:** CI is green and the API runs from a container.

### Stage 5: Extras (pick one at a time)
1. Folder-intake worker service
2. Audit hash chain in SQL Server
3. Front end (Blazor or Next.js)
4. COIDA / CIDB evidence records
5. A real registry or AVS adapter
6. Local model used only to write the report summary, never to decide
7. Structured e-invoice input once South African rules settle

## Hardware note

On an 8 GB machine, stages 1 and 2 need no Docker. Run the SQL Server container only while working on stage 3, and cap WSL2 memory (for example 3 GB in `.wslconfig`).
