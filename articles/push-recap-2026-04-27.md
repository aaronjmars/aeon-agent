# Push Recap — 2026-04-27

## Overview
Four meaningful commits across both watched repos in the last 24h after two consecutive QUIET recap days. Three of them are PR merges to `aaronjmars/aeon` that flush the top of the backlog in one window — the skill-analytics fleet-observability widget, the contributor-reward planner that closes the leaderboard→distribute-tokens loop, and a SHOWCASE.md that turns repo discoverability into a single landing page. The fourth is a one-line aeon-agent fix that ends a two-day BANKR `subscription_required` outage and unblocks tweet-allocator.

**Stats:** 12 files changed, +874/-3 lines across 4 meaningful commits (~30 autonomous scheduler/cron auto-commits filtered)

---

## aaronjmars/aeon — 3 PRs merged

### Theme 1: Backlog Flush — Three Meta-Skills Land in One 22-Hour Window

**Summary:** PR #142 (skill-analytics) and PR #144 (contributor-reward) both squash-merged at 2026-04-26 17:03Z — the autonomous-PR queue that had been stalling at ~28h finally cleared. Then 21h later PR #145 (SHOWCASE.md) merged at 2026-04-27 13:46Z. All three were `feature` skill outputs that had been flagged as highest-priority unbuilts in earlier `repo-actions` cycles. None of them touch each other's code — but together they fill the three observability/community gaps the agent has been brainstorming about for a week.

**Commits:**

- `98193f9` — **feat: skill-analytics — fleet-level skill-run analytics widget (#142)** (+318/-1, 3 files)
  - New file `skills/skill-analytics/SKILL.md` (+316 lines): Wednesday 18:30 UTC meta-skill. Pipeline reads `./scripts/skill-runs --json --hours 168` as ground truth, cross-references aeon.yml schedules (silent-scheduled detection), `memory/cron-state.json` (consecutive_failures), and `memory/logs/*.md` regex grep (best-effort exit-taxonomy parsing — captures the `SKIP_UNCHANGED`/`NEW_INFO`/`SKIP_QUIET` exits from autoresearch-evolution rewrites that existing health checks have been misclassifying as failures). Emits a ranked article + json-render dashboard spec, and only notifies when ≥1 of six anomaly flags fires (🔴 SILENT, 🔴 ALL_FAIL, 🟠 CONSECUTIVE_FAILURES, 🟠 LOW_SUCCESS, 🟡 ALL_SKIP, 🟡 DUPLICATE_RUNS — first match wins). Significance gate follows the autoresearch-evolution / fork-skill-digest pattern: clean fleet = silent run, article + JSON still written.
  - Changed `aeon.yml` (+1 line): registered with Wednesday 18:30 UTC schedule on `claude-sonnet-4-6`, disabled by default.
  - Changed `.github/workflows/aeon.yml` (+1/-1): added `skill-analytics` to the meta-skills quality-analysis skip list at the case statement so the Haiku post-run scorer doesn't grade structural output as content.

- `46a7a24` — **feat: contributor-reward — turn fork-contributor-leaderboard into a tier-priced rewards plan (#144)** (+255/-0, 2 files)
  - New file `skills/contributor-reward/SKILL.md` (+254 lines): Monday 09:30 UTC (16h after Sunday's 17:30 leaderboard run). Reads the latest `articles/fork-contributor-leaderboard-*.md`, rejects >8d stale, parses the Top Contributors table via tolerant regex on the documented column layout, prices each rank-1-to-5 contributor with score ≥10 against a tier table (1=25, 2=15, 3=10, 4-5=5 USDC) plus +5 first-PR bonus once-ever per login. Writes the plan to `memory/distributions.yml` under a `contributors-YYYY-Wnn` list; idempotency state in `memory/state/contributor-reward-state.json` keyed on (week, login) plus a flat `first_pr_bonus_paid` list. Plan-generation only — does NOT execute transfers (distribute-tokens stays the single execution boundary, preserving its preflight + per-recipient idempotency; the distributions.yml diff is the human-visible audit trail before any money moves). Re-runs same week with identical plan = silent no-op; re-runs with diffs = add only deltas, never claw back demoted entries. Exit taxonomy: OK / DRY_RUN / ALREADY_PROCESSED / NO_LEADERBOARD / STALE_LEADERBOARD / PARSE_FAIL / NO_ELIGIBLE / ERROR. Pure local file I/O — no curl, no env-var-expansion, no new prefetch/postprocess.
  - Changed `aeon.yml` (+1 line): registered next to fork-contributor-leaderboard on `claude-sonnet-4-6`, disabled by default.

- `2774f7f` — **feat: add SHOWCASE.md with active forks + ecosystem comparison (#145)** (+74/-0, 2 files)
  - New file `SHOWCASE.md` (+72 lines): Active Forks table sourcing the top 6 by skill count from `articles/skill-leaderboard-2026-04-26.md` (tomscaria 94, maacx2022 15, DannyTsaii 3, davenamovich 3, 0xfreddy 2 with custom macos-apps, pezetel 2 with github-trending) + Ecosystem Comparison table (Aeon vs AutoGen, CrewAI, n8n, LangGraph across 11 dimensions: runtime, scheduling, skill format, persistent memory, self-healing, quality scoring, reactive triggers, setup floor, hosting cost, operator role, external integration) + one-line per-framework summaries + an "Add yourself" note explaining how forks can be listed.
  - Changed `README.md` (+2 lines): one-line pointer to SHOWCASE from the existing comparison section. The existing Aeon-vs-Claude-Code/Hermes/OpenClaw table stays intact — SHOWCASE covers the broader-ecosystem question that lands inbound HN/MCP-registry traffic.

**Impact:** The three highest-priority unbuilts from the last two `repo-actions` brainstorm cycles are now live. skill-analytics closes the fleet-observability triangle alongside heartbeat (per-run) and skill-health (per-skill) — the agent can now see across all skills at once, not just one at a time. contributor-reward closes the loop between knowing-who-contributes and paying-them — the wiring has been a documented gap in the leaderboard's own SKILL.md since it shipped. SHOWCASE.md is the cheapest discoverability lever before the May-25 300-star deadline (currently 244 stars, +49 wow). Topics-expansion half of the SHOWCASE idea is deferred — `gh api repos/aaronjmars/aeon/topics -X PUT` returned 403 because the agent's token lacks admin scope; the exact one-shot command sits in PR #145's body for the maintainer.

---

## aaronjmars/aeon-agent — 1 PR merged (real fix), ~30 autonomous auto-commits filtered

### Theme 2: Two-Day BANKR Outage Resolved by Two Lines

**Summary:** Tweet-allocator had been hard-stopping with `TWEET_ALLOCATOR_ERROR` for two consecutive days because Bankr's `/agent/prompt` endpoint started returning `subscription_required` around 2026-04-25. The cache file `.bankr-cache/verified-handles.json` was sitting at `{}` and tripping the no-wallet-verification hard-stop. The fix is a payload addition: send `maxMode: {enabled: true, model: "claude-sonnet-4.6"}` so the prompt bills against Bankr's separate LLM-credits pool. Verified end-to-end before merge — handle resolves and returns the same wallet recorded in `memory/logs/2026-04-24.md`.

**Commits:**

- `14577ba` — **fix(bankr): send maxMode with prefetch so Agent API stops returning subscription_required (#20)** (+229/-3, 7 files; 2 are the actual fix, 5 are co-merged auto-commit artifacts)
  - Changed `scripts/prefetch-bankr.sh` (+2/-1): single jq payload addition. The lookup body changes from `{prompt: "..."}` to `{prompt: "...", maxMode: {enabled: true, model: "claude-sonnet-4.6"}}`. That's the entire fix.
  - Changed `skills/tweet-allocator/SKILL.md` (+1/-1): updated the `BANKR_API_KEY` env-var doc to flag the new requirement: "Bankr's Agent API now requires Max Mode for AI prompts, so the account must have LLM credits topped up at https://bankr.bot/llm?tab=credits (separate pool from regular API credits)." Operator-facing setup note so a fresh fork doesn't hit the same wall.
  - Co-merged via the squash: `articles/tweet-allocator-2026-04-26.md` (+21), `dashboard/outputs/tweet-allocator-2026-04-26T17-36-35Z.json` (+173), `memory/logs/2026-04-26.md` (+14), `.outputs/tweet-allocator.md` (+17/-1), `memory/token-usage.csv` (+1) — these are the autonomous skill-run output that landed at the same time the fix was tested live, not new logic.

**Impact:** Tweet-allocator is unblocked. Run 4 yesterday (post-merge, 17:23Z) succeeded — 3 tweets paid, $10 USD-equivalent in $AEON distributed; today's run (08:10Z) succeeded again (2 tweets paid, $10 distributed). The 2026-04-26 log records four runs in sequence: runs 1-3 errored on the empty cache, run 4 succeeded after the merge. Post-fix, the lesson in MEMORY.md about "Bankr prefetch empty-cache pattern" is partly stale — the empty-cache symptom is fixed at the API-payload layer, not just the dedup layer.

---

## Developer Notes
- **New dependencies:** none.
- **Breaking changes:** none in code. Operator-facing change: Bankr `BANKR_API_KEY` accounts now require LLM credits topped up at https://bankr.bot/llm?tab=credits (separate from regular API credits) — fresh forks need this or tweet-allocator's prefetch will fail.
- **Architecture shifts:** `skills/skill-analytics/` introduces the fleet-wide observability layer alongside per-run (heartbeat) and per-skill (skill-health). `skills/contributor-reward/` formalises the leaderboard→distribute-tokens handoff but deliberately keeps distribute-tokens as the single execution boundary — the new skill writes plans, doesn't move money.
- **Tech debt:** SHOWCASE topics expansion deferred — needs admin-scope token to call `gh api repos/aaronjmars/aeon/topics -X PUT`. Same root cause as the 10-day-old `workflows`-scope PAT issue (heartbeat in 7-day extended-persistence backoff, day 10).

## What's Next
- skill-analytics first scheduled run: Wednesday 2026-04-29 18:30 UTC. First chance to see fleet-wide silent-scheduled or LOW_SUCCESS flags fire across the actual run population.
- contributor-reward first scheduled run: Monday 2026-04-27 09:30 UTC has already passed without a run today — schedule is registered but disabled by default; needs operator opt-in or chain wiring (`fork-contributor-leaderboard → contributor-reward → distribute-tokens dry-run` is documented as a one-line aeon.yml change in the SKILL).
- Apr-26 unbuilts after today: #1 Auto-Merge Agent PRs (still blocked on workflows-scope PAT), #3 AEON Token Pulse on Status Page (pure heartbeat-rendering edit, no perms blocker — likely next pickup), #4 Twitter Thread Auto-Formatter, #5 External PR Triage. Apr-22 idea #1 Smithery + MCP Registry Submission still unbuilt — blocked on external PRs.
- Open PRs at recap time: aeon-agent PR #19 (improve/tweet-allocator-error-dedup, opened by @aaronjmars Apr 26 13:29Z) — partly overtaken by today's PR #20 fix; needs human review on whether to keep the dedup-layer improvement or close as superseded.
- Backport of 80 autoresearch-evolution rewrites (aeon PRs #46–#136) to aeon-agent: day 10, still outstanding. The skill-analytics widget shipping today depends on those exit taxonomies (`SKIP_UNCHANGED`/`NEW_INFO`/`SKIP_QUIET`) being live in the running instance — the gap between aeon repo (where they exist) and aeon-agent (where they don't) is now load-bearing for at least one meta-skill.
