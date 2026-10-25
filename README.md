# AI Agent Registry

> A standardized, hierarchical persona system for multi-agent AI applications.

[![CI](https://github.com/fentonmartin/ai-agent-registry/actions/workflows/ci.yml/badge.svg)](https://github.com/fentonmartin/ai-agent-registry/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/fentonmartin/ai-agent-registry/blob/main/CONTRIBUTING.md)
[![Personas](https://img.shields.io/badge/personas-32-orange)](#the-hierarchy)
[![L0-L4](https://img.shields.io/badge/hierarchy-L0--L4--TEAM-purple)](#the-hierarchy)

---

## What Is It?

The AI Agent Registry is an open framework for organizing AI assistants into
a structured multi-layer hierarchy (**L0 through L4 + TEAM**). Instead of
ad-hoc prompt collections, personas are:

- **Parented** to L1 domain experts (e.g., `ian-api` belongs to `ian`)
- **Scoped** to narrow domains (e.g., `ran-brand` handles domains/trademarks only)
- **Invoked** via a consistent interface (`/personality <key>`)
- **Validated** structurally by the sync script

**Goal:** Make it trivial to create, maintain, and operate a fleet of
specialized AI agents across any runtime — Hermes, AutoGen, CrewAI,
LangGraph, or custom gateways.

---

## The Hierarchy

| Layer | Role | Count |
|-------|------|-------|
| **L0** | Default voices (Zan answers when no persona is named) | 2 |
| **L1** | Domain experts — peers, no children (except Ian/Ran/Lan) | 10 |
| **L2** | Specialist children of Ian (9), Ran (8), Lan (3) | 20 |
| **L3** | Sub-specialists (reserved for future expansion) | 0 |
| **L4** | External tools / APIs invoked as agents | N/A |
| **TEAM** | Cross-functional collaborators outside the hierarchy | Variable |

### How Dispatch Works

| Task Type | Flow |
|-----------|------|
| **Simple** (single domain) | Invoke L1 directly: `/personality pan` |
| **Complex** (multi-domain) | L0 routes to multiple L1s, each may delegate to L2 |
| **Research needed** | L1 delegates to its L2 children (Pan → Ran-*, Lan → Ran-Brand) |

### Key Rules

- **Only Ian, Ran, Lan** have L2 children. Ban, Ean, Han, Pan, Qan, San, Van
  are single-focus L1 experts.
- **Ran-People** is strictly for real-person identity verification.
  Use **Ran-Brand** for domains/trademarks instead.
- **Pan** handles product strategy and delegates research to Ran-* children.
- Internal keys are lowercase (`ian-api`). Display names use ALL-CAPS
  acronyms (`Ian-API`, `Ian-DevOps`, `Ian-SecRed`).

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/fentonmartin/ai-agent-registry.git
cd ai-agent-registry
```

### 2. Configure Identities

```bash
cp config/identities.example.yaml config/identities.yaml
# Edit config/identities.yaml with your values
```

Persona files contain tokens like `<USER>`, `<COMPANY>`, `<EMAIL>`, `<MODEL>`.
These resolve to your real values during sync.

### 3. Sync to Your Runtime

```bash
export HERMES_HOME=~/.hermes
python sync/sync_personas.py
```

> **No dependencies.** The sync script uses only the Python standard library.
> PyYAML is optional (hierarchy validation only).

### 4. Invoke a Persona

```
/personality zan        # L0: Executive Assistant (default)
/personality pan        # L1: Product Expert
/personality ran-brand  # L2: Brand & domain research
/personality ian-api    # L2: API design specialist
/personality lan-ip     # L2: Intellectual property legal advice
```

---

## Persona File Format

Each persona is a Markdown file with YAML frontmatter:

```markdown
---
name: ran-brand
title: Ran-Brand — Brand & Domain Research
role: Ran L2 sub-context for domain, trademark, and handle availability
parent: ran
triggers:
  - /personality ran-brand
  - domain check
---

You are Ran-Brand, a research assistant specializing in brand identity...
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Internal key (lowercase, kebab-case) |
| `title` | No | Display name (ALL-CAPS acronyms preferred) |
| `role` | No | Short description |
| `parent` | No | L1 parent key (for L2 personas) |
| `triggers` | No | Activation keywords |

---

## Import Into Your Runtime

| Runtime | Support |
|---------|---------|
| **Hermes** | Native — `python sync/sync_personas.py` |
| **AutoGen** | [Import guide](docs/IMPORT-GUIDE.md#autogen) |
| **CrewAI** | [Import guide](docs/IMPORT-GUIDE.md#crewai) |
| **LangGraph** | [Import guide](docs/IMPORT-GUIDE.md#langgraph) |
| **Any runtime** | Copy the prompt text from the file body |

Full code examples: [docs/IMPORT-GUIDE.md](docs/IMPORT-GUIDE.md)

---

## Repository Structure

```
ai-agent-registry/
├── personas/
│   ├── l0/      # Default voices (Zan, Jan)
│   ├── l1/      # 10 domain experts
│   └── l2/
│       ├── ian/  # 9 engineering specialists
│       ├── ran/  # 8 research specialists
│       └── lan/  # 3 legal specialists
├── config/
│   └── identities.example.yaml  # Copy → identities.yaml (gitignored)
├── sync/
│   └── sync_personas.py         # Stdlib-only sync + validator
├── scripts/
│   ├── validate_personas.py
│   └── check_duplicates.py
├── docs/
│   ├── HIERARCHY.md
│   ├── IMPORT-GUIDE.md
│   └── NAMING.md
├── examples/                    # Template persona files
├── .github/workflows/ci.yml     # Validation CI
├── LICENSE                      # MIT
└── README.md
```

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
full guide on adding personas, improving prompts, and extending the framework.

**Quick ways to contribute:**
1. Add a persona — create a new `.md` file in the right `personas/` folder
2. Improve an existing prompt — open a PR
3. Add an import guide — help more runtimes adopt this
4. Report bugs — open an issue

---

## License

MIT — use freely in commercial and non-commercial projects.

See [LICENSE](LICENSE).
