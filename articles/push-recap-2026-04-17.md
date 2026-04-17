# Push Recap — 2026-04-17

## Overview
15 meaningful commits by 2 authors (@aaronjmars, aeonframework) across 2 repos. The main thrust: a complete overhaul of the fetch-tweets pipeline — from broken sandbox calls to a reliable cache-first system with persistent dedup — paired with a new tweet-allocator skill that pays contributors in $AEON. A new skill dependency graph also shipped on the main aeon repo.

**Stats:** ~15 files changed, +1,050/-250 lines across 15 meaningful commits (plus ~40 auto-commit chores)

---

## aaronjmars/aeon-agent

### Fetch Tweets Pipeline Overhaul
**Summary:** The fetch-tweets skill had been returning FETCH_TWEETS_EMPTY for 4+ consecutive days because it never read from the pre-fetched XAI cache. This batch of 8 commits rebuilt the entire pipeline: cache-first reads, broadened search queries, a Python post-filter for false positives, and a persistent seen-file for dedup that survives across runs.

**Commits:**

- `2a0d9b7` — improve: add xai-cache read to fetch-tweets skill (#13)
  - Changed `skills/fetch-tweets/SKILL.md`: Restructured step 3 to check `.xai-cache/fetch-tweets.json` first, fall back to direct API, then WebSearch. Added Sandbox note section (+30, -16 lines)
  - Root cause: prefetch-xai.sh cached results but the skill never read them — always attempted the blocked direct API call

- `58b0e98` — fix: prefetch-xai reads var from aeon.yml + add tweet-allocator skill
  - Changed `scripts/prefetch-xai.sh`: Added Python fallback to read `var` from aeon.yml when not passed as argument (+14 lines)
  - Changed `aeon.yml`: Updated fetch-tweets var, added tweet-allocator entry and @aeonframework handle (+4, -1 lines)
  - New file `skills/tweet-allocator/SKILL.md`: Full 201-line skill definition for $10/day USDC rewards to top tweeters (+201 lines)

- `f115b7c` — chore: widen fetch-tweets to 3-day window, ask for 10+ tweets
  - Changed `scripts/prefetch-xai.sh`: Expanded Grok search prompt to request 10+ tweets with broader time window (+2, -1 lines)

- `7a3b9c0` — fix(fetch-tweets): emphatic no-dedup + broaden var to ORs
  - Changed `aeon.yml`: Var from AND-joined narrow intersection to OR'd cashtag/handle/repo terms (+1, -1 lines)
  - Changed `skills/fetch-tweets/SKILL.md`: Added explicit "DO NOT dedup against memory/logs/" directive (+6, -2 lines)
  - Context: Run 6 still dedup'd 11 of 14 Grok results despite updates — model was following patterns from older log entries

- `9878b81` — fix(fetch-tweets): 1-day window, github.com/ in var, untrack .xai-cache
  - Changed `.gitignore`: Added .xai-cache/, .bankr-cache/, .pending-notify/, .outputs/ (+4 lines)
  - Changed `aeon.yml`: Var now includes full `github.com/aaronjmars/aeon` URL (+1, -1 lines)
  - Changed `scripts/prefetch-xai.sh`: 3-day → 1-day search window (+2, -2 lines)
  - Changed `skills/fetch-tweets/SKILL.md`: Synced direct-API fallback to 1-day window (+1, -1 lines)
  - Removed `.xai-cache/fetch-tweets.json` from tracked files

- `bab038b` — fix(fetch-tweets): re-enable dedup (broader search + 1d window kept)
  - Changed `skills/fetch-tweets/SKILL.md`: Restored 3-day SEEN_TWEETS check after confirming broadened search returns more results (+9, -9 lines)
  - Dedup was temporarily removed to verify the broadened search was actually returning more tweets

- `bfb903e` — fix(fetch-tweets): tighten Grok prompt + add post-filter for false positives
  - New file `scripts/filter-xai-tweets.py`: 110-line Python post-filter that rewrites the cache, keeping only tweet blocks containing required tokens (cashtag, handle, or URL). Drops bare-word "aeon" matches (+110 lines)
  - Changed `scripts/prefetch-xai.sh`: Stricter Grok prompt explicitly rejecting bare-word matches (+8, -1 lines)
  - Context: Grok returned tweets using bare word "aeon" (a person's name) without the $ cashtag

- `16780ff` — improve(fetch-tweets): persistent dedup via seen-file (#14)
  - New file `memory/fetch-tweets-seen.txt`: 58-line persistent list of all previously reported tweet URLs (+58 lines)
  - Changed `skills/fetch-tweets/SKILL.md`: Skill now unions two dedup sources — the seen-file and 3-day log scan — into SEEN_TWEETS (+7, -1 lines)
  - Solves the problem of log-based dedup breaking when logs rotate or get compacted

**Impact:** fetch-tweets went from 4+ days of FETCH_TWEETS_EMPTY to reliably returning 10+ tweets per run. The two-layer guard (Grok prompt tightening + Python post-filter) eliminated false positives from bare-word matches. Persistent dedup via seen-file means tweet notifications no longer repeat across days even when logs get compacted.

---

### Tweet Allocator: $AEON Rewards System
**Summary:** A new tweet-allocator skill that distributes $10/day in $AEON tokens to the top tweeters about the project was introduced, then rapidly iterated through 3 refinement commits. The flow went from USDC to native $AEON denomination, added Bankr wallet verification as the single gate for payouts, and introduced a required-token filter to prevent rewarding off-topic tweets.

**Commits:**

- `99245ba` — feat: tweet-allocator pays in $AEON, add BANKR_API_KEY to workflow
  - Changed `.github/workflows/aeon.yml`: Added BANKR_API_KEY to workflow env secrets (+4 lines)
  - Changed `skills.json`: Added tweet-allocator to the skill catalog, bumped total from 54 to 55 (+18, -8 lines)
  - Changed `skills/tweet-allocator/SKILL.md`: Switched denomination from USDC to $AEON throughout (+15, -15 lines)

- `445e0ca` — feat: broaden fetch-tweets, cache-first bankr, "$X in $AEON" wording
  - New file `scripts/prefetch-bankr.sh`: 133-line bash script that pre-fetches Bankr wallet verifications outside the sandbox, saves to `.bankr-cache/verified-handles.json` (+133 lines)
  - Changed `skills/tweet-allocator/SKILL.md`: Now reads .bankr-cache first (sandbox-safe), outputs "$X.XX in $AEON" for clarity (+26, -19 lines)
  - Changed `skills/fetch-tweets/SKILL.md`: Passes var verbatim to Grok, removes crypto-specific rewrite (+7, -19 lines)

- `2fc5add` — fix(tweet-allocator): apply required-token filter to candidates
  - Changed `skills/tweet-allocator/SKILL.md`: Added defensive filter that reads fetch-tweets var from aeon.yml and drops candidates whose text contains none of the required OR tokens (+2 lines)
  - Context: Previous run allocated to @_mpils whose tweet said "I love this clown aeon" — no cashtag, caught by the stale pre-filter log

- `70845cb` — simplify(tweet-allocator): Bankr wallet is the single gate
  - Changed `skills/tweet-allocator/SKILL.md`: Massive simplification — removed "unverified" fallbacks, "pending" states, redundant filters. If Bankr cache is missing, skill hard-stops. If handle has no wallet, silently dropped. Only 0x-verified addresses get allocated (+57, -144 lines)
  - Net reduction of 87 lines — cleaner, more predictable flow

**Impact:** Contributors who tweet about $AEON with a verified Bankr wallet now get automatically allocated rewards. The single-gate design means no more "pending (manual send, unverified)" states — if your wallet isn't linked, you simply don't get paid. Clean, deterministic.

---

### Infrastructure & Notification Fixes
**Summary:** Two targeted fixes for the CI/CD pipeline: Telegram notifications were mangling Twitter handles with underscores, and the chain-runner couldn't access skill outputs because .outputs/ was gitignored.

**Commits:**

- `a06943e` — fix(notify): switch Telegram to HTML mode to preserve handle underscores
  - Changed `.github/workflows/aeon.yml`: Replaced Telegram's legacy Markdown mode with HTML mode. Added inline Python pre-pass that saves bold/links to placeholders, HTML-escapes the rest, then restores as `<b>` and `<a href>` tags. Falls back to plain text if HTML send fails (+20, -2 lines)
  - Context: Legacy Markdown mode treated single underscores as italic delimiters — `BioStone_chad` became `BioStonechad`

- `c87d2a3` — fix: don't ignore .outputs/ — workflow's chain-runner needs those tracked
  - Changed `.gitignore`: Removed `.outputs/` from ignore list (+0, -1 lines)
  - Context: Chain-runner saves skill outputs to `.outputs/{skill}.md` for downstream steps to consume — gitignoring them broke the chain

**Impact:** Telegram notifications now render correctly with all special characters preserved. Chain-runner can properly pass outputs between skill steps.

---

## aaronjmars/aeon

### New Feature: Skill Dependency Graph
**Summary:** A new meta-skill that generates a Mermaid dependency map of all 91 Aeon skills, grouped by category with dependency edges showing how skills connect. Shipped as PR #38.

**Commits:**

- `393fc37` — feat: add skill dependency graph — Mermaid map of all 91 skills (#38)
  - Changed `README.md`: Added dependency graph link under the Skills table (+2 lines)
  - Changed `aeon.yml`: Registered skill-graph on Sunday 5 PM UTC schedule (+1 line)
  - New file `docs/skill-graph.md`: 245-line Mermaid diagram with 91 nodes across categories (Market & Social, Content, Dev, Meta, Infrastructure), 18 dependency edges across 4 types (direct, chain, data-flow, self-healing), highlights the self-healing loop and content pipeline (+245 lines)
  - New file `skills/skill-graph/SKILL.md`: 56-line skill definition — parses aeon.yml for skill entries and chains, reads SKILL.md files for depends_on references, generates grouped Mermaid flowchart (+56 lines)

**Impact:** Developers and operators can now visually understand how Aeon's 91 skills relate to each other. Key findings: 73/91 skills are fully independent, 4 have direct `depends_on` edges, a 5-skill self-healing loop (heartbeat → skill-health → skill-repair → skill-evals → heartbeat), and a 4-skill content pipeline (repo-actions → feature → repo-article → syndicate-article).

---

## Developer Notes
- **New dependencies:** `scripts/filter-xai-tweets.py` (Python 3, stdlib only), `scripts/prefetch-bankr.sh` (bash, uses BANKR_API_KEY)
- **Breaking changes:** tweet-allocator now denominates in $AEON instead of USDC; requires BANKR_API_KEY secret and pre-fetched `.bankr-cache/verified-handles.json` or skill hard-stops
- **Architecture shifts:** Dedup moved from ephemeral log-scanning to persistent `memory/fetch-tweets-seen.txt` file; Telegram notifications switched from legacy Markdown to HTML parse mode
- **Tech debt:** None introduced — the simplify commit on tweet-allocator actually removed 87 lines of complexity

## What's Next
- The persistent seen-file (`memory/fetch-tweets-seen.txt`) may grow indefinitely — a periodic cleanup or rotation mechanism will be needed
- tweet-allocator rewards are still "PENDING (manual send)" — automated on-chain distribution via Bankr API is the natural next step
- Skill dependency graph is registered but disabled — operators need to enable it in their aeon.yml
- The fetch-tweets var broadening (OR-based) and post-filter (Python) should stabilize tweet quality; monitor for any remaining false positives
