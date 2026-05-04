# Push Recap — 2026-05-04

## Overview
Three substantive PRs across the three watched repos in the 24-hour window, all merged at 12:53 UTC today by aaronjmars in a single coordinated wave: a new freshness-watchdog skill on `aeon`, a backport of the weekly operator scorecard to `aeon-agent`, and a 34th column type on `minitor`. The shape of the day is the inverse of yesterday's flush — yesterday cleared a backlog of feature-skill PRs in a 16-minute merge train; today shipped one purpose-built fix per repo. Plus the usual ~26 routine bot auto-commits on `aeon-agent` `main` (token-report, fetch-tweets, tweet-allocator, repo-pulse, weekly-shiplog, feature, self-improve, repo-actions, repo-article, project-lens, skill-leaderboard, memory-flush, heartbeat cron side effects).

**Stats:** 12 files changed, +971 / -4 lines across 3 substantive commits. Plus ~38 routine bot auto-commits on `aeon-agent` `main` (cron success markers + auto-commit pairs + scheduler state ticks).

---

## aaronjmars/aeon

### New skill: `skill-freshness` — silent-staleness watchdog for chained skills
**Summary:** A daily 08:00 UTC sonnet skill that walks every enabled skill in `aeon.yml`, parses both explicit (`chains: consume:`) and implicit (`articles/`, `.outputs/`, `memory/topics/`, `memory/state/`) file dependencies inside each `SKILL.md`, and checks whether the on-disk file each consumer is about to read is fresh enough to be worth reading. The gap it closes is the one the existing reliability stack misses entirely: a chained skill that runs on schedule, with no API errors and a 100% pass rate, can still silently consume yesterday's output when its upstream producer failed and nothing replaced the file.

**Commits:**
- `32c77d7` — feat(skill-freshness): audit enabled skills' upstream file deps for staleness (#157) — merged 12:53 UTC
  - New file `skills/skill-freshness/SKILL.md` (+286). Per-class freshness thresholds derived at runtime from each producer's cron, not hardcoded per dependency: daily-producer articles → 28h (24h cadence + 4h grace); weekly-producer articles → 192h (168h + 24h); `.outputs/{skill}.md` chain-runner files → 4h; `memory/topics/{name}.md` reference files → 7d; `memory/state/{name}.json` → 30d. Severity bands `OK` / `WARN` (past threshold but ≤2×) / `STALE` (past 2×, real degradation not a one-day blip) / `MISSING` (file doesn't exist — only fired for **explicit** deps + canonical `articles/{producer}-${today}.md` patterns, never for grep-discovered references that may have been pseudocode or comments). Worst-of-deps rolls up to consumer verdict; worst-of-consumers to fleet verdict. Fingerprint-based dedup (sha1 of sorted `consumer:dep:severity` triples excluding `OK` rows) with 7-day re-emit window so chronic stale files aren't forgotten in the noise floor. Pure local file I/O — no `curl`, no `gh api`, no env-var-in-headers, no prefetch. Read-only across producers (never re-runs / never deletes / never edits another skill's `SKILL.md` — the skill reports; operator or `skill-repair` acts). Read-only across `memory/issues/` (filing belongs to `skill-health`, not here). Notify gated `FRESHNESS_OK → silence`, only emit on fingerprint change. Has its own `var=dry-run` mode + single-skill scope override.
  - Modified `aeon.yml` (+1) — registers `skill-freshness: { enabled: false, schedule: "0 8 * * *", model: "claude-sonnet-4-6", var: "" }` between `skill-graph` and `smithery-manifest` in the meta block.
  - Modified `skills.json` (+13, -1) — `total: 108 → 109`, new `productivity`-category entry.

**Impact:** Closes Apr-30 repo-actions idea #4 / May-2 idea #2 (Skill Dependency Freshness Validator — carried 2 cycles, listed in MEMORY.md Next Priorities). The complementary triangle is now: `heartbeat` catches failures-this-run, `skill-analytics` ranks degradations-over-time, `skill-health` tracks consecutive-failure streaks, `skill-update-check` flags upstream `SKILL.md` drift in imported skills. None of those four catch the case where everything ran fine but the cached output is from last Tuesday. `skill-freshness` is the fifth pillar — narrow scope, no overlap. Shipped `enabled: false`; per the MEMORY.md note, it's worth turning on once `tweet-allocator` + `repo-pulse` + `token-report` plus a couple of chained outputs are live so the audit has surface area to flag.

---

## aaronjmars/aeon-agent

### Backport: `operator-scorecard` lands on aeon-agent
**Summary:** Yesterday's aeon PR #153 (the weekly "was this week worth it?" three-paragraph synthesis) lands here as PR #28 with no logic changes — it was selected for fast-track backport precisely because it has zero upstream-PR-#46-to-#136 dependencies (pure `articles/` + `memory/` reads, no curl, no `gh api`, no env-var-in-headers), so it can ship independently of the 80-PR autoresearch-evolution backport queue this fork is still on day 13 of grinding through.

**Commits:**
- `2f61c2a` — feat(operator-scorecard): backport weekly was-this-week-worth-it scorecard (#28) — merged 12:53 UTC
  - New file `skills/operator-scorecard/SKILL.md` (+257). Weekly Monday 10:30 UTC sonnet skill. Three-paragraph contract — agent health (`success_pct` + heartbeat verdicts + open issues) / community growth (stars + forks + new contributors + notable mentions) / economic activity ($AEON distributed + recipient count + token 7d delta + verdict). Worst-of-three rollup with `DEGRADED > WATCH > OK` precedence; `INSUFFICIENT_DATA` lanes degrade overall to `WATCH` (not `DEGRADED`) so partial-data weeks still flag as worth checking. Verdict vocabulary mirrors heartbeat's P-flag glyphs (🟢 / 🟡 / 🔴) for visual continuity — operators don't learn new terminology. Reads articles this fork already produces: `skill-analytics`, `heartbeat` (or daily heartbeat sections in `memory/logs/` as fallback), `tweet-allocator`, `token-report`, `repo-pulse`, `distribute-tokens`. Synthesis-only by contract — every number prints from a file another skill wrote, never fabricated. Per-lane verdicts: agent health `OK` if `success_pct ≥ 90 AND anomaly_count ≤ 1 AND heartbeat_p0/p1 == 0`; community growth `OK` if `total_stars_added ≥ 20 OR new_contributors ≥ 1`; economic activity `OK` if `total_distributed > 0 AND token_7d_pct ≥ -10`. Writes `articles/operator-scorecard-${today}.md` + `dashboard/outputs/operator-scorecard.json` (Stack/Card/Grid/Table catalog spec). `var=dry-run` skips notify but still writes artifacts (dashboard refreshes regardless). Exit taxonomy: `OPERATOR_SCORECARD_OK` / `OPERATOR_SCORECARD_QUIET` (dry-run) / `OPERATOR_SCORECARD_NO_DATA` (every lane `INSUFFICIENT_DATA` on a fresh fork).
  - Modified `aeon.yml` (+1) — registers `operator-scorecard: { enabled: false, schedule: "30 10 * * 1", model: "claude-sonnet-4-6", var: "" }` between `weekly-review` and `repo-scanner` in the productivity cluster.
  - Modified `skills.json` (+11, -1) — `total: 55 → 56`, new `productivity`-category entry slotted next to `weekly-review` and the existing weekly-meta neighbours (`self-review`, `skill-health`, `goal-tracker`).

**Impact:** First non-trivial backport this week from aeon → aeon-agent. The 80-PR autoresearch-evolution queue (aeon PRs #46–#136) still hangs over this fork, but operator-scorecard slots in cleanly because its inputs are existing-fork-native (no chained-skill-output dependencies that would require the chain-runner work). First natural Monday run lands May 11 if the operator enables it (May 4 already cron-passed by build time today). MEMORY.md Next Priorities row updated to reflect the May 11 trigger date.

---

## aaronjmars/minitor

### New plugin: `lobsters` — 34th column type
**Summary:** Tech-focused community of ~30k engineers running on lobste.rs added as a column type. Adjacent to Hacker News in audience but with narrower / higher-signal submissions and a tag taxonomy that supports filtered feeds (rust, ai, programming, security, etc.). Closes the obvious gap in the News & Web cluster — HN was the only general-tech discussion column.

**Commits:**
- `e28392d` — feat(plugins): add lobsters column type (#27) — merged 12:53 UTC
  - New file `lib/columns/plugins/lobsters/plugin.ts` (+43) — Zod schema `{ mode: "hottest" | "newest" | "active" | "tag" default "hottest", tag: string default "" }`. Anchor icon (a nod to lobster-claw branding without copying proprietary imagery), brand red `#ac130d` (lobster-claw red on lobste.rs/about — distinct from HN's orange `#ff6600`, so the two news-source columns stay visually differentiated when stacked together). `news` category, `paginated: true`. Default title format `Lobsters · t/{tag}` for tag mode, `Lobsters · {ModeLabel}` otherwise.
  - New file `lib/columns/plugins/lobsters/server.ts` (+31) — cursor-based pagination with one defensive fallback: if user picks `tag` mode without filling in a tag, server falls back to `hottest` so the column always renders something rather than throwing a 404 from `/t/.json`.
  - New file `lib/columns/plugins/lobsters/client.tsx` (+160) — renderer with tag pills under the snippet (HN's renderer doesn't have this since HN has no tags; Lobsters' tag taxonomy is core to the signal). Story title links to external article when present; comment-count badge links to `lobste.rs/s/{short_id}` (matches HN's pattern of distinct external-vs-comments URLs).
  - New file `lib/integrations/lobsters.ts` (+159) — keyless integration. `.json` variants of every public Lobsters page expose the same story array; pagination via `/page/N/{mode}.json` with the page-1-is-bare-root quirk handled in `endpointFor()` (page 1 is `/hottest.json`, not `/page/1/hottest.json`). Multi-tag support via comma-joined slugs (`/t/rust,go.json` matches Lobsters' upstream URL convention). Three Lobsters-specific quirks handled in the integration layer: (1) `submitter_user` can be either bare string username OR `{ username }` object — `unwrapAuthor()` handles both shapes; (2) `description` is sanitised HTML (p / br / code / em / a only) — targeted regex strip (`stripHtml()`) safe without pulling in a full HTML parser, falls back to `description_plain` if upstream sends it; (3) `hasMore` detection uses upstream page size (≥25) NOT post-filter slice, so the visible `PAGE_SIZE` clamp doesn't stop pagination early on full pages. Schema-drift safe — drops stories missing `short_id` or `title` rather than rendering dead rows. User-agent header identifies minitor (`minitor/1.0 (+https://github.com/aaronjmars/minitor)`) — Lobsters' admins ask scrapers to identify themselves so they can throttle cooperatively if needed.
  - Modified `lib/columns/plugins/manifest.ts` (+2), `lib/columns/registry.ts` (+2), `lib/columns/server-registry.ts` (+2) — standard 3-edit plugin registration. Server-registry parity check at server module init throws if drift, so a missing edit in any of the three files surfaces as a startup error rather than a silently broken column.
  - Modified `README.md` (+3, -3) — column count `33 → 34`, News & Web row count `4 → 5` (now includes `lobsters` alongside `bing`, `google-news`, `news-search`, `rss`), hero paragraph picks up "Lobsters" alongside "Hacker News".

**Impact:** Per the MEMORY.md row, this is the 34th column type and the 6th-or-7th in the News & Web cluster (depending on Bluesky merge ordering from earlier this week). Audience overlap with HN is high but the signal profile is meaningfully different — Lobsters' invite-only registration and tag system surface different discussion threads than the HN front page, and many users want both as side-by-side columns rather than as substitutes. Founder / open-source maintainer / ML-research dashboards tend to read both; this lands minitor's value prop for that segment without requiring an API key.

---

## aeon-agent cron noise (background)

The remaining 38 commits in the window on `aeon-agent` are routine cron auto-commits — every scheduled skill produces a pair (the skill's `auto-commit` of its outputs + the cron-runner's `success` marker) plus a `scheduler` `update cron state` tick. Today's cron-cycle commits visible in the window: `token-report`, `fetch-tweets`, `tweet-allocator`, `weekly-shiplog`, `repo-pulse`, `feature`, `self-improve`, `repo-actions`, `project-lens`, `repo-article`, `skill-leaderboard`, `memory-flush`, `heartbeat`. No anomalies — every paired `chore(cron): {skill} success` confirms the corresponding skill exited cleanly.

---

## Developer Notes
- **New dependencies:** None. All three PRs use existing libraries (Zod, lucide-react `Anchor` icon already imported elsewhere) and the standard fetch API. Lobsters integration is pure native fetch + regex.
- **Breaking changes:** None. All three new SKILL.md / column-type entries are additive. `enabled: false` on both new aeon-side skills means no live cron behavior changes. Lobsters column type is opt-in per deck — existing minitor users see no change unless they add the column.
- **Architecture shifts:** `skill-freshness` introduces a new convention worth noting: **per-class freshness thresholds derived from producer cadence in `aeon.yml`**, not per-skill or per-dependency. This keeps the table maintainable as the fleet grows from 109 → 200+ skills without forcing every new skill to declare its own thresholds. Operator-scorecard backport reinforces the **"backport-by-isolation"** pattern — pure local-file-I/O skills can be cherry-picked from aeon → aeon-agent ahead of the chained-skill backport queue, because they have no dependencies on the autoresearch-evolution work.
- **Tech debt:** None introduced. `skill-freshness` explicitly documents that implicit (grep-discovered) dependencies are best-effort with tolerated false positives and accepted false negatives — explicit `chains: consume:` edges remain the source of truth. Operator-scorecard backport documents `INSUFFICIENT_DATA → WATCH` (not `DEGRADED`) as the partial-data fallback, which avoids the failure mode of every weekly run on a fresh fork crying wolf.

## What's Next
- Three Next Priorities rows in MEMORY.md flip to "shipped, awaiting enable":
  - `skill-freshness` on aeon (PR #157) — turn on once chained outputs accumulate so the audit has surface to flag silent-staleness.
  - `operator-scorecard` on aeon-agent (PR #28) — first natural Monday run May 11.
  - The aeon-side `operator-scorecard` enable (shipped May 3 PR #153) — first natural Monday run was today May 4 if enabled, but already past the 10:30 UTC cron mark; next opportunity May 11.
- Backport queue moved one step forward (operator-scorecard ✓). Remaining priority backport targets in MEMORY.md: `skill-freshness` (just-shipped aeon PR #157, hot off the press), `pr-triage`, `thread-formatter`, `smithery-manifest`, `fork-cohort`, `show-hn-draft`, `skill-analytics`, `fork-contributor-leaderboard`. The 80-PR autoresearch-evolution backport (aeon PRs #46–#136) remains the larger work item this fork is on day 13 of.
- `lobsters` column completes the obvious News & Web cluster expansions for now. The MEMORY.md repo-actions Apr-26 idea #1 (Auto-Merge Agent PRs) remains blocked on workflows-scope PAT — the same blocker that's been there for 8+ days. No open thread visible in today's diffs that wasn't already known.
