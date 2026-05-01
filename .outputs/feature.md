*Feature Built — 2026-05-01 — aaronjmars/minitor*

GitHub releases column
Minitor — the dashboard-of-feeds with 30 column types — now has a per-repo release tracker. Operators can add a column like Stars or Forks but for releases instead, with a checkbox to include or exclude pre-releases. Until now you had to drop down to a generic RSS column on the repo's `releases.atom` feed, which lost tag and pre-release metadata and didn't get the per-source rendering treatment.

Why this matters:
Minitor already had 7 GitHub plugins (trending, issues, prs, stars, forks, search, backlinks). Releases was the obvious missing one — it's a top-3 monitoring need for any operator tracking dependencies, library upgrades, or competitor velocity. The README's GitHub row literally already said `(8)` but only listed 7 entries; the count was right for the planned set, wrong for the shipped set. The integration layer (`lib/integrations/github.ts`) had `fetchReleases` and a `'releases'` branch in `fetchGitHub` that no plugin was using — the plumbing was there, just no surface.

What was built:
- lib/columns/plugins/github-releases/plugin.ts: Zod config `{ repo, includePrereleases: boolean = true }`, Tag icon (lucide), green `#22c55e` accent — distinct from the orange flame on github-trending and yellow star on github-stars
- lib/columns/plugins/github-releases/server.ts: calls `fetchGitHub('releases', { repo }, PAGE_SIZE, page)`; pagination cursor uses upstream page size NOT post-filter size so the pre-release toggle doesn't stop pagination early on release-heavy repos
- lib/columns/plugins/github-releases/client.tsx: ConfigForm with repo input + prerelease checkbox; ItemRenderer shows release/pre-release pill, repo name, monospace tag, relative time, the title in serif (matching github-trending's heading treatment), and body line-clamp-3
- lib/columns/plugins/manifest.ts + registry.ts + server-registry.ts: the 3 standard registry edits (parity check at server module init throws if any drift)
- README.md: GitHub row entries 7 → 8, count `(8)` already correct

How it works:
The 3-file plugin contract (`plugin.ts` / `server.ts` / `client.tsx`) is the documented way to add a new column type. The plugin metadata declares the icon, Zod schema, accent color, and capabilities. The server fetcher is server-only and reuses the existing GitHub integration. The client renderer is `"use client"` and gets a typed `FeedItem<GHReleasesMeta>` so it doesn't need runtime type guards. The manifest is the canonical id list — both registries are validated against it at server module init. Pagination uses the same pattern as github-trending: when the upstream page is full (PAGE_SIZE items), advance regardless of how many items the local filter dropped.

What's next:
Natural follow-ups: a global "watchlist" column that aggregates releases across multiple watched repos, or a release-frequency badge in the renderer (e.g. "first release in 90 days"). Both would build on this plugin without changing the contract.

PR: https://github.com/aaronjmars/minitor/pull/23
