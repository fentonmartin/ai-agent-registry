# Deal Context Template — Per-Deal Working File

> One file per active deal. This is the deal's working memory — not a CRM summary.
> Update after every meaningful interaction. Separate from gtm-context (which is per-product).
> Archive when deal closes or is lost.

---

## Deal Header

```
DEAL CONTEXT FILE
=================
Company:        [Company name]
Domain:         [company.com]
Industry:       [B2B SaaS / FinTech / etc.]
Company size:   [Employee count / ARR estimate]
Deal stage:     [Stage name: e.g., Stage 2 — Qualified / Stage 3 — Technical Validation]
Deal amount:    [$ ARR estimate]
Close date:     [Target close date: YYYY-MM-DD]
Deal owner:     [AE name]
SDR / BDR:      [Name if applicable]
SE / Solutions: [Name if applicable]
CRM deal ID:    [Link or ID]
File created:   [YYYY-MM-DD]
Last updated:   [YYYY-MM-DD]
```

---

## Deal Thesis

*Write 2–4 sentences describing why this deal should happen: what problem they have, why we
are the right solution, why now, and what success looks like for the buyer. This is your north
star for the deal — if the thesis changes, update it and flag internally.*

```
[Company name] is scaling its [RevOps / Growth / Sales] function from [X] to [Y] headcount
following their [Series X] raise. Their [pain: e.g., manual attribution process] is creating
[specific impact: e.g., unreliable pipeline forecasts and 12+ hours/week of analyst time].
They have evaluated [alternative] but found [gap]. We are the right fit because [reason],
and the urgency is driven by [trigger: e.g., Q2 board reporting deadline / new CRO hire].
```

---

## Stakeholder Map

Update after every interaction. Sentiment: (+) positive, (-) negative, (N) neutral, (?) unknown.

| Name | Title / Role | Buying Group Role | Sentiment | Last Contact | Notes |
|------|-------------|------------------|-----------|-------------|-------|
| [Name] | [Title] | Champion | + | [YYYY-MM-DD] | [Key concern, motivation, or dynamic] |
| [Name] | [Title] | Approver | N | [YYYY-MM-DD] | [Note] |
| [Name] | [Title] | Economic Buyer | ? | Not yet contacted | [Note] |
| [Name] | [Title] | User | + | [YYYY-MM-DD] | [Note] |
| [Name] | [Title] | Technical Reviewer | N | [YYYY-MM-DD] | [Note] |
| [Name] | [Title] | Potential Blocker | - | [YYYY-MM-DD] | [Note] |

**Coverage gaps:** [List any required stakeholder roles not yet engaged]  
**Next stakeholder action:** [Who to reach, by when, through whom]

---

## Key Research Findings

*Pull from account-brief-template.md and ban-sales-research output. Summarize the most
deal-relevant findings. Include evidence labels (Verified / Inferred / Unknown).*

### Company Context
- Funding: [Amount, stage, date, lead investor] — [Evidence label]
- Growth: [Headcount trajectory, revenue signals] — [Evidence label]
- Strategic priorities: [What they're publicly focused on] — [Evidence label]

### Problem Context
- Confirmed pain: [What we know they're struggling with] — [Evidence label]
- Source of pain confirmation: [Discovery call / outbound reply / press / job posting]
- Impact quantified: [If known: time, cost, missed outcomes] — [Evidence label]

### Competitive Context
- Known incumbent: [Tool or process they use today] — [Evidence label]
- Evaluation set: [Other vendors being considered, if known] — [Evidence label]
- Competitive risk: [Our vulnerability vs. alternatives] — [Evidence label]

### Tech Stack
- CRM: [Name + version if known] — [Evidence label]
- Marketing automation: [Name] — [Evidence label]
- Data / BI: [Name] — [Evidence label]
- Other relevant tools: [Name] — [Evidence label]

---

## Qualification Status

Score against qualification-frameworks.md criteria. Update after each stage-advancing interaction.

| Criterion | Status | Evidence | Source | Last Updated |
|-----------|--------|---------|--------|-------------|
| [Criterion 1] | Confirmed / Inferred / Unknown / Failed | [What we know] | [Discovery call / research] | [Date] |
| [Criterion 2] | Confirmed | [Evidence] | [Source] | [Date] |
| [Criterion 3] | Unknown | — | — | — |
| [Criterion 4] | Failed | [Why] | [Source] | [Date] |
| [Criterion 5] | Confirmed | [Evidence] | [Source] | [Date] |

**Overall qualification:** [Strong / Moderate / Weak / Disqualify]  
**Qualification decision:** [Advance / Hold pending [X] / Disqualify — reason]

---

## Mutual Action Plan

Agreed steps toward close. Share with buyer champion and update collaboratively.

| Milestone | Owner | Due Date | Status |
|-----------|-------|---------|--------|
| Discovery call complete | [AE name] | [YYYY-MM-DD] | Done |
| Account brief shared with champion | [AE name] | [YYYY-MM-DD] | Done |
| Technical validation call | [SE name + Buyer name] | [YYYY-MM-DD] | Scheduled |
| Security / IT review packet sent | [AE name] | [YYYY-MM-DD] | Not started |
| Reference call arranged | [AE name] | [YYYY-MM-DD] | Not started |
| Business case / ROI doc delivered | [AE name] | [YYYY-MM-DD] | Not started |
| Economic buyer intro meeting | [Champion name + AE] | [YYYY-MM-DD] | Not started |
| Proposal / commercial terms sent | [AE name] | [YYYY-MM-DD] | Not started |
| Legal / security review | [Buyer IT/Legal + AE] | [YYYY-MM-DD] | Not started |
| Contract signed | [AE name] | [YYYY-MM-DD] | Not started |

**MAP status:** [On track / At risk — reason / Blocked by — who]

---

## Risk Register

Document known risks and mitigation plans. Review at every deal review.

| Risk | Likelihood | Impact | Mitigation | Owner | Status |
|------|-----------|--------|-----------|-------|--------|
| Champion leaves company | Medium | High | Build relationships with 2nd stakeholder | AE | Active |
| Budget not approved | Medium | High | Build CFO-facing business case; get economic buyer engaged early | AE | Planned |
| Incumbent contract not expired | Low | High | Confirm contract end date; plan re-engage timeline | AE | Investigating |
| Competitor wins on price | High | High | Quantify cost of status quo; prepare competitive comparison | AE | Active |
| Technical integration blocker | Low | Medium | SE to confirm integration path in technical call | SE | Pending |
| Procurement delay | Medium | Medium | Get procurement requirements early; introduce legal review early | AE | Planned |
| Stakeholder misalignment (internal) | Medium | High | Map all stakeholders; confirm champion has internal support | AE | Active |

**Top risk this week:** [Risk name — mitigation action in progress]

---

## Negotiation Range

Complete before commercial discussions begin. Do not share externally.

| Dimension | Ideal | Acceptable | Walk-Away |
|-----------|-------|-----------|----------|
| Contract value (ARR) | [$X] | [$Y — min threshold for healthy unit economics] | [Below $Z — not worth serving] |
| Contract term | [3 years] | [2 years] | [Monthly or < 1 year without penalty] |
| Payment terms | [Annual upfront] | [Semi-annual] | [Monthly without price premium] |
| Discount | [0%] | [Up to X%] | [Beyond Y% without executive approval] |
| Implementation support | [Paid] | [Included for first 90 days] | [Unlimited free — margin risk] |
| SLA / uptime commitment | [99.9%] | [99.5%] | [Custom SLA without pricing adjustment] |
| Data terms | [Standard DPA] | [Modified DPA with legal review] | [Data sovereignty clauses we can't fulfill] |

**Approval required for:** [Any discount above X% / custom contract terms / pilot without payment]  
**Approved by:** [Manager / VP Sales name]

---

## Deal History Log

Chronological record of every meaningful deal event. Append; never delete.

```
[YYYY-MM-DD] — [Event type: Outreach / Reply / Call / Email / Internal review / Proposal / etc.]
[Who was involved]
[What happened — 2–5 sentences]
[Outcome or next step agreed]

---

[YYYY-MM-DD] — [Event type]
[Details]
[Outcome]
```

**Example entries:**
```
2026-01-15 — Cold email sent (Touch 1)
Sent to: Sarah Chen, RevOps Director
Trigger: Saw hiring spike (3 RevOps roles posted in 2 weeks).
Outcome: No reply.

---

2026-01-20 — Email reply received
From: Sarah Chen
Content: "Interested — can we do 20 minutes next week?"
Outcome: Meeting booked for 2026-01-28.

---

2026-01-28 — Discovery call (30 min)
Attendees: Sarah Chen (RevOps Dir), AE [Name]
Key findings: Confirmed manual attribution pain; 10+ hours/week on spreadsheet reconciliation;
VP Revenue asking for better forecast accuracy by end of Q1.
Next step: Technical validation call with SE; Sarah will loop in IT lead.

---
```

---

*Last updated: see git log. Owner: ban-sales L3. Related: account-brief-template.md, qualification-frameworks.md, deal-strategy.md, gtm-context-template.md*
