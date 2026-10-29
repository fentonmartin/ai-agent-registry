WORKING STANDARDS
Skills: /skill deployment-patterns (CI/CD, health checks, rollback) and /skill canary-watch (post-deploy verification, log at ~/.hermes/canary-watch.log).
Quality gate: no deploy without a tested rollback and a health check. After deploy, run the canary check and report PASS or FAIL.
Alert thresholds and paging are not covered by these skills. Define them here and mark LOW CONFIDENCE when unsure.
