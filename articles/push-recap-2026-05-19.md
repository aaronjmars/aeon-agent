# Push Recap — 2026-05-19

## Overview
Five substantive PRs merged across two repos in the last 24h (2 in `aeon`, 3 in `aeon-agent`; `minitor` was quiet — the operator was already three columns ahead with PR #44 still open). The window's centre of gravity is fork-intelligence + cron-path hygiene: aeon-agent absorbed two upstream backports (`fork-skill-gap`, `fork-first-run-alert`) and the last enabled-eligible XAI consumer (`refresh-x`) was rewired off the broken direct-curl primary path. aeon shipped a new surveillance skill (`competitor-launch-radar`) and squashed the macOS Bash 3.2 empty-array crash that was silently turning a clean `[PASS]` into `✗ BLOCKED` on every fresh fork.

**Stats:** 10 files changed (substantive), +1,114 / −15 lines across 5 PR merges (plus ~30 aeon-agent cron auto-commits, aggregated).

---

## aaronjmars/aeon

### New surveillance angle: framework launches outside the cohort
**Summary:** `competitor-launch-radar` is the 8th read-only "watch the AI-agent ecosystem from a different angle" skill in the aeon stack — and the first one pointed at *new entrants* rather than the locked-in 9-framework cohort already tracked by `ai-framework-watch`. PH RSS + HN Algolia get keyless polled weekly for any launch matching one of 9 framework-shape keywords; cohort slugs are suppressed so LangGraph Studio v2 doesn't double-fire here.

**Commits:**
- `8ca965f` — feat: competitor-launch-radar skill (#183)
  - New file `skills/competitor-launch-radar/SKILL.md` (+442 lines): 10-step skill body with a 7-status exit taxonomy (OK/QUIET/DRY_RUN/NO_SOURCES/PARTIAL/STATE_CORRUPT/BAD_VAR), 9 framework keywords (`agent framework`/`autonomous agent`/`agentic`/`multi-agent`/`mcp server`/`mcp client`/`ai agent`/`claude agent`/`llm agent`), 9-slug cohort suppression list, 10+ upvote/point noise floor, classification priority (framework > mcp > product), LRU-200 state at `memory/topics/competitor-launch-radar-state.json` keyed by `ph:slug` or `hn:objectID`, and a WebFetch fallback for the curl-blocking sandbox.
  - Modified `aeon.yml` (+1 line): registered weekly Monday 10:00 UTC, sonnet-4-6, enabled:false.
  - Modified `skills.json` (+13, −1): slotted between `code-health` and `contributor-reward`; bump 119 → 120.

**Impact:** Closes the Monday-morning AI-ecosystem intelligence triple — `ai-framework-watch` (09:01) tracks cohort momentum, `fleet-state` (08:00) reads its own fork fleet, and now `competitor-launch-radar` (10:00) scans for ungated newcomers. Count-driven notify (0=QUIET, 1-3=individual, 4+=top-8 batch with overflow footer) keeps quiet weeks silent and viral weeks legible.

### Bug fix: macOS operators no longer see false BLOCKED
**Summary:** Every macOS operator running `./add-skill` was hitting `✗ BLOCKED: security issues` immediately after `scan.sh` printed `[PASS]` — Issue #182, silent first-touch failure for everyone on Apple's default `/bin/bash` 3.2. The JSON output path of `scan.sh` already guarded the print loops on array length; the human-readable path didn't.

**Commits:**
- `7e38a0d` — fix: guard empty-array expansion in scan.sh for Bash 3.2 (#186) — closes #182
  - Modified `skills/skill-security-scan/scan.sh` (+17, −9): wrapped each of the three print loops (`highs`/`mediums`/`lows`) in `[[ ${#arr[@]} -gt 0 ]]` length guards before the `for x in "${arr[@]}"` expansion. Under `set -euo pipefail` on Bash 3.2, `"${arr[@]}"` of a zero-element array is treated as unbound and aborts; Bash 4+ tolerates it, so the guard is a no-op on Linux CI. Inline comment names the Bash-3.2 constraint so a future cleanup doesn't drop the guards.

**Impact:** First-touch experience for the 78+ forks (14 new in the last 24h alone) — `./add-skill <gh-source> <slug>` now succeeds cleanly on a clean scan instead of bailing on the trap. Mirrors the existing JSON-path guards at lines 250/253/256; the human-readable branch was the only one missing them.

---

## aaronjmars/aeon-agent

### Same-day-after backports continue (8th and 9th in the sequence)
**Summary:** Two verbatim backports landed in the same merge wave — `fork-skill-gap` (upstream PR #176, merged May-16) and `fork-first-run-alert` (upstream PR #179, merged May-17). Both close named fork-intelligence questions in aeon-agent that were already answered upstream. The same-day-after cadence (operator-scorecard May-3→4, skill-freshness May-4→5, skill-update-check May-8→9, fork-cohort May-9→10, thread-formatter May-11→12, v4-readiness May-12→13, product-hunt-launch May-15→17, fork-first-run-alert May-17→18) is now into its 8th and 9th iteration.

**Commits:**
- `39e3e02` — feat: backport fork-skill-gap from upstream aeon PR #176 (#52)
  - New file `skills/fork-skill-gap/SKILL.md` (+304 lines): per-fork upstream-skill-adoption gap report. 11 steps, 8-status exit taxonomy (OK / QUIET / DRY_RUN / NO_ACTIVE / NO_UPSTREAM_MANIFEST / PARENT_CHANGED / API_FAIL / BAD_VAR). Reads `memory/topics/fork-cohort-state.json` when fresh (≤8d) for cached POWER+ACTIVE list; falls back to live `gh api .../actions/runs?per_page=1` per fork when cohort state is missing. Compares on slug presence in `skills.json` (not enabled state — that's fork-skill-digest's job). Manifest absence is `unreadable=true`, never inflated to "missing N skills". 80-fork cap, bot allowlist (dependabot/github-actions/aeonframework).
  - Modified `aeon.yml` (+1): registered Sunday 21:00 UTC enabled:false sonnet-4-6 — slots 1h after contributor-spotlight (20:00) and 1.5h after fork-release-tracker (19:30).
  - Modified `skills.json` (+10): bump 87 → 88, slotted between fork-skill-digest and huggingface-trending.

- `ecfa912` — feat: backport fork-first-run-alert from upstream aeon PR #179 (#50)
  - New file `skills/fork-first-run-alert/SKILL.md` (+285 lines): named same-day alert the first time any fork completes a workflow run. 7-status exit taxonomy (OK / QUIET / DRY_RUN / NO_STATE / API_FAIL / PARENT_CHANGED / BAD_VAR). Two-tier data sourcing (cohort cache ≤8d fresh, live `gh api repos/{parent}/forks --paginate` fallback). LRU-500 seen-list at `memory/topics/fork-first-run-state.json` (canonicalised to lowercase). Count-driven notify (0=QUIET, 1-3=per-fork named, 4+=batch capped at 8 rows with "... and N more" footer). First-ever run backfills current ACTIVE set into seen (no loud day-one flood). Bot allowlist same as fork-skill-gap.
  - Modified `aeon.yml` (+1): registered Daily 20:30 UTC enabled:false sonnet-4-6.
  - Modified `skills.json` (+11, −1): bump 86 → 87.

**Impact:** Aeon-agent's fork-intelligence layer is now at full parity with upstream — `fork-cohort` (alive?) + `fork-release-tracker` (shipped?) + `contributor-spotlight` (who pushed code?) + `fork-skill-gap` (what hasn't been adopted?) + `fork-first-run-alert` (when did it activate?). All five chain off the same state files; none of them write to fork repos. The backport pipeline has now consumed every May-6 upstream skill.

### XAI direct-curl primary path retired (4th and last consumer migrated)
**Summary:** `refresh-x` was the last enabled-eligible XAI consumer still using `curl -H "Authorization: Bearer $XAI_API_KEY"` as its primary fetch — a pattern that's silently broken inside the GitHub Actions sandbox because env-var expansion in curl headers is blocked. The skill body has been rewritten to read `.xai-cache/refresh-x.json` (already written by `scripts/prefetch-xai.sh`, case `refresh-x)`, lines 149-160) as Path A, with `.error` and `.truncated` markers driving short-circuit branches.

**Commits:**
- `fd5effb` — improve: refresh-x — read prefetch cache instead of broken direct curl (#51)
  - Modified `skills/refresh-x/SKILL.md` (+29, −4): step 1 rewritten with the four-path ladder (Path A prefetch cache → Path A error short-circuit on `.xai-cache/refresh-x.json.error` → Path A truncated marker on `.xai-cache/refresh-x.json.truncated` → Path B direct-curl for local mode → Path C WebSearch fallback). Step 3 log template extended with `Source:` and `Status:` fields covering 5 statuses (OK / OK_TRUNCATED / PREFETCH_FAILED / NO_PREFETCH / EMPTY). Step 5 notification adapts (one-line error reason on PREFETCH_FAILED, append warning on OK_TRUNCATED). The misleading "If `XAI_API_KEY` is not set, skip and log" line — which historically caused 5 days of false-positive logs even with a valid key — removed. Sandbox note appended pointing at the prefetch script case. Environment Variables Required reworded: XAI_API_KEY is consumed by the prefetch script, not by the skill directly on the cron path.

**Impact:** Fourth explicit-marker / cache-read contract since May 10 — after PR #37 (`.error` marker, tweet-allocator), PR #43 (`.truncated` extension across narrative-tracker / remix-tweets / tweet-roundup), and PR #48 (fetch-tweets-log fallback in token-report). Every XAI consumer on the cron path now treats the prefetch cache as the source of truth. `refresh-x` is `enabled:false`, so this is a latent fix — but a future enable will land without the 5-day false-positive log noise PR #48 just eliminated for token-report.

---

## Developer Notes
- **New dependencies:** none.
- **Breaking changes:** none.
- **Architecture shifts:** the XAI prefetch-cache contract (Path A → A-error → A-truncated → B local → C WebSearch) is now codified across all four enabled-eligible XAI consumers. The same explicit-marker shape applies to Bankr (`.bankr-cache`) and is the canonical sandbox-fallback pattern in this codebase.
- **Tech debt:** PR #51 (`refresh-x`) is a latent fix — the skill is `enabled:false`, so the fix won't be exercised on the cron path until the operator flips the switch. No new TODOs.

## What's Next
- aeon-agent backports caught up: every same-day-after target from the upstream sync section is now closed. Next backport opportunity depends on the next upstream merge.
- Three aeon-agent PRs still open on May-18 fixes (#48 token-report, #50 fork-first-run-alert backport, #52 fork-skill-gap backport) all merged this window — open queue dropped 3.
- competitor-launch-radar (aeon PR #183) is the 8th fork/peer-watch skill but `enabled:false`; first Monday 10:00 UTC run after enable will write the cold-start state file.
- scan.sh fix unblocks `add-skill` for every macOS operator joining the fleet — the 12 new forks in the last 24h alone is the proximate beneficiary.
- minitor's open PRs (#41 column-alert-keywords, #43 github-discussions, #44 CoinGecko) are still in flight — no merges this window.

## Sources
- [aeon PR #183](https://github.com/aaronjmars/aeon/pull/183) — competitor-launch-radar
- [aeon PR #186](https://github.com/aaronjmars/aeon/pull/186) — scan.sh Bash 3.2 fix (closes Issue #182)
- [aeon-agent PR #52](https://github.com/aaronjmars/aeon-agent/pull/52) — fork-skill-gap backport
- [aeon-agent PR #51](https://github.com/aaronjmars/aeon-agent/pull/51) — refresh-x prefetch cache
- [aeon-agent PR #50](https://github.com/aaronjmars/aeon-agent/pull/50) — fork-first-run-alert backport
