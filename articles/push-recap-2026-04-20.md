# Push Recap — 2026-04-20

## Overview
Five PRs merged on `aaronjmars/aeon` and four mirror fixes applied directly on `aaronjmars/aeon-agent` main — two of yesterday's open feature branches (Memory Search API PR #41 and Fork Contributor Leaderboard PR #42) landed, and three operational fixes closed silent-failure paths in the notification stack and the Grok prefetch pipeline. Both feature work and fixes were authored by @aaronjmars; the aeon-agent commits are the running-instance mirror of the aeon upstream fixes, so every change is already in production.

**Stats:** 13 files changed, +795/-56 lines across 9 meaningful commits (44 autonomous cron/chore auto-commits on aeon-agent excluded)

**Window:** 2026-04-19T15:40Z → 2026-04-20T15:40Z (24h)

---

## aaronjmars/aeon (5 PRs merged)

### Theme 1 — Two shipping features from yesterday's open branches
**Summary:** The two features whose branches were flagged "still open" in yesterday's recap both merged to `main` at 12:03 UTC. Both expand the surface area through which external systems (or the agent itself) can reach into Aeon's state.

**Commits:**
- `4bb5081` — feat: add Memory Search API to dashboard (#41)
  - New file `dashboard/lib/memory.ts` (+308 lines): shared reader that does path-safe resolution (`safeJoin` + SLUG/DATE/ISSUE regexes so query params can't escape `memory/`), tokenised full-text `searchMemory()` scoring by match count, distinct-term coverage and per-source weight, and returns `{source, id, title, snippet, line, score}` per hit.
  - Seven new route files under `dashboard/app/api/memory/`: index (+38), search (+40), logs list/fetch (+26), topics list/fetch-by-slug (+12/+22), issues list/fetch-by-id (+12/+22). Total +480 lines, zero deletions — a pure additive surface.
  - No middleware: each route wraps the reader, catches errors as `{error: message, 500}`.

- `6a1dd4a` — feat: add fork-contributor-leaderboard skill (#42)
  - New file `skills/fork-contributor-leaderboard/SKILL.md` (+160 lines, 10-step runbook): ranks community devs across the 30+ fork fleet on a 4-factor score — merged upstream PR +10, open PR +3, fork commit +1 (cap 30), new skill authored +5 (cap 5), fork star +2. Bots + core team filtered; opt-out via `memory/topics/leaderboard-optout.md`.
  - `aeon.yml` (+1 line): Sunday 17:30 UTC cron entry.
  - `README.md` (+1/-1): Meta/Agent skill count 11 → 12, adds the new skill name to the row.

**Impact:** The Memory Search API is the **third external interface** to Aeon — the MCP adaptor and A2A Gateway expose skill *execution*; GitHub Pages / Dev.to / Farcaster syndication expose skill *output*; this API exposes skill *state*. All the markdown files that the agent has been writing to `memory/` since day one are now consumable without scraping raw files. Fork-contributor-leaderboard rounds out the people/skills/forks triangle (skill-leaderboard = what's popular, fork-fleet = which forks diverge, this = who are the people). Reward distribution is explicitly deferred until signal is proven over a few weekly runs.

---

### Theme 2 — Notification delivery hardening (3 PRs)
**Summary:** Three fixes closed real failure modes that had been eating notifications on live Aeon instances — one truncating long messages mid-paragraph, two producing unclickable or 404 links. All three were landed in sequence at 13:08–13:09 UTC.

**Commits:**
- `2601d0e` — fix(notify): chunk long Telegram messages instead of truncating (#45)
  - `.github/workflows/aeon.yml` (+54/-20 on aeon-agent, same shape in the merged aeon PR): replaced the single `TG_MSG="${TG_MSG:0:3990}…(truncated)"` slice with a Python chunker that splits `$MSG` at `\n\n` paragraph boundaries first, then `\n` line boundaries, and falls back to hard-split only when a single paragraph/line exceeds 3900 chars. Each chunk gets a `[i/N]` suffix. Chunks are emitted as newline-separated base64 so embedded newlines survive the `while read` loop. Existing Markdown→HTML conversion + raw-text fallback run per-chunk unchanged; 0.3s `sleep` between sends preserves channel order.
  - Trigger: `feature` and `weekly-shiplog` routinely produce >4KB messages; the former had its PR link and "How it works" section sliced off the end of every run. Split-first, parse-second keeps the HTML conversion per-chunk so formatting doesn't straddle a boundary.

- `93e1782` — fix(skills): emit clickable article URLs via $GITHUB_REPOSITORY (#44)
  - `skills/article/SKILL.md` (+3/-1): was `https://github.com/OWNER/REPO/blob/main/...` with the instruction "get the repo name from `git remote get-url origin`" — ambiguous when a skill also scans a watched repo's forks (Claude was resolving `OWNER/REPO` to the target repo and producing 404 URLs). Now: `https://github.com/${GITHUB_REPOSITORY}/blob/main/articles/${today}.md`, with an explicit "NOT the watched repo" note.
  - `skills/skill-leaderboard/SKILL.md` (+3/-1): notification used a bare `articles/skill-leaderboard-YYYY-MM-DD.md` path, rendering as plain text (unclickable) on Telegram/Discord. Same fix.
  - `skills/fork-contributor-leaderboard/SKILL.md` (+3/-1): same bare path in today's new skill — self-fix in the same PR as PR #42, before the skill ever ran in production. Pre-emptive repair.

- `0ff9d8d` — fix(fetch-tweets): prefetch timeout + workflow var expansion (#43)
  - `scripts/prefetch-xai.sh` (+11/-4): bumped `curl --max-time` from 60s to 180s for Grok `x_search` calls; added a one-time retry on curl exit 28 (timeout) tracked via a new `attempt` counter; switched to `-sS` for visible curl errors on stderr. The 60s ceiling was hitting every run — x_search takes 60–120s to search X, rank tweets, and return structured output, so `.xai-cache/fetch-tweets.json` was never written and the skill silently fell through to WebSearch (which is a dead end, per yesterday's self-improve).
  - `.github/workflows/aeon.yml` (+4/-1): the prefetch step had `VAR="${{ inputs.var }}"` inlined at template-substitution time, so a var string like `$AEON OR @aeonframework OR github.com/aaronjmars/aeon` caused bash to expand `$AEON` to empty *before* the filter script saw it. `filter-xai-tweets.py` then saw only 2/3 OR-patterns and dropped every tweet matching only the missing one. Fix: route `inputs.var` through a new `SKILL_VAR` env var (the same pattern the "Run" step at line 210 was already using), and read `VAR="$SKILL_VAR"` inside bash — literal value preserved, no bash re-expansion.
  - Verified on `miroshark-aeon` (one of the forks): filter output went from "kept 0/5" to "kept 11/11" after both fixes; prefetch now completes in ~85s versus the 60s timeout ceiling.

**Impact:** Three distinct failure surfaces closed in one sequence. The notify chunker preserves every byte of `feature` and `weekly-shiplog` output that was previously truncated mid-paragraph. The `$GITHUB_REPOSITORY` migration removes a whole class of ambiguity — skills that scan a target repo's forks were producing notifications pointing at the scanned repo instead of the running repo, so users clicking through hit 404s. The fetch-tweets fixes are the more consequential pair: two days in a row (Apr 19, Apr 20 morning) the skill silently returned empty because curl timed out and because cashtags in the query were being eaten. Post-fix, the 12:32 UTC retry run (via cache) reported 12 tweets — first successful run in 48 hours.

---

## aaronjmars/aeon-agent (4 direct-to-main commits, same changes as aeon PRs)
**Summary:** The four fixes above were also landed directly on `aeon-agent` main (this running instance) between 12:26 and 13:07 UTC — so the agent was running the fixed code before the upstream PRs merged. This is the standard aeon-agent ⇄ aeon sync pattern: prove the fix on the running instance, then open the upstream PR.

**Commits (all authored by Aaron Elijah Mars, direct push):**
- `d73ec08` (12:26 UTC) — fix(fetch-tweets): prefetch timeout + workflow var expansion — identical diff to aeon PR #43 (+15/-5 across the two files).
- `8563ccf` (12:42 UTC) — fix(skill-leaderboard): emit clickable article URL — identical to the skill-leaderboard portion of aeon PR #44 (+3/-1).
- `86b2feb` (12:44 UTC) — fix(article): use $GITHUB_REPOSITORY for article URL, not OWNER/REPO — identical to the article portion of aeon PR #44 (+3/-1).
- `6e9b34b` (13:07 UTC) — fix(notify): chunk long Telegram messages — identical to aeon PR #45 (+54/-20).

**Impact:** Every fix is already deployed on this instance; the aeon upstream merges are distribution to the fork fleet. No fork-contributor-leaderboard or Memory Search API equivalents on aeon-agent — those are strictly upstream features (the skill runs on any fork with the cron entry enabled, and the dashboard API lives in aeon's dashboard directory).

---

## Developer Notes
- **New dependencies:** None. PR #41 uses `next/server` which is already a workspace dep; the memory reader uses Node's built-in `fs/promises` and `path`.
- **Breaking changes:** None. The `$GITHUB_REPOSITORY` migration is a strict upgrade (was broken ambiguity; now deterministic). The notify chunker preserves single-message behaviour for `≤3900`-char payloads.
- **Architecture shifts:** The Memory Search API introduces a `dashboard/lib/memory.ts` shared reader pattern that's now the blessed way to access markdown state from within the dashboard — future features (MCP tools, A2A endpoints, dashboard Memory tab) should layer on top of it rather than re-parsing files.
- **Tech debt:** `fork-contributor-leaderboard` reward distribution is explicitly deferred — the scoring rubric and output format are now frozen, but the "send $AEON to top 3" pipeline is a TODO blocking on real weekly data.
- **Pattern observations:** The fetch-tweets fixes confirm a pattern first flagged in yesterday's self-improve log — *sandbox + template-interpolation mismatches are a repeated failure class*. Two bugs in one file (60s timeout, `$VAR` re-expansion) both had silent-failure modes that consumed tokens without producing output. Yesterday's self-improve PR #16 (`prefetch-error-marker`) added the observability layer; today's PR #43 fixed the two root causes.

## What's Next
- **Memory Search API surfacing:** aeon PR #41 is merged but not yet wired into MCP adaptor or A2A gateway (both would need a non-skill tool branch in each server). Expected follow-up: expose `/api/memory/*` as `aeon-memory-*` tools, build a dashboard Memory tab consuming the routes.
- **First fork-contributor-leaderboard run:** skill enters cron at Sunday 17:30 UTC — first scheduled run is 2026-04-26 (this coming Sunday). At <2 contributors it skips notification silently, so the leaderboard quality depends on the fork fleet's active-dev population over the window.
- **Propagate timeout/var fixes to adjacent skills:** the same `xai_search()` is called by `refresh-x`, `remix-tweets`, `narrative-tracker`, `article`, `tweet-roundup` — the `SKILL_VAR` workflow fix applies universally (it's at the pre-fetch level), but the skill-level short-circuit from yesterday's PR #16 only covers `fetch-tweets`. If other skills start silently empty-ing, the pattern is the same.
- **Open PRs:** `aeon-agent` — none open as of writing (yesterday's #16 merged overnight). `aeon` — none (all five #41–45 merged today). Clean board.
