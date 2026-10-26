---
title: Hermes Google Workspace + WhatsApp Integration Research
date: 2026-10-26
version: v2026.0.1
status: Draft
author: Ran-Tech
---
# Hermes Google Workspace + WhatsApp Integration

## Overview
This document covers two integration paths for Hermes:
1. **Google Workspace** — Gmail, Calendar, Drive, Sheets, Docs through OAuth2 + gws CLI
2. **WhatsApp** — two adapter options (Baileys bridge for personal accounts, Cloud API for business bots)

---

## 1. Google Workspace Integration

### Architecture
Hermes manages OAuth2 tokens and delegates API calls through a thin CLI wrapper.
The skill auto-refreshes tokens and works headlessly (browser, Telegram, Discord).

**Installation:**
```bash
hermes skills install google-workspace
```
Or standalone:
```bash
pip install --user git+https://github.com/BruceLanLan/hermes-google-workspace.git
gws --version     # gws 2.2.0
gws-setup --check
```

### Setup Flow (4 steps)
1. **Create a Google Cloud project** — enable Gmail API, Calendar API, Drive API, Sheets API, Docs API, People API
2. **Create OAuth 2.0 credentials** (Desktop app type) — download client_secret JSON
3. **Authorize** — Hermes generates an auth URL; approve in browser; paste back redirect URL
4. **Done** — token auto-refreshes; no manual renewal needed

> **Tip:** If you only need email, use the `himalaya` skill instead — Gmail App Password, 2-minute setup. No Google Cloud project needed.

### Gmail Usage
```bash
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail get MESSAGE_ID
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1>" --html
$GAPI gmail send --to user@example.com --from '"Research Agent" <you@company.com>' --body "..."
```
**Return format:** `{id, threadId, from, to, subject, date, labels, body}` for send/reply.

### Calendar Usage
```bash
$GAPI calendar list
$GAPI calendar list --start 2026-10-26T00:00:00Z --end 2026-10-27T23:59:59Z
$GAPI calendar create --summary "Team Standup" --start 2026-10-26T10:00:00-07:00 --end 2026-10-26T10:30:00-07:00
$GAPI calendar create --summary "Lunch" --start 2026-10-27T12:00:00Z --end 2026-10-27T13:00:00Z --location "Cafe" --attendees "alice@co.com,bob@co.com"
$GAPI calendar delete EVENT_ID
```
> **Warning:** Calendar times MUST include timezone offset (e.g., `-07:00`) or use UTC (`Z`). Bare datetime strings are treated as UTC.

**Return format:** `[{id, summary, start, end, location, description, htmlLink}]`

### Safety Rules
1. **Never send email or create/delete calendar events without user confirmation first**
2. **Check auth before first use** — run `setup.py --check`
3. **Respect rate limits** — avoid rapid-fire API calls
4. **Use Gmail search syntax reference** for complex queries
5. **Calendar times must include timezone** — ISO 8601 with offset or UTC

### Key Dependencies
- Python 3.9+ (3.11+ recommended)
- Google account or Workspace
- Desktop OAuth client from Google Cloud Console

---

## 2. WhatsApp Integration

Hermes supports two WhatsApp paths:

### Option A: Baileys Bridge (Unofficial — Personal Accounts)

**Best for:** Quick demos, personal use, testing, single-user setups.

**Pros:**
- No Meta developer account or Business verification required
- No public HTTPS URL needed
- Works with personal WhatsApp numbers
- Quick QR-code pairing in minutes

**Cons:**
- Unofficial — risk of account restriction/ban from WhatsApp
- WhatsApp periodically updates Web protocol, breaking compatibility
- Single-number limitation (can't handle many users cleanly)
- Session persistence stores encryption keys locally (~/.hermes/platforms/whatsapp/session)

**Setup:**
```bash
hermes whatsapp
# Wizard: scan QR code → settings persist automatically
```

**Prerequisites:** Node.js v18+ (bridge runs as Node subprocess). No Chromium needed.

**Config:**
```bash
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot                 # or "self-chat"
WHATSAPP_ALLOWED_USERS=15551234567  # comma-separated with country code
# OR WHATSAPP_ALLOWED_USERS=*
```

**Bot-mode phone number** — three options:
| Option | Cost | Notes |
|---|---|---|
| Google Voice | Free | US only |
| Prepaid SIM | $5-15 | Keep active (call every 90 days) |
| VoIP services | Free-$5/mo | Some numbers blocked by WhatsApp |

### Option B: WhatsApp Business Cloud API (Official — Business Bots)

**Best for:** Real business bots, stability, compliance.

**Pros:**
- Official Meta-supported path
- No account ban risk
- Professional-grade reliability
- Can handle multiple users

**Cons:**
- Requires Meta Business account (not personal WhatsApp)
- Bot operates on a dedicated business number (not your personal number)
- Requires public HTTPS URL for webhook (Cloudflare Tunnel recommended)
- Replies >24h after user's last message require pre-approved templates
- More setup overhead (Meta verification, template paperwork)

**Prerequisites:**
1. Meta Business account at business.facebook.com
2. Meta app with WhatsApp enabled (developers.facebook.com)
3. Public HTTPS URL (Cloudflare Tunnel free tier recommended)
4. ffmpeg on PATH (for voice message rendering as native bubbles)

**Setup Steps:**
1. Create Meta app → "Connect with customers through WhatsApp"
2. Note four values from dashboard:
   - Phone Number ID (15-17 digits — NOT the phone number)
   - Access Token (starts with `EAA`, 100+ chars)
   - App Secret (32-char hex from Settings → Basic)
   - App ID (optional, 15-16 digits)
3. Generate permanent System User token (never expires) with permissions:
   - `business_management`
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
4. Set token expiration to "Never"
5. Configure webhook:
   - Callback URL: `https://<your-tunnel>/whatsapp/webhook`
   - Verify Token: from `python -c "import secrets; print(secrets.token_urlsafe(32))"`
6. Subscribe to "messages" field in webhook configuration
7. Expose Hermes to internet:
   ```bash
   cloudflared tunnel --url http://localhost:8090
   ```

**Config (.env):**
```
WHATSAPP_CLOUD_PHONE_NUMBER_ID=<15-17 digits>
WHATSAPP_CLOUD_ACCESS_TOKEN=EAA...
WHATSAPP_CLOUD_APP_SECRET=<32-char hex>
```

**Inbound message types supported:**
- Text messages → passed to agent
- Images → auto-downloaded, vision models read directly
- Voice notes → .ogg, transcribed via STT, handed as text
- Documents → small text files (<100KB) inlined; larger cached locally
- Button taps → routed to matching handler
- Reply context → original text attached as context

**Security Notes:**
- App Secret = password — anyone with it can forge webhooks
- Access Token = bot identity — rotate immediately if compromised
- Without App Secret, inbound delivery refused with HTTP 503
- `/health` endpoint unauthenticated — safe but can be restricted at proxy layer

### Option C: WhatsApp Agent Platform Plugin (Meta Beta)

**Best for:** Users with Meta's beta WhatsApp Agents feature.

**Requirements:** Hermes Agent >= 0.21.4 (GitHub release v2026.9.21 or newer)

```bash
hermes plugins install whatsapp-agent-platform
WHATSAPP_AGENT_PLATFORM_API_KEY=<your-key-from-whatsapp-settings-agents>
```
Uses long-poll (no public URL needed), Meta's official `/agent/v1` endpoints.

---

## 3. Pro-Cons Analysis

### Google Workspace Integration

| Pros | Cons |
|---|---|
| OAuth2 with automatic token refresh | Google Cloud project setup required (10-15 min) |
| Full Gmail + Calendar + Drive + Sheets + Docs coverage | Google may prompt for re-consent after scope changes |
| Works headlessly (browser, Telegram, Discord) | Rate limits on bulk operations |
| Agent-driven setup wizard | Requires Google account with API access |
| `--from` header customization for shared accounts |  |
| Search, read, send, reply, labels for Gmail |  |
| Full CRUD for Calendar events |  |

**Risk mitigation:** Skill rules require user confirmation before any write operation (send email, create/delete event). Calendar times require explicit timezone to avoid ambiguity.

### WhatsApp — Baileys Bridge

| Pros | Cons |
|---|---|
| Minutes to set up | Unofficial — ban risk from WhatsApp |
| No Meta account | Protocol breakage on WhatsApp updates |
| No public URL needed | Personal number only |
| Works now | Session file must be backed up securely |
|  | No template support for 24h+ delayed messages |

**Ban-minimization practice:** Use a dedicated phone number (not personal), keep usage conversational, don't spam.

### WhatsApp — Cloud API

| Pros | Cons |
|---|---|
| Official Meta-supported | Requires Meta Business account |
| No ban risk | Dedicated business number required |
| Production-grade | Public HTTPS URL required |
|  | 24h conversation window + template approval process |
|  | More setup steps (verification, templates) |

---

## 4. Recommendations

### For Email + Calendar (Google Workspace)
Use the bundled `google-workspace` skill. The agent-driven setup wizard handles OAuth2 end-to-end. If email-only is needed, prefer the `himalaya` skill (2-minute App Password setup).

### For WhatsApp — Business Bot
Use **Cloud API**. The ban risk of Baileys is not worth it for anything beyond a personal demo. Cloudflare Tunnel (free tier) solves the public URL requirement.

### For WhatsApp — Personal Testing
Use **Baileys bridge** but on a dedicated phone number (VoIP or prepaid SIM). Keep volume low and conversational.

### For WhatsApp — Meta Beta Users
Use the **WhatsApp Agent Platform plugin** if you have access — it's the cleanest path (long-poll, no public URL, official).

### For Responding On Behalf of User
The Cloud API bot can respond on your behalf once you're registered as an allowed user in `WHATSAPP_ALLOWED_USERS`. Baileys bridge works identically — the bot reads inbound messages and the agent replies through the same channel. Both support the `--from` header customization for Google Workspace emails.

---

## 5. Integration Map

```
Hermes Gateway (port 8090)
  |
  +-- Google Workspace Skill
  |     |-- OAuth2 token (auto-refresh)
  |     |-- gws CLI wrapper (gmail, calendar, drive, sheets, docs)
  |     |-- himalaya (email-only, fallback)
  |
  +-- WhatsApp Platform Adapters
  |     |
  |     |-- Baileys Bridge (Node.js subprocess)
  |     |     |-- QR pairing → session saved
  |     |     |-- Personal number
  |     |
  |     |-- WhatsApp Business Cloud API
  |     |     |-- Webhook → /whatsapp/webhook
  |     |     |-- Public HTTPS (Cloudflare Tunnel)
  |     |     |-- 24h window + templates
  |     |
  |     |-- WhatsApp Agent Platform Plugin (Community)
  |           |-- Long-poll /agent/v1
  |           |-- Meta beta users only
  |
  +-- Google Calendar Sync
        |-- Events created/updated/deleted via $GAPI calendar create/delete
        |-- Timezone-aware ISO 8601 required
```

---

## 6. References

- Hermes Google Workspace skill: `https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-google-workspace`
- Hermes WhatsApp (Baileys): `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp`
- Hermes WhatsApp Business Cloud API: `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud`
- gws CLI: `https://github.com/BruceLanLan/hermes-google-workspace`
- WhatsApp Agent Platform plugin: `https://hermes-agent.nousresearch.com/docs/plugins/whatsapp-agent-platform`
