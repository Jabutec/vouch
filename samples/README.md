# Sample documents

Synthetic invoices only. Never commit real invoices (use `samples/private/`, which is git-ignored).

Plan: about 30 files covering clean company, sole-proprietor and VAT-vendor invoices; wrong arithmetic; missing required fields; malformed CIPC/VAT numbers; name mismatches; duplicates; changed bank account; first-time supplier; "banking details changed" wording; a PDF edited after creation; messy amount formats.

Each file gets an expected-result file (see `expected.example.json`). Hold back five files you never tune against.
