*Push Recap — 2026-05-10*
3 watched repos — 6 substantive commits / 4 merged PRs in the 24h window. All authored by @aaronjmars, all from agent-opened PRs.

*Closing the contributor flywheel (aeon)*: PR #163 lands `contributor-spotlight` — Sunday 20:00 UTC, exactly one hour after fork-cohort. Picks one POWER fork per week (ACTIVE fallback), reads its diverged work, writes a recognition paragraph. 4-week dedup so the spotlight rotates across the fleet. Operator-authored skills get a ★ marker. Closes the social loop yesterday's hyperstitions market opened.

*Drift detection becomes legible (aeon-agent)*: PR #34 backports skill-update-check from upstream. v1 was a flat catalog of SHAs; v2 is CRITICAL/HIGH/MEDIUM/LOW priority triage based on drift size × security verdict × enabled state, plus an ACCEPT mode for one-off lock advancement. Most-leveraged backport because every other drift on aeon-agent (80+ pre-autoresearch versions) becomes a triaged line item once this runs.

*Observability for the silent xAI clip (aeon-agent)*: PR #33 closes the May-6 fetch-tweets regression — emits a `::warning::` GitHub annotation when `output_tokens` lands within 5% of `max_output_tokens=16384`, breaking out reasoning vs visible tokens. Heartbeat picks up annotations. Five downstream skills (fetch-tweets, refresh-x, remix-tweets, tweet-roundup, narrative-tracker, article) protected.

*arXiv column lands and goes deeper (minitor)*: PR #31 ships the 38th plugin — keyless Atom-XML, 12 cs/stat/math.OC categories, revision badge for v2+. PR #32 is a 50-minute follow-up: `<arxiv:comment>` (~56% populated, contains "Accepted to ICML 2026" / code links / page count) is now extracted and rendered as a small italic line below the abstract.

Plus aeon-agent PR #35 closed the 22-day PAT-workflows-scope escalation thread — heartbeat will stop re-emitting weekly. Auto-Merge Agent PRs is genuinely unblocked.

Stats: 20 files changed, +1,195 / -110 lines.
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-10.md
