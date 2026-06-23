*Feature Built — 2026-06-23 — aaronjmars/minitor* ⭐

Input validation across four more columns
linkedin, bluesky, mastodon, youtube took your search term and handed it straight to the upstream API — no check. Type nothing, hit a wasted Grok call or a broken AppView/Mastodon/YouTube fetch, and get back a cryptic error with no hint that you forgot the input. This PR makes them fail clean instead.

Why this matters:
PR #78 fixed exactly this last week — but only for the five Grok search columns. These four slipped through. farcaster and every github-* column already trim-and-throw on their required input; now the social/search columns match. Consistency is the point: a column that needs a query should say so, not waste an API call to find out.

What was built:
- `linkedin/server.ts`: throws on empty query (Grok-backed, one required input), forwards the trimmed value.
- `bluesky/server.ts` + `mastodon/server.ts`: throw on empty query in search/hashtag mode, empty handle in author mode.
- `youtube/server.ts`: throws on empty query/channel/playlist for whichever mode is active.

How it works:
Guard-only — an early `throw new Error("… is required.")` before any network call, matching the existing farcaster pattern exactly. The values passed downstream are unchanged (linkedin aside, which now trims like its siblings). Each moded column guards per-mode, so author/channel/playlist inputs get the same treatment as the keyword path. Zero behavior change for valid inputs.

What's next:
Closes the column-validation parity gap. The remaining minitor hardening — a build-time CI gate on `lib/columns/plugins/**` so TS errors surface before Vercel deploy — needs a workflows-scoped token, so it stays queued.

PR: https://github.com/aaronjmars/minitor/pull/79
