# AI Agent Registry

> A standardized, hierarchical persona system for multi-agent AI applications.

[![CI](https://github.com/fentonmartin/ai-agent-registry/actions/workflows/ci.yml/badge.svg)](https://github.com/fentonmartin/ai-agent-registry/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/fentonmartin/ai-agent-registry/blob/main/CONTRIBUTING.md)
[![Personas](https://img.shields.io/badge/personas-32-orange)](#the-hierarchy)
[![Hierarchy](https://img.shields.io/badge/hierarchy-L0--L4--TEAM-purple)](#the-hierarchy)
[![Release](https://img.shields.io/github/v/tag/fentonmartin/ai-agent-registry?label=release)](https://github.com/fentonmartin/ai-agent-registry/releases)

---

## What Is It?

The AI Agent Registry is an open framework for organizing AI assistants into
a structured multi-layer hierarchy (**L0 through L4 + TEAM**). Instead of
ad-hoc prompt collections, personas are:

- **Parented** to L1 domain experts (e.g., `ian-api` belongs to `ian`)
- **Scoped** to narrow domains (e.g., `ran-brand` handles domains/trademarks only)
- **Invoked** via a consistent interface (`/personality <key>`)
- **Validated** structurally by the validator scripts and CI

**Goal:** Make it trivial to create, maintain, and operate a fleet of
specialized AI agents across any runtime — Hermes, AutoGen, CrewAI,
LangGraph, or custom gateways.

---

## The Hierarchy

| Layer | Role | Count |
|-------|------|-------|
| **L0** | Default voices (Zan answers when no persona is named) | 2 |
| **L1** | Domain experts — peers, no children (except Ian/Ran/Lan) | 11 |
| **L2** | Specialist children of Ian (9), Ran (7), Lan (3) | 19 |
| **L3** | Sub-specialists (reserved for future expansion) | 0 |
| **L4** | External tools / APIs invoked as agents | N/A |
| **TEAM** | Cross-functional collaborators outside the hierarchy | Variable |

### How Dispatch Works

| Task Type | Flow |
|-----------|------|
| **Simple** (single domain) | Invoke L1 directly: `/personality pan` |
| **Complex** (multi-domain) | L0 routes to multiple L1s, each may delegate to L2 |
| **Research needed** | L1 delegates to L2 specialists (Pan → Ran-*, Lan → Ran-Brand) |

### Key Rules

- **Only Ian, Ran, Lan** have L2 children. Ban, Ean, Han, Pan, Qan, San, Van,
  Wan are single-focus L1 experts.
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

> The sync script runs on the Python standard library alone. Install PyYAML
> (`pip install -r requirements.txt`) to enable identity tokens, hierarchy
> validation and the validator scripts.

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

### All Personas at a Glance

L0 (Zan) is the entry point — it assigns and routes tasks to the right persona.

```
L0  Zan  (default dispatcher — assign tasks to the right persona) · Jan (explicit only — desktop assistant, analyst tone)
├─── L1  Ian     (engineering umbrella)
│   ├── L2  ian-api        API design · OpenAPI · ERD
│   ├── L2  ian-devops     CI/CD · deployment · infrastructure
│   ├── L2  ian-flutter    Flutter mobile development
│   ├── L2  ian-plan       Project planning · task breakdown
│   ├── L2  ian-alpha      Lead orchestration · delivery board
│   ├── L2  ian-secred     Offensive security · red-teaming
│   ├── L2  ian-secblue    Defensive security · blue-team ops
│   ├── L2  ian-ux         UX research · journeys · testing
│   └── L2  ian-ui         Visual design · Figma · handoff
├─── L1  Ran     (research umbrella)
│   ├── L2  ran-people     Real-person identity verification ONLY
│   ├── L2  ran-brand      Domain · trademark · handle research
│   ├── L2  ran-tech       Technology research · stack analysis
│   ├── L2  ran-business   Business · market research
│   ├── L2  ran-web        Web · SEO research
│   ├── L2  ran-app        Mobile app research
│   └── L2  ran-general    General knowledge research
├─── L1  Ban     (business · finance · revenue)
├─── L1  Ean     (learning · mentoring · knowledge)
├─── L1  Han     (health · wellness · fitness)
├─── L1  Lan     (legal umbrella · compliance + IP)
├─── L1  Pan     (product · strategy · roadmap)
├─── L1  Qan     (quoting · estimation · pricing)
├─── L1  San     (psychology · mental health · wellbeing)
├─── L1  Van     (devil's advocate · critical review)
└─── L1  Wan     (writing · content · communication)

L2 children under Lan: lan-contract · lan-compliance · lan-ip
```

### Use-Case Allocation

| When you need... | Zan assigns to |
|------------------|----------------|
| Engineering code review / architecture | Ian → Ian-API or Ian-DevOps |
| Mobile app (Flutter) development | Ian → Ian-Flutter |
| Project planning / sprint breakdown | Ian → Ian-Plan |
| Multi-specialist delivery / task board | Ian → Ian-Alpha |
| Red-team / penetration testing | Ian → Ian-SecRed |
| Security monitoring / incident response | Ian → Ian-SecBlue |
| User research / journey mapping | Ian → Ian-UX |
| Visual design / design systems | Ian → Ian-UI |
| Verify a person's identity (real person) | Ran → Ran-People |
| Check domain / trademark availability | Ran → Ran-Brand |
| Technology stack research | Ran → Ran-Tech |
| Market / competitor research | Ran → Ran-Business |
| Web / SEO research | Ran → Ran-Web |
| Mobile app market research | Ran → Ran-App |
| General research / background facts | Ran → Ran-General |
| Contract review / negotiation | Lan → Lan-Contract |
| GDPR / SOC 2 / HIPAA compliance | Lan → Lan-Compliance |
| Trademark / IP legal analysis | Lan → Lan-IP |
| Business strategy / financials | Ban |
| Learning / mentoring plan | Ean |
| Health / wellness coaching | Han |
| Product strategy / roadmap | Pan |
| Pricing / quote estimation | Qan |
| Psychological support / counseling | San |
| Challenge assumptions / critique | Van |
| Writing / content / copy | Wan |

---

## Runtime Compatibility

The AI Agent Registry is designed to work across multiple agent runtimes.
Persona files are plain Markdown with YAML frontmatter — no vendor lock-in.

| Runtime | Support | Notes |
|---------|---------|-------|
| **Hermes** | Native | `python sync/sync_personas.py` auto-syncs to `config.yaml`. Hierarchy validation built-in. |
| **AutoGen** | Supported | Scripts in [docs/IMPORT-GUIDE.md](docs/IMPORT-GUIDE.md#autogen) |
| **CrewAI** | Supported | Scripts in [docs/IMPORT-GUIDE.md](docs/IMPORT-GUIDE.md#crewai) |
| **LangGraph** | Supported | Scripts in [docs/IMPORT-GUIDE.md](docs/IMPORT-GUIDE.md#langgraph) |
| **n8n** | Supported | Workflow in [docs/IMPORT-GUIDE.md](docs/IMPORT-GUIDE.md#n8n) |
| **Any runtime** | Raw import | Copy the prompt text from the file body after `---` |

**Hermes native features:**
- `/personality <key>` — invoke any registered persona
- Auto-reloads on config.yaml mtime change (no restart needed)
- Hierarchy dispatch: L0 default → L1 → L2 escalation
- `/personality zan, <query>` — greet + task in one message

---

## Repository Structure

```
ai-agent-registry/
├── personas/
│   ├── l0/      # Default voices (Zan, Jan)
│   ├── l1/      # 11 domain experts
│   └── l2/
│       ├── ian/  # 9 engineering specialists
│       ├── ran/  # 7 research specialists
│       └── lan/  # 3 legal specialists
├── config/
│   └── identities.example.yaml  # Copy → identities.yaml (gitignored)
├── sync/
│   └── sync_personas.py         # Sync into runtime config + hierarchy check
├── scripts/
│   ├── validate_personas.py
│   └── check_duplicates.py
├── docs/
│   ├── HIERARCHY.md
│   ├── IMPORT-GUIDE.md
│   └── NAMING.md
├── tests/                       # Unit tests (python -m unittest discover -s tests)
├── examples/                    # Template persona files
├── .github/                     # CI workflow, issue & PR templates
├── requirements.txt             # PyYAML
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
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

## Versioning

We use **year-based versioning**: `v{year}.{major}.{minor}`

- **v2026.0.1** — Initial public release (current)
- **v2026.1.0** — Would be the next major update in 2026
- Patch releases increment the minor: `v2026.0.2`, `v2026.0.3`, ...

Major version (the middle number) resets to 0 each year. A new year starts
at `.0.1`.

See [Releases](https://github.com/fentonmartin/ai-agent-registry/releases).

---

## License

**MIT** — use freely in commercial and non-commercial projects.

The AI Agent Registry uses prompt-based files (Markdown + YAML frontmatter),
not compiled code. MIT was chosen because:

- **Prompts are meant to be adapted** — MIT lets anyone modify personas for
  their own use case without copyleft obligations
- **Zero friction for adoption** — no legal review needed to integrate into
  commercial products or internal agent systems
- **Encourages contribution** — companies won't hesitate to submit improvements
  knowing they retain full rights to their changes

**You can:**
- Use these personas in any project (commercial or personal)
- Modify prompts to fit your team's needs
- Re-license derivative works under any license
- Submit PRs adding new personas or improving existing ones

**You cannot:**
- Hold the original authors liable (as-is, no warranty)
- Remove the license notice from distributions

See [LICENSE](LICENSE).
