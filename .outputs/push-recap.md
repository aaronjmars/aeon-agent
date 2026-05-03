*Push Recap — 2026-05-03*
14 substantive commits across aeon / aeon-agent / minitor, all merged in a single 16-min train at ~13:20 UTC. Yesterday's open-PR pile from the per-repo factory's first sweep cleared in one go.

Three new aeon skills (all enabled: false): show-hn-draft (Show HN launch post pre-writer, workflow_dispatch), operator-scorecard (weekly "was this week worth it?" synthesis), fork-cohort (weekly fork activation-stage tracker). Closes 3 multi-cycle highest-priority ideas.

Two follow-up housekeeping commits caught skills.json metadata drift the merge wave surfaced — 97 → 108 total + 5 orphan skills mapped out of "other".

aeon-agent ships scripts/cron-state (local viewer for the scheduler's per-skill state, --unhealthy/--stale exit codes for health checks), scripts/skill-runs gains --skill filter + --duration mode (closes the slow-rot anomaly bucket the existing flags miss), self-improve PR-filter sleeper bug fixed, prefetch-bankr gets the .error marker pattern (last script without one).

minitor ships three column types in the same wave: github-releases (8th GitHub plugin, fills count claim that's been wrong since launch), bluesky (keyless via public AppView), mastodon (keyless hashtag + federated author). Decentralized-social trifecta complete (Farcaster + Bluesky + Mastodon). Column count 30 → 32.

External: tomscaria PR #150 closes shell-injection in dashboard secrets API (execFileSync swap, +3/-3).

Stats: 38 files, +2,657/-279 lines.
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-03.md
