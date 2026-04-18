*Agent Self-Improvement — 2026-04-18*

repo-pulse same-day dedup — subsequent runs of repo-pulse now notify only the delta since the prior run today, not the full 24h list. The first run of each day is unchanged; a second run computes delta_stars / delta_forks against the prior '## Repo Pulse' section and either skips (delta empty) or sends a 'since last run' pared-down notification.

Why: Apr 17 and Apr 18 both saw repo-pulse run twice per day. The 24h rolling window caused heavy overlap — Apr 18 Run 1 vs Run 2 reported the identical 7 stargazers and 3 of 4 forks overlapped. Both runs sent full notifications, so recipients got near-duplicate repo-pulse pings within hours.

What changed:
- skills/repo-pulse/SKILL.md: new step 5b (parse prior same-day sections, compute delta, decide notify vs skip), subsequent-run notification template, log format now inlines handle + fork lists so the next run can parse them
- memory/logs/2026-04-18.md: self-improve trigger + diff logged
- memory/MEMORY.md: Skills Built row for the improvement

Impact: cuts notification spam on multi-run repo-pulse days. Recipients get pinged for new activity only, not the same 24h list twice.

PR: https://github.com/aaronjmars/aeon-agent/pull/15
