# AI Agent Registry

> A standardized, hierarchical persona system for multi-agent AI applications.

[![CI](https://github.com/fentonmartin/ai-agent-registry/actions/workflows/ci.yml/badge.svg)](https://github.com/fentonmartin/ai-agent-registry/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/fentonmartin/ai-agent-registry/blob/main/CONTRIBUTING.md)
[![Persona Count](https://img.shields.io/badge/personas-32-orange)](#the-l0-l4--team-hierarchy)
[![Hierarchy](https://img.shields.io/badge/hierarchy-L0--L4--TEAM-purple)](#)
[![Sync Status](https://img.shields.io/badge/sync-passing-brightgreen)](#)

---

```
                          ╔══════════════════╗
                          ║   L0 — Default    ║
                          ║     Voices        ║
                          ║   Zan  ·  Jan     ║
                          ╚═══╤═══════════════╝
                              │
                    ┌─────────┼─────────┐
                    │         │         │
              ╔═════╪═════╗ ╔═══╪═════╗ ╔═══╪══════════════╗
              ║  L1: Ian  ║ ║  L1: Ran ║ ║  L1: Lan       ║
              ║ Engineering ║ ║  Research ║ ║  Legal         ║
              ╚═════╤═════╝ ╚═══╤═════╝ ╚═══╤══════════════╝
                    │         │         │
       ┌────┬────┬──┼──┬────┬─┘         │
       │ API│DevO│Fl│Pl│Alp│UI│UX│SecRd│ScB│         │
       │API │DevOps│ut│an│pha│  │  │Red │ecB│         │
       └────┴────┴──┴──┴────┴─┴─────────┘         │
                                                  │
    ┌───┬────┬───┬────┬───┬───┐                   │
    │Ppl│Brand│Tec│Busi│Web│App│Gen│                  │
    └───┴────┴───┴────┴───┴───┘                   │
         (Ran Children)                            │
                                                  │
    ┌───────┬────────┬──┐                          │
    │Ctrct │Complnc │IP│                          │
    └───────┴────────┴──┘                          │
         (Lan Children) ←──────────────────────────┘

         L3: Sub-specialists  |  L4: External Tools/APIs
         TEAM: Cross-functional collaborators
```

---

## What Is It?

The AI Agent Registry is an **open, standardized framework** for building
fleets of specialized AI assistants organized into a **multi-layer hierarchy**
(L0–L4 + TEAM).

Instead of ad-hoc prompt collections, personas are:
- **Parented** to L1 domain experts (e.g., `Ian-API` belongs to `Ian`)
- **Scoped** to narrow domains (e.g., `Ran-People` only verifies real human identity)
- **Invoked** via a consistent interface (`/personality <key>`)
- **Validated** structurally by the sync script

**Goal:** Make it trivial to create, maintain, and operate a fleet of
specialized AI agents — for Hermes, AutoGen, CrewAI, LangGraph, or any runtime.

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
```

Edit `config/identities.yaml` with your details. Persona prompts use
tokens like `<USER>`, `<COMPANY>`, `<EMAIL>`, `<MODEL>` that get resolved
at sync time.

### 3. Sync to Your Runtime

```bash
export HERMES_HOME=~/.hermes
python sync/sync_personas.py
```

> **No dependencies.** Uses only Python's standard library. PyYAML is
> optional (hierarchy validation only).

### 4. Invoke a Persona

```
/personality zan        # L0: Executive Assistant (default)
/personality pan        # L1: Product Expert
/personality ran-brand  # L2: Brand & domain research
/personality ian-api    # L2: API design specialist
/personality lan-ip     # L2: Intellectual property legal advice
```

---

## The L0–L4 + TEAM Hierarchy

| Layer | Role | Count | Example |
|-------|------|-------|---------|
| **L0** | Default voices (no name = Zan) | 2 | `zan`, `jan` |
| **L1** | Domain experts (10 peers) | 10 | `ian`, `ban`, `ran`, `pan` |
| **L2** | Specialist children of Ian/Ran/Lan | 20 | `ian-api`, `ran-people`, `lan-ip` |
| **L3** | Sub-specialists (reserved) | 0 | Future expansion |
| **L4** | External tools / APIs | N/A | Shell, web search |
| **TEAM** | Cross-functional collaborators | Variable | Human experts |

### All 32 Personas at a Glance

```
L0  │ Zan (default) · Jan (analyst)
    │
L1  │ Ian (eng) · Ban (biz) · Ean (learn) · Han (health)
    │ Lan (legal) · Pan (product) · Qan (quotes) · Ran (research)
    │ San (psych) · Van (devil's advocate)
    │
L2  │ ┌── Ian ──┐ ┌── Ran ──┐ ┌── Lan ──┐
    │ │ API     │ │ People  │ │ Contract│
    │ │ DevOps  │ │ Brand   │ │ Complnc │
    │ │ Flutter │ │ Tech    │ │ IP      │
    │ │ Plan    │ │ Business│ │         │
    │ │ Alpha   │ │ Web     │ │         │
    │ │ SecRed  │ │ App     │ │         │
    │ │ SecBlue │ │ General │ │         │
    │ │ UX      │ │         │ │         │
    │ │ UI      │ │         │ │         │
    │ └─────────┘ └─────────┘ └─────────┘
```

### Key Rules

- **Only Ian, Ran, Lan** have L2 children. All other L1s are single-focus experts.
- **Ran-People** is strictly for real-person identity verification.
  Use **Ran-Brand** for domains/trademarks instead.
- **Pan** handles product strategy and delegates research to Ran-* children.
- Internal keys are lowercase (`ian-api`). Display names use ALL-CAPS acronyms (`Ian-API`, `Ian-DevOps`, `Ian-SecRed`).

### Escalation Protocol

```
Simple task  → invoke L1 directly via /personality
Complex task → L0 → L1 → L2 → (resolve)
Need facts   → L1 delegates to its L2 research children
```

**Example:** Pan needs pricing data

```
Pan (L1 Product) → "Ran-Business, research competitor X pricing"
                 → Ran-Business (L2) returns findings
                 → Pan synthesizes and decides
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
triggers: ["/personality ran-brand", "domain check", "trademark"]
---

You are Ran-Brand, a research assistant specializing in brand identity...
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Internal key (lowercase, kebab-case) |
| `title` | No | Display name (ALL-CAPS preferred) |
| `role` | No | Short description |
| `parent` | No | L1 parent key (for L2 personas) |
| `triggers` | No | Activation keywords |
| `help` | No | Help invocation |

---

## Import Into Your Runtime

| Runtime | Support |
|---------|---------|
| **Hermes** | Native — `python sync/sync_personas.py` |
| **AutoGen** | [Import guide](docs/IMPORT-GUIDE.md#autogen) |
| **CrewAI** | [Import guide](docs/IMPORT-GUIDE.md#crewai) |
| **LangGraph** | [Import guide](docs/IMPORT-GUIDE.md#langgraph) |
| **Raw/Gateway** | Copy prompt text from any `.md` file body |

See [docs/IMPORT-GUIDE.md](docs/IMPORT-GUIDE.md) for code examples.

---

## Repository Structure

```
ai-agent-registry/
├── personas/
│   ├── l0/                   # Default voices (Zan, Jan)
│   ├── l1/                   # 10 domain experts
│   └── l2/
│       ├── ian/              # 9 engineering specialists
│       ├── ran/              # 8 research specialists
│       └── lan/              # 3 legal specialists
├── config/
│   └── identities.example.yaml  # Copy → identities.yaml (gitignored)
├── sync/
│   └── sync_personas.py         # Stdlib-only sync + hierarchy validator
├── docs/
│   ├── HIERARCHY.md             # Full framework documentation
│   ├── IMPORT-GUIDE.md          # Porting to other runtimes
│   └── NAMING.md                # Naming conventions
├── examples/                    # Template persona files
├── .github/workflows/
│   └── ci.yml                    # Persona validation CI
├── LICENSE                       # MIT
└── README.md
```

---

## Contributing

**Contributions welcome!** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick ways to contribute:
1. **Add a persona** — create a new `.md` file in the right `personas/` folder
2. **Improve a prompt** — PR with refinements
3. **Add an import guide** — help more runtimes adopt this
4. **Report bugs** — open an issue

All persona files must:
- Have valid YAML frontmatter with `name:` and `parent:`
- Pass the sync validation script
- Use ALL-CAPS acronyms in titles (`Ian-API`, not `Ian-Api`)
- Keep internal keys lowercase (`ian-api`, not `Ian-API`)

---

## License

MIT — use freely in commercial and non-commercial projects.

See [LICENSE](LICENSE).
