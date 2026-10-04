Memory flush complete for the 2026-09-27 → 2026-10-04 window. Here's what changed:

## Promoted to MEMORY.md
- **Recent Digests**: added 5 missing tweet-digest rows (09-29 through 10-03 — Hook #8 showcase, feedback-builder/OpenAI-Dots-rename cycle, Arc Studio spotlight, audit-dashboard/weekly-recap, a thin 0-new-originals cycle).
- **New lesson**: tweet-digest's skip-RTs rule must key on the tweet's text prefix, not the API's `isRetweet` field — confirmed 10-02 when a genuine RT came back with `isRetweet=null`.
- **`aeon` priority**: refreshed the shiplog headline from the 09-14→09-21 window to the newer 09-21→09-28 window (130 PRs/15 repos, MiroShark's first public dataset release, 757 stars).
- **`aeon-agent fork sync`**: updated from PR #229 (baseline `ba01e9f`) to PR #232, confirmed **merged** 2026-09-28 14:03 UTC, baseline now `531f575`, 15 pending conflicts, lifetime success rate 64%→67%.
- **Working-tree anomaly**: bumped to 47+ days (reconfirmed via `git status` today — still present, not caused by this run).

## New findings surfaced and recorded
- **Scratch-file git hygiene** was far worse than documented: re-counting via `git ls-files` found **268 tracked scratch files**, not the handful previously logged — the dominant offender is a **102-file dump under `output/.tmp-aeon-update/`** (a stale clone artifact from the aeon-update PR #232 run). Rewrote the priority with real numbers and the root cause.
- **3rd open health issue**: GitHub #234 (`health: tweet-digest`, opened 09-30 for an isolated "hype-adjacent" quality dip) joins #230/#231 as still open despite the skill re-scoring clean (4/5, no flags) on 10-03 — added to the auto-close priority.
- **`secured-watch` is disabled** (`enabled: false` in `aeon.yml`) and has been since ~10-01 with no log entry explaining why — now 4 days unconfirmed by the operator. Added as a new priority; annotated the related note-field-parser lesson/priority as moot while it stays off.

## Housekeeping
- Archived 6 oldest digest rows (09-14→09-19) to `memory/topics/digests-history.md`, keeping the table at 14 rows.
- Confirmed 0 open PRs / 0 "improve:" PRs — nothing to prune there.
- Logged the run to `memory/logs/2026-10-04.md` and stamped the watermark (`memory_prep.py stamp` → `2026-10-04`).

## Summary
- **Files modified**: `memory/MEMORY.md` (digests, lessons, priorities), `memory/logs/2026-10-04.md` (run log), `memory/topics/digests-history.md` (archive), `memory/memory-flush-state.json` (watermark).
- **Follow-up needed**: a skill-repair pass for the 268-file scratch-file cleanup (especially the 102-file aeon-update dump), an auto-close mechanism for recovered health issues (#230/#231/#234), and an operator decision on the undocumented `secured-watch` disable.
- No code changes, no PR needed — this is a memory-only consolidation.
