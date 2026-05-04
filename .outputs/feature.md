*Feature Built — 2026-05-04 — aaronjmars/minitor*

Lobsters Column
Minitor now has a Lobsters column — the 34th column type. Lobsters is a tech-focused community of about 30,000 engineers running on lobste.rs, adjacent to Hacker News in audience but with narrower, higher-signal submissions and a tag taxonomy that makes it a great fit for filtered feeds (rust, ai, programming, security, ...). Four modes — Hottest, Newest, Active discussions, and Tag (single tag, or comma-separated multi-tag like rust,go).

Why this matters:
HN was the only general-tech discussion column in minitor before today. Anyone running a founder dashboard, an open-source maintainer dashboard, or an ML-research dashboard tends to read both Hacker News and Lobsters — being able to stack the two next to each other on the same deck is the natural layout. Lobsters' tag system also makes it a particularly good companion: where HN is one undifferentiated firehose, a Lobsters column can be scoped to t/rust or t/security and stay on-topic.

What was built:
- lib/integrations/lobsters.ts: keyless JSON fetcher for the four modes. Schema-drift-safe story mapper drops rows missing short_id or title rather than rendering dead content. HTML strip handles the description field (Lobsters returns sanitised fragments — p/br/code/em/a only — so a targeted regex strip is safe without pulling in a full parser; falls back to description_plain if upstream sends it).
- lib/columns/plugins/lobsters/{plugin,client,server}.ts: standard 3-file plugin. Anchor icon (a nod to the lobster claw without copying the proprietary logo). Brand red #ac130d (lobster-claw red on lobste.rs/about — distinct from HN's orange #ff6600 so the two news-source columns stay visually differentiated when stacked together). Tag pills under the snippet for the first 4 tags (HN's renderer doesn't have this since HN has no tags).
- lib/columns/plugins/manifest.ts + registry.ts + server-registry.ts: three registry edits per the README contract; the parity check at server module init throws if any registry drifts.
- README.md: column count 33 → 34, News & Web row 4 → 5, hero paragraph picks up Lobsters alongside Hacker News.

How it works:
Lobsters exposes JSON variants of every public page — /hottest, /newest, /active, and per-tag /t/<tag> all return the same story array via .json. No auth, no token. Pagination flows through /page/N/{mode}.json (page 1 is the bare root, no /page/1/ segment — handled in endpointFor). Three Lobsters-specific quirks were handled in the integration: submitter_user can be either a bare string username or an object with .username (unwrapAuthor handles both); tag mode with empty tag falls back to hottest in server.ts to avoid a 404 on /t/.json so the column always renders; hasMore detection uses upstream page size (>=25) NOT the post-filter slice, so the visible PAGE_SIZE clamp doesn't stop pagination early on full pages. A user-agent header identifies minitor — Lobsters' admins ask scrapers to identify themselves so they can throttle cooperatively if needed.

What's next:
The keyless news/discussion cluster gets fuller — HN, RSS, Google News, Bing, and now Lobsters. Natural follow-on: a Lemmy column (federated Reddit alternative, also keyless) would round out the decentralised social pattern that Bluesky + Mastodon + Farcaster started.

PR: https://github.com/aaronjmars/minitor/pull/27
