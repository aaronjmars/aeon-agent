*Feature Built — 2026-05-21 — aaronjmars/minitor*

Deck share link
Adds a third primitive to the deck-portability set: alongside Export (copy JSON, May-15) and Import (paste JSON modal, May-15), the operator can now copy a self-contained URL that anyone can open to auto-import the deck. No new server route, no new auth, no persistence — the deck JSON is base64url-encoded into the URL fragment, the receiver decodes it client-side on first paint, and the hash is stripped via history.replaceState so refreshes don't double-import.

Why this matters:
minitor sits at 9⭐ / 0 forks today. The deck export/import primitive made decks portable but JSON copy-paste is not a viral loop. A share URL is — the operator tweets "my AI research dashboard" → link → one click → live dashboard. Picked from articles/repo-actions-2026-05-20.md idea #4. Pairs cleanly with the planned Starter Deck Templates Gallery (May-20 idea #5) — once that ships, each template is just a pre-baked share link, no new schema or API surface needed.

What was built:
- lib/deck-share.ts (new, 95 lines): four pure functions — `encodeDeckShareHash`, `decodeDeckShareHash`, `readDeckShareFragment`, `buildDeckShareUrl`. UTF-8-safe via TextEncoder (raw btoa mishandles non-ASCII column titles/configs). 32 KB hard cap on the encoded payload — guards against 64-column pathological decks blowing past browser URL limits. Fragment parser tolerates extra `&`-separated params (campaign taggers, utm IDs) so it doesn't crash on appended keys.
- components/sidebar-01/nav-header.tsx: new Share2-icon ⌘K command "Share current deck (copy URL)", sibling to Export. Reuses the existing copyToClipboard helper (navigator.clipboard with execCommand fallback for permission-blocked browsers, console.log as last resort).
- components/deck/deck-view.tsx: new useEffect gated on `hydrated` reads window.location.hash once after first hydration, decodes the #deck=... fragment, runs it through the existing importDeck server action (same Zod validation, same `(imported)` rename, same activate), toasts the result, and clears the hash via history.replaceState. Malformed payloads toast an error AND still clear the hash so the user isn't trapped.

How it works:
The deck is encoded by feeding the existing exportDeck JSON output through TextEncoder → btoa → base64url-replace, then concatenated as `${origin}${pathname}#deck=${encoded}`. The receiver's deck-view useEffect — running once `hydrated` flips true (after loadSnapshot completes) — does the inverse: pulls the fragment, base64url-pads, atob, TextDecoder with `fatal:true` so corrupt UTF-8 fails closed. The decoded JSON hits the same importDeck server action that powers manual paste-import (same Zod schema, same `(imported)` rename, same activate-as-new-deck behaviour) — so the share path is forward-compatible with every future schema field including the alertKeywords from May-14 PR #41, which round-trips automatically. No new dependencies (lucide-react already includes Share2).

What's next:
Starter Deck Templates Gallery (May-20 idea #5) is the obvious follow-up — write 4-5 static template JSON files (AI Research, Base Ecosystem, Crypto DeFi, Startup Tracker), surface them as a first-launch overlay with "Use this deck" → share-link import. Zero new schema, zero new API.

PR: https://github.com/aaronjmars/minitor/pull/46
