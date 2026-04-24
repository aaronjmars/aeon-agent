*Push Recap — 2026-04-24*
aaronjmars/aeon + aaronjmars/aeon-agent — 2 meaningful commits by @aaronjmars (squash-merged from autonomous PRs)

Heartbeat evolves in two directions simultaneously. PR #141 (aeon) turns heartbeat into a public broadcaster — every run now regenerates docs/status.md with a 🟢/🟡/🔴 verdict, per-skill table, and open-issues feed at aaronjmars.github.io/aeon/status/. Forks that enable Pages inherit the page for free. PR #18 (aeon-agent) goes the other way — once an issue has been escalated for 7+ consecutive days, the 48h re-notify cadence drops to every 7 days so operator-dependent issues stop pinging every-other-day indefinitely.

Heartbeat got louder externally and quieter internally in the same push window, both via pure skill-spec edits with zero net-new data sources or secrets.

Key changes:
- docs/status.md (new, +31) + skills/heartbeat/SKILL.md (+69/-1) — new Public status page section codifies 3 overall states (DEGRADED/WATCH/OK), the exact markdown template, and formatting rules; README gains a shields.io agent-status badge
- skills/heartbeat/SKILL.md in aeon-agent (+8/-3) — 3rd-tier escalation rule 'Extended-persistence backoff (7+ days)', plus new log marker 'Notification sent: no (7d extended-persistence backoff)' so future runs detect + respect the backoff
- PAT-workflows-scope issue (day 7) is the triggering case: today's heartbeat 20:00 UTC still fires on 48h cadence; next re-notify ~May 1 under the new rule

Stats: 5 files changed, +110/-4 lines across 2 meaningful commits (24 autonomous scheduler/cron commits excluded)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-24.md
