WORKING STANDARDS
Build loop for any build request:
1. Size it in one line: trivial (1 file), small, standard (2-5 files), large (cross-cutting, new dependency, or public API). Anything touching auth, user input, data, secrets or a public API is at least standard.
2. Plan: Ian-Plan drafts the work packages. GATE 1: no implementation until <USER> approves the plan (skipped for trivial).
3. Build: tests first where a test is possible. One specialist per work package, one output path each.
4. Verify before saying done: build, tests, lint, secret scan, diff review. Report PASS or FAIL for each check, then READY or NOT READY.
5. Review: bring in Ian-SecRed whenever the size rule above was triggered by a security area. Van challenges the final plan on request.
6. GATE 2: show the diff summary and the proposed commit message. Commit or deploy only after <USER> confirms.
7. Remember: add the status to ACTIONS.log and one lesson line to MEMORY.md in the project folder.
Context discipline: load specialist skills on demand with /skill <name>, never preload. If two consecutive checkpoints show no progress, stop and report to <USER>.
