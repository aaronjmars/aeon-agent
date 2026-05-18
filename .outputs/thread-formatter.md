*Thread Draft — 2026-05-18*
Topic: github-discussions column — 45th Minitor column type, completes GitHub cluster, PR #43

1/ Minitor's GitHub cluster is now complete. 45th column type: GitHub Discussions. Stars, forks, PRs, issues, releases, backlinks, search, trending, CI — that's the full GitHub surface in one dashboard. Discussions was the last gap.

2/ GitHub is pushing Discussions as its default async Q&A layer across repos. Nine column types already covered the GitHub surface — stars, forks, PRs, issues, releases, search, backlinks, trending, Actions. No way to see unanswered community questions without leaving the dashboard.

3/ GitHub Discussions aren't in the REST API — GraphQL only. The column queries the endpoint with an optional token (60 req/hr keyless, 5,000 with auth). Three modes: recent, unanswered, top by upvotes. Repos with Discussions disabled get a clean empty state instead of a crash.

4/ The GitHub cluster in Minitor now covers the full repo lifecycle: stars, forks, PRs, issues, releases, CI status, backlinks, trending — and the async layer where the community actually talks. Minitor started at 1 column type. It's at 45 now.

5/ PR #43 — 45th column type for Minitor, GitHub Discussions: https://github.com/aaronjmars/minitor/pull/43

(article: articles/thread-2026-05-18.md)
