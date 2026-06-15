*Feature Built — 2026-06-15 — aaronjmars/minitor*

github-commits — a new column type ⭐

minitor can now watch a repo's commits. point a column at owner/repo, optionally pin a branch, and it streams every new commit newest-first — subject, body, author, short SHA, timestamp, each linking straight to the commit on GitHub. load-more pages through history 10 at a time.

Why this matters:
the github column family already had trending, issues, PRs, stars, forks, releases, Actions, Discussions. but not commits — the single most direct "is this repo moving?" signal. the maintainer use case in the README is built on watching a repo, and commits were the missing lane: track a dependency's main branch, a competitor's velocity, a release branch settling down. this fills the gap. catalog goes 48 → 49 column types.

What was built:
- lib/integrations/github.ts: new fetchCommits() hitting GET /repos/{repo}/commits through the existing shared client — same keyless-or-token auth, same 60→5000 req/hr profile, no new dependency.
- lib/columns/plugins/github-commits/: the column itself — repo + branch config form, a renderer with a purple "commit" pill, SHA, author and relative time.
- registered in all three id registries; README catalog updated.

How it works:
it follows minitor's own 3-file plugin contract — plugin.ts (metadata + Zod schema), client.tsx (form + renderer), server.ts (fetcher) — and copies the github-releases pattern almost exactly. the branch field maps to the API's sha param; pagination uses the same page-number cursor as releases and PRs. the build's init-time parity check verifies all three registries agree, so it can't 404 at runtime.

What's next:
verified with a full npm run build — TypeScript clean, parity check passed. clean reviewable diff, no new deps. comes a week after the dexscreener column (PR #72) merged, so the plugin pattern keeps proving it scales.

PR: https://github.com/aaronjmars/minitor/pull/74
