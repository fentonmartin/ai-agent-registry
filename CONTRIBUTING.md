# Contributing to AI Agent Registry

Thank you for your interest in contributing! This document outlines how to
add personas, improve prompts, and extend the framework.

## How to Add a New Persona

### 1. Choose the Right Layer

| Layer | When to add | Example |
|-------|-------------|---------|
| **L1** | A new domain that doesn't fit existing L1s | A "Security" expert |
| **L2** | A specialist under an existing L1 parent | Added under `Ian` or `Ran` or `Lan` |

### 2. Create the Persona File

```bash
# L2 under Ian
touch personas/l2/ian/ian-security.md

# L1 new domain
touch personas/l1/security.md
```

### 3. Add YAML Frontmatter

```yaml
---
name: ian-security      # lowercase, kebab-case
title: Ian-Security     # ALL-CAPS preferred
role: Ian sub-context for security review
parent: ian              # L1 parent (required for L2)
triggers:
  - /personality ian-security
  - security review
  - threat model
help: /personality ian-security
---
```

### 4. Write the System Prompt

After the `---` closing the frontmatter, write a clear, scoped system prompt:

- **Start with identity:** "You are Ian-Security, ..."
- **Define scope:** What does this persona do? What is it explicitly NOT responsible for?
- **List key responsibilities:** Numbered or bulleted
- **Specify output format:** Where does it write results?
- **Add escalation rules:** When to delegate or escalate

### 5. Run the Sync Script

```bash
python sync/sync_personas.py --check
```

This validates:
- All frontmatter is well-formed YAML
- All `parent:` references point to existing L1 personas
- No duplicate keys
- No orphaned personas

### 6. Submit a Pull Request

```bash
git checkout -b add-persona-ian-security
git add personas/l2/ian/ian-security.md
git commit -m "Add Ian-Security: security review specialist"
git push origin add-persona-ian-security
```

## Naming Conventions

| Element | Format | Example |
|---------|--------|---------|
| Internal key | lowercase-kebab | `ian-security` |
| Display title | MixedCase + ALL-CAPS acronyms | `Ian-Security`, `Ian-API` |
| File name | match internal key | `ian-security.md` |
| L2 parent field | L1 key only | `parent: ian` |

**DO:** `Ian-API` (ALL-CAPS acronym)
**DON'T:** `Ian-Api` (lowercase "api")

**DO:** `Ran-People` (ALL-CAPS research domain)
**DON'T:** `Ran-people` (inconsistent casing)

## Layer Rules

- **Only Ian, Ran, Lan** can have L2 children
- All other L1s are single-focus (no children)
- L3 is reserved for future sub-specialists
- L4 is for external tools, not personas

## Testing Your Changes

```bash
# Check persona files are valid
python sync/sync_personas.py --check --persona-dir personas --identities config/identities.example.yaml

# Full sync (dry run)
python sync/sync_personas.py --dry-run
```

## CI Checks

All PRs must pass:
1. Persona file frontmatter validation
2. Hierarchy integrity check (no stale parent references)
3. No sensitive data patterns

## Need Help?

- Open an issue with the `question` label
- Start a discussion in [GitHub Discussions](https://github.com/fentonmartin/ai-agent-registry/discussions)
