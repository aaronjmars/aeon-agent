All three notifications staged for post-run delivery. Task done.

## Summary

Built one feature per watched repo, opened a PR on each, and queued a detailed Telegram notification for each one. All three picked from yesterday's `articles/repo-actions-2026-05-30.md`.

| Repo | Idea | PR | Notification |
|------|------|-----|--------------|
| aaronjmars/aeon | #1 — Treasury wallet balance tracker (extends `skills/token-report/SKILL.md` step 2b: BaseScan + Alchemy + WebFetch fallback chain, Treasury subsection, `treasury_low_alert` < 0.01 ETH override) | [#306](https://github.com/aaronjmars/aeon/pull/306) | `.pending-notify/feature-aeon-001.md` |
| aaronjmars/aeon-agent | #4 — New `skills/upstream-gap/SKILL.md` (Mon-12:00-UTC weekly diff of local `skills/` vs upstream, URGENT/STALE/FRESH tiering, closed-loop bookkeeping, sticky merge-date state) — first non-backport feature on aeon-agent in the chain | [#72](https://github.com/aaronjmars/aeon-agent/pull/72) | `.pending-notify/feature-aeon-agent-002.md` |
| aaronjmars/minitor | #5 — Column data export (JSON) — new `downloadColumnItems` store action + Download menu entry; pure client-side blob → object URL → synthetic anchor click; works for all 47+ column types | [#56](https://github.com/aaronjmars/minitor/pull/56) | `.pending-notify/feature-minitor-003.md` |

**Files changed in this repo (committed by post-run step on main):**
- `memory/MEMORY.md` — 3 new Skills Built rows + Repo Actions Ideas Pipeline updated (May-31 burns ideas #1, #4, #5; #2/#3 deferred — #2 blocked on AntFleet capabilities-field PRs landing, #3 medium-effort)
- `memory/logs/2026-05-31.md` — feature skill section appended with per-repo outcomes
- `.gitignore` — added `.pr-bodies/` exclusion for future feature runs

**Follow-ups:** All three PRs open and awaiting review. May-30 ideas #2 (capabilities coverage map) and #3 (PR merge-priority digest) carry to next cycle. 18th consecutive same-day-after backport chain interrupted today — aeon-agent's upstream-gap is itself the meta-fix that makes the chain self-monitoring.
