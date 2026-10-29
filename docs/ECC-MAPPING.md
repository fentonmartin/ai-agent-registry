---
name: ECC Mapping Reference
date: 2026-10-29
version: v2026.0.2
status: Verified against ECC release tag v2.2.3 (not main)
---

# ECC Mapping Reference

Single reference for `ian-sync`. Machine-readable twin: `sync/ecc-mapping.json` (the script reads it; this file explains it).

Every item was checked against ECC release v2.2.3: the file exists and its description was read. Nothing is mapped by name guess. The first draft guessed names and 7 of 9 did not exist; that draft was discarded.

## Principles

1. Persona fields (`title`, `role`, `triggers`, body) stay authoritative. ECC is a reference.
2. ECC prompt text is never pasted into a persona. Each persona gets a short WORKING STANDARDS block written in our own words (`sync/standards/<key>.md`), which names the ECC skills to load on demand with `/skill <name>`.
3. ECC skills are imported verbatim from the release tag into `skills/ecc/` in the Hermes home, with a lockfile. Local edits always win.
4. A `gap` is a valid result. A mapping is never invented to fill it.
5. Domains that ECC does not cover (wellness, legal advice, quotation, learning coaching, real-person research) stay untouched.

## Fit per persona

| Persona | Fit | ECC items | Imported skills used |
|---|---|---|---|
| Ian | partial | 5 | - |
| Ian-Plan | strong | 5 | blueprint |
| Ian-Alpha | partial | 3 | - |
| Ian-API | partial | 4 | api-design, contract-first, database-migrations, postgres-patterns |
| Ian-DevOps | strong | 3 | canary-watch, deployment-patterns |
| Ian-SecRed | partial | 3 | security-review |
| Ian-SecBlue | gap | 0 | - |
| Ian-UI | partial | 4 | accessibility |
| Ian-UX | gap | 0 | - |
| Ian-Flutter | strong | 7 | dart-flutter-patterns, flutter-dart-code-review |
| Pan | partial | 4 | product-lens |
| Ban | partial | 3 | competitive-platform-analysis, investor-materials, market-research |
| Van | partial | 2 | council |
| Wan | partial | 2 | article-writing, brand-voice |
| Zan | partial | 3 | counterparty-channel-discipline, operator-approval-loop |
| Ran | partial | 3 | market-research |
| Ran-Business | partial | 3 | benchmark-methodology, competitive-platform-analysis, market-research |
| Ran-Brand | partial | 2 | benchmark-methodology, brand-voice |
| Ran-People | gap | 0 | - |
| Ean | gap | 0 | - |
| Han | gap | 0 | - |
| San | gap | 0 | - |
| Qan | gap | 0 | - |
| Lan | gap | 0 | - |
| Lan-Contract | gap | 0 | - |
| Lan-IP | gap | 0 | - |
| Lan-Compliance | gap | 0 | - |

Not assessed in this pass: Jan, Ran-Tech, Ran-Web, Ran-App, Ran-General.

## Concepts adapted, not copied

- Ian L1 build loop: size the request, plan, GATE 1 (approval), build tests-first, verify with PASS or FAIL, review, GATE 2 (confirm before commit or deploy), remember. Based on `orch-pipeline`, `verification-loop`, `tdd-workflow`; rewritten for our work (not Node/TS, not Claude Code commands).
- Stall rules for Ian-Alpha (from `loop-operator`): stop after two checkpoints without progress.
- Independent review (from `santa-method`): the reviewer is never the author. Placed in Van and Ian.
- Context discipline (from `context-budget`): skills load on demand, never preloaded.
- Zan outbound approval (from `operator-approval-loop`): draft, show exact text, send only after approval of that exact text, keep a record.

## Imported skills (26)

Verbatim from v2.2.3, MIT. Patches only where a path or command does not exist in Hermes.

- `api-design`: ian-api
- `postgres-patterns`: ian-api
- `database-migrations`: ian-api
- `deployment-patterns`: ian-devops
- `canary-watch`: ian-devops (patched)
- `security-review`: ian-secred
- `accessibility`: ian-ui
- `dart-flutter-patterns`: ian-flutter
- `flutter-dart-code-review`: ian-flutter
- `blueprint`: ian-plan
- `contract-first`: ian-api
- `council`: van (patched)
- `product-lens`: pan
- `market-research`: ban, ran, ran-business
- `investor-materials`: ban
- `competitive-platform-analysis`: ban, ran-business
- `benchmark-methodology`: ran-business, ran-brand
- `brand-voice`: wan, ran-brand
- `article-writing`: wan
- `production-audit`: ian-devops, ian-secred
- `parallel-execution-optimizer`: ian-alpha
- `competitive-report-structure`: ban, ran-business
- `make-interfaces-feel-better`: ian-ui
- `seo`: ran-web
- `operator-approval-loop`: zan
- `counterparty-channel-discipline`: zan

## Not imported, with reason

- `security-scan`: scans .claude/ config with AgentShield, Claude-specific
- `docker-patterns`: built around ECC's own docker/plugin-setup compose files
- `design-system`: examples use ECC slash commands that do not exist in Hermes; reference only
- `frontend-design-direction`: ECC-specific design direction; reference only
- `security-bounty-hunter`: bounty-triage framing ('does this pay?') does not match SecRed's review mandate; reference only
- `plan-orchestrate`: emits ECC slash commands, useless outside ECC
- `verification-loop`: Node/TS-centric commands and /verify; concept to be adapted into Ian L1, not imported
- `orch-pipeline`: depends on the orch-* command family; concept to be adapted into Ian L1
- `team-agent-orchestration`: git-branch based; concept only
- `deep-research`: needs firecrawl/exa MCP; Ran uses web_search/web_extract. Reference only
- `research-ops`: reference only
- `hipaa-compliance`: US healthcare law; not relevant to Indonesian HR platform. Not mapped
- `santa-method`: references Claude Code; concept (independent reviewer must not be the author) folded into Van and Ian standards
- `context-budget`: audits Claude Code agents/MCP/rules; concept folded into Ian standards
- `tdd-workflow`: 21 KB, Node/TS commands; concept folded into Ian build loop
- `product-capability`: dev-oriented PRD to capability plan; reference only
- `ai-first-engineering`: principles already covered by the Ian build loop; its hiring-signals section does not apply
- `architecture-decision-records`: writes to docs/adr/, which conflicts with our project-folder protocol. Needs a decision on where decisions are recorded
- `dashboard-builder`: Grafana and SigNoz only; our monitoring stack is not defined yet
- `email-ops`: reference for Zan; Hermes has no mail surface wired yet
- `loop-design-check`: built on Claude Code /loop and /goal; stall rules already folded into Ian-Alpha
- `intent-driven-development`: 17 KB, large fixed context cost; acceptance-criteria idea already in Ian-Plan

## Known gaps

- Ian-SecBlue: no ECC coverage for incident response, SIEM or monitoring. Needs another source.
- Ian-UX: no ECC coverage for user research. Needs another source.
- ECC agent and command items are listed as references only. Hermes has no equivalent format, so they are not installed.
- Hooks: ECC ships two Hermes-native hooks (`config-protection`, `check-console-log`). Not installed: this needs an edit to `config.yaml` and a separate decision.

## How ian-sync uses this

- `--check`: reads the mapping, verifies every item exists at the latest ECC release, reports a new release, missing items, and locally modified imports.
- `--import-skills [--yes]`: copies mapped skills from the release tag. Dry run by default. Skips any skill whose local files changed. Aborts a skill if a patch target is missing.
- `--apply-personas [--local-source DIR] [--user NAME] [--yes]`: sets `ecc-mapping` and `ecc-fit` (registry) and upserts the standards block between `ian-sync:standards` markers. Dry run by default. Refuses to write unresolved identity tokens. Idempotent.
- `--write [--yes]`: legacy Ian L2 metadata writer.
- Order for changes: update this file, then `sync/ecc-mapping.json`, then `sync/standards/`, then run the commands.

## Native Hermes skills used by personas

Not from ECC. Listed in `native_skills` in the mapping file and checked by `--audit` (must be installed and named in the persona standards).

- `grounded-citations`: ran, ran-tech, ran-general
- `web-perf`: ran-web
- `blocked-page-recovery`: ran-web

## Own material, no external source

- Ian-SecBlue: contain, fix, learn incident runbook, written by us. ECC has no incident response or SIEM material. The `ai-sec-incident` skill in `berani-ai-skills` was read and informed the three-move shape, but it is tied to that suite's `.ai-skills/` folder layout and its paths, so it was not imported.
- Ran-Tech, Ran-App, Ran-General: no ECC fit. Ran-Tech would need the Context7 MCP server for ECC `documentation-lookup`, which is not configured.
