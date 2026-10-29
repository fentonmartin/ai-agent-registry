---
name: ECC Mapping Reference
date: 2026-10-29
version: v2026.0.1
status: Verified against ECC release tag v2.2.3 (not main)
---

# ECC Mapping Reference (Ian L2)

Single reference for `ian-sync`. Machine-readable twin: `sync/ecc-mapping.json` (source of truth for the script; this file explains the reasoning).

Every item below was checked against the live ECC repository (`affaan-m/ECC`, release v2.2.3): the file exists and its description was read. Nothing is mapped by name guess.

## Rules

1. Persona fields (`title`, `role`, `triggers`, body) stay authoritative. ECC is a reference, never a replacement.
2. `ian-sync` writes two frontmatter fields only: `ecc-mapping` (list of `type:name`) and `ecc-fit` (`strong`, `partial`, `gap`).
3. `ian-sync` never copies ECC prompt text into a persona.
4. A `gap` is a valid result. Do not invent a mapping to fill it.
5. On every run, each item is re-checked against the live ECC tree. Missing items are reported as MISSING and are never auto-removed. A human decides.
6. When a persona's own choices differ from an ECC pattern (for example the fixed Flutter stack in Ian-Flutter), the persona wins.

## Fit summary

| Persona | Fit | ECC items |
|---|---|---|
| Ian-Flutter | strong | 7 |
| Ian-DevOps | strong | 3 |
| Ian-Plan | strong | 5 |
| Ian-API | partial | 4 |
| Ian-SecRed | partial | 3 |
| Ian-UI | partial | 4 |
| Ian-Alpha | partial | 3 |
| Ian-SecBlue | gap | 0 |
| Ian-UX | gap | 0 |

## Per-persona detail

### Ian-Flutter (strong)
- `skill:dart-flutter-patterns`: null safety, immutable state, state management, GoRouter, networking.
- `skill:flutter-dart-code-review`: library-agnostic review checklist.
- `agent:flutter-reviewer`, `agent:dart-build-resolver`: review and build error repair.
- `command:flutter-build`, `command:flutter-review`, `command:flutter-test`.
- Gap: Java to Flutter migration scan is not in ECC. Ian-Flutter keeps it.
- Note: ECC lists several state managers; Ian-Flutter's fixed stack stays authoritative.

### Ian-DevOps (strong)
- `skill:deployment-patterns`: CI/CD, Docker, health checks, rollback, production readiness. Direct match to the release, rollback, and health-check mandate.
- `skill:docker-patterns`: Dockerfile and Compose patterns, container security.
- `skill:canary-watch`: post-deploy smoke and canary verification.
- Gap: alert thresholds and paging.

### Ian-Plan (strong)
- `agent:planner`: planning specialist for complex features.
- `skill:blueprint`: one-line objective to step-by-step plan with dependency graph.
- `skill:plan-orchestrate`: decompose a plan into steps.
- `command:plan`: waits for user confirmation before any code. Fits the go/no-go gate.
- `command:plan-prd`: lean problem-first PRD.
- Gap: routing work packages to Pan, Ban, Lan and cost/timeline framing stay in the persona.

### Ian-API (partial)
- `skill:api-design`: REST only (naming, status codes, pagination, errors, versioning).
- `skill:postgres-patterns`, `skill:database-migrations`, `agent:database-reviewer`: schema design and migrations, PostgreSQL focus.
- Gaps: ERD authoring, OpenAPI spec output, non-REST styles.

### Ian-SecRed (partial)
- `skill:security-review`: security checklist (auth, input, secrets, endpoints).
- `skill:security-bounty-hunter`: remotely reachable, reportable vulnerabilities.
- `agent:security-reviewer`: vulnerability detection in code.
- Gaps: active pentest execution, perf-spike and cost-blowout review (not security topics).

### Ian-UI (partial)
- `skill:design-system`: extract or audit design tokens from a codebase.
- `skill:accessibility`: WCAG 2.2 AA across web, iOS, Android.
- `skill:frontend-design-direction`: product-specific UI direction.
- `agent:a11y-architect`: WCAG 2.2 architecture.
- Gaps: Figma libraries, visual design authoring, handoff specs.
- Excluded: `frontend-a11y` (React and Next.js only, too narrow for this persona).

### Ian-Alpha (partial)
- `skill:team-agent-orchestration`: owners, kanban state, branch isolation, merge gates.
- `skill:orch-pipeline`: gated research, plan, TDD, review, commit pipeline with two human gates.
- `agent:loop-operator`: monitor loops and intervene when they stall.
- Gap: ECC orchestration is git-branch based. Ian-Alpha's board also covers non-code roles, so the persona keeps its own board format.

### Ian-SecBlue (gap)
- No real ECC coverage: incident response, SIEM and SOC triage, monitoring, breach handling.
- `skill:security-scan` only scans `.claude/` config (AgentShield). `skill:agent-security-hardening` exists on `main` but not in release v2.2.3. Neither is mapped.
- `ecc-mapping` stays empty. That is the correct result.

### Ian-UX (gap)
- Nothing in ECC covers user research, journey mapping, usability testing, or information architecture.
- Closest research tooling (`deep-research`, `research-ops`) belongs to Ran, not Ian-UX.

## Found during verification, for later personas (not applied)

- `agent:chief-of-staff`: triages email, Slack, LINE, Messenger and drafts replies. Candidate for Zan.
- `skill:operator-approval-loop`: approval contract for agent-drafted outbound messages. Directly relevant to the WhatsApp reply-on-behalf design.
- `skill:deep-research`, `skill:research-ops`: cited research workflows. Candidates for Ran.
- `skill:hipaa-compliance`: candidate for Lan-Compliance.
- Ian L1 level: `skill:orch-pipeline`, `skill:verification-loop`, `skill:tdd-workflow`.

## Corrections from the first draft

The first mapping was name guesses. Checked against the ECC tree, 7 of 9 did not exist: `deployment-pipeline`, `security-monitoring`, `security-audit`, `ux-research`, `mobile`, `project-plan`, `orchestrator`. Only `api-design` and `design-system` were real. This file replaces that draft.

## How ian-sync uses this

1. Load `sync/ecc-mapping.json`.
2. Fetch the live ECC tree and confirm every item exists (skills at `skills/<name>/SKILL.md`, agents at `agents/<name>.md`, commands at `commands/<name>.md`).
3. Report MISSING items, new ECC release version, and personas whose `ecc-fit` is `gap`.
4. On `--write`, set `ecc-mapping` and `ecc-fit` in each persona frontmatter. Nothing else.
5. Any new mapping or fit change is added to this file first, then to the JSON.

## Import policy (what lands in Hermes)

Imports are copied verbatim from the release tag (never `main`) into `skills/ecc/` in the Hermes home. A lockfile (`skills/ecc/.ecc-lock.json`) stores the upstream and local hashes of every file.

Imported now (10 skills, MIT, copyright notice retained by ECC's LICENSE):
- Ian-API: `api-design`, `postgres-patterns`, `database-migrations`
- Ian-DevOps: `deployment-patterns`, `canary-watch` (one patch: log path `~/.claude/` to `~/.hermes/`)
- Ian-SecRed: `security-review`
- Ian-UI: `accessibility`
- Ian-Flutter: `dart-flutter-patterns`, `flutter-dart-code-review`
- Ian-Plan: `blueprint`

Rules enforced by `ian_sync.py --import-skills`:
1. Dry run by default. `--yes` is required to write.
2. Only the `skills/ecc/` namespace is touched. Existing Hermes skills are never overwritten.
3. A skill whose local files differ from the lockfile is SKIPPED, not overwritten (local edits win).
4. A patch whose target text is not found aborts that skill. Upstream changes are never patched blindly.
5. Re-running with no upstream change is a no-op.
6. `--check` reports a new ECC release and any locally modified skill.

Deliberately not imported, with reason (also in `sync/ecc-mapping.json` under `not_imported`):
- `security-scan`: Claude-specific. `docker-patterns`: tied to ECC's own compose files.
- `design-system`, `frontend-design-direction`: reference only (ECC slash commands).
- `security-bounty-hunter`: bounty-triage framing does not match the SecRed mandate.
- `plan-orchestrate`, `verification-loop`, `orch-pipeline`, `team-agent-orchestration`: concepts to adapt for Ian L1, not to import as-is.
- `operator-approval-loop` (Zan), `deep-research` and `research-ops` (Ran), `hipaa-compliance` (Lan): later phases.

Hooks: ECC ships two Hermes-native hooks (`config-protection`, `check-console-log`). They are NOT installed. Installing them means editing `config.yaml`, which needs a separate decision.
