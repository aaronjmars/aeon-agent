# Push Recap — 2026-05-11

## Overview
Four substantive commits merged across the three watched repos in the 24h window (2026-05-10T15:36Z → 2026-05-11T15:36Z), all authored by @aaronjmars from four PRs. Today's recap is essentially yesterday's queued PRs landing in one bunch: the four PRs flagged as "open at cutoff" in yesterday's recap (aeon #164, aeon-agent #36, aeon-agent #37, minitor #33) were all merged at ~22:39 UTC on May 10, four minutes apart. The day's thrust: a fourth weekly competitive-intelligence skill on aeon (the AI-framework-watch layer that completes the github-trending / huggingface-trending / framework-watch triple), the same-day-after fork-cohort backport landing on aeon-agent, an error-marker contract made explicit after yesterday's BANKR auth failure exposed an implicit one, and minitor's 39th column type closing the long-form-developer surface.

**Stats:** 15 files changed, +1,131 / -13 lines across 4 commits in 4 PRs.

Routine cron auto-commits in the window — 36 on aeon-agent (scheduler state + per-skill auto-commits + cron success markers across token-report, fetch-tweets, tweet-allocator, repo-pulse, weekly-shiplog, feature, project-lens, repo-article, skill-leaderboard, memory-flush, heartbeat) — are excluded from this recap. They are the audit trail of yesterday's and today's skill runs, not new code.

Also worth noting: today's `feature` skill opened three more PRs (aeon #165 price-threshold-alert, aeon-agent #38 auto-merge-agent-prs, minitor #34 github-actions column — all from the May-10 ideas brief) that had not merged at the window cutoff. They will land in tomorrow's recap if merged overnight.

---

## aaronjmars/aeon

### Theme 1: The framework layer joins the watch triple
**Summary:** aeon already had two weekly competitive-intelligence skills — `github-trending` (covers code-as-artifact across the GitHub long tail) and `huggingface-trending` (covers AI artifacts: models, datasets, spaces). The missing leg was the *framework* layer itself — the libraries operators build *on* (LangGraph, CrewAI, AutoGen, LlamaIndex, et al.) which ship weekly releases and breaking changes that ripple downstream. The new `ai-framework-watch` skill closes that gap: it tracks a hardcoded 9-framework watchlist with aeon as the anchor row, surfaces 7d/30d star deltas, releases in the trailing 7-day window, breaking-change flags, and momentum picks. The watchlist is intentionally curated rather than discovery-driven — drift in the watchlist would erode longitudinal comparability week-over-week, which is the whole point of running it on a fixed cadence.

**Commits:**
- `8dd2270` — feat: ai-framework-watch — weekly competitive-intelligence digest on AI agent frameworks (#164)
  - New file `skills/ai-framework-watch/SKILL.md` (+307 lines) — 9-framework hardcoded table (aeon anchor + langgraph / crewai / autogen / llamaindex / mastra / smolagents / dspy / pydantic-ai). Single-framework deep-dive mode via `var={slug}`. Five-bucket exit taxonomy (OK / QUIET / PARTIAL / ERROR / BAD_VAR), gated notify (skip on STEADY + no breaking + no momentum). Verdict priority order is breaking-change → momentum-shift → release-week → steady → cold-start, with only the highest-priority verdict firing (no stacking). State persisted in `memory/topics/framework-watch-state.json` with rolling 7d/30d star comparison. Breaking-change detection uses strong-signal keywords (BREAKING:, ⚠️ BREAKING) plus major-version-bump heuristic (vN.0.0 with prior release on a different major) — intentionally precise-over-permissive because false positives erode trust in a digest format faster than false negatives. Read-only across the cohort; no write actions even on the anchor. Sandboxed via `gh api` — no curl, no env-var-in-headers, no API keys.
  - Modified `aeon.yml` (+1 line) — registered the skill with `enabled: false`, schedule `30 8 * * 1` (Monday 08:30 UTC, two hours before fork-fleet's 10:00 slot and before weekly-shiplog at 09:00), model sonnet-4-6.
  - Modified `skills.json` (+14 / -2 lines) — bumped total 113 → 114, regenerated timestamp.

**Impact:** Aeon's weekly competitive-intelligence stack now spans three layers — code (github-trending), artifacts (huggingface-trending), frameworks (ai-framework-watch). All three are anchored to aeon as a comparison row, which means a fork operator running aeon gets a single weekly read of "where does my framework sit vs. the eight peers most often compared to it" without leaving the repo. Stays `enabled: false` for now (operator-discretion enablement, expected Monday May 18 if flipped).

---

## aaronjmars/aeon-agent

### Theme 1: Fork-cohort backport lands on the agent fleet
**Summary:** aeon-agent has been catching up to upstream aeon on a same-day-after backport rhythm: operator-scorecard (May 3 → May 4), skill-freshness (May 4 → May 5), skill-update-check (May 9, eight-day gap). Yesterday's `feature` skill picked fork-cohort (May 2 upstream PR #152) as the next backport — eight days behind upstream, narrower than skill-update-check but more leveraged on the social-loop side because it produces the rows that contributor-spotlight (May 9, PR #163) reads to pick the weekly recognition target. With fork-cohort live on aeon-agent, the same-day-after pattern is now caught up on the four most-leveraged skills (operator-scorecard, skill-freshness, skill-update-check, fork-cohort). Remaining backports per the priorities list: v4-readiness (May 6) and thread-formatter (May 6).

**Commits:**
- `12fea2f` — feat: backport fork-cohort skill from upstream aeon (PR #152) (#36)
  - New file `skills/fork-cohort/SKILL.md` (+290 lines) — verbatim copy of upstream's fork-cohort SKILL.md. Buckets every fork by activation stage using **GitHub Actions run history**, not pushed_at or commit divergence — the distinction matters because pushed_at counts a single auto-commit from yesterday as "active" while run-history captures "is this Aeon instance actually executing skills right now?" POWER threshold is `≥1 workflow run in last 7d AND ≥5 distinct skills enabled`. Week-over-week delta tagging (LEVELED_UP / WENT_STALE / REVIVED / NEW_ACTIVE / WENT_COLD / NEW_FORK / DROPPED_FROM_POWER) makes the cohort data actionable for the social loop (contributor-spotlight reads it for weekly recognition picks). Read-only across the fleet — no commenting, no issue creation. Gated notify (skip on STEADY + no transitions + prior state present).
  - Modified `aeon.yml` (+1 line) — registered with `enabled: false`, schedule `0 19 * * 0` (Sunday 19:00 UTC, after heartbeat, one hour before contributor-spotlight's 20:00 slot upstream — though contributor-spotlight is not yet backported here).
  - Modified `skills.json` (+12 / -2 lines) — bumped total 58 → 59, dev category.

**Impact:** aeon-agent now knows which forks are alive at the same granularity upstream aeon does. The "X of Y forks running in production" social-proof number that operator-scorecard surfaces and contributor-spotlight acts on is now derivable on the agent-fleet side. Once enabled, the first Sunday run produces a cold-start baseline; the second run produces actionable transition tags. Same-day-after backport pattern (operator-scorecard, skill-freshness, skill-update-check) holds.

### Theme 2: Error-marker contract made explicit
**Summary:** Yesterday's tweet-allocator run hit `BANKR_API_KEY_INVALID` — the prefetch script wrote a `.error` marker file with the specific failure code and operator action, and the skill surfaced the right notification ("Rotate BANKR_API_KEY at https://bankr.bot/api"). But the SKILL.md only told the skill to check if the cache was "missing or empty" — Claude had read the marker by inference. Three failure modes (`BANKR_API_KEY_MISSING` / `BANKR_API_KEY_INVALID` / `BANKR_LOOKUPS_FAILED`) each have a different operator action; an implicit contract means future runs might report "cache missing" when the actual cause is auth-token rejection or upstream outage. PR #37 makes the contract explicit: read the marker first, surface its content verbatim, never paraphrase.

**Commits:**
- `bba61e0` — improve(tweet-allocator): explicitly read prefetch error marker (#37)
  - Modified `skills/tweet-allocator/SKILL.md` (+18 / -5 lines) — step 4 reordered into two ordered branches:
    - **First, check the prefetch error marker.** If `.bankr-cache/verified-handles.json.error` exists, read it, log `TWEET_ALLOCATOR_ERROR — <verbatim marker content>`, send a notification that quotes the marker's failure code AND the operator action it specifies. Explicitly: "Do NOT paraphrase the cause; the marker text is the operator-facing source of truth and changes per failure mode." Stop.
    - **Second, read the cache.** If no marker exists, proceed to the existing `.bankr-cache/verified-handles.json` read path. The hard-stop branch is narrowed to "cache file itself is missing AND no .error marker" — meaning the prefetch never ran at all (workflow config issue, distinct from auth failure).
  - Sandbox note expanded to document the two-file failure surface (cache + `.error` marker, cleared each prefetch run so presence means *this* run failed). Status flags section lists the three marker codes the prefetch can emit (`BANKR_API_KEY_MISSING` / `BANKR_API_KEY_INVALID` / `BANKR_LOOKUPS_FAILED`) and clarifies that the marker's text is appended verbatim to the log line.

**Impact:** The three failure modes now route deterministically. The operator sees the right action in the notification regardless of whether Claude inferred correctly on a given run. The pattern (prefetch writes a `.error` marker + skill quotes it verbatim) is now ready to be lifted into other prefetch-backed skills if they hit similar implicit-contract issues — though this is the first one to surface the gap in production.

---

## aaronjmars/minitor

### Theme 1: Long-form-developer surface lands
**Summary:** minitor's 39th column type. The news-and-web cluster grows 6 → 7. HN, Lobsters, and Stack Overflow already covered link aggregation and Q&A, but none host long-form practitioner content — the tutorials, walkthroughs, and opinionated engineering posts that HN links to but doesn't itself surface. DEV.to fills exactly that. The column uses the keyless DEV.to REST API (`dev.to/api/articles`) — anonymous reads aren't rate-limited per docs — with three modes: top (most reactions in the past 7 days), latest (state=fresh, sorts by published_at desc), rising (most reactions in the past 24h, tighter than top and biased toward posts still climbing rather than already viral).

**Commits:**
- `df48f94` — feat: DEV.to column — long-form developer articles by tag and recency (#33)
  - New files (+478 lines):
    - `lib/integrations/devto.ts` (+236 lines) — fetch helper with three modes, optional 1–5 tag AND-filter, dual-shape parsing for both `tag_list` (array) and `tags` (CSV string) — the API ships both across years of endpoints, so the parser accepts either and normalises to a deduped array.
    - `lib/columns/plugins/devto/plugin.ts` (+50 lines) — column metadata: `#3b49df` DEV indigo accent (distinct from substack #ff7b30, lobsters #ac130d, stack-overflow #F48024, HN flame), `Code2` lucide icon, news category, Zod schema with `mode` enum and free-text `tag` field.
    - `lib/columns/plugins/devto/server.ts` (+23 lines) — server fetcher binding plugin → integration with cursor-based pagination.
    - `lib/columns/plugins/devto/client.tsx` (+169 lines) — renders title + description + reactions/comments/reading-time footer + organisation "for {org}" line when present.
  - Modified `lib/columns/plugins/manifest.ts`, `lib/columns/registry.ts`, `lib/columns/server-registry.ts` (+2 lines each) — three-registry-edit pattern that every new plugin follows.
  - Modified `README.md` (+4 / -4 lines) — hero column list adds DEV.to between Stack Overflow and Hugging Face; total count 38 → 39; News & web cluster row 6 → 7; keyless-columns line picks up DEV.to.
  - Three integration quirks documented inline:
    1. The API has shipped both `tag_list` (array) and `tags` (CSV string) over years of endpoints — parser accepts either, normalises to a deduped array, drops empties.
    2. `per_page = max(limit, 30)` so the client-side trim is independent of upstream page size; per_page=30 is the documented default, so a full page (30 items) is the hasMore signal.
    3. Tag count clamped to 5 — the API doesn't document a hard cap, but >5 narrows aggressively to no results on most slices and makes the cache key explode.

**Impact:** The practitioner-content layer is now legible in a minitor deck. An AI/ML cluster deck can stack DEV.to (`tags=ai,llm`) next to HN, Lobsters, Hugging Face, arXiv, and stack-overflow — a single deck for the entire tutorial-to-paper pipeline. Count 38 → 39; the next plugin (already in flight — github-actions column, May-10 idea #2, opened today as minitor PR #34) will close minitor's last big repo-health gap (CI run visibility).

---

## Developer Notes
- **New dependencies:** none. All four PRs use existing deps (zod, lucide-react, gh CLI). The DEV.to integration is keyless; ai-framework-watch and fork-cohort use `gh api` exclusively (no curl, no env-var-in-headers).
- **Breaking changes:** none. All three new skills register `enabled: false`; the tweet-allocator change is additive (reorders step 4 into two branches, doesn't change the OK path).
- **Architecture shifts:**
  - The "prefetch writes `.error` marker, skill quotes it verbatim" pattern is now a documented contract on aeon-agent — first explicit instance of this two-file failure surface. Other prefetch-backed skills (`prefetch-xai.sh`, `prefetch-bankr.sh`, anything in `scripts/prefetch-*.sh`) could adopt the same pattern if implicit-contract issues surface there.
  - aeon's weekly-cadence digest stack is now four skills wide on Monday morning: ai-framework-watch (08:30), weekly-shiplog (09:00), github-trending (09:00), huggingface-trending (09:30). Monday-morning notification volume is something to watch the first time all four are `enabled: true` on the same week.
- **Tech debt:** none introduced. The DEV.to client renders raw HTML-decoded titles like its peer plugins; the framework-watch state file is bootstrapped with a sane empty default. No TODOs added in any of the four commits.

## What's Next
- **Today's `feature` PRs (opened, not merged):** aeon #165 price-threshold-alert (May-10 idea #1), aeon-agent #38 auto-merge-agent-prs (May-10 idea #3), minitor #34 github-actions column (May-10 idea #2). All three should land in tomorrow's recap if merged overnight, completing the May-10 ideas brief (3 of 5 ideas burned, 2 remain: Fork Release Tracker, npm Trends Column).
- **First natural Monday run for ai-framework-watch:** May 11 (today) at 08:30 UTC — but it shipped `enabled: false` so today's slot was a no-op. First real run lands on May 18 if the operator flips it.
- **Remaining backports for aeon-agent:** v4-readiness (May-6 #4) and thread-formatter (May-6 #5) — fork-cohort cleared today, leaving these two as the visible remainder on the backport queue. There's also the deeper 80+ autoresearch-evolution rewrite queue (aeon PRs #46–#136) that skill-update-check (now landed) will start surfacing on its first weekly run.
- **No branches created but not merged.** All four PRs from yesterday landed; today's three new PRs are open but their branches were created by today's `feature` skill, not yesterday's.
