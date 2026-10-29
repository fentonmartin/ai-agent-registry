---
name: ian-sync Design
date: 2026-10-29
version: v2026.0.2
status: Current (replaces the first draft, which used guessed ECC names)
---

# ian-sync

`ian_sync.py` keeps persona knowledge in step with external tools. ECC is the first registered tool. The mapping itself lives in `docs/ECC-MAPPING.md` and `sync/ecc-mapping.json`; this file describes how the script behaves.

## Rules

1. Advisory first. Every command that writes is a dry run unless `--yes` is passed.
2. Nothing is overridden silently. Persona `title`, `role`, `triggers` and body stay authoritative.
3. Pinned. Imports come from a release tag, never from `main`.
4. Local edits win. An imported skill whose files changed locally is skipped, not overwritten.
5. No auto-commit. The script never commits; a human reviews `git diff` and commits.
6. L3 is opt-in (`--allow-l3`). It is created only for a concrete need.

## Commands

| Command | Effect |
|---|---|
| `--check` | Read-only report: Ian L2 state, live check of every mapped ECC item at the latest release, import drift, locally modified skills |
| `--audit` | Offline consistency check of mapping, imports and standards. No network. Runs in CI |
| `--import-skills [--yes]` | Copy mapped skills verbatim from the release tag into `skills/ecc/` in the Hermes home, with a lockfile and declared patches |
| `--apply-personas [--local-source DIR] [--user NAME] [--yes]` | Set `ecc-mapping` and `ecc-fit` (registry) and upsert the standards block between `ian-sync:standards` markers. Refuses to write unresolved identity tokens |
| `--write [--allow-l3] [--yes]` | Legacy Ian L2 metadata writer (version field). Creates a backup first |
| `--status` | Short summary |

## Safety properties (each tested)

- Re-running with no upstream change is a no-op.
- A locally edited import is reported as SKIPPED.
- A patch whose target text is missing aborts that skill.
- `--audit` fails on: persona missing from mapping, gap persona with items, skill with no import or not_imported decision, imported skill in no mapping, standards naming a skill that is not imported.
- Backups are written to `ian-sync-backup/` in the Hermes home before any write.

## Order of change

1. Decide in `docs/ECC-MAPPING.md`.
2. Update `sync/ecc-mapping.json` and `sync/standards/<key>.md`.
3. `--audit`, then `--import-skills`, then `--apply-personas` (dry run first).
4. Review the diff and commit.

## Adding another tool

Add a mapping file for the tool, a pinned release source, and its own import and standards entries. Reuse the same rules above. A new tool never edits another tool's entries.
