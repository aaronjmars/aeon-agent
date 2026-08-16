## Summary

Ran the memory-flush skill against the full gap since last consolidation (2026-08-09 → 2026-08-16, since memory-flush runs weekly):

**Promoted:**
- 5 missing tweet-digest rows (08-10, 08-11, 08-12, 08-15, 08-16) into MEMORY.md's Recent Digests table

**Pruned (stale/resolved content):**
- Archived 12 older Recent Digests rows (07-17 → 08-09) to a new `memory/topics/digests-history.md`
- Removed the resolved "Stuck skills (Aug 2-4 outage)" bullet from Next Priorities — fully confirmed recovered, and the diagnostic lesson is already captured elsewhere in Lessons Learned
- Updated a stale Lesson Learned that told skills to use a `scripts/prefetch-*.sh` cache-file workaround for auth'd curls — that pattern is now explicitly retired per CLAUDE.md; repointed it to `./secretcurl`
- Tightened the verbose minitor and aeon Next Priorities bullets (dropped resolved historical narrative, kept actionable state)

**Verified, no action needed:**
- No open "improve:" PRs (no section to prune)
- PR #872 (external contributor fix) closed unmerged 08-16 — no follow-up
- No new skills built this window

**Files changed:** `memory/MEMORY.md` (72 → 66 lines, last-consolidated bumped to 2026-08-16), `memory/topics/digests-history.md` (new), `memory/logs/2026-08-16.md` (logged the flush).
