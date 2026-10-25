# Changelog

All notable changes to this project are documented here. Versions follow
the year-based scheme described in the [README](README.md#versioning).

## [Unreleased]

### Added
- GitHub Pages site (`index.md`, Cayman theme with dark overrides).
- n8n section in the import guide.
- `requirements.txt`, unit tests (`tests/`), and a Python 3.9–3.13 CI matrix.
- Stricter validation: required fields, file and folder layout, L2 parent
  rules, key prefixes, and persona counts quoted in the docs.
- `.gitattributes`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  and issue/PR templates.

### Fixed
- The sync no longer writes a second top-level `agent:` key into
  `config.yaml`, which made YAML drop either the hierarchy or the
  personalities. Legacy blocks are migrated automatically.
- The documented hierarchy format now matches what the validator reads.
- Identity token names in the example config and docs (`<REPO_PATH>`,
  `<DASHBOARD_PORT>`).
- `check_duplicates.py` crashing on Windows with non-ASCII persona files.
- The CI sync check could never fail.
- Contradictory counts, labels and broken tables across README, index and
  docs.

## [v2026.0.1] - 2026-10-25

Initial public release: 32 personas (L0: 2, L1: 11, L2: 19), the
`sync_personas.py` sync script for Hermes, validators, and import guides
for AutoGen, CrewAI and LangGraph.

[Unreleased]: https://github.com/fentonmartin/ai-agent-registry/compare/v2026.0.1...HEAD
[v2026.0.1]: https://github.com/fentonmartin/ai-agent-registry/releases/tag/v2026.0.1
