Watermark stamped and mirrored correctly. This is a `read-only`-mode-compatible skill run with local file writes only (no `git`/`gh` mutation, `gh pr list`/`gh pr view` were read-only lookups) — memory-flush is a `write` mode skill per its metadata, so this is expected to land directly.

## Summary

Ran `memory-flush` for the 2026-09-06→09-13 window (8 log files).

**Promoted:**
- 5 missing Recent Digests rows (09-07, 09-10, 09-11, 09-12, 09-13)
- Refreshed `repo-pulse` bullet with 09-07's weekly data (aeon 717★/256 forks, soul.md 663★, opendia 1920★ — was stale on 08-31 figures)
- Updated `aeon-update` bullet: PR #221 confirmed **merged** 2026-09-07 (baseline now `21b82db`), success rate 50%→56%
- Bumped working-tree-anomaly confirmation to today (26+ days unresolved)

**Found and flagged as a new issue:** the 09-13 `tweet-digest` run re-reported 4 of 5 "new" tweets that were exact duplicates of tweets already published in the 09-11 digest — its dedup only checked the most-recent day's log (09-12) instead of the full 09-10..09-13 fetch window it declared. Logged as both a new Lesson Learned and a new Next Priority (dedup lookback needs to span the full fetch window).

**Pruned:** archived 5 oldest digest rows and 2 low-value lessons ("eyebrow can run in sandbox" — superseded; "feature governance-docs" one-off) to their respective `-history.md` files to stay within budget. Confirmed 0 open improvement PRs, 0 open issues — nothing else to prune.

**Files touched:** `memory/MEMORY.md`, `memory/topics/digests-history.md`, `memory/topics/lessons-history.md`, `memory/logs/2026-09-13.md`, `memory/memory-flush-state.json` (watermark stamp).

**Follow-up needed:** someone should fix `tweet-digest`'s dedup logic to check every log inside its declared fetch window, not just the prior day — otherwise it'll keep re-publishing stale content.
