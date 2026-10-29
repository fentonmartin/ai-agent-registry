---
title: ian-sync Design Document
date: 2026-10-26
version: v2026.0.1
status: Draft — pending user approval
author: Zan (exec assistant)
---

# ian-sync: Ian Ecosystem Sync Command

## Purpose
Sync knowledge, framework mappings, and version state for all Ian‑related personas (L2, possibly L3). When run, it checks the latest version of registered tools (currently ECC, with capacity for future tools) and re‑adjusts mappings against the current Ian L2/L3 hierarchy — without overwriting existing content recklessly.

## Core Guarantees (the "safe‑by‑default" contract)

| Guarantee | What It Means |
|---|---|
| **Read‑only by default** | `ian-sync` does NOT modify any file unless `--write` is explicitly passed. Running `ian-sync --check` reports status only. |
| **Backup before write** | If `--write` is used, every modified `.md` file is backed up to `~/.hermes/ian-sync-backup/<timestamp>/` before any changes land. |
| **No automatic overrides** | The script never replaces a existing `title:`, `role:`, `triggers:`, or `description:` field. It only adds or augments fields that are currently missing (e.g., `version:`, `ecc-mapping:`, `latest-version:`). |
| **Explicit user confirmation** | Before any file is changed, the script prints a summary of what it would change and requires the user to reply `yes` (case‑insensitive) to proceed. |
| **L3 only fills when there’s a natural split** | L3 children are only added when an L2 specialist has ≥3 natural sub‑categories (e.g., `ian-api` having REST/GraphQL/Webhooks). Otherwise L3 stays empty `{` as it is now`. |
| **Version metadata added only where missing** | Any L2 or L3 file without a `version:` field gets `version: 1.0` appended at the end of the YAML frontmatter. Files that already have `version:` are left untouched. |
| **ECC mapping is additive, not replacement** | An `ecc-mapping:` field is added that lists the corresponding ECC agent/skill names. Existing content in `title:`, `role:`, `triggers:` is never removed. |

## Workflow

```
Step 1: ian-sync --check
  • Scans all Ian L2 .md files under personas/l2/ian/
  • Checks latest ECC version from GitHub (currently v2.2.3)
  • Reports:
    – Which L2 files have `version:` metadata (and which don’t)
    – Current ECC latest version
    – Natural ECC‑skill candidates for each L2 (based on trigger keywords)
    – Whether L3 should be populated (count of natural sub‑categories)
  • Exit code 0 – info only; exit code 1 if anything is missing version metadata (optional flag)

Step 2: ian-sync --write  (after user says “yes”)
  • Backs up every modified file to ~/.hermes/ian-sync-backup/<timestamp>/
  • For each L2 file:
    – If no `version:` → add `version: 1.0` (at end of frontmatter)
    – If natural ECC mapping exists → add `ecc-mapping:` list (append only)
    – If L3 should be populated → create L3 sub‑files with minimal frontmatter
  • For each L3 file (if created):
    – Inherits `parent: <L2-key>` from its L2 parent
    – Gets `version: 1.0` if missing
    – Gets `ecc-mapping:` referencing the parent’s ECC mapping
  • Commits all changes with message “ian-sync: bump versions & add ECC mappings (user-approved)”

Step 3: ian-sync --status
  • Reports current state:
    – Total L2 files, how many have version metadata
    – ECC latest version vs each L2’s recorded version
    – L3 population status (empty or with children)
    – Summary of added ecc‑mapping entries
```

## ECC Natural‑Mapping Table (read‑only reference)

| Ian L2 (current) | ECC Agent / Skill (likely match) | Reason |
|---|---|---|
| `ian-api` | `ecc` agent for `api-design` / skill `api‑design` | Both handle ERD + OpenAPI path design; Ian‑API’s triggers `api`, `erd`, `desain data` line‑up with ECC’s API‑design focus. |
| `ian-devops` | ECC agent/skill `deployment‑pipeline` | Release steps, rollback plans, health checks map 1:1 to ECC’s deployment‑pipeline skill. |
| `ian-secblue` | ECC agent/skill `security‑monitoring` (blue‑team) | Defensive security, SIEM triage, incident response match ECC’s security‑monitoring agent. |
| `ian-secred` | ECC agent/skill `security‑audit` (red‑team) | Adversarial reviews, OWASP checks, vulnerability mapping match ECC’s security‑audit agent. |
| `ian-ux` | ECC skill `research‑docs` / `ux‑research` | UX research, journey mapping, persona validation align with ECC’s research‑docs skill. |
| `ian-ui` | ECC skill `design‑system` | Figma components, design tokens, handoff specs map to ECC’s design‑system skill. |
| `ian-flutter` | ECC harness `mobile` / `cross‑platform` | Mobile‑Flutter specialization naturally fits ECC’s mobile‑harness adapter. |
| `ian-plan` | ECC skill `project‑plan` | Checklist‑based planning, go/no‑go gates map to ECC’s project‑plan skill. |
| `ian-alpha` | ECC agent `orchestrator` | Lead‑orchestrator role (assign specialists, track YAML checkpoints) matches ECC’s orchestrator agent. |

**Note:** This table is **read‑only** — `ian-sync` never writes to `title:`, `role:`, or `triggers:` based on it. It only adds an `ecc-mapping:` field that lists the ECC names, for the user’s reference.

## L3 Population Logic (when `--write` is used)

L3 is currently empty: `children: {` in config.yaml.

`ian-sync` will add L3 children **only** if the parent L2 has ≥3 natural sub‑categories detectable from its `triggers:` and description. The logic:

1. Count distinct keyword groups in `triggers:` and the file’s description.
2. If ≥3 groups → create L3 sub‑files under that L2 parent.
3. If <3 groups → leave L3 empty; record `l3-populated: false` in the L2 file’s frontmatter.

**Example:** `ian-api` has triggers `["api", "erd", "desain data"]` → 3 distinct groups → L3 populated with:
- `ian-api‑rest` (REST‑focused API design)
- `ian-api‑graphql` (GraphQL‑focused API design)
- `ian-api‑webhooks` (Webhook design & subscription)

Each L3 file gets minimal frontmatter:
```yaml
name: ian-api-rest
title: Ian-API‑REST — RESTful API Design
parent: ian-api
version: 1.0
ecc-mapping: [ecc api-design]
triggers: ["rest", "openapi", "resource"]
```

**Do NOT create L3** if the L2 already has a flat, cohesive mandate (e.g., `ian-flutter` has a very focused scope). `ian-sync` will flag this and skip L3 creation.

## Version‑Metadata Policy

| State | Action by `ian-sync` |
|---|---|
| L2/L3 file has `version:` already | Leave untouched. |
| L2/L3 file missing `version:` | Append `version: 1.0` at the very end of the YAML frontmatter (before the closing `---`). |
| L2/L3 file has `version: 1.0` (first run) | No change on subsequent runs. |
| User upgrades a file manually to `version: 2.1` | Script respects user’s version; does not downgrade. |

## Implementation (bash + python sketch)

The actual command is a bash wrapper that calls a small Python script (`~/hermes/scripts/ian_sync.py`). The Python script:

1. Reads each `personas/l2/ian/*.md` file’s YAML frontmatter.
2. Calls `gh api repos/affaan-m/ECC/releases` to get latest ECC version.
3. Uses a simple keyword‑grouping heuristic on `triggers:` and description to determine ECC mappings and L3 need.
4. Prints a human‑readable "check" summary.
5. If `--write` is flagged and user confirms `yes`, applies the additive changes described above.

**Safety invariants enforced by the script:**
- Never `git mv` or delete original content.
- Never overwrite an existing `version:`, `title:`, `role:`, or `triggers:`.
- Never create L3 files unless the ≥3‑group threshold is met.
- Always backup before writing.
- Exit with a clear summary; no silent changes.

---

## User Decision Points (before running `--write`)

1. **Accept ECC mappings?** The script will propose adding `ecc-mapping:` to some or all L2 files. If you say no, those lines are skipped.
2. **Populate L3?** The script will report which L2 specialists qualify (have ≥3 natural sub‑categories). If you say no, L3 stays empty `{` as it is now`.
3. **Set custom versions?** If any L2 file already has a `version:` other than `1.0`, the script will keep your version and not overwrite it.
4. **Backup location?** Default is `~/.hermes/ian-sync-backup/`. Can be overridden with `--backup-dir <path>`.

---

## Next Steps (after user approval)

1. Create the skill/file: `scripts/ian_sync.py` (Python) + `scripts/ian-sync` (bash wrapper).
2. Run `ian-sync --check` → review the summary.
3. If OK, run `ian-sync --write` → after user replies `yes`, changes land.
4. Verify: `read_file` each modified file to confirm only additive fields were added.
5. Commit the changes to the repo with a clear message.

---
---
**This design document is the recommendation.** It prioritizes:
- **Safety** — no automatic overrides, backup‑first, explicit confirmation.
- **Precision** — only add metadata where it’s missing or where there’s a natural ECC fit.
- **Respect for existing work** — every existing `title:`, `role:`, `triggers:` is preserved exactly as‑is.
- **Future‑proofing** — L3 only fills when there’s a real need; ECC mappings are additive reference data, not replacements.

---
---
**CEO Lens Score: 5/10** — the design is sound and the safeguards are strong, but the real value depends on whether the ECC mappings actually help your day‑to‑day Ian orchestration. The conservative default (no changes until you say `yes`) makes it very low risk.

---
---
**Your call:** Do you want me to (a) proceed with creating the `ian-sync` script and run `ian-sync --check` to show you the report, (b) skip the sync entirely and go straight to "elevating every persona with ECC power", or (c) something else? Let me know and I’ll execute accordingly.