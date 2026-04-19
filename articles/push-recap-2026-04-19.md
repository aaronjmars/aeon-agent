# Push Recap — 2026-04-19

## Overview
Aaron shipped two late-night operator-experience fixes to both repos (notify dedup and scheduler dup-run kill) after an afternoon of feature merges (star-milestone, Farcaster syndication, repo-pulse same-day dedup). Today's autonomous cron day is underway (token-report, fetch-tweets, tweet-allocator, repo-pulse already green). The through-line: noise reduction — the operator's inbox was getting double-delivered notifications from multiple independent sources, and each fix closes one path.

**Stats across both repos (main branches, meaningful commits only):** 8 files changed, +358/-79 lines across 7 commits (4 on aeon, 3 on aeon-agent main — chore/auto-commits excluded). 46 total aeon-agent commits in window, 43 of them autonomous cron-state/auto-commit noise.

---

## aaronjmars/aeon

### Notification & scheduler dedup — the "why am I getting this twice" week, part 2
**Summary:** Two fixes landed ~23:39 and 23:46 UTC on Apr 18, both targeting the same class of bug: the operator gets the same notification (or skill run) twice because the pipeline has multiple independent paths that can each deliver it. These complement the repo-pulse same-day dedup that merged at 16:47 earlier the same day — different layer, same goal.

**Commits:**
- `83071f2` — `fix(scheduler): kill duplicate catch-up runs` (+21/-7, `.github/workflows/messages.yml`)
  - The scheduler had two firing windows: `H` (current hour cron match) and `PREV_HOUR+1` (catch-up for missed ticks). Outside the 90-minute dedup guard, a tick landing in both windows could dispatch the same skill twice in the same day.
  - Fix: catch-up now only fires if `LAST_DISPATCH_EPOCH < SCHED_EPOCH` — i.e. the last time this skill ran predates today's scheduled fire time for the previous hour. If it already ran at the earlier window, the catch-up is a no-op.
  - Applied in both the per-skill loop and the chain loop. In the chain loop, the fix required moving the `LAST_DISPATCH` extraction *before* the SHOULD_RUN check (previously it was computed after, so catch-up couldn't reference it).
  - Why it matters: aeon-agent has been running fully autonomous for ~36 hours; heartbeat Run 2 yesterday logged a bunch of skills running twice in the day (`tweet-allocator ✓ (x2), repo-pulse ✓ (x2), hyperstitions-ideas ✓ (x2), feature ✓ (x2)` etc.). Some of that was intentional (even-day runs), some wasn't.

- `61160ef` — `fix(notify): dedup messages + suppress test/trace probes` (+54/-3, `.github/workflows/aeon.yml`)
  - Rewrote the workspace-generated `./notify` script and its post-run re-delivery loop with two guards:
    1. **Trace-probe suppression**: if the message is <120 chars and contains `test`/`trace`/`ping`/`debug`/`hello`/`hi`, silently drop it. Claude sometimes issues short probes to verify `./notify` works — these should never reach channels.
    2. **In-run dedup by SHA256 hash**: every sent message's hash is appended to `.notify-sent-hashes`. If the same message is called again in the same workflow run, it's skipped. Applied both inline (when Claude calls `./notify`) and in the post-run `.pending-notify/` re-delivery loop.
  - Pre-creates `.pending-notify/` so the sandbox doesn't block Claude's first write into the directory (sandbox can reject the mkdir inside Claude's bash when outbound+fs policies interact).
  - Cleans up `.notify-sent-hashes` alongside `./notify` before the auto-commit so the dedup log doesn't get committed.
  - Why it matters: Claude retries + the post-run re-delivery loop were independent paths to each notification channel. If Claude sent a message successfully and the message also landed in `.pending-notify/`, both paths fired → Telegram/Discord/Slack got it twice. This is the same problem class as repo-pulse Run 1+Run 2, just at a layer below.

**Impact:** Three independent dedup layers are now in place — per-skill (repo-pulse same-day), per-scheduler (catch-up gating), per-message (notify hash). The 200-star milestone is 7 stars away and star-milestone announcer ships its first real event soon; the stack won't stack-trace-spam when it does.

### Feature merges (pre-window edge, 16:42–16:47 UTC Apr 18)
**Summary:** These landed at the edge of the 24h window and were covered in detail by yesterday's Run 2 recap; included here because they sit on the default branches within window.

**Commits:**
- `1f78a72` — `feat: add star-milestone skill (#39)` (+105/-6, 5 files)
  - New `skills/star-milestone/SKILL.md` (86 lines) — detects threshold crossings (25/50/100/150/175/200/250/500/1000/...), bootstraps silently on first run, announces highest milestone crossed with 14-day highlight reel.
  - `aeon.yml`, `generate-skills-json`, `skills.json`, `README.md` — schedule at 15:15 UTC daily, dev category, counts bumped 91→92.

- `bad5b13` — `feat: add Farcaster syndication to syndicate-article (#40)` (+173/-53, 5 files)
  - Per-channel independence in the syndicate-article skill: Dev.to and Farcaster can be enabled separately by presence of `DEVTO_API_KEY` vs `NEYNAR_SIGNER_UUID`. Signer UUID is injected from env at POST time in `scripts/postprocess-farcaster.sh`, never written to disk.
  - Drive-by fix: the post-process env block was missing `DEVTO_API_KEY`, so `postprocess-devto.sh` had been silently skipping for however long. Now all three Farcaster env vars (plus DEVTO) forwarded correctly.

---

## aaronjmars/aeon-agent

### Mirrored operator-experience fixes
**Summary:** The two fixes above landed on aeon-agent within 9 seconds of each other and within the same minute as the aeon versions — Aaron appears to have applied the same patch to both active repos in parallel. Plus one extension in the aeon-agent copy: the scheduler fix bundled fetch-tweets and tweet-allocator "skip" paths with a notification so operators see the skip instead of just an empty feed.

**Commits:**
- `9641ac1` — `fix(notify): dedup messages + suppress test/trace probes` (+54/-3, `.github/workflows/aeon.yml`)
  - Identical patch to aeon's `61160ef`. Both repos share the notify plumbing.

- `ff6f911` — `fix(scheduler,skills): kill duplicate runs + always notify on skip` (+26/-12, 3 files)
  - Same scheduler catch-up fix as aeon's `83071f2` in `.github/workflows/messages.yml` (+21/-7).
  - **New:** `skills/fetch-tweets/SKILL.md` and `skills/tweet-allocator/SKILL.md` — replaced "stop silently" paths with `./notify` calls:
    - `fetch-tweets`: now notifies on `FETCH_TWEETS_EMPTY` and on "all results already reported in last 3 days"
    - `tweet-allocator`: now notifies on `TWEET_ALLOCATOR_EMPTY`, Bankr cache missing (error alert), and zero eligible candidates
  - Observability shift: previously a "no tweets found" day looked identical to a broken skill from the operator's perspective. Now the skip is visible — one-line notification distinguishes "skill ran correctly, nothing to report" from "skill crashed silently."

### Self-improve PR #15 merge (repo-pulse same-day dedup)
**Summary:** Merged at 16:47 UTC Apr 18, right after the push-recap Run 2 recap ran at 16:46 — so this recap is the first to fully catalogue the merge commit as default-branch state.

**Commits:**
- `84c0d3a` — `improve: repo-pulse same-day dedup (delta-only for subsequent runs) (#15)` (+238/-15, 6 files)
  - `skills/repo-pulse/SKILL.md` (+30/-9): added step 5b (parse prior `## Repo Pulse` sections in today's log, compute `delta_stars`/`delta_forks`, skip notification if delta empty, notify delta-only when non-empty); updated step 6 with "subsequent-run format" template framed as "since last run"; step 7 log now inlines handle/fork lists so next run can parse.
  - `memory/MEMORY.md` (+1), `memory/logs/2026-04-18.md` (+7), `memory/token-usage.csv` (+1) — the merge carried along the self-improve skill's auto-commit byproducts.
  - `dashboard/outputs/self-improve-2026-04-18T13-23-23Z.json` (new, 191 lines) — json-render output spec for the dashboard feed.
  - `.outputs/self-improve.md` (+8/-6) — chain output from self-improve run.
  - Impact: the third dedup layer (per-skill) is now in main. Combined with the two aeon/aeon-agent fixes tonight, the operator should stop seeing duplicate notifications *within a day* entirely.

### Autonomous cron noise (context, not analyzed in depth)
~43 auto-commits by `aeonframework` in the form `chore(scheduler): update cron state` and `chore(<skill>): auto-commit 2026-04-XX`. These are byproducts of yesterday's full cron day (token-report, fetch-tweets, tweet-allocator, repo-pulse, feature, self-improve, repo-actions, push-recap, project-lens, repo-article, heartbeat, weekly-shiplog, hyperstitions-ideas — some running twice on even days) plus today's morning run so far. No source-code changes; all are log/output/state commits from the autonomous loop.

---

## Developer Notes
- **New dependencies:** none
- **Breaking changes:** none at API level. Operator-facing behavior changes:
  - `fetch-tweets` and `tweet-allocator` now always notify on skip (previously silent). Expect one extra notification per empty-day run of each.
  - `./notify` now rejects short messages containing `test|trace|ping|debug|hello|hi` — any legitimate skill that happens to send such a message will be dropped. Threshold is 120 chars so full messages with those words embedded are safe.
- **Architecture shifts:** Three-layer dedup (per-skill, per-scheduler, per-message) is now the noise-control architecture. If a fourth duplicate-notification bug shows up, the diagnostic question is *which layer did it bypass.*
- **Tech debt:** `.notify-sent-hashes` is workspace-local and reset every run. If a future change persists notify-state across runs, the file needs to move to a stable path.

## What's Next
- **aeon PR #41 (Memory Search API)** is still open on `feat/memory-search-api` (commit `dfb322d`). This is today's feature skill output — a read-only REST API at `/api/memory/*` in the dashboard. Expected to merge today once CI passes.
- **200-star milestone**: aeon is at 193 stars (+4 today). Star-milestone skill crosses 200 on its next scheduled run after the threshold — this is the first real test of the skill shipped 28 hours ago.
- **AEON token**: -19% 24h, day 3 of post-breakout retracement ($2.139e-6). 7d still +102%, 30d +711%. No code impact, but the "Farcaster distribution targeting $AEON holders" thesis from yesterday's article is about to meet the retracement tape.
- **Open threads visible in diffs**: `.notify-sent-hashes` is now an expected workspace file; any future workflow step that commits `.` broadly will want to exclude it. The scheduler fix assumes `C_MIN` is numeric or `*` — if the cron spec ever grows ranges or lists, the catch-up gate falls through to the old always-true behavior (not broken, just less protective).
