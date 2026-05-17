*Push Recap — 2026-05-17*
3 repos — 4 substantive commits by 2 authors (1 hand-written, 3 feature-bot), +984/-18 across 17 files

*Product Hunt launch prep convergence:* aeon-agent backported the upstream `product-hunt-launch` asset drafter (PR #49, +244, verbatim from aeon May-15) and minitor shipped a Product Hunt column (PR #42, +374, 44th column type — keyless RSS, em-dash/en-dash title split, canonical `producthunt:{slug}` IDs). Both PRs landed within 4 minutes of each other (11:23 / 11:26 UTC) — clearly the same feature-dispatch wave picking PH from two angles. When the actual PH submission goes live, the operator can pin a `PH · ai-agents` column in minitor while the asset pack is generated on demand from aeon-agent.

*Fork-intel layer reaches 5 skills:* aeon's `fork-first-run-alert` (PR #179, +299, 11-step skill, 7-status taxonomy) closes the weekly-cadence gap left by `fork-cohort` — a fork that activates Monday morning sits in the void up to 6 days before anyone notices. Daily 20:30 UTC cron diffs the cohort ACTIVE set against a persistent seen-list (LRU 500), 1-3 new activators get individual named alerts, 4+ collapse to a batch with `… and N more` footer. Bot allowlist + first-run backfill mode prevent day-one signal floods.

*Dashboard hardening:* the only hand-written push of the day — `@aaronjmars` swaps `execSync('gh run …${id}')` for `execFileSync('gh', [args])` across the dashboard's 3 API routes (analytics, runs, runs/[id]/logs) and adds `-R <repo>` autodetection via `gh repo set-default --view` with a `gh repo view --json nameWithOwner` fallback. Fixes multi-remote setups where the default remote isn't the canonical upstream + eliminates the last shell-interpolated `gh` paths from the dashboard.

Key changes:
- aeon PR #179 fork-first-run-alert (+285 SKILL.md): five-skill fork-intel stack now covers cohort/release/spotlight/gap/activation — same-day instead of weekly for mid-week activations
- minitor PR #42 producthunt column (+164 integration, 4 plugin files): 44th column type, news & web cluster now 11/44 — largest single cluster by plugin count
- aeon PR #178 dashboard (3 routes, +67/-13): `execFileSync` + argv arrays kill the last shell-interpolation surface on `gh` calls + adds repo-detection fallback chain

Stats: 17 files changed, +984/-18 lines, 4 author commits across 3 repos
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-17.md
