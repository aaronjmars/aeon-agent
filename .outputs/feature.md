*Feature Built — 2026-06-12 — aaronjmars/minitor*

Fixed a broken production build on minitor's main branch
minitor's `main` branch does not currently compile — `next build` fails with 62 errors. Every build and deploy is blocked until it's fixed. This PR finds the single root cause and unblocks the whole app.

Why this matters:
A dead build stops every contributor and any deploy of the dashboard. The break is subtle: `app/actions.ts` is a Next.js `"use server"` module, and those are only allowed to export async functions — but it also exported six plain constants and helper functions (refresh-interval rules, the tab-group cap, the color-hex validator, the deck export version). Turbopack rejects them, the module fails to load, and 62 cascading "module has no exports" errors take down the build. `tsc` doesn't check this rule, so it passed typecheck and slipped onto a green-looking main.

What was built:
- lib/deck-rules.ts (new): a plain shared module holding the deck/column validation rules — refresh-interval allowlist, TAB_GROUP_MAX, the hex-color regex + normalizer, and the deck export version. Moved verbatim, no behavior change.
- app/actions.ts: removed those six non-async exports and imports them back from the new module. It now exports only Server Actions, which is what "use server" requires.
- lib/store/use-deck-store.ts: the client store now imports those constants/validators from the plain module instead of across the server boundary — getting the real synchronous values it always used them as.

How it works:
The fix separates "server actions" from "shared rules". A `"use server"` file becomes an RPC surface where every export is callable from the client as an async server function — so non-function exports are illegal. By hoisting the constants and sync validators into an ordinary module, both the server actions and the client store import them as plain values, and `actions.ts` is left as a clean action-only surface. Existing duplicate copies of these constants in two dialog components were left untouched to keep the diff minimal and focused on the build fix.

Verification: `next build` now compiles and generates all 7 routes; `tsc --noEmit` and eslint both clean.

What's next:
Once this merges and main builds again, a ready follow-up is queued: a keyless Dexscreener column plugin (on-chain DEX pair search + contract watchlist) — built and passing typecheck/lint, held back so this critical fix lands on its own.

PR: https://github.com/aaronjmars/minitor/pull/71
