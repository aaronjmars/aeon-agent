*Feature Built — 2026-05-02 — aaronjmars/minitor*

Bluesky column type
Minitor just got a Bluesky column. Two modes: search by keyword (latest posts, sorted newest first) and follow a single author by handle. It's keyless — no API key, no env var, no signup. The column works the moment you add it.

Why this matters:
Minitor leads with a "first column up in under a minute, zero infra" promise, and the founder-dashboard, journalist, and OSS-maintainer use cases in the README all benefit from cross-platform monitoring. Bluesky has captured a meaningful share of the X-exodus crowd over the past year — and the public AppView at public.api.bsky.app is keyless and well-documented, so adding it preserves the zero-config promise. The Social cluster grows from 5 plugins (x-search, x-trending, reddit, hacker-news, farcaster) to 6, and minitor's total column count goes from 30 to 31.

What was built:
- lib/integrations/bluesky.ts: keyless integration for app.bsky.feed.searchPosts and app.bsky.feed.getAuthorFeed; handles three Bluesky-specific quirks — at:// URI to bsky.app permalink conversion via small regex with raw-URI fallback for schema drift, handle normalization (bare "jay" resolves to "jay.bsky.social", "@user.com" strips the leading @, custom domains pass through unchanged), and a repost filter on author feeds because Bluesky's filter=posts_no_replies removes replies but keeps reposts which would break the "by @author" attribution; schema-drift safe (drops posts missing handle or uri rather than rendering dead content).
- lib/columns/plugins/bluesky/plugin.ts: Zod schema { mode: "search"|"author", query, handle }, Cloud icon, Bluesky brand blue #0085ff accent (distinct from x-search's #1d9bf0 so the social cluster stays visually differentiated), paginated capability.
- lib/columns/plugins/bluesky/server.ts: typed fetcher passing PAGE_SIZE through with cursor-based pagination.
- lib/columns/plugins/bluesky/client.tsx: ConfigForm with mode select + mode-conditional input (query field for search, handle field for author with the bare-username hint inline); ItemRenderer matches farcaster's avatar-led card layout with serif post text and engagement footer (replies / reposts / likes — quote-counts collapsed into reposts since Bluesky exposes them separately but readers consume them as the same primitive).
- README.md: column count 30 → 31, Social row 5 → 6 entries, description list adds Bluesky between X and Reddit.

How it works:
Standard 3-file plugin (plugin.ts + server.ts + client.tsx) plus the 3 registry edits — manifest.ts, registry.ts, server-registry.ts. The parity check at server module init throws loudly if any of the three drift, so out-of-sync registries fail at boot rather than 404 at request time. Cursor pagination flows through unchanged: Bluesky returns an opaque cursor field that we pass straight to the next call. No new env vars, no new build dependencies, no schema migration.

What's next:
Two natural follow-ups when demand surfaces — feed-level keyword filtering (Bluesky supports starter packs and labelled feeds, both keyless) and a NewsNow-style "trending posts on Bluesky right now" feed if/when Bluesky publishes a public trending endpoint.

PR: https://github.com/aaronjmars/minitor/pull/25
