# Naming Conventions

This document defines the naming conventions for the AI Agent Registry.

## Internal Keys (Slug Format)

Used in `config.yaml`, file names, and invocation commands.

- Lowercase only
- Hyphen-separated (kebab-case)
- Derived via the `slug()` function in `sync/sync_personas.py`
- **Pattern:** `^[a-z][a-z0-9-]*$`

**Examples:**
| Display Name | Internal Key |
|-------------|-------------|
| Zan | `zan` |
| Ian-API | `ian-api` |
| Ian-DevOps | `ian-devops` |
| Ian-SecRed | `ian-secred` |
| Ran-People | `ran-people` |
| Lan-Compliance | `lan-compliance` |

## Display Names

Used in frontmatter `title:` field and human-facing references.

### ALL-CAPS Acronyms

Technical and domain acronyms are written in ALL CAPS:

| Acronym | Meaning |
|---------|---------|
| API | Application Programming Interface |
| DevOps | Developer Operations |
| UX | User Experience |
| UI | User Interface |
| SecRed | Security Red Team |
| SecBlue | Security Blue Team |
| IP | Intellectual Property |
| QA | Quality Assurance |
| DBA | Database Administrator |
| GDPR | General Data Protection Regulation |
| SOC 2 | Service Organization Control 2 |
| HIPAA | Health Insurance Portability and Accountability Act |
| PCI-DSS | Payment Card Industry Data Security Standard |
| ISO 27001 | Information Security Management |

### Research Domain Names (Ran Family)

The "Ran" prefix and the domain word are both capitalized (acronyms stay ALL-CAPS):

| Key | Display Name |
|-----|-------------|
| `ran-people` | Ran-People |
| `ran-brand` | Ran-Brand |
| `ran-tech` | Ran-Tech |
| `ran-business` | Ran-Business |
| `ran-web` | Ran-Web |
| `ran-app` | Ran-App |
| `ran-general` | Ran-General |

## File Names

- Match the internal key exactly
- `.md` extension
- Located in the hierarchy-appropriate folder under `personas/`

```
personas/l0/zan.md
personas/l0/jan.md
personas/l1/ian.md
personas/l1/ban.md
personas/l2/ian/ian-api.md
personas/l2/ran/ran-brand.md
personas/l2/lan/lan-ip.md
```

## Hierarchy Placement Rules

| Layer | Who Can Have Children | Rule |
|-------|---------------------|------|
| L0 | N/A | Default voices only; no children |
| L1 | Only Ian, Ran, Lan | All other L1s are single-focus |
| L2 | Under Ian, Ran, or Lan | Parent must be specified in frontmatter |
| L3 | Under L2 (future) | Reserved for sub-specialists |
| L4 | External tools | Not personified |

## Trigger Keywords

Persona files optionally specify `triggers:` in frontmatter. These are the
keywords users type to invoke a persona:

- `/personality <key>` — explicit invocation
- `<key>` as a greeting in any message — soft invocation

**Example:**
```yaml
---
name: ran-brand
triggers:
  - /personality ran-brand
  - ran-brand
```

## Identity Tokens

Persona prompts may contain uppercase token placeholders:

| Token | Resolved From |
|-------|--------------|
| `<USER>` | `identity.user` |
| `<COMPANY>` | `identity.company` |
| `<PRODUCT>` | `identity.product` |
| `<EMAIL>` | `identity.email` |
| `<HERMES_HOME>` | `infrastructure.hermes_home` |
| `<REPO_URL>` | `infrastructure.repo_url` |
| `<REPO_PATH>` | `infrastructure.repo_path` |
| `<OUTPUT_DIR>` | `infrastructure.output_dir` (e.g. `scratch/output`) |
| `<API_PROVIDER>` | `infrastructure.api_provider` |
| `<MODEL>` | `infrastructure.model` |
| `<FALLBACK>` | `infrastructure.fallback` |
| `<FREE_TIER>` | `infrastructure.free_tier` |
| `<DASHBOARD_PORT>` | `infrastructure.dashboard_port` |

Custom tokens can be added to `config/identities.yaml` under any section.
Each key resolves as `<KEY>` (uppercased). The section name is not part of
the token, so keys must be unique across sections. The sync script warns
when two sections define the same key.

### Runtime placeholders

Lowercase placeholders such as `<project>`, `<topic>` and `<yymmdd>` are
**not** resolved at sync time. The agent fills them in per task. For
example, `<OUTPUT_DIR>/<yymmdd>-<project>-api.md` might become
`scratch/output/261026-checkout-api.md`.
