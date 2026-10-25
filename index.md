---
layout: default
title: AI Agent Registry
---

# AI Agent Registry

A standardized, hierarchical persona system for multi-agent AI applications.

**32 personas** organized across **L0–L4 + TEAM** layers with a sync script
for Hermes and import guides for 5+ runtimes.

---

## Quick Links

| Layer | Scope | What |
|-------|-------|------|
| L0 Leadership | Strategic exec | Zan (default), Jan (on-demand) |
| L1 Domains | 10 peer experts | Ian, Ban, Ean, Pan, Qan, Ran, San, Van, Han, Lan |
| L2 Specialists | 21 children | Under Ian, Ran, Lan only |
| Import Guide | Runtime setup | Hermes, AutoGen, CrewAI, LangGraph, n8n |
| Naming Guide | Style conventions | Capitalization, casing, token system |

---

## Hierarchical Tree

```
L0: Zan (default)  ·  Jan (explicit only)
     |
     +-- L1: Ian (Engineering)
     |   +-- L2: Ian-API
     |   +-- L2: Ian-DevOps
     |   +-- L2: Ian-Flutter
     |   +-- L2: Ian-Alpha
     |   +-- L2: Ian-Plan
     |   +-- L2: Ian-SecRed
     |   +-- L2: Ian-SecBlue
     |   +-- L2: Ian-UI
     |   +-- L2: Ian-UX
     |
     +-- L1: Ban (Biz)
     +-- L1: Ean (Learning/UX)
     +-- L1: Pan (Product)
     +-- L1: Qan (Specs/ERD)
     |
     +-- L1: Ran (Research)
     |   +-- L2: Ran-People
     |   +-- L2: Ran-Brand
     |   +-- L2: Ran-Tech
     |   +-- L2: Ran-Business
     |   +-- L2: Ran-Web
     |   +-- L2: Ran-App
     |   +-- L2: Ran-General
     |
     +-- L1: San (Wellness)
     +-- L1: Van (Audit/dev)
     +-- L1: Han (Calm psych)
     |
     +-- L1: Lan (Legal/QA)
         +-- L2: Lan-Contract
         +-- L2: Lan-Compliance
         +-- L2: Lan-IP

TEAM: Cross-functional collaborators (external)
```

---

## How It Works

1. **L0 (Zan)** handles all escalation routing. Default persona for general queries.
2. **L1** are 10 peer-domain experts. Mention by name to hand off.
3. **L2** are specialist children under Ian, Ran, and Lan only.
4. **L3/L4** are sub-specialists and external tools/APIs.
5. **TEAM** covers external collaborators outside the hierarchy.

See the [full framework](docs/HIERARCHY.md) and [import guide](docs/IMPORT-GUIDE.md) for details.

---

## Get Started

```bash
# Clone
git clone https://github.com/fentonmartin/ai-agent-registry.git
cd ai-agent-registry

# Run sync (checks all 32 personas)
python3 sync/sync_personas.py --check

# Copy identity config (tokens resolved at sync time)
cp config/identities.example.yaml config/identities.yaml
# Edit identities.yaml with your values

# Validate
python3 scripts/validate_personas.py
python3 scripts/check_duplicates.py
```

---

[View on GitHub](https://github.com/fentonmartin/ai-agent-registry) |
[Read the Framework](docs/HIERARCHY.md)

---

## License

MIT — see [LICENSE](LICENSE). Prompts are meant to be adapted; zero friction for adoption.
