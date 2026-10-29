WORKING STANDARDS
Skills: /skill deployment-patterns (CI/CD, health checks, rollback) and /skill canary-watch (post-deploy verification, log at ~/.hermes/canary-watch.log).
Quality gate: no deploy without a tested rollback and a health check. After deploy, run the canary check and report PASS or FAIL.
Alert thresholds and paging are not covered by these skills. Define them here and mark LOW CONFIDENCE when unsure.
Before any launch or customer demo, run /skill production-audit: it ends with a ship or block call, a score, the evidence checked and the evidence missing. Never run a remote scanner or upload source for it.
