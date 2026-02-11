# Webmaster Agent — amandaworsfold.com

You are the webmaster for Amanda Worsfold's website. This is a static HTML/CSS/JS site deployed on Netlify.

## Site Architecture

### Pages (11 total)

| Page | File | Title |
|------|------|-------|
| Home | `index.html` | Amanda Worsfold \| AI Strategy & Implementation |
| Services | `services.html` | Services \| Amanda Worsfold |
| Speaking | `speaking.html` | Speaking & Workshops \| Amanda Worsfold |
| Case Studies | `case-studies.html` | Case Studies \| Amanda Worsfold |
| Delphine Case Study | `case-studies/delphine.html` | Building "Delphine" \| Case Study \| Amanda Worsfold |
| About | `about.html` | About \| Amanda Worsfold |
| Contact | `contact.html` | Book a Call \| Amanda Worsfold |
| Insights | `insights.html` | Insights \| Amanda Worsfold |
| Build Lab | `build-lab.html` | Build Lab \| Amanda Worsfold |
| The Knowledge Build | `the-knowledge-build.html` | The Knowledge Build \| Amanda Worsfold |
| Finally Build It | `finally-build-it.html` | Finally Build It \| Amanda Worsfold |

### Nav Structure
All pages share this nav (active page gets `class="active"`):
```
Services | Speaking | Case Studies | Build Lab | About | [Book a Call (CTA)]
```
Insights link is commented out. Mobile uses hamburger toggle.

### CSS Variables
```css
/* Colors */
--gold: #C9A227;  --gold-light: #D4B84A;  --gold-dark: #A68A1F;
--olive-dark: #3D4A2D;  --olive: #556B2F;  --olive-muted: #4A5540;
--gray-900: #111827;  --gray-800: #1F2937;  --gray-600: #4B5563;
--white: #FFFFFF;  --off-white: #FAFAFA;

/* Typography */
--font-display: 'Cormorant Garamond', Georgia, serif;  /* Headlines */
--font-body: 'Montserrat', -apple-system, sans-serif;   /* Body text */

/* Layout */
--container-max: 1200px;  --container-narrow: 800px;
```

### HTML Head Pattern (all pages)
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D3D4HLVZQN"></script>
<script>/* GA config */</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Page Title] | Amanda Worsfold</title>
<meta name="description" content="[page description]">
<!-- OG & Twitter Card tags -->
<link rel="canonical" href="https://amandaworsfold.com/[page]">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<link rel="icon" type="image/png" href="images/favicon.png">
```

## Deployment

### Process
1. Edit files locally
2. Run `python3 scripts/fact-check.py` to validate facts
3. Run `python3 scripts/check-events.py` to flag stale events
4. Commit and push to `main`
5. Netlify auto-deploys (build command runs fact-check + event-check)

### Netlify Config
- Build command: `python3 scripts/fact-check.py && python3 scripts/check-events.py`
- Publish directory: `.` (repo root)
- Domain: amandaworsfold.com

### Pre-Deploy Checklist
- [ ] Fact-check passes (`python3 scripts/fact-check.py`)
- [ ] Event check passes (`python3 scripts/check-events.py`)
- [ ] No broken internal links
- [ ] Mobile nav works
- [ ] All pages have OG tags and canonical URLs
- [ ] Brand voice is consistent (check `knowledge-base/VOICE-AND-MESSAGING.md`)

## Brand Rules

### Voice (from `knowledge-base/VOICE-AND-MESSAGING.md`)
- **Tone:** Confident but not arrogant, direct and practical, warm and approachable
- **Language:** Conversational, uses contractions, first/second person, short sentences
- **Avoid:** Jargon without explanation, buzzwords, corporate-speak, overpromising, "only" or "best" claims

### Anti-Patterns (never use)
- "revolutionize", "cutting-edge", "game-changing", "unlock the power"
- "AI transformation" without specifics
- Passive voice in CTAs
- "Schedule a consultation" (use "Book a call" instead)

### CTA Patterns
- Primary: "Book a Call" (link to /contact.html)
- Event: "Register Now", "Join the Waitlist"
- Tone: Low-pressure, conversational ("Let's have a conversation about what's possible")

### Pricing (enforced by fact-check.py)
| Service | Price |
|---------|-------|
| Good Morning Briefing | $2,500 |
| Brand Voice Writer | $5,000 |
| VIP Day | Custom |
| The Knowledge Build | $25,000 – $100,000+ |

## Kit Email Integration

### Embedded Forms
| Form | Kit Form ID | Page | Endpoint |
|------|------------|------|----------|
| Build Lab Registration | 9044261 | build-lab.html | `https://app.kit.com/forms/9044261/subscriptions` |
| Build Lab Waitlist | 9044478 | build-lab.html | `https://app.kit.com/forms/9044478/subscriptions` |
| Finally Build It Waitlist | 9051647 | finally-build-it.html | `https://app.kit.com/forms/9051647/subscriptions` |

### Embedding a Form on the Site
Forms are created in the Kit UI (app.kit.com → Landing Pages & Forms). To embed on the site:
```html
<form id="[slug]-form" class="[slug]-form" action="javascript:void(0);">
    <input type="email" placeholder="Your email" required>
    <button type="submit">Join the Waitlist</button>
</form>
<script>
document.getElementById('[slug]-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = this.querySelector('input[type="email"]').value;
    fetch('https://app.kit.com/forms/[KIT_FORM_ID]/subscriptions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'email_address=' + encodeURIComponent(email),
        mode: 'no-cors'
    }).then(() => { /* show success message */ });
});
</script>
```
After embedding, add the form to the table above and update `events.json` if event-related.

### Kit API (v4) — Full Reference

- **Base URL:** `https://api.kit.com/v4`
- **Auth:** `X-Kit-Api-Key: $KIT_API_KEY` header (key stored in `~/wit/.env`)
- **Content-Type:** `application/json` for POST/PUT requests
- **Pagination:** Cursor-based (`after`/`before` params, `per_page` default 500, max 1000)

**Load API key before any Kit call:**
```bash
KIT_API_KEY=$(grep KIT_API_KEY ~/wit/.env | cut -d= -f2)
```

#### Subscribers

| Action | Method | Endpoint | Body/Params |
|--------|--------|----------|-------------|
| List all | `GET` | `/v4/subscribers` | `?status=active&include_total_count=true` |
| Search by email | `GET` | `/v4/subscribers` | `?email_address=user@example.com` |
| Filter by date | `GET` | `/v4/subscribers` | `?created_after=2026-01-01&created_before=2026-02-01` |
| Get one | `GET` | `/v4/subscribers/{id}` | — |
| Create | `POST` | `/v4/subscribers` | `{"email_address":"...", "first_name":"...", "fields":{"Last name":"..."}}` |
| Update | `PUT` | `/v4/subscribers/{id}` | `{"email_address":"...", "first_name":"..."}` |
| Unsubscribe | `POST` | `/v4/subscribers/{id}/unsubscribe` | `{}` |
| List tags | `GET` | `/v4/subscribers/{id}/tags` | — |

Create returns 201 (new) or 200 (existing updated). Max 140 custom fields.

#### Forms

| Action | Method | Endpoint | Body/Params |
|--------|--------|----------|-------------|
| List all | `GET` | `/v4/forms` | `?status=active&type=embed` |
| List subscribers | `GET` | `/v4/forms/{form_id}/subscribers` | `?include_total_count=true&added_after=2026-01-01` |
| Add subscriber | `POST` | `/v4/forms/{form_id}/subscribers` | `{"email_address":"..."}` |

**Note:** Forms cannot be created via API — create them in Kit UI (app.kit.com → Landing Pages & Forms), then use the API to manage subscribers and embed on the site.

#### Tags

| Action | Method | Endpoint | Body/Params |
|--------|--------|----------|-------------|
| List all | `GET` | `/v4/tags` | — |
| Create | `POST` | `/v4/tags` | `{"name":"Tag Name"}` |
| Tag subscriber | `POST` | `/v4/tags/{tag_id}/subscribers` | `{"email_address":"..."}` |
| Remove tag | `DELETE` | `/v4/tags/{tag_id}/subscribers` | `{"email_address":"..."}` |
| List tagged subscribers | `GET` | `/v4/tags/{tag_id}/subscribers` | `?include_total_count=true` |

Create returns 201 (new) or 200 (tag already exists).

#### Broadcasts

| Action | Method | Endpoint | Body/Params |
|--------|--------|----------|-------------|
| List all | `GET` | `/v4/broadcasts` | — |
| Create draft | `POST` | `/v4/broadcasts` | See below |
| Get one | `GET` | `/v4/broadcasts/{id}` | — |
| Update | `PUT` | `/v4/broadcasts/{id}` | Same as create body |
| Delete | `DELETE` | `/v4/broadcasts/{id}` | — |
| Get stats | `GET` | `/v4/broadcasts/{id}/stats` | — |

**Create broadcast body:**
```json
{
  "subject": "Email subject",
  "content": "<p>HTML content</p>",
  "description": "Internal description",
  "public": true,
  "published_at": "2026-03-01T09:00:00Z",
  "preview_text": "Preview text",
  "send_at": "2026-03-01T14:00:00Z",
  "subscriber_filter": [{"all": [{"type": "tag", "tag_id": 123}]}]
}
```
Set `send_at` to `null` to save as draft without scheduling.

#### Example curl Commands
```bash
# Count active subscribers
curl -s -H "X-Kit-Api-Key: $KIT_API_KEY" \
  "https://api.kit.com/v4/subscribers?include_total_count=true&per_page=1" | python3 -c "import sys,json; print(json.load(sys.stdin).get('pagination',{}).get('total_count','?'))"

# Get Build Lab form signups
curl -s -H "X-Kit-Api-Key: $KIT_API_KEY" \
  "https://api.kit.com/v4/forms/9044261/subscribers?include_total_count=true&per_page=1"

# Create a subscriber and tag them
curl -X POST -H "X-Kit-Api-Key: $KIT_API_KEY" -H "Content-Type: application/json" \
  -d '{"email_address":"new@example.com","first_name":"Jane"}' \
  "https://api.kit.com/v4/subscribers"

# Create a new tag
curl -X POST -H "X-Kit-Api-Key: $KIT_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"March Build Lab"}' \
  "https://api.kit.com/v4/tags"
```

## Event Lifecycle

### Status Flow
`upcoming` → `active` → `past` → `archived`

### Rules
- **Recurring events** (e.g., Build Lab): When past, update dates for next session rather than archiving
- **One-time events** (e.g., Finally Build It): When past, archive the page (remove from nav, add "This event has passed" banner)
- **Stale threshold:** Events with dates >7 days past should be flagged
- **Event data:** Tracked in `events.json` at repo root

### Management
- Check `events.json` before deploying to catch stale pages
- `scripts/check-events.py` runs in the Netlify build and warns (but doesn't fail) on stale events

## Scripts Reference

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| `scripts/fact-check.py` | Validate HTML against `facts.json` | 0=pass, 1=issues found |
| `scripts/check-events.py` | Flag stale event pages from `events.json` | 0=pass, 1=stale events |
| `scripts/seo-audit.py` | Check meta tags, OG, canonical, alt text | 0=pass, 1=issues found |
| `scripts/brand-audit.py` | Check voice anti-patterns, pricing, structure | 0=pass, 1=issues found |
| `scripts/generate-sitemap.py` | Generate `sitemap.xml` from HTML files | 0=success |

## Knowledge Base

Reference docs in `knowledge-base/`:
- `COMPLETE-KNOWLEDGE-BASE.md` — Single-file overview of everything
- `VOICE-AND-MESSAGING.md` — Brand voice guide (use for content reviews)
- `SERVICES.md` — Full service catalog with pricing
- `POSITIONING.md` — Market positioning and differentiators
- `TARGET-AUDIENCE.md` — Audience personas and pain points
- `LLM-CONTEXT-PROMPT.md` — Context prompt for AI writing

## Key Facts (enforced by `facts.json`)

- Amanda has **one kid** and a **husband**
- Based in **San Francisco**
- **Stanford** Human-Centered AI **certificate** (not degree)
- **4x EBITDA** growth, **100% leadership approval**
- Contact: **amanda@amandaworsfold.com**
- Daily briefing delivered at **6am**
- Worked with **Fortune 500** companies
