# Check catalogue

Tiers: **MVP** (build), **Later** (extras), **Stretch** (only with spare energy), **Out** (not built; link to where to check).

| Group | Check | Source of evidence | Tier |
|---|---|---|---|
| Document | Required tax-invoice fields | The invoice (confirm current VAT Act requirements) | MVP |
| Document | Arithmetic and VAT rate | The invoice | MVP |
| Document | Format validation (CIPC, VAT, branch code, account number) | Offline rules | MVP |
| Document | Internal consistency (name vs email domain vs account holder) | The invoice | MVP |
| Document | Red flags (PDF metadata, free email, urgency wording) | The invoice | MVP |
| Identity | Supplier type classification | The invoice | MVP |
| Identity | CIPC status and name match | CIPC register via adapter or manual evidence | MVP (adapter) |
| Identity | VAT vendor match | SARS VAT Vendor Search (manual evidence) | MVP |
| Tax | Tax Compliance Status | Needs a PIN from the supplier; manual evidence | Later |
| Standing | COIDA Letter of Good Standing | Verify certificate number on the Compensation Fund site | Later |
| Standing | CIDB grading | CIDB register (construction) | Later |
| Standing | B-BBEE certificate or affidavit | Issuer verification | Stretch |
| Payment | Bank change versus history | Own history | MVP |
| Payment | Account ownership (AVS) | Via bank or intermediary, commercial agreement | Later |
| History | First-seen supplier, duplicate invoice | Own history | MVP |
| History | Amount or sequence anomalies | Own history | Later |
| Footprint | Domain age, email/domain match | Public lookups | Stretch |
| Screening | Court judgments, director history, sanctions | Regulated or paid sources | Out |

Statuses: Pass, Warn, Fail, Unverified, Not applicable.

Reminder: a legitimate business may lack some of these (sole proprietors have no CIPC number; small suppliers may not be VAT-registered). Missing evidence is only a flag when the invoice itself claims it.
