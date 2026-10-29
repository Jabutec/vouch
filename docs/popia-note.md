# Data handling note (POPIA)

This is a draft design note, not legal advice.

- Invoices contain personal information (names, contact details, banking details).
- Process locally; do not send invoice contents to external services.
- Store extracted fields and file hashes by default, not original files.
- Restrict access to the database and log access to evidence.
- Keep real invoices out of the repository (`samples/private/` is git-ignored).
- Define retention: how long reports and evidence are kept, and how to delete them.

TODO: complete before any use with real data.
