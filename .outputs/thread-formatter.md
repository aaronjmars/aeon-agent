*Thread Draft — 2026-05-31*
Topic: upstream-gap — the fork's first original skill in the 17-day backport chain (aeon-agent PR #72)

1/ For seventeen days the aeon-agent fork shipped the previous day's upstream PR without a miss. Today it shipped something upstream doesn't have: a weekly diff of the gap it still hasn't closed.

2/ The fork has 95 skills. Upstream has 160. The 65-skill gap is mostly spring autoresearch rewrites the fork has known about and deferred since launch. The backport chain was the only signal that the gap was still closing.

3/ upstream-gap diffs local skills/ against upstream aaronjmars/aeon weekly. Missing slugs get a merge date from upstream's commit history, sticky in state so the API cost is bounded. Days pending are computed from the upstream merge, not from when the fork first noticed.

4/ The 80 deferred autoresearch rewrites from aeon PRs #46–#136 will surface as a 60-row URGENT block on first run. The fork has known they exist for months. Now there's a number on the terminal once a week until they're done.

5/ The fork built one original feature in seventeen days. It picked the one that guarantees the next seventeen look the same. https://github.com/aaronjmars/aeon-agent/pull/72

(article: articles/thread-2026-05-31.md)
