# Sample documents

**Synthetic invoices only.** Every company, registration number, VAT number and bank detail here is fictional. Never commit real invoices (use `samples/private/`, which is git-ignored).

Regenerate or extend with `python tools/generate_samples.py` (needs `pip install reportlab`).

## Batch 1 (10 files)

| File | What it tests | Context |
|---|---|---|
| 01-clean-company-vat | Everything consistent (baseline) | isolated |
| 02-clean-sole-proprietor | No CIPC, no VAT; must NOT be flagged | isolated |
| 03-arithmetic-wrong-subtotal | Lines do not add up to the subtotal | isolated |
| 04-vat-rate-wrong | VAT is not the standard rate | isolated |
| 05-vat-charged-no-vat-number | Tax invoice with VAT but no supplier VAT number | isolated |
| 06-malformed-cipc | CIPC number in the wrong format | isolated |
| 07-name-mismatch | Account holder and email domain do not match the supplier | isolated |
| 08-bank-changed-urgent | Bank account differs from history, "details changed" and urgency wording | after 01 |
| 09-duplicate-invoice | Same supplier, number and amounts as 01 | after 01 |
| 10-messy-amount-formats | Correct invoice with mixed amount formats | isolated |

## Expected results

Each `*.expected.json` has:

- `expectedParsed`: the values a parser should extract
- `expected`: per-check status (`pass`, `warn`, `fail`, `unverified`, `notApplicable`)
- `highestLevelReached`: `0` if no document-level check fails, otherwise `"none"` (levels 1 to 3 need external evidence, so none of these reach them)
- `context`: `isolated` means run against an empty database; `after` means first process the files in `seedHistoryFrom`

`manifest.json` lists the run order. Hold back some files (set `heldBack: true`) that you never tune against.

## Notes and assumptions

- The standard VAT rate is assumed to be 15%; confirm the current rate before relying on it.
- Branch codes and account numbers are made up and only test structure.
- `registry.cipcStatus` and `vat.vendorMatch` are `unverified` by design: no external lookup is performed without evidence.
- `history.firstSeen`: `warn` means a new supplier (informational).
