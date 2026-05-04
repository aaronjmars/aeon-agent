*Repo Action Ideas — 2026-05-04*
Generated from analysis of aaronjmars/aeon (270★, 41 forks), aaronjmars/aeon-agent (7★), aaronjmars/minitor (5★, 34 column types).

1. Star Momentum Alert (Growth, Small)
   Fires one targeted notification when the 300★ projection window lands 7–14 days out on a Tue–Thu — bridging show-hn-draft ready and operator-knows-when-to-dispatch.

2. RSS/Atom Feed Column for minitor (Integration, Small)
   Adds keyless RSS 2.0 / Atom 1.0 / JSON Feed support — covers every blog, newsletter, status page, and package changelog, the last universal monitoring primitive not yet in minitor's 34 column types.

3. skill-freshness Backport to aeon-agent (Feature, Small)
   Ships today's skill-freshness (aeon PR #157) to this fork — closes the silent-staleness gap where tweet-allocator could run successfully on week-old token-report data with no error signal.

4. pr-triage Backport to aeon-agent (DX/Community, Small)
   Backports the Apr-29 first-touch PR triage skill (aeon PR #147) — aeon-agent has no PR triage path at all; pure SKILL.md + state JSON, no workflows-scope PAT needed.

5. v4 Readiness Checker (DX/Community, Small)
   workflow_dispatch skill that reads the fork's aeon.yml + skills.json + MEMORY.md and generates a personalized upgrade checklist; v4 ~2 weeks out, 41 forks running on current architecture.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-04.md
