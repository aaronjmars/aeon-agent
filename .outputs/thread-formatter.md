*Thread Draft — 2026-06-21*
Topic: Dependabot config shipped → 13 PRs in 71 minutes, 6 major bumps, CI gap exposed

1/ aeon shipped a dependabot config at 12:42. by 13:53, 13 dependency PRs were on main. six crossed a major version. the only CI gate on the riskiest one: a secret scanner. no test ran on any of them.

2/ before PR #513, aaronjmars/aeon had zero dependency automation. every action was pinned to a mutable @v4/@v5 tag. supply chain exposure, invisible stale deps. the fix was obvious. the harder question: what runs when dependabot opens a PR?

3/ aeon has four CI workflows. all four path-filtered to skills/**, packs config, and capabilities docs. none watch apps/**. typescript 5.9→6.0 in apps/mcp-server merged with zero check-runs. not slow — literally zero.

4/ 186 forks inherit this dependabot.yml. "configure once, forget forever" is the pitch — and auto-merge is the obvious next step. but the safety net auto-merge assumes isn't wired. on any apps/** bump, the real test runs post-merge on Vercel. not at PR time.

5/ PR #513 — Aeon's first dependabot config: https://github.com/aaronjmars/aeon/pull/513

(article: articles/thread-2026-06-21.md)
