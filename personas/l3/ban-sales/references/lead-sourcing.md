# Lead Sourcing Reference

Source: leadmagic/gtm-skills, zarif3624/gtm-skills, keinsaasforever/gtm-pipeline-skills

## Multi-Source Methodology

Single-source lists have systematic gaps. Every batch requires minimum 2 complementary sources.

## Source Priority Matrix

| Source | Best for | Coverage bias | Cost |
|---|---|---|---|
| Apollo.io | B2B contacts, tech companies | US-heavy, SMB-Enterprise | Paid |
| LinkedIn Sales Navigator | Decision makers, titles | Global, all sizes | Paid |
| Crunchbase | Funded startups, growth signals | VC-backed companies | Freemium |
| BuiltWith / SimilarTech | Tech stack targeting | Web-based companies | Paid |
| LinkedIn Jobs | Hiring signals, org structure | All public companies | Free |
| G2 / Capterra | SaaS buyers, software stack | SaaS verticals | Free |
| Tracxn | Emerging markets, SEA | Developing markets | Paid |
| Conference lists | Qualified buyers in vertical | Event attendees | Free (scrape) |
| Industry directories | Niche verticals | Long-tail | Free |
| Product Hunt | Early-stage, tech buyers | Startup-heavy | Free |

## Enrichment Waterfall

```
1. SOURCE       → get company list (domain as primary key)
2. DEDUPE       → match by domain, not name
3. ENRICH       → firmographics (size, revenue est., HQ, industry)
4. TECHNOGRAPH  → tech stack via BuiltWith / job postings
5. CONTACT      → find key buyer (title match from ICP)
6. VERIFY       → email + LinkedIn URL validation
7. SCORE        → ICP tier (1/2/3)
8. OUTPUT       → enriched list ready for research or outreach
```

## Deduplication Rules
- Primary key: **company domain** (not company name — names vary)
- Secondary: LinkedIn company URL
- Never merge two different companies with similar names — flag for manual review

## Missing Data Protocol
- Mark as `Unknown` — never infer or invent
- Email: `Unknown — not verified`
- Revenue: `Unknown — estimate pending enrichment`
- A contact with an invented email is worse than no contact

## Output Format

| Field | Required | Source |
|---|---|---|
| Company name | ✅ | |
| Domain | ✅ | |
| Industry | ✅ | |
| HQ country | ✅ | |
| Employee count | ✅ | |
| Revenue estimate | Optional | |
| Tech stack | Optional | BuiltWith |
| Key contact name | ✅ | |
| Key contact title | ✅ | |
| Key contact LinkedIn | Optional | |
| Email | Optional | Verified only |
| Funding stage | Optional | Crunchbase |
| ICP tier | ✅ | Scored |
| Source | ✅ | |
| Notes | Optional | |
