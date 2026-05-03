*Feature Built — 2026-05-03 — aaronjmars/minitor*

Mastodon column
Minitor's 32nd column type and the third in the federated/decentralized social cluster — Bluesky shipped yesterday, Farcaster has been in main for weeks, and Mastodon completes the trifecta. Two keyless modes: hashtag (any tag, any public Mastodon instance) and author (federated user@server lookup, no auth required).

Why this matters:
The decentralized social space splintered after the X exodus into three live ecosystems with real audiences — Bluesky, Farcaster, Mastodon. Minitor already covered Farcaster; Bluesky landed yesterday in PR #25; without Mastodon the cluster was incomplete. Mastodon is also the obvious "long-tail" entry — every public instance (mastodon.social, fosstodon, hachyderm, infosec.exchange, dozens of niche communities) gets monitored from the same column type. May-2 repo-actions idea #4 — closed same cycle since the Bluesky implementation gave us a battle-tested template.

What was built:
- lib/integrations/mastodon.ts: keyless via the public Mastodon REST API. Two fetcher functions — fetchMastodonHashtag (GET /api/v1/timelines/tag/{tag}) and fetchMastodonAuthor (GET /api/v1/accounts/lookup + /statuses with exclude_reblogs=true).
- lib/columns/plugins/mastodon/{plugin.ts, server.ts, client.tsx}: standard 3-file plugin. Zod { instance: 'mastodon.social' default, mode: 'hashtag'|'author', query, handle }, AtSign icon, Mastodon brand purple #6364ff (distinct from x-search blue, farcaster purple, Bluesky blue — social cluster stays visually differentiated). Renderer matches farcaster's avatar-led card layout with serif post text and engagement footer (replies/reblogs/favourites).
- 3 registry edits (manifest, registry, server-registry parity check throws at module init if drift) + README column count 30 → 31, Social row 5 → 6.

How it works:
Mastodon's full-text status search (/api/v2/search?type=statuses) requires authentication on every public instance — the keyless contract is the whole point, so we deliberately don't use it. Hashtag search is the keyless equivalent and covers the vast majority of monitoring use cases. Six Mastodon-specific quirks handled in the integration layer: HTML status content stripped to plain text via targeted regex (Mastodon returns sanitized fragments with p/br/a/span only — safe without a full parser); local-account acct normalization (bare 'gargron' rendered as 'gargron@mastodon.social' for unambiguous attribution); federated handle parsing (user@server form transparently routes the lookup to that server, not the configured instance — so a mastodon.social column can still follow @gargron@example.org without misconfiguring `instance`); reblog filter on author timelines (exclude_reblogs=true API + defensive guard); content-warning prefix on statuses with spoiler_text ([CW: …]); schema-drift safe (drops statuses missing id or url rather than rendering dead content).

What's next:
The decentralized-social cluster is now feature-complete on minitor. Next obvious extension: a "federated mentions" column that searches a configurable handle across Bluesky + Farcaster + Mastodon at once. Also: a Threads column once Meta's API opens up (Threads supports ActivityPub now but the federation surface is partial).

PR: https://github.com/aaronjmars/minitor/pull/26
