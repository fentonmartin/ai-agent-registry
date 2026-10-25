# The L0-L4 + TEAM Hierarchy Framework

## Overview

The AI Agent Registry organizes AI assistants into a five-layer hierarchy
(L0 through L4) plus a cross-functional TEAM layer. This document defines
the framework, the escalation protocol, and the rules for placing personas.

## Layer Definitions

### L0 — Default Voices

The layer invoked when no persona is explicitly named. Only one L0 persona
is active at a time (the default). `Zan` is the standard default.

| Key | Display Name | Role |
|-----|-------------|------|
| `zan` | Zan | Executive Assistant, default voice |
| `jan` | Jan | Default analyst tone (pull-only) |

**Rules:**
- L0 is listed in `agent.hierarchy.L0.members`; the active default is set
  by the top-level `display.personality` key.
- Only one L0 persona should be set as the active default.
- Jan activates only on explicit "Jan" mention.

### L1 — Domain Experts

Eleven peer domain experts. Each L1 owns an entire domain of responsibility.
Most L1s do NOT have L2 children — they handle their domain end-to-end.

| Key | Display Name | Domain | Has L2 Children? |
|-----|-------------|--------|------------------|
| `ian` | Ian | Intelligent Assistant (engineering) | Yes |
| `ban` | Ban | Business | No |
| `ean` | Ean | Learning/Education | No |
| `han` | Han | Health & Wellness | No |
| `lan` | Lan | Legal & Compliance | Yes |
| `pan` | Pan | Product | No |
| `qan` | Qan | Quoting & Estimation | No |
| `ran` | Ran | Research | Yes |
| `san` | San | Psychology & Mental Health | No |
|| `van` | Van | Devil's Advocate / Critical Review | No |
|| `wan` | Wan | Writing / Content / Communication | No |

**Rules:**
- L1 personas are peers — no parent-child relationships between them.
- Pan (Product) handles strategy and delegates research to Ran-* children.
- Lan (Legal) handles high-level legal and escalates to Lan-* specialists.
- Ian (Engineering) handles general engineering and delegates to Ian-* specialists.
- Only Ian, Ran, and Lan have L2 children. All other L1s are single-focus.

### L2 — Specialists (Children of L1)

Narrow-expertise personas parented to their respective L1.

#### Ian L2 (9 specialists) — Engineering

| Key | Display Name | Specialization |
|-----|-------------|----------------|
| `ian-api` | Ian-API | API design, REST, GraphQL |
| `ian-devops` | Ian-DevOps | CI/CD, deployment, infrastructure |
| `ian-flutter` | Ian-Flutter | Flutter mobile development |
| `ian-plan` | Ian-Plan | Project planning, task breakdown |
| `ian-alpha` | Ian-Alpha | Alpha testing, exploratory QA |
| `ian-secred` | Ian-SecRed | Offensive security, red-teaming |
| `ian-secblue` | Ian-SecBlue | Defensive security, blue-team operations |
| `ian-ux` | Ian-UX | UX research, user journeys, testing |
| `ian-ui` | Ian-UI | Visual design, Figma, design handoff |

#### Ran L2 (7 specialists) — Research

| Key | Display Name | Specialization |
|-----|-------------|----------------|
| `ran-people` | Ran-People | Real-person identity verification, digital footprint |
| `ran-brand` | Ran-Brand | Domain, trademark, handle availability research |
| `ran-tech` | Ran-Tech | Technology research, stack analysis |
| `ran-business` | Ran-Business | Business/market research, competitor analysis |
| `ran-web` | Ran-Web | Web/SEO research |
| `ran-app` | Ran-App | Mobile app research |
| `ran-general` | Ran-General | General knowledge research |

**Rules:**
- **Ran-People** is strictly for real-person identity verification — never
  use it for technical/product research.
- **Ran-Brand** handles domains, trademarks, and platform handle checks.
  It collaborates with Lan-IP for trademark conflict analysis.
- Pan delegates research to Ran-* children when facts are needed.
- Lan-IP collaborates with Ran-Brand for trademark research findings.

#### Lan L2 (3 specialists) — Legal

| Key | Display Name | Specialization |
|-----|-------------|----------------|
| `lan-contract` | Lan-Contract | Contract law, negotiation, CLM |
| `lan-compliance` | Lan-Compliance | GDPR, SOC 2, HIPAA, ISO 27001, PCI-DSS |
| `lan-ip` | Lan-IP | Intellectual property (trademarks, copyright, patents) |

### L3 — Sub-specialists

Reserved for future expansion (e.g., Ian-Flutter splitting into
Ian-Flutter-Android / Ian-Flutter-iOS).

### L4 — External Tools / APIs

External tools and APIs invoked as agent actions. Not personas — these are
executable capabilities (shell, web search, file system, databases).

### TEAM — Cross-functional Collaborators

External human or system collaborators outside the agent hierarchy.
These are not AI personas but integration points (e.g., GitHub, Linear,
Slack bots, human expert channels).

## Escalation Protocol

### Simple Tasks (Single-Domain)

- **Scope:** Single L1 domain, <500 words, linear task
- **Action:** Invoke L1 directly via `/personality <key>`
- **Example:** `/personality ban` — "What's our Q4 revenue forecast?"

### Complex Tasks (Multi-Domain)

- **Scope:** Multiple domains, needs coordination
- **Action:** L0 → L1 → L2 hierarchy escalation
- **Example:** Product launch needs legal + tech + research:
  1. Zan (L0) routes to Pan (L1 Product)
  2. Pan escalates to Ran-Tech (L2) for stack analysis
  3. Pan escalates to Ran-Business (L2) for market research
  4. Pan escalates to Lan-Compliance (L2) for regulatory check

### Research Delegation Pattern

- **When an L1 needs research:** The L1 invokes its L2 research children
- **Pan (L1 Product)** does STRATEGY — asks Ran-* children for FACTS
- **Lan (L1 Legal)** does JUDGMENT — asks Ran-Brand for FACTS, applies law
- **Ian (L1 Engineering)** does ORCHESTRATION — asks Ian-* children for execution

### Verification Gate (L0 → L1+ Escalation)

Before escalating:
1. State target domain + confidence level
2. If confidence < 80%: clarify first
3. If confidence >= 80%: escalate directly via name-greeting

### Direct Handoff (Swarm Bypass)

- Domain is clear + ambiguity is low → bypass L0 translation
- Directly invoke the L1 specialist

## Hierarchy Config Format

In `config.yaml`:

```yaml
display:
  personality: zan          # default L0 voice (top-level key)

agent:
  hierarchy:
    L0:
      members: [zan, jan]
    L1:
      members: [ian, ban, ean, han, lan, pan, qan, ran, san, van, wan]
    L2:
      children:
        ian: [ian-api, ian-devops, ian-flutter, ian-plan, ian-alpha,
              ian-secred, ian-secblue, ian-ux, ian-ui]
        ran: [ran-people, ran-brand, ran-tech, ran-business,
              ran-web, ran-app, ran-general]
        lan: [lan-contract, lan-compliance, lan-ip]
    L3:
      members: []
    L4:
      members: []
    TEAM:
      members: []
  # >>> PERSONALITY SYNC (auto-managed) >>>
  personalities:
    # (written by sync_personas.py — do not edit by hand)
  # <<< PERSONALITY SYNC <<<
```

`sync_personas.py` validates this block after every sync. All six layers
(`L0`–`L4`, `TEAM`) must be present, every key listed under `members` or
`children` must be a synced persona, and every synced persona must appear
somewhere in the hierarchy.

## Counting the Personas

Current total: **32 personas**
- L0: 2 (Zan, Jan)
- L1: 11 (Ian, Ban, Ean, Han, Lan, Pan, Qan, Ran, San, Van, Wan)
- L2: 19 (9 under Ian, 7 under Ran, 3 under Lan)
- L3: 0 (reserved)
- L4: External tools (not personified)
- TEAM: Variable (external collaborators)
