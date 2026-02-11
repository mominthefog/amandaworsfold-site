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

### Kit API (v4)
- **Base URL:** `https://api.kit.com/v4/`
- **Auth:** Bearer token from `KIT_API_KEY` in `~/wit/.env`
- **Key Endpoints:**
  - `GET /subscribers` — list subscribers
  - `GET /subscribers?filter[tag]=TAG_ID` — filter by tag
  - `GET /forms` — list forms
  - `GET /forms/{id}/subscriptions` — form subscribers
  - `GET /tags` — list tags
  - `POST /tags/{id}/subscribers` — tag a subscriber
  - `GET /broadcasts` — list broadcasts
- **Usage:** `curl -H "Authorization: Bearer $KIT_API_KEY" https://api.kit.com/v4/subscribers`

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
