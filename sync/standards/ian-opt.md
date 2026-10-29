WORKING STANDARDS
Skills: /skill web-perf (audit, diagnose, optimize loading and interactivity — Core Web Vitals, TTFB, LCP, CLS, INP) and /skill parallel-execution-optimizer (speed up tasks via dependency graph, parallel lanes, batched tool calls — isolate write surfaces, map dependencies first).
Baseline rule: every recommendation must be backed by a measured before/after delta. A change without a measurement is a guess, not an optimization.
Budget: report Core Web Vitals against Google thresholds (LCP <2.5s, INP <200ms, CLS <0.1). Flag any metric above "needs improvement" as a blocker before launch.
Verdict: IMPROVED (delta + evidence), REGRESSED (what got worse and why), INCONCLUSIVE (baseline missing or environment unstable).
