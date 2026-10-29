WORKING STANDARDS
Skill: /skill security-review (auth, input handling, secrets, endpoints, cloud infrastructure).
Always review these areas: authentication and authorization, user input, database queries, file paths, external calls, cryptography, secrets. Report each finding as likelihood, severity and a one-line fix. Mark anything not proven LOW CONFIDENCE.
For a ship or block call across the whole release, use /skill production-audit. Cap the verdict when auth, secrets, idempotency or rollback is missing.
