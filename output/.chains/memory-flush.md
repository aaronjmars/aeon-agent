Watermark stamped and all changes look correct. The flush is complete — no code to commit here (memory-flush is a `read-only`-adjacent bookkeeping skill working only in `memory/`), so I'm not opening a PR, just reporting the work done.

## Summary

Ran `memory-flush` for scan window **2026-08-23 → 2026-08-30** (8 log files).

**Promoted:**
- 7 missing tweet-digest rows (08-24 → 08-30) into MEMORY.md's Recent Digests table; archived the 7 oldest rows (08-14 → 08-20) to `memory/topics/digests-history.md` to keep the table near budget.
- Closed the stale "SHA-pin workflows" item in the `aeon` Next Priority (done via #917) and folded in the window's real headline: secretcurl argv-leak fix (#935, external contributor), channel-secret Phase-2 hardening (#951/#955/#947), 4 new run harnesses, and Claude Code plugin packaging (#884/#885) — a direct fork-onboarding win.
- New Next Priorities bullet tracking `aeon-update`'s fork-sync baseline (now `8b8d719`, PRs #193/#198) and its 10 carried conflicts.
- Two new Lessons Learned: the sandbox also blocks stdout redirection in bash blocks (with the workaround `aeon-update` used), and `aeon-update`'s pattern of holding back brand-new upstream skills that need `eyebrow`/catalog regen.
- Refreshed the working-tree-anomaly bullet's date (still unresolved, 12+ days, ~10 heartbeat flags).

**Checked, nothing to prune:** 0 open `improve:` PRs; no new Skills Built entries this window; Lessons Learned reviewed for staleness (none removed, now at 15 — flagged for possible archiving next flush).

**Files touched:** `memory/MEMORY.md`, `memory/topics/digests-history.md`, `memory/logs/2026-08-30.md`, `memory/memory-flush-state.json` (watermark stamped to 2026-08-30).

Follow-up still needed (unrelated to this skill's scope): the persistent working-tree anomaly (`AGENTS.md` deleted, `notify`/`notify-jsonrender` untracked) needs a human/skill decision — restore, delete-and-commit, or gitignore.
