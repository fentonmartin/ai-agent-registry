# ICP Framework — Ideal Customer Profile Definition

> Evidence-based ICP definition and scoring reference for ban-sales L3 specialists.
> Every claim in this file should carry an evidence label. Update when new data arrives.

---

## 1. ICP Statement Template

```
[Company name / product name] primarily serves [company size / industry vertical] companies
that are [situation or growth stage], where [key role] is struggling to [core problem]
without sacrificing [valued outcome]. These buyers choose us because [primary differentiator]
and we can prove it with [evidence type].
```

**Example:**
> Acme AI primarily serves Series B–D SaaS companies with 50–500 employees in the
> revenue-operations or growth function, where the RevOps lead is struggling to attribute
> pipeline to specific motions without manual spreadsheet reconciliation. These buyers choose
> us because we close the attribution loop in under 48 h with no engineering lift, proven
> across 40+ closed-won accounts.

---

## 2. Fit Table

| Criterion | Rationale | Importance | Evidence | Confidence |
|-----------|-----------|------------|----------|------------|
| Industry: B2B SaaS / tech-enabled services | Our problem is specific to subscription + pipeline metrics | Must-have | 80% of closed-won accounts | Verified |
| Company size: 50–500 employees | Below 50: no budget; above 500: longer cycle, different buyer | Strong | Win/loss analysis Q1–Q3 | Verified |
| Funding stage: Series A–D | Pre-series A: no budget; post-D: often have in-house solution | Strong | CRM cohort analysis | Verified |
| Tech stack: CRM + marketing automation in place | Our product enriches existing data; empty stack = no signal | Must-have | Product onboarding data | Verified |
| RevOps or Growth function exists | Identifies the champion; otherwise no internal owner | Strong | Champion interviews | Verified |
| Recent growth signal: headcount +20%+ in 12 months | Pain of manual work is acute when team is scaling | Moderate | LinkedIn headcount data | Inferred |
| Active pipeline problem: stated or observable | Ensures urgency exists, not just latent pain | Strong | Discovery call transcripts | Hypothesis |
| Budget cycle: Q1 or Q3 start | Aligns to planning windows for faster close | Nice-to-have | Deal velocity analysis | Inferred |

---

## 3. Disqualifiers

### Hard Exclusions — Stop Immediately

- **No CRM in place** — our product has no data to work with
- **B2C or transactional retail** — pipeline concept does not apply
- **Government / highly regulated (HIPAA primary)** — compliance overhead exceeds deal value
- **Single-person company / solo founder** — no budget, no champion dynamic
- **Active competitor contract with 18+ months remaining** — switch cost too high

### Caution Signals — Qualify Further Before Advancing

| Signal | Why It Matters | Qualification Question |
|--------|---------------|----------------------|
| Revenue < $2M ARR | Budget often insufficient | "What's your current tech stack budget?" |
| Engineering-led buying process | Longer cycle; different champion | "Who owns your data infrastructure decisions?" |
| Recent layoffs in RevOps | Champion may not have authority | "Is the RevOps function currently being rebuilt?" |
| Already evaluating 4+ vendors | Shopping for price, not fit | "What does success look like in 90 days for you?" |
| No stated timeline | Latent pain only | "What happens if this problem isn't solved by Q2?" |

---

## 4. Buying Group Map

| Role | Who They Are | What They Care About | How to Identify | Engagement Strategy |
|------|-------------|---------------------|-----------------|-------------------|
| **User** | RevOps analyst, marketing ops | Reduces manual work, accuracy, ease of use | LinkedIn: "RevOps", "Marketing Ops" titles | Product demo, workflow walk-through |
| **Champion** | RevOps Manager / Director | Looks good to leadership, solves a real problem | Person who booked the first call | Enable with materials, check in weekly |
| **Approver** | VP Revenue / CRO | Pipeline confidence, board reporting | Ask champion: "Who signs off on tools?" | Executive brief, ROI summary |
| **Economic Buyer** | CFO / VP Finance | ROI, payback period, contract terms | CC'd on procurement emails | Business case doc, TCO comparison |
| **Technical Reviewer** | IT / Security | Data residency, SSO, API contracts | Added late in process | Security one-pager, SOC 2 cert |
| **Blocker** | Existing vendor relationship | Incumbent loyalty, switching cost narrative | Emerges in negotiation | Competitive comparison, reference call |

**Coverage rule:** By Stage 3 (Technical Validation), you must have direct contact with at minimum: Champion + one Approver.

---

## 5. Trigger Events Table

| Trigger Event | Why It Matters | How to Detect | Lead Time to Outreach |
|--------------|---------------|---------------|----------------------|
| Series B/C/D funding announcement | New budget, growth pressure, hiring spree | Crunchbase, TechCrunch, LinkedIn news | Within 5 business days |
| VP Revenue / CRO hire | New leader will audit toolstack | LinkedIn job change alerts | Within 3 business days |
| RevOps job posting (new role, not backfill) | Function expanding = pain point active | LinkedIn Jobs, Greenhouse, Lever | Same week |
| Headcount growth >20% in 6 months | Manual processes breaking under scale | LinkedIn company page, Bombora intent | Rolling, monthly scan |
| Competitor churn signal | Opportunity to capture displaced buyer | G2 reviews, community forums | Within 1 week of signal |
| Conference / event attendance | Mindshare moment, warm context | Event attendee lists, social posts | Within 2 days post-event |
| Product launch announcement | New go-to-market motion = new attribution need | Product Hunt, press release | Within 1 week |
| Leadership change (CEO/CMO) | Strategy reset, re-evaluation of stack | LinkedIn, press | Within 1 week |

---

## 6. Evidence Labels

Apply these labels to every claim in ICP documentation, deal notes, and positioning materials:

| Label | Definition | When to Use |
|-------|-----------|-------------|
| **Verified** | Confirmed by multiple independent data sources (CRM data, customer interviews, win/loss analysis) | Only after 3+ consistent signals |
| **Inferred** | Logical conclusion from related data; one step removed from direct evidence | Pattern exists but not directly confirmed |
| **Hypothesis** | Untested assumption that drives current strategy | Starting point; must have a test plan |
| **Unknown** | Acknowledged gap; no data yet | Better than a false label |
| **Conflicting** | Signals point in different directions | Flag for investigation, do not use to justify decisions |

**Rule:** Never present an **Inferred** claim as **Verified** in customer-facing materials.

---

## 7. ICP Scoring Tiers

Score each account against the Fit Table criteria before investing outreach time.

| Tier | Score | Profile | Action |
|------|-------|---------|--------|
| **Tier 1** | 4+ criteria met (including both Must-haves) | Highest fit; likely to close, likely to succeed | High-touch manual prospecting; prioritize in pipeline |
| **Tier 2** | 2–3 criteria met; at least 1 Must-have | Good fit with gaps; worth qualifying | Semi-automated outreach; qualify gap criteria in discovery |
| **Tier 3** | 1 criterion met; or Must-haves absent | Low fit; not worth active pursuit now | Low-touch or exclude; revisit in 6 months |

**Scoring process:**
1. Fill in Fit Table for each account (use Unknown liberally)
2. Count confirmed criteria (Verified or Inferred only)
3. Assign tier; document rationale in account record
4. Review tier assignment after discovery call

---

## 8. Validation Plan

ICP definitions are hypotheses. Run this validation cycle quarterly.

### Quarterly Validation Checklist

- [ ] Pull closed-won deals from last 90 days; score against current ICP criteria
- [ ] Pull closed-lost deals; identify where ICP overlap existed but deal failed
- [ ] Run 3 win interviews (customers) — confirm which criteria they would have scored highest
- [ ] Run 2 loss interviews (churned or lost prospects) — identify false positives
- [ ] Review open pipeline against ICP tiers; flag Tier 3 accounts in active stages

### Validation Questions

| Question | What It Tests |
|----------|--------------|
| Did Tier 1 accounts close faster than Tier 2? | Tier validity |
| Are Tier 1 customers retaining at higher rates? | Downstream ICP accuracy |
| Which criteria appear in >80% of closed-won? | Must-have candidates |
| Which criteria appear in >50% of closed-lost? | Potentially wrong criteria or caution signals |
| Are there winning accounts that don't fit the ICP? | ICP expansion opportunity |

### When to Update the ICP

- 3+ wins from an account type not currently in ICP → add as new segment
- 3+ losses despite strong ICP fit → revisit Must-have criteria
- Major product change → full ICP review
- New competitive entrant → check if ICP needs to sharpen differentiation criteria

---

*Last updated: see git log. Owner: ban-sales L3. Evidence labels: see Section 6.*
