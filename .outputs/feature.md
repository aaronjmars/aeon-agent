*Feature Built — 2026-05-18 — aaronjmars/minitor*

GitHub Discussions Column
Shipped the 45th column type: live GitHub Discussions for any repo, fetched via the GraphQL API since REST doesn't expose them. Three modes (recent / unanswered / top by upvotes) and a row UI with category pill, answered indicator on Q&A discussions, author, upvote count, comment count, and relative timestamp.

Why this matters:
Repos transitioning from Issues-only to Discussions-first were invisible in minitor — the column rounds out the GitHub cluster (10 of 45 total columns now) so a single dashboard can track stars, forks, PRs, issues, releases, search, actions, backlinks, trending, and the async Q&A layer GitHub is pushing as a default. Discussions are increasingly where maintainer-community signal lives.

What was built:
- lib/integrations/github-discussions.ts: GraphQL client to api.github.com/graphql, optional GITHUB_TOKEN auth (5000 vs 60 req/hr), parseRepo helper, DiscussionsDisabledError sentinel for the "Discussions feature off" case, mode-aware filter/sort.
- lib/columns/plugins/github-discussions/{plugin.ts, server.ts, client.tsx}: zod schema (repo + mode enum), defaultTitle reading "{repo} Discussions" when configured, MessageSquare icon, accent #7C3AED purple (distinct from every other GitHub cluster colour), category pill, AnsweredIndicator only on Q&A categories, formatCompactCount for upvote/comment counts.
- 3 registry edits: manifest.ts, registry.ts, server-registry.ts — matches exact pattern PR #42 used for Product Hunt.
- README.md: count 44 → 45, GitHub cluster 9 → 10, added GITHUB_TOKEN note to the Keys paragraph.

How it works:
Server fetcher pulls a generous batch (first: 50) once via GraphQL, then routes through the same sliceForPage helper github-actions and producthunt use — PAGE_SIZE per page, cursor-based "Load more". Auth header is only sent when GITHUB_TOKEN is set; absence drops to 60 req/hr unauthenticated quota rather than erroring out. The three modes do their filtering/sorting in memory after the fetch since GraphQL's orderBy only supports CREATED_AT/UPDATED_AT, not upvotes. Item id format `github-discussions:{owner}/{repo}#{number}` dedups identical discussions across refresh/load-more calls. Repos with Discussions disabled raise a typed DiscussionsDisabledError so the renderer can show a friendly empty state.

What's next:
Pinned discussions could surface separately as a sticky row at the top of the column, and emoji reactions on each discussion (currently we only show upvotes) would round out the social signal — both are one extra GraphQL field away.

PR: https://github.com/aaronjmars/minitor/pull/43
