*Push Recap — 2026-05-04*
Three substantive PRs across watched repos, all merged 12:53 UTC by aaronjmars in a single coordinated wave (one per repo), plus ~38 routine cron auto-commits on aeon-agent. The shape is the inverse of yesterday — yesterday cleared a backlog in a 16-minute merge train; today shipped one purpose-built fix per repo.

Silent-staleness watchdog (aeon #157): New skill-freshness — daily 08:00 UTC sonnet skill that walks every enabled skill in aeon.yml, parses explicit chains: consume: edges + implicit articles/.outputs/topics/state references in each SKILL.md, checks file mtimes against per-class thresholds derived from each producer's cron (daily 28h / weekly 192h / .outputs 4h / topics 7d / state 30d), and flags consumers about to read stale upstream files. Closes the gap heartbeat + skill-analytics + skill-health all miss — a chained skill that runs on schedule with no API errors and 100% pass rate can still silently consume yesterday's output. Fingerprint dedup with 7-day re-emit. Pure local file I/O. Closes Apr-30 idea #4 / May-2 idea #2 (carried 2 cycles).

Operator scorecard backport (aeon-agent #28): Yesterday's aeon PR #153 lands here unchanged — weekly Monday 10:30 UTC three-paragraph synthesis (agent health / community growth / economic activity), worst-of-three rollup with INSUFFICIENT_DATA degrading to WATCH not DEGRADED so partial-data weeks still flag. Selected for fast-track backport because it has zero upstream-PR-#46-to-#136 dependencies — pure articles/+memory/ reads. First non-trivial backport this week from aeon → aeon-agent ahead of the 80-PR autoresearch-evolution queue (day 13).

34th column type (minitor #27): lobsters plugin — keyless integration via .json variants of every public Lobsters page, four modes (hottest / newest / active / tag with comma-multi-tag like /t/rust,go.json), cursor-paginated with the page-1-is-bare-root quirk handled. Brand red #ac130d, Anchor icon, tag pills under snippet (HN doesn't have these — Lobsters' tag taxonomy is core to the signal). Closes the obvious News & Web gap — HN was the only general-tech discussion column.

Key changes:
- skills/skill-freshness/SKILL.md (+286): per-class freshness thresholds derived at runtime from producer cadence, severity bands OK/WARN/STALE/MISSING, fingerprint-based dedup
- skills/operator-scorecard/SKILL.md (+257): backported verbatim, slots between weekly-review and repo-scanner in productivity cluster
- lib/integrations/lobsters.ts (+159): three Lobsters quirks handled — submitter_user dual shape (string | {username}), HTML description regex strip, hasMore via upstream page size not post-filter slice

Stats: 12 files changed, +971/-4 lines across 3 substantive commits (plus ~38 aeon-agent cron auto-commits).
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-04.md
