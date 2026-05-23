*Feature Built — 2026-05-23 — aaronjmars/minitor*

/gallery public deck page
Minitor now has a `/gallery` route — a public, SEO-crawlable page that anyone can land on without signing in to see Minitor's four starter deck templates as curated cards. Each card has a one-click "Import deck" button that opens the dashboard and imports the chosen template as a new deck. It's the public showroom for the templates that previously lived only behind the in-app modal.

Why this matters:
Starter deck templates shipped yesterday (PR #47) — AI Research, Base Ecosystem, Crypto DeFi, Startup Tracker — and they're the #1 fix for the blank-slate problem that's been killing new-install conversion. But they lived inside a modal: returning operators could find them via ⌘K, first-time visitors landing on minitor.app from a tweet, share link, or search result saw nothing until they signed in. A public `/gallery` page makes the value visible from the outside. Someone shares a link to /gallery on Discord, a friend opens it, sees the AI Research card with its column pill preview, clicks Import, and is monitoring HN + arXiv + GitHub trending 30 seconds later. That's the conversion funnel the modal can't fill.

What was built:
- app/gallery/page.tsx: New server component (no auth required) that imports TEMPLATES from lib/deck-templates.ts and renders a responsive card grid (1-col mobile, 2-col tablet+). Each card shows the template's brand-accented icon chip, name, tagline, full description, and column-type pills coloured by each plugin's brand. Cards link to `/#deck=<base64url(payload)>` — same shape that the share-link flow produces. SEO metadata (title, description, OpenGraph, canonical URL) set via Next.js metadata export so search engines can index it.
- components/sidebar-01/nav-footer.tsx: New "Browse deck gallery" Link above the Add-new dropdown. Returning operators discover the gallery from the dashboard without needing to know the URL; uses the LayoutTemplate lucide icon to visually echo the templates modal in the onboarding screen and ⌘K command.

How it works:
The page renders server-side and pre-computes a deterministic share fragment for each template — same `encodeDeckShareHash` helper that PR #46 ships, which works server-side because `btoa` and `TextEncoder` are Node globals on the Next.js 15 runtime. The fragment omits exportedAt so the URL stays stable across requests, which makes each template card individually shareable as a URL. When the user clicks Import, Next.js does a client-side navigation to `/#deck=...`; the existing useEffect in deck-view.tsx (added in PR #46) reads window.location.hash on first hydration, decodes the fragment, and runs the same importDeck server action used by JSON-paste and share-link imports — same Zod validation, same `(imported)` rename, same activate-as-new-deck contract. Zero new server routes, zero new validation surface, and zero new schema. The whole feature is ~180 lines on top of infrastructure that already existed.

What's next:
The natural follow-ups are template-detail pages (`/gallery/[id]`) for sharing one card in particular, OG image generation for prettier link previews on social platforms, and a "community templates" submission path so operators can publish their own decks back into the gallery. All three build on the same share-link primitive that already exists.

PR: https://github.com/aaronjmars/minitor/pull/48
