Consolidation complete for the 2026-08-30 → 2026-09-06 window.

## Summary

**Promoted / corrected:**
- Filled 3 missing Recent Digests rows (09-01, 09-04, 09-05)
- Fixed a stale fact: `aeon-update` PR #220 was recorded as "awaiting operator merge" but had actually **merged** 2026-09-04 02:37 UTC (baseline now `bf33365`); updated lifetime success rate 43%→50% (no longer chronic)
- Refreshed the `repo-pulse` bullet from stale 08-24 data to the freshest 08-31 re-dispatch (aeon 711★/253 forks, soul.md 658★ ACTIVE, opendia 1914★)
- Reconfirmed the working-tree anomaly (`AGENTS.md`/`notify`) is still unresolved as of today (19+ days)

**Removed / added lessons:**
- Removed a falsified lesson ("eyebrow can't run in sandbox") — 09-01's `aeon-update` run disproved it; replaced with the corrected capability
- Added a new lesson on the 08-31 GLM-gateway outage (zero-token failure signature = infra outage, not a code bug); merged its "weekly skills don't self-heal" angle into the existing 08-02 lesson instead of duplicating

**Pruned for budget:** archived 3 oldest Recent Digests rows and 2 lowest-value Lessons Learned to new/existing history files (`digests-history.md`, new `lessons-history.md`), keeping both sections within their ~10-15 row budget.

**Files touched:** `memory/MEMORY.md`, `memory/topics/digests-history.md`, `memory/topics/lessons-history.md` (new), `memory/logs/2026-09-06.md`, `memory/memory-flush-state.json` (watermark stamped to 2026-09-06).

No follow-up actions needed — this is local memory-file work only, no PR required.
