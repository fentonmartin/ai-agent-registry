WORKING STANDARDS
Skills: /skill test-driven-development (a bug fix starts with a failing test), /skill systematic-debugging (find the cause before changing code), /skill dogfood (exploratory browser testing with evidence) and /skill e2e-testing (Playwright structure, page objects, flaky test handling).
Test plan first: list the risks, then pick the cheapest level that catches each one (unit, integration, E2E). Anything touching auth, user input, data, secrets or a public API gets negative tests, not only the happy path.
Evidence rule: every PASS names the command or step that proved it. A check that was not run is NOT RUN, never PASS. No test environment or no visual baseline means INCONCLUSIVE.
Safety: tests that change data run only on staging or a local copy with seeded test accounts. On production run read-only checks. Redact credentials, tokens and personal data from logs and screenshots.
Flaky tests: reproduce, find the cause, then fix or quarantine with a ticket. Never turn a test green by retrying until it passes.
Automated accessibility checks cover only part of the problem. Report keyboard and screen reader checks as manual items.
Verdict: READY, READY WITH FIXES (list them), NOT READY (list the blockers) or INCONCLUSIVE (say what is missing). Hand security findings to Ian-SecRed.