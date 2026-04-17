# Push Recap — 2026-04-17

## Overview
35 meaningful commits across `aaronjmars/aeon` (8) and `aaronjmars/aeon-agent` (27), by @aaronjmars and aeonframework. The main thrust was a two-way parallel repo cleanup — porting mature pipeline work between the fork and upstream — plus a full default-model bump to Opus 4.7 and another long day of fetch-tweets / tweet-allocator hardening until both pipelines stabilized. A skill dependency graph also shipped on upstream.

**Stats:** ~90 files changed, +2,200/-1,000 lines across 35 meaningful commits (plus ~40 auto-commit chores).

---

## aaronjmars/aeon (upstream)

### Theme 1: Fork → Upstream Port (resilience + scripts)
**Summary:** Three commits pulled hardened pipeline code from the fork(s) back into upstream aeon, closing the gap where the fork had been running ahead on resilience work.

**Commits:**
- `ed946a9` — harden(fetch-tweets): port miroshark's hardened pipeline (+51/-20)
  - Rewrote `skills/fetch-tweets/SKILL.md` with Path A/B/C fallback chain: prefetch cache → X.AI API → WebSearch
  - Added persistent seen-file logic (`memory/fetch-tweets-seen.txt`) surviving log rotation
  - Added 3-day log scan union into SEEN_TWEETS for dedup
  - Added `FETCH_TWEETS_NO_NEW` short-circuit when every result is already reported
  - Kept aeon's frontmatter conventions (capitalized name, `tags: [social]`)
- `5c0ec44` — harden: port eval-audit + XAI prefetch error logging from aeon-aaron (+284, all new)
  - New file `scripts/eval-audit`: 272-line Python coverage auditor. Reports which skills have eval specs, generates stubs for uncovered skills, emits JSON. Used by skill-evals, skill-health, self-review, tool-builder
  - Modified `scripts/prefetch-xai.sh`: on HTTP 429/401/403, appends an "XAI Prefetch Error" entry to `memory/logs/${today}.md` so health skills see credit exhaustion instead of silent cache misses
- `2fa6d0d` — harden: XAI 429 retry + GH_GLOBAL token fallback (+28/-16)
  - `scripts/prefetch-xai.sh`: single 30s-backoff retry on HTTP 429 (401/403 still fail immediately)
  - `.github/workflows/aeon.yml` + `messages.yml`: checkout tokens fall through `GH_GLOBAL || GITHUB_TOKEN`, unblocking cross-repo pushes when `GH_GLOBAL` is the configured secret (previously silently fell back to the repo-scoped default)

**Impact:** Aeon upstream now has the same resilience primitives the fork has been running for days — eval coverage auditing, XAI credit-exhaustion visibility, 429 retry, and a working cross-repo token fallback.

### Theme 2: Opus 4.7 Default Bump + Secret Forwarding
**Summary:** Promoted Opus 4.7 from optional to default model after a successful pilot run, then patched the environment block to actually forward secrets the newer skills rely on.

**Commits:**
- `15d8f18` — feat: upgrade default opus model 4.6 → 4.7 (+10/-10 across 6 files)
  - `aeon.yml`: default model + option comment updated
  - `.github/workflows/aeon.yml` + `messages.yml`: workflow_dispatch default and fallback changed
  - `README.md`: docs + dropdown options
  - `dashboard/lib/constants.ts`: UI picker
  - `skills/cost-report/SKILL.md`: pricing row key
  - Historical references in `memory/token-usage.csv`, logs, and articles deliberately left untouched — they record what actually ran
  - Pilot run on `aeon-aaron/memory-flush` verified Opus 4.7 works cleanly (2m49s, token accounting intact)
- `65e095b` — fix: forward DEVTO/NEYNAR/VERCEL (+BANKR in aeon/aaron) to skill runtime (+4)
  - Audit of all 100+ skills found several reference `$VAR` at runtime (WebFetch Bearer auth, curl, env checks) but the main Run env block wasn't forwarding them: `BANKR_API_KEY` (tweet-allocator + bankr-gated skills), `VERCEL_TOKEN` (vercel-projects, deploy-prototype), `DEVTO_API_KEY` (syndicate-article), `NEYNAR_API_KEY` (farcaster-digest)
  - Without this fix these skills would have silently failed at the first auth call

**Impact:** Agent now runs Opus 4.7 by default across the board, and new integration skills no longer fail silently on missing env vars.

### Theme 3: Workspace Hygiene + Skill Graph
**Commits:**
- `78dfd06` — chore: standardize .gitignore across aeon repos — explicit patterns for caches, tmp/scratch, stale artifacts. Replaces 4-line minimal ignore; prepares parallel cleanup across forks
- `d525907` — fix(skills): correct output paths + add images/ folder. Replaced stale `output/articles/` → `articles/` and `output/skills/` → `.outputs/` in channel-recap, tool-builder, vuln-scanner (the `output/` dir has never existed — writes were going nowhere). Added `images/` with `.gitkeep` since skills reference `images/*` paths for hero images
- `393fc37` — feat: add skill dependency graph — Mermaid map of all 91 skills (PR #38 merged)

**Impact:** Ends a silent-data-loss class (writes to non-existent dirs) and unlocks the post-process hero-image download path.

---

## aaronjmars/aeon-agent (fork)

### Theme 1: Upstream → Fork Polish Backport
**Summary:** Three commits pulled tags frontmatter and sandbox-note conventions from upstream aeon into the fork, finishing the metadata consistency sweep.

**Commits:**
- `2fcbb91` — sync(skills): backport upstream polish + hardened fetch-tweets (+82/-39)
  - 15 skills touched: changelog, code-health, defi-overview, github-issues, github-trending, issue-triage, pr-review, reddit-digest, reflect, research-brief, rss-digest, search-skill, security-digest, token-movers, weekly-review
  - `skills/reflect/SKILL.md`: added skill-health trend check
  - `skills/fetch-tweets/SKILL.md`: normalized frontmatter (capitalized name, `tags: [social]`) to match upstream conventions
- `fdf6470` — chore(skills): inject tags frontmatter from upstream aeon (+33 across 33 skills)
  - Adds missing `tags:` lines to 33 skills that existed in upstream but were behind on frontmatter metadata
  - Now 100% of skills shared with upstream have tags; remaining untagged are fork-specific
- `7dafd02` — chore(skills): tag fork-only skills + fix stale output/ paths + images/ (+18/-7)
  - Added tags to 11 fork-specific skills (build-skill, feature, hn-digest, hyperstitions-ideas, memory-flush, polymarket, search-papers, self-review, trending-coins, tweet-digest, wallet-digest)
  - Mirror of the upstream path fix (channel-recap, tool-builder, vuln-scanner)
  - Added `images/.gitkeep`

**Impact:** Every skill in the fork now has consistent `tags:` frontmatter — unblocks any skill tooling that filters/groups by tag (catalog views, skill-graph, cost-report, leaderboard).

### Theme 2: fetch-tweets Pipeline — The Long Day
**Summary:** Eleven commits iterating the fetch-tweets pipeline until it actually returned *new* tweets. Bug classes addressed: dedup too aggressive, Grok returning bare-word false positives, search window too narrow, cached artifacts polluting fresh runs, seen-list not persisting across log rotation.

**Commits:**
- `2a0d9b7` — improve: add xai-cache read to fetch-tweets skill (PR #13, +30/-16). Skill now reads `.xai-cache/fetch-tweets.json` first, falls back to API, then WebSearch — the cache was being populated but never read for four days
- `58b0e98` — fix: prefetch-xai reads var from aeon.yml + add tweet-allocator skill (+225/-5; 201-line new skill)
- `f115b7c` — chore: widen fetch-tweets to 3-day window, ask for 10+ tweets
- `7260ec3` + `3f981e0` — chore: clear xai cache + fetch-tweets seen list for fresh run
- `445e0ca` — feat: broaden fetch-tweets, cache-first bankr, "$X in $AEON" wording (+166/-38; new `scripts/prefetch-bankr.sh` 133 lines)
- `7a3b9c0` — fix(fetch-tweets): emphatic no-dedup + broaden var to ORs. Run 6 was still deduping 11 of 14 Grok results — the model was pattern-matching older log entries. Explicit "DO NOT dedup against memory/logs" directive added
- `9878b81` — fix(fetch-tweets): 1-day window, github.com/ in var, untrack .xai-cache
- `bab038b` — fix(fetch-tweets): re-enable dedup (broader search + 1d window kept)
- `bfb903e` — fix(fetch-tweets): tighten Grok prompt + add post-filter (+118, new `scripts/filter-xai-tweets.py` 110 lines). Grok was returning tweets using the bare word "aeon" (a name, casual usage) without the `$` cashtag. Two-layer guard: stricter prompt rejecting bare-word matches, plus a post-filter that rewrites the cache keeping only tweet blocks whose text contains one of the exact OR-separated tokens. Example dropped: "I love this clown aeon with all my heart dude"
- `16780ff` — improve(fetch-tweets): persistent dedup via seen-file (PR #14, +65/-1). `memory/fetch-tweets-seen.txt` layered on top of the 3-day log window; seeded with 58 URLs from existing logs. Prevents WebSearch-favored older tweets from cycling back after log rotation. Ported from `miroshark-aeon#16`

**Impact:** fetch-tweets went from `FETCH_TWEETS_EMPTY` every run → 6–15 fresh tweets per run with reliable dedup and no false positives. The `_mpils` bare-word bug is no longer possible.

### Theme 3: tweet-allocator — $AEON + Bankr as Single Gate
**Summary:** Four commits evolving tweet-allocator from unverified-USDC-rewards to a Bankr-gated $AEON distribution system with strict input filtering.

**Commits:**
- `99245ba` — feat: tweet-allocator pays in $AEON, add BANKR_API_KEY to workflow (+37/-23). Rewards denominated in `$AEON` not USDC; `BANKR_API_KEY` mapped in workflow env; added to `skills.json`
- `2fc5add` — fix(tweet-allocator): apply required-token filter to candidates (+2). Today's earlier run allocated to `@_mpils` whose tweet says "I love this clown aeon" with no cashtag. Allocator now reads the fetch-tweets var and drops any candidate whose text contains none of the OR tokens. Mirrors the Grok-cache post-filter but at allocation time
- `70845cb` — simplify(tweet-allocator): Bankr wallet is the single gate (+57/-144). Flow collapsed to: today's log → exclude project + already-paid → Bankr check → pay. No "unverified" fallback, no "pending" states, no redundant filters. Missing Bankr cache → `TWEET_ALLOCATOR_ERROR`. Missing wallet → silently dropped. Only verified 0x addresses get allocated

**Impact:** Tweet-allocator no longer sends to unverified handles, no longer sends $AEON for non-$AEON tweets, and no longer has a "pending/manual" side-path. Today it successfully paid 10 distinct handles across three runs — all verified Bankr addresses.

### Theme 4: Opus 4.7 Bump (mirrored from aeon)
**Commits:**
- `58753a9` — feat: upgrade default opus model 4.6 → 4.7 (mirror of aeon `15d8f18`, same files)
- `385e6d4` — fix: forward DEVTO/NEYNAR/VERCEL (+BANKR) to skill runtime (mirror of aeon `65e095b`)

### Theme 5: Infrastructure + Notification Fixes
**Commits:**
- `a06943e` — fix(notify): switch Telegram to HTML mode to preserve handle underscores (+20/-2). Legacy Markdown mode ate single underscores in handles (`BioStone_chad` → `BioStonechad`) because Telegram's parser treats them as italic delimiters even when unpaired. HTML mode keeps underscores verbatim. Added an inline python3 pre-pass in `./notify`: saves Markdown bold (`*x*`) and links (`[t](u)`) to placeholders, HTML-escapes the rest, restores as `<b>` / `<a href>`, falls back to plain text on failure
- `c87d2a3` — fix: don't ignore .outputs/ — workflow's chain-runner needs those tracked (-1). A silent breakage of chain-runner that shipped with the earlier gitignore consolidation
- `d83e8b5` — harden: XAI 429 retry + GH_GLOBAL token fallback (mirror of aeon `2fa6d0d`)
- `6d4429c` — resolve merge conflict in logs

### Theme 6: .gitignore + Scratch File Purge
**Commits:**
- `24ea742` — chore: standardize .gitignore, remove tracked scratch files (+44/-634)
  - `.gitignore` aligned with upstream aeon format (explicit patterns)
  - Removed 14 scratch files that had leaked into the repo: 10× `.tmp-*` payloads (aeon.yml, pr-body, push scripts, secrets, skill), `.xai_key` (content was "CLEARED"), `fetch_tweets.sh`, `run_xai.py` (one-off scripts whose functionality lives in `scripts/prefetch-xai.sh` and `skills/fetch-tweets/`)

**Impact:** Repo lost 634 lines of dead scratch code, future tmp files will be ignored properly, and one redacted (but still tracked) secret file is gone.

### Theme 7: Daily Content
**Commits:**
- `5a5650b` — feat(repo-article): "The Agent That Pays Its Own Community — autonomous growth flywheel"
- `5982730` — article: project-lens "The 85% Problem" (contrarian take on agent reliability vs intelligence)

---

## Developer Notes
- **New scripts:** `scripts/eval-audit` (272 lines, aeon), `scripts/filter-xai-tweets.py` (110 lines, aeon-agent), `scripts/prefetch-bankr.sh` (133 lines, aeon-agent)
- **New files:** `memory/fetch-tweets-seen.txt` (58-URL seed), `images/.gitkeep` (both repos)
- **Breaking changes:** tweet-allocator no longer has an "unverified/pending" code path — missing Bankr cache → hard-stop with `TWEET_ALLOCATOR_ERROR`. Operators running without `BANKR_API_KEY` configured will see this immediately instead of silent misfires
- **Model bump:** default is now Opus 4.7 across both repos. Old logs still render 4.6 pricing correctly because cost-report key is keyed by the row it reads
- **Architecture shifts:** fetch-tweets now has a persistent seen-file layer independent of log rotation. Tags frontmatter is 100% consistent across all skills shared with upstream
- **Dead code removed:** 14 scratch files (634 lines) from aeon-agent

## What's Next
- PR #38 (skill-graph) merged — next likely step is wiring the Sunday 5PM UTC run into aeon-agent too (currently only in upstream aeon.yml)
- fetch-tweets has stabilized after ~11 iterations; self-improve should detect zero `FETCH_TWEETS_EMPTY` entries for 24h+ and close that thread
- tweet-allocator's "single gate" leaves no pending/manual path — if Bankr prefetch fails, the whole skill fails fast. Monitor heartbeat for `TWEET_ALLOCATOR_ERROR` over the next 24h
- The new aeon-side `eval-audit` port means eval-driven repair loops (skill-evals + skill-repair) can generate missing specs automatically — expected uptick in auto-opened PRs
