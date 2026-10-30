# Prospecting Plan — Structured Outbound Framework

> Operational template for ban-sales L3 prospecting. Fill one plan per campaign or quarter.
> Handoff to ban-sales-research when criteria in Section 7 are met.

---

## 1. Prospecting Plan Template

```
PROSPECTING PLAN — [Quarter / Campaign Name]
============================================
Goal:             [Qualified meetings booked | Pipeline created $]
ICP Tier Focus:   [Tier 1 / Tier 2 / Both]
Primary Sources:  [LinkedIn Sales Nav / Crunchbase / G2 / Event lists / Referrals]
Weekly Meeting Target: [N meetings/week]
Weekly Outreach Target:[N new accounts/week | N new contacts/week]
Campaign Duration: [Start date → End date]
Owner:            [Your name]
Review Cadence:   Every Friday 30 min
```

---

## 2. Account Tier Model

### Tier 1 — High-Touch Manual

**Profile:** 4+ ICP criteria met; both Must-haves confirmed  
**Time investment:** 45–60 min per account for research + personalization  
**Activities:**
- Custom account brief (use account-brief-template.md)
- Multi-threaded outreach: champion + approver simultaneously
- Personalized email sequence (no templated first line)
- LinkedIn connection + InMail + phone if available
- Direct outreach from AE or sales leader (not SDR) for largest accounts

**Volume targets:** 5–10 net-new Tier 1 accounts per week  
**Sequence length:** 8–10 touches over 3–4 weeks  

---

### Tier 2 — Semi-Automated

**Profile:** 2–3 ICP criteria met; at least one Must-have confirmed  
**Time investment:** 15–20 min per account (review + light personalization)  
**Activities:**
- Light research: company name, trigger event, one specific detail
- Templated email with personalization slot filled (first line customized)
- LinkedIn connection request only (no InMail unless reply to email)
- Standard sequence from outbound-templates.md

**Volume targets:** 15–25 net-new Tier 2 accounts per week  
**Sequence length:** 5–6 touches over 2–3 weeks  

---

### Tier 3 — Low-Touch

**Profile:** 1 ICP criterion met; Must-haves unconfirmed  
**Time investment:** 5 min per account  
**Activities:**
- Generic template with company name only
- Single LinkedIn connection (no message)
- Add to nurture sequence (marketing-owned)
- Do not spend AE/SDR time beyond initial touch

**Volume targets:** Batch 50–100 per month  
**Sequence length:** 2–3 touches max; move to nurture or discard  

---

## 3. Contact Coverage Model

| Account Tier | Minimum Contacts | Roles to Cover | Priority Order |
|-------------|-----------------|----------------|----------------|
| Tier 1 | 3–5 contacts | Champion + Approver + User + Economic Buyer | Champion first; then multi-thread within 72 h |
| Tier 2 | 2–3 contacts | Champion + one Approver | Champion first; second contact on touch 3 |
| Tier 3 | 1 contact | Most likely champion based on title | Single thread only |

**Role priority for first contact:**
1. RevOps Manager / Director of Revenue Operations
2. VP Revenue / CRO (if small company, <100 employees)
3. Head of Growth / Marketing Operations
4. VP Sales (if RevOps doesn't exist)

**Do NOT start with:** CEO (unless <20 employees), CFO (they are economic buyers, engage later), Engineering leads.

---

## 4. Weekly Cadence Targets

| Day | Activity | Target |
|-----|---------|--------|
| Monday | Research + qualify new accounts for the week | 10–20 accounts reviewed; tier assigned |
| Monday | Load new contacts into sequences | All new contacts added before noon |
| Tuesday | Personalize and send Tier 1 first touches | 5–10 Tier 1 first emails out |
| Tuesday–Wednesday | LinkedIn connection requests | 15–25 connections sent |
| Wednesday | Follow-up on sequence touches due | All scheduled touches reviewed + sent |
| Thursday | Responses: positive replies → book meeting; objections → handle | Same-day reply target |
| Thursday | Research for next week's Tier 1 accounts | 5–10 accounts pre-researched |
| Friday | Weekly learning loop (see Section 6) | 30-min self-review completed |
| Friday | Update CRM / account list | All activity logged; tiers updated |

**Non-negotiable weekly minimums:**
- 5 qualified meetings booked (Tier 1 or 2)
- 10 new Tier 1 first touches
- 20 new Tier 2 first touches
- 100% CRM activity logged within 24 h

---

## 5. Account & Contact List Schema

Use this schema for every account list. CSV headers exactly as shown.

```
company, domain, industry, company_size, hq_city, hq_country,
contact_name, contact_title, linkedin_url, email, email_confidence,
icp_tier, icp_score, icp_notes,
source, source_date, trigger_event, trigger_date,
sequence_name, sequence_status, last_touch_date, next_touch_date,
meeting_booked, meeting_date, outcome,
notes, owner, last_updated
```

### Field Definitions

| Field | Description | Valid Values / Format |
|-------|-------------|----------------------|
| `company` | Legal or trading name | Text |
| `domain` | Primary website domain | e.g. acme.com |
| `industry` | Primary industry | B2B SaaS / FinTech / MarTech / etc. |
| `company_size` | Employee count band | 1-10 / 11-50 / 51-200 / 201-500 / 501-1000 / 1000+ |
| `hq_city` | Headquarters city | Text |
| `hq_country` | Headquarters country | ISO 3166-1 alpha-2 |
| `contact_name` | Full name | First Last |
| `contact_title` | Job title as listed | Text (copy from LinkedIn) |
| `linkedin_url` | Contact's LinkedIn profile | URL |
| `email` | Work email | email@domain.com |
| `email_confidence` | Confidence in email validity | Verified / Guessed / Unknown |
| `icp_tier` | Assigned tier | 1 / 2 / 3 |
| `icp_score` | Number of criteria met | 0–8 integer |
| `icp_notes` | Which criteria matched | Free text |
| `source` | Where account was found | LinkedIn / Crunchbase / Referral / Event / G2 / Inbound |
| `source_date` | When found | YYYY-MM-DD |
| `trigger_event` | What triggered outreach | Funding / Hire / Job posting / Headcount growth / None |
| `trigger_date` | When trigger occurred | YYYY-MM-DD |
| `sequence_name` | Which email sequence running | e.g. Tier1-Funding-Q1 |
| `sequence_status` | Where in sequence | Not started / Active / Paused / Completed / Replied |
| `last_touch_date` | Most recent outreach | YYYY-MM-DD |
| `next_touch_date` | Scheduled next touch | YYYY-MM-DD |
| `meeting_booked` | Meeting scheduled | Yes / No |
| `meeting_date` | Discovery call date | YYYY-MM-DD HH:MM |
| `outcome` | Final result | Meeting booked / No response / Not interested / Referral / Nurture |
| `notes` | Any additional context | Free text |
| `owner` | SDR or AE responsible | Name |
| `last_updated` | Last record update | YYYY-MM-DD |

---

## 6. Weekly Learning Loop

Answer these questions every Friday before the weekend.

**Volume & Activity**
- How many new accounts did I add this week vs. target?
- How many first touches went out? (Tier 1 / Tier 2 / Tier 3 split)
- What was my reply rate by tier?

**Quality**
- Which messages got replies? What pattern made them work?
- Which messages got no reply? What would I change?
- Did any replies reveal a new ICP signal or disqualifier?

**Pipeline**
- How many meetings booked vs. target?
- What was the quality of meetings booked (ICP tier of accounts)?
- Any patterns in what triggered positive responses?

**ICP Calibration**
- Did any Tier 1 accounts not reply? Could they be mis-tiered?
- Did any Tier 2 or 3 accounts engage unexpectedly? Should I revise criteria?
- Are there disqualifiers I should add based on this week's learnings?

**Next Week**
- What's my top priority change in approach?
- Which accounts from this week need follow-up?
- Am I on track for quarterly goals?

---

## 7. Handoff Criteria to ban-sales-research

Escalate to ban-sales-research when:

| Condition | Handoff Action |
|-----------|---------------|
| Tier 1 account replied positively; discovery call in < 5 days | Request full account brief (use account-brief-template.md) |
| Multi-stakeholder deal; need stakeholder map built | Share account domain + known contacts; request org research |
| Competitive intelligence needed before discovery | Provide competitor name + deal context |
| Account has complex tech stack or unusual industry nuance | Request technical environment summary |
| Deal advancing to Stage 3+ | Full research package: stakeholder map, financials, competitive |

**Handoff format:**
```
TO: ban-sales-research
ACCOUNT: [Company name] | [Domain]
CONTEXT: [1–2 sentences on why we're in conversation]
KNOWN CONTACTS: [Name / Title / LinkedIn for each]
REQUEST: [Specific research needed]
TIMELINE: [When discovery call is scheduled]
PRIORITY: [Tier 1 / Urgent / Standard]
```

---

*Last updated: see git log. Owner: ban-sales L3. Related: icp-framework.md, outbound-templates.md*
