# Push Recap — 2026-05-18

## Overview

Eight substantive PRs landed across the three watched repos in the last 24 hours, plus the usual fleet of cron auto-commits inside `aeon-agent`. The thrust was twofold: aeon shipped two more fork-intelligence skills (`fork-skill-gap`, `fork-first-run-alert`) — the layer that answers "what does each fork know, when did they wake up?" — and minitor crossed 44 column types with Product Hunt landing as a keyless launch-monitoring surface plus a column-level alert-keyword highlighter that retrofits all 43 existing plugins on day one. aeon-agent absorbed yesterday's upstream skills (token-report sandbox fix, product-hunt-launch backport) and turned over its own self-improve / feature / repo-actions cron loop without intervention.

**Stats:** 33 files changed, +2,917 / −47 lines across 8 substantive commits + ~50 cron auto-commits

---

## aaronjmars/aeon

Four PRs merged at the May-17 21:57–23:59 UTC window (one human-edit FAQ contribution carried over to 23:59 UTC, three operator merges in the 21:57–21:58 window).

### Theme 1: Fork-intelligence layer expanded from 3 → 5 skills

**Summary:** The fleet now has a complete fork-monitoring stack: `fork-cohort` (weekly, *is this fork alive?*), `fork-release-tracker` (weekly, *has any fork shipped?*), `contributor-spotlight` (weekly, *who is pushing the most code?*), plus the two skills merged today — `fork-skill-gap` (weekly, *what's in upstream that this fork hasn't adopted?*) and `fork-first-run-alert` (daily, *which fork ran its first workflow today?*). Both new skills are designed to chain off `fork-cohort-state.json` when fresh and fall back to live `gh api` queries when the cache is missing — so they work on day one before the cohort skill is even enabled.

**Commits:**
- `f587d30` — feat: fork-skill-gap skill (#176)
  - New file `skills/fork-skill-gap/SKILL.md` (+304 lines): 11-step skill, weekly Sunday 21:00 UTC, sonnet-4-6, `enabled: false`. 8-status exit taxonomy (OK / QUIET / DRY_RUN / NO_ACTIVE / NO_UPSTREAM_MANIFEST / PARENT_CHANGED / API_FAIL / BAD_VAR). Compares per-fork `skills.json` slug presence against parent's manifest. Manifest-unreadable forks marked as such rather than inflated to "missing 119 skills." Quiet-week gate suppresses notify when all readable forks are within 5 of upstream AND prior state exists AND no new top-missing slugs. Article body includes the inverse view — top-10 universally unadopted upstream slugs by fork-count missing — so upstream sees which new shipments are launching into silence.
  - Changed `aeon.yml` (+1): registered at Sunday 21:00 UTC, slotted 1h after contributor-spotlight (20:00) and 1.5h after fork-release-tracker (19:30).
  - Changed `skills.json` (+12): bumped 118 → 119; slotted between `code-health` and `contributor-reward`.
- `f6d6c6b` — feat: fork-first-run-alert skill (#179)
  - New file `skills/fork-first-run-alert/SKILL.md` (+285 lines): daily 20:30 UTC, sonnet-4-6, `enabled: false`. 7-status exit taxonomy. LRU-500 seen-list at `memory/topics/fork-first-run-state.json` (canonicalised lowercase to prevent double-alerts on casing drift). Count-driven notify policy — 1–3 new activators get individual named alerts, 4+ get a single batch notification (8-row cap with overflow footer). First-ever-run backfill mode populates seen with current ACTIVE/POWER set without per-fork alerts (prevents loud day-one signal at enable time). Bot allowlist (dependabot/github-actions/aeonframework) added to seen but suppressed from alerts.
  - Changed `aeon.yml` (+1): registered at daily 20:30 UTC.
  - Changed `skills.json` (+13, −1): bumped 118 → 119 (separate slug from fork-skill-gap, same number bump because PRs landed minutes apart against the same baseline).

**Impact:** Closes two genuine blind spots in the fork-monitoring layer that the existing weekly cohort skill couldn't reach. A fork that activates Monday morning waited up to six days before anyone noticed under the old cadence — now it gets a same-day named alert. And the gap report flags upstream skills the fork hasn't adopted, which both serves the fork operator (who can pull the missing pieces) and serves upstream (which can see when a new shipment launches into silence). Both are `enabled: false` at merge — operator dispatch or first natural Monday run will validate.

### Theme 2: Dashboard analytics & log routes fixed for multi-remote setups

**Summary:** Three dashboard API routes were using `execSync` with shell-interpolated `gh` commands that implicitly resolved against `cwd`'s default repo. On multi-remote setups (operators with both `aaronjmars/aeon` and a fork as remotes, or running the dashboard from a different working tree), this would either fail silently or pull data from the wrong repo. The fix replaces every `gh run list / view` call with `execFileSync` + explicit `-R {owner}/{repo}` arguments, with a resolver that tries `gh repo set-default --view` first and falls back to `gh repo view --json nameWithOwner`.

**Commits:**
- `8443858` — fix(dashboard): pass -R repo to gh run list/view so multi-remote setups work (#178)
  - Changed `dashboard/app/api/analytics/route.ts` (+21, −3): added `ghRepo()` + `ghArgsRepo()` helpers, switched `gh run list` from shell-interp to argv.
  - Changed `dashboard/app/api/runs/[id]/logs/route.ts` (+25, −7): same pattern applied to `gh run view {id}` for both run metadata and `--log` / `--log-failed` log retrieval.
  - Changed `dashboard/app/api/runs/route.ts` (+21, −3): same pattern applied to the run-list endpoint.
  - Also closes the latent command-injection surface that shell-interpolated `${id}` opened up: `id` is now validated upstream and passed as an argv element instead of being concatenated into a shell string.

**Impact:** Operators running the dashboard with non-default remotes (forks, mirrors, multi-repo development) now see the correct runs. Side benefit: removed three shell-interpolation surfaces from the dashboard's API layer.

### Theme 3: README FAQ section added (community contribution)

**Summary:** First external contributor edit in the window — `meichuanyi` added a 111-line FAQ block to the README covering positioning ("How does Aeon differ from Claude Code / Hermes / OpenClaw?"), getting started, custom skills, instance fleet, self-healing, notifications, and troubleshooting.

**Commits:**
- `37a5a0d` — docs: Add FAQ section (#177)
  - Changed `README.md` (+111 lines): appended a comparison table and 13 Q&A blocks below the existing star-history chart.

**Impact:** Lowers the bar for new visitors hitting the README — the comparison-table answer to "is this Claude Code?" is the most common first question. Notable: the FAQ claims 117 skills across 6 categories, which is now slightly stale after the May-17 / May-18 skill landings (119 → 120 in `skills.json` after `competitor-launch-radar` lands).

---

## aaronjmars/aeon-agent

Two substantive PRs from the operator (`@aaronjmars`) merged at May-17 21:58–22:01 UTC, plus the full 24h cron loop — ~50 auto-commits across token-report, fetch-tweets, weekly-shiplog, tweet-allocator, ai-framework-watch, operator-scorecard, star-momentum-alert, repo-pulse, self-improve, feature, and repo-actions runs. The cron commits are not detailed here — they're the agent doing its job — but the artefacts they wrote (articles, dashboard outputs, memory updates) are summarised below.

### Theme 1: Sandbox fix — last enabled-eligible XAI consumer migrated off direct-curl

**Summary:** `token-report`'s step 5 was curling the XAI API directly with `$XAI_API_KEY` in the Authorization header, but the GitHub Actions sandbox blocks env-var expansion inside curl headers — so the skill spent five consecutive days logging "XAI_API_KEY not set" even though the key was set and being used by other skills' prefetch scripts. PR #48 rewrites step 5 to read the most recent `## fetch-tweets` section from `memory/logs/` instead (today's log first, yesterday's as fallback, omit the Social Pulse section entirely if no log within 2 days).

**Commits:**
- `2c47def` — improve: token-report social pulse from fetch-tweets log (#48)
  - Changed `skills/token-report/SKILL.md` (+10, −14): rewrote step 5 (live curl → log-read), explicitly stripped the "XAI_API_KEY not set" line from the report template (data source is now logs, not a live key).
  - Touched the related self-improve outputs and `memory/logs/2026-05-16.md` to record the trigger and PR.

**Impact:** Closes the loop on the four-patch "explicit-marker / cache-read contract" pattern (PR #37 `.error` marker, PR #43 `.truncated` extension, PR #48 fetch-tweets-log fallback, PR #51 today's refresh-x rewrite). All four eliminate misleading "key not set / cache empty" lines that conflate sandbox limitations with real config gaps. `token-report` was the last enabled-eligible XAI consumer still on direct-curl as its primary path.

### Theme 2: product-hunt-launch backport (same-day-after upstream sync)

**Summary:** Verbatim backport of upstream aeon PR #175 (merged May-15). Continues the same-day-after backport pattern (operator-scorecard May-3→4, skill-freshness May-4→5, skill-update-check May-8→9, fork-cohort May-9→10, thread-formatter May-11→12, v4-readiness May-12→13). Drafts the full Product Hunt launch asset pack — tagline ≤60ch / description ≤260ch / first comment ≤500ch / maker comment ≤500ch / six 80ch feature bullets — from live repo state.

**Commits:**
- `c9db544` — feat: product-hunt-launch backport (#49)
  - New file `skills/product-hunt-launch/SKILL.md` (+232 lines): `workflow_dispatch` only, `enabled: false`. Single-section regeneration via `var={tagline,description,first-comment,maker-comment,bullets}`. Same input set as `show-hn-draft` (README, SHOWCASE, skills.json, aeon.yml, last 7d articles/logs, MEMORY.md Skills Built) so HN+PH launches stay coherent. Enforces PH's character ceilings with footer counts, banned-marketing-words list, 5-status exit taxonomy with PARTIAL for missing-input / over-limit cases.
  - Changed `aeon.yml` (+1): registered immediately after `show-hn-draft`.
  - Changed `skills.json` (+11, −1): bumped 86 → 87.

**Impact:** aeon-agent forks now have the same launch-asset surface as upstream — both HN and PH drafts available on dispatch. Pivoted from May-16 idea #3 (which was a false signal — the Skill Health Triad it proposed was already present in aeon-agent).

### Theme 3: Autonomous cron loop (no human intervention)

**Summary:** The agent ran its daily content + intelligence stack end-to-end on schedule. Articles produced this window:
- `articles/repo-article-2026-05-17.md` — Product Hunt launch pre-flight piece (May-17 16:10 UTC)
- `articles/project-lens-2026-05-17.md` — "cron-as-architecture" (May-17 16:10 UTC)
- `articles/token-report-2026-05-18.md` — AEON +41.7% day, ATH at $0.0000984 (May-18 06:34 UTC)
- `articles/weekly-shiplog-2026-05-18.md` — week-over-week roll-up (May-18 09:06 UTC)
- `articles/ai-framework-watch-2026-05-18.md` — RELEASE WEEK, 6 frameworks shipped (May-18 09:06 UTC)
- `articles/operator-scorecard-2026-05-18.md` — 🟡 WATCH verdict (May-18 10:46 UTC)
- `articles/repo-actions-2026-05-18.md` — fresh 5-idea pipeline seeded (May-18 14:48 UTC)

And one self-improve PR opened: `aeon-agent#51` — refresh-x prefetch-cache rewrite, mirroring the token-report fix to the last latent XAI consumer (still `enabled: false`, so the fix is preemptive).

**Impact:** Demonstrates the loop the project has been building toward — daily content writes itself; self-improve identifies and patches its own latent bugs; repo-actions seeds the next day's idea pipeline. Zero human intervention in the window outside of the two PR merges at 21:58–22:01 UTC.

---

## aaronjmars/minitor

Two PRs merged at May-17 21:58:48–21:58:54 UTC (back-to-back within 6 seconds).

### Theme 1: Product Hunt as the 44th column type — completes the launch-monitoring trio

**Summary:** 44th column type, News & web cluster 10 → 11. Fills minitor's "no visibility into the world's #1 launch platform" gap — directly relevant to the operator's own pending PH submission (aeon `product-hunt-launch` shipped May-15, aeon-agent backport shipped today). Keyless `producthunt.com/feed` RSS (PH's GraphQL endpoint needs OAuth + per-app rate caps that aren't usable for a keyless column). Two modes: `today` (full daily slate) and `topic` (5-keyword OR-match cap — AND would zero out queries since PH launches are sparse per day).

**Commits:**
- `0471fae` — feat: producthunt column (#42)
  - New file `lib/integrations/producthunt.ts` (+164 lines): RSS fetcher with em-dash / en-dash title splitter (PH titles ship as `{Product Name} — {tagline}` but use either em or en dash in the wild; ASCII hyphen-minus is reserved for names like "Add-on" and stays inside the product name). Slug extraction from `/posts/{slug}` URLs for canonical `producthunt:{slug}` IDs — same product across multiple fetches collapses to one row in the column store (the feed includes a rolling tail of the previous day's launches).
  - New plugin files `lib/columns/plugins/producthunt/{plugin.ts (+46), server.ts (+25), client.tsx (+130)}`: Zod schema, `#DA552F` brand accent (PH "Rocket" orange, distinct from existing palette), `Rocket` icon, paginated capability, `defaultTitle` that switches to `PH · {first-keyword}` when topic is set.
  - Changed `lib/columns/plugins/manifest.ts` (+2), `lib/columns/registry.ts` (+2), `lib/columns/server-registry.ts` (+2): three registry edits.
  - Changed `README.md` (+3, −3): count 43 → 44, News & web cluster 10 → 11, keyless list updated.

**Impact:** Together with the existing `hacker-news` and `show-hn` columns (and the May-13 PyPI / May-14 crates additions), minitor now covers every major launch-monitoring surface for a dashboard column. The "monitor the launch I'm about to do" use case is now self-served.

### Theme 2: Column-level alert keywords — retrofits highlight + badge across all 43 plugins

**Summary:** Optional `alertKeywords` string on every column — matching items get a yellow inset ring; column header shows a Bell pill badge with the live match count and a tooltip listing the active terms. Works with all 43 existing plugins on day one because the value is a column-level property (sibling to `title`), never sent to server fetchers — sidesteps every plugin's strict Zod schema.

**Commits:**
- `428ee22` — feat: column-level alert keywords with highlight + badge (#41)
  - New file `lib/columns/keyword-match.ts` (+51 lines): `parseAlertKeywords` (comma/semicolon/whitespace separators, 64-char-per-term cap, 16-term cap, deduped, lowercased) and `itemMatchesAlertKeywords` (wide haystack — author name + handle + content + URL).
  - New migration `drizzle/0001_alert_keywords.sql` (+1 line, additive nullable column): `ALTER TABLE "columns" ADD COLUMN "alert_keywords" text;`. Existing decks import cleanly without the field.
  - Changed `app/actions.ts` (+31, −1): `updateColumnAlertKeywords` server action + export/import round-trip + `loadSnapshot` wiring (existing deck export/import shipped May-15 now carries `alertKeywords` with backward-compat).
  - Changed `lib/store/use-deck-store.ts` (+24): `updateAlertKeywords` store action + import wiring.
  - Changed `components/column/column-card.tsx` (+47, −3): `useMemo` parsed terms + match set, yellow ring wrap around matched items, Bell badge in the header.
  - Changed `components/column/configure-column-dialog.tsx` (+51, −1): new form field.
  - Changed `lib/columns/types.ts` (+7) and `lib/db/schema.ts` (+1): type additions.

**Impact:** The first feature that crosses every plugin without per-plugin work — a true column-axis primitive. Three days after deck export/import (May-15), this is the second "retrofitted feature" to land — both pieces designed to share between operators. Honest naming: badge is "matches in current visible window" — no new read/unread persistence layer (intentional to avoid scope creep).

---

## Developer Notes

- **New dependencies:** None added in this window. All new code uses already-vendored libs (Zod, drizzle-orm, lucide-react, `@/lib/integrations/rss` for RSS parsing).
- **Breaking changes:** None. The minitor migration is additive (nullable text column); existing decks export-import cleanly with or without `alertKeywords`. The aeon dashboard fix preserves the existing default-remote behaviour when no `-R` is needed.
- **Architecture shifts:**
  - Fork-intelligence layer matured into a 5-skill cluster with composable state-file chaining: `fork-cohort` → `fork-skill-gap` reads its `forks` list when fresh, `fork-first-run-alert` reads its ACTIVE/POWER set, `fork-release-tracker` operates independently. All three new skills include the live `gh api` fallback so they work without the upstream cache.
  - Sandbox-marker pattern hardened: PR #48 (token-report log-fallback) completes the four-patch sequence that started May-10 with the `.error` marker. Pattern is now: sandbox-blocked auth steps write a typed marker, downstream skills read the marker rather than re-curling.
- **Tech debt:**
  - aeon's README FAQ (`#177`) cites "117 skills" — already stale by 2 (`fork-skill-gap` + `fork-first-run-alert` = 119; `competitor-launch-radar` PR #183 will bring it to 120). A future docs sweep should make this number a placeholder generated from `skills.json`.
  - aeon-agent's `skills.json` count is on a parallel track from upstream (87 → 88 today, vs. upstream's 119 → 120). The 22-PR catchup PR #44 (May-14) closed the bulk of the gap; backports are now incremental.
  - Minitor TypeScript compilation was not verified inside the sandbox for the producthunt PR (the feature run log notes this). Manifest parity check in `server-registry.ts` will throw loudly at init if any registry drifts.

## What's Next

- **`fork-first-run-alert` and `fork-skill-gap` first execution** — both `enabled: false` at merge. First natural Sunday run May-24 for `fork-skill-gap`; daily 20:30 UTC for `fork-first-run-alert` once the operator flips the switch. Backfill behaviour is the load-bearing safety check — the first run should populate seen-state without flooding alerts.
- **aeon-agent PR #50** — `fork-first-run-alert` backport landed in the same `2026-05-18` cron window (`feature` skill picked it as the same-day-after candidate); it's the corresponding `enabled: false` skill on the fork-side.
- **aeon-agent PR #51 (refresh-x prefetch-cache rewrite)** — open from today's self-improve run, mirroring PR #48. Latent fix (refresh-x is `enabled: false`) but completes the explicit-marker contract across every XAI consumer in aeon-agent.
- **aeon PR #183 (competitor-launch-radar)** — opened today by the `feature` skill; weekly Monday 10:00 UTC scan of PH RSS + HN Algolia for new AI-agent-framework launches outside the 9-framework cohort. Closes the last open May-16 idea for aeon and slots under `ai-framework-watch` to complete the Monday-morning intelligence stack.
- **minitor PR #43 (github-discussions column)** — opened today; GraphQL-only column for the GitHub Discussions Q&A surface, completes the GitHub cluster at 10 columns. Closes the last open May-16 idea for minitor.
- **Open thread:** README FAQ skill count (117 → 119 → 120). Manual docs edit or skill that regenerates the section from `skills.json` would close the drift.
