# Per-Deal Folder Conventions

## Per-Deal Folder Structure

Each deal lives under `.agents/DEAL_SLUG/` and contains:

- `gtm-context.md` — product context (GTM positioning, ICP, value props, objection handling)
- `deal-context.md` — per-deal specifics (company background, contacts, deal stage, notes)

## Output Folder

All artifacts for a deal are written to:

```
scratch/output/ban-sales/DEAL_SLUG/
```

## File Naming Convention

Format: `YYMMDD-TYPE.md`

Examples:
- `261030-market.md` — market research output
- `261030-research-COMPANY.md` — deep company OSINT research
- `261030-qualify.md` — qualification scorecard

## Starting a New Deal

1. Copy `gtm-context-template.md` → `.agents/DEAL_SLUG/gtm-context.md`
2. Copy `deal-context-template.md` → `.agents/DEAL_SLUG/deal-context.md`
3. Fill in deal-specific fields in `deal-context.md`
4. Create output folder: `scratch/output/ban-sales/DEAL_SLUG/`

## How Specialists Find Context

1. Always check `.agents/DEAL_SLUG/` first (deal-specific overrides)
2. Fall back to `.agents/gtm-context.md` for global GTM context if deal folder is missing a file

## Multi-Deal Isolation

Each deal is fully isolated — specialists must never read context from another deal's folder. No cross-reading between deals.

## DEAL_SLUG Format

Lowercase, hyphenated company name.

Examples:
- `pt-abc-corp`
- `acme-logistics`
- `bumi-resources-tbk`
