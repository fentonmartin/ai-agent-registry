# AI Agent Registry

A standardized, hierarchical persona system for multi-agent AI applications.

## What Is It?

The AI Agent Registry is a framework for organizing AI assistants into a
structured, multi-layer hierarchy (L0–L4 + TEAM). Instead of ad-hoc prompt
collections, personas are grouped by domain, parented to L1 experts, and
dispatched through a clear escalation protocol.

**Goal:** Make it easy to create, maintain, and operate a fleet of
specialized AI assistants — each scoped to a domain, each with well-defined
parent-child relationships, and each invokable via a consistent interface.

---

## The L0–L4 + TEAM Hierarchy

```
L0  — Default Voice(s)
    ├── Zan     — Executive Assistant (default)
    └── Jan     — Default Analyst Tone

L1  — Domain Experts (10 peers)
    ├── Ian     — Intelligent Assistant (engineering umbrella)
    ├── Ban     — Business Assistant
    ├── Ean     — Learning Coach
    ├── Han     — Health Coach
    ├── Lan     — Legal Advisor (legal/compliance umbrella)
    ├── Pan     — Product Expert
    ├── Qan     — Quote Expert
    ├── Ran     — Research Assistant (research umbrella)
    ├── San     — Calm Psychologist
    └── Van     — Devil Advocate

L2  — Specialists (children of L1)
    ├── Ian ── Ian-API, Ian-DevOps, Ian-Flutter, Ian-Plan,
    │         Ian-Alpha, Ian-SecRed, Ian-SecBlue, Ian-UX, Ian-UI
    ├── Ran ── Ran-People, Ran-Brand, Ran-Tech, Ran-Business,
    │         Ran-Web, Ran-App, Ran-General
    └── Lan ── Lan-Contract, Lan-Compliance, Lan-IP

L3  — Sub-specialists
L4  — External tools / APIs

TEAM — Cross-functional collaborators (external to all levels)
```

### How It Works

| Layer | Role | Example |
|-------|------|---------|
| **L0** | Default voice invoked without a name greeting | `Zan` answers when no persona is specified |
| **L1** | Domain experts — single-focus, no children (unless specified) | `Lan` handles all legal; `Pan` handles all product |
| **L2** | Specialist children of L1 — narrow expertise | `Ran-People` (people research), `Ran-Brand` (domains/trademarks) |
| **L3** | Sub-specialists under L2 | Reserved for future expansion |
| **L4** | External tools / APIs invoked as agents | Shell, web search, file system |
| **TEAM** | External collaborators outside the agent hierarchy | Human experts, external services |

### Escalation Protocol

1. **Simple task** (single-domain, linear) — invoke L1 directly
2. **Complex task** (multi-domain) — use L0 → L1 → L2 escalation chain
3. **Research needed by a strategist** — L1 delegate calls its L2 research children
   - Example: *Pan needs market data → Pan asks Ran-Business to research*

### Key Rules

- **Naming convention:** Internal keys are lowercase (`ian-api`, `ran-people`).
  Display names use ALL-CAPS acronyms (`Ian-API`, `Ian-DevOps`, `Ian-SecRed`).
- **L2 parents:** Only Ian, Ran, and Lan own L2 children. Other L1s
  (Ban, Ean, Han, Pan, Qan, San, Van) are single-focus domain experts.
- **Ran-People scope:** Strictly for real-person identity verification.
  Use `Ran-Brand` for domain/trademark research instead.
- **Pan workflow:** Pan (L1) handles product strategy and delegates
  research to Ran-* children — Pan does not collect research itself.

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/your-org/ai-agent-registry.git
cd ai-agent-registry
```

No dependencies — the sync script uses only the Python standard library.
PyYAML is optional (used for hierarchy validation only).

### 2. Configure Identities

Copy the example config and fill in your values:

```bash
cp config/identities.example.yaml config/identities.yaml
# Edit config/identities.yaml with your details
```

Persona files use tokens like `<USER>`, `<COMPANY>`, `<EMAIL>`, `<MODEL>`.
These are resolved at sync time from `config/identities.yaml`.

### 3. Sync to Your Runtime

```bash
# Set your runtime config path
export HERMES_HOME=~/.hermes

# Run the sync
python sync/sync_personas.py
```

This writes personas into your `config.yaml` under `agent.personalities:`
and validates the L0-L4 hierarchy.

### 4. Invoke a Persona

In Hermes (or compatible runtime):

```
/personality zan      # L0 default: Executive Assistant
/personality pan      # L1: Product Expert
/personality ran-brand # L2: Brand & domain research
/personality ian-api   # L2: API design specialist
```

---

## Repository Structure

```
ai-agent-registry/
├── personas/
│   ├── l0/            # Default voices (Zan, Jan)
│   ├── l1/            # Domain experts (Ian, Ban, Ean, Han, Lan, Pan, Qan, Ran, San, Van)
│   └── l2/
│       ├── ian/       # Ian's specialists (API, DevOps, Flutter, Plan, Alpha, SecRed, SecBlue, UX, UI)
│       ├── ran/       # Ran's research specialists (People, Brand, Tech, Business, Web, App, General)
│       └── lan/       # Lan's legal specialists (Contract, Compliance, IP)
├── config/
│   ├── identities.example.yaml   # Template — copy to identities.yaml
│   └── identities.yaml           # Your values (gitignored)
├── sync/
│   └── sync_personas.py          # Stdlib-only sync script
├── docs/
│   ├── HIERARCHY.md              # Full L0-L4 + TEAM framework
│   ├── IMPORT-GUIDE.md           # Importing into Hermes, CrewAI, AutoGen, etc.
│   └── NAMING.md                 # Naming conventions & style guide
├── examples/                     # Example persona files
├── LICENSE                      # MIT
└── README.md                    # You are here
```

---

## Persona File Format

Each persona is a Markdown file with optional YAML frontmatter:

```markdown
---
name: ran-people
title: Ran-People — People Research
role: Verifies real-person identities, digital footprint analysis, handle disambiguation
parent: Ran
triggers:
  - /personality ran-people
  - @ran-people
help: /rhelp ran-people
---

You are Ran-People, a research assistant specialized in verifying real-person
identities...

Key responsibilities:
1. Identity verification
2. Digital footprint analysis
...
```

**Frontmatter fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Internal key (lowercase, kebab-case) |
| `title` | No | Display name (ALL-CAPS acronyms) |
| `role` | No | Short description |
| `parent` | No | L1 parent key (for L2 personas) |
| `triggers` | No | Activation keywords |
| `help` | No | Help invocation |

The body (after `---`) is the system prompt.

---

## Customization

### Adding a New Persona

1. Create `personas/l2/ian/ian-security.md` (or appropriate L2 folder)
2. Add YAML frontmatter with `name:`, `title:`, `role:`, `parent:`
3. Write the system prompt in the body
4. Run `python sync/sync_personas.py`

### Naming Conventions

- **Internal keys:** lowercase, kebab-case (`ian-api`, `ran-people`)
- **Display names:** ALL-CAPS for acronyms and research domains
  (`Ian-API`, `Ian-DevOps`, `Ian-SecRed`, `Ran-People`)
- **File names:** match internal keys (`ian-api.md`)

See [docs/NAMING.md](docs/NAMING.md) for the full style guide.

---

## License

MIT — use freely in commercial and non-commercial projects.

See [LICENSE](LICENSE).
