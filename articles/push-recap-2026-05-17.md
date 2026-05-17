# Push Recap — 2026-05-17

## Overview

Four substantive commits landed in the last 24h across the three watched repos, and three of them are tightly correlated: two repos shipped Product Hunt launch infrastructure within four minutes of each other, while aeon added the daily counterpart to its weekly fork-cohort scan. The fourth is the only hand-written push of the day — a small but well-targeted fix from the operator that hardens the dashboard's `gh` CLI calls against multi-remote setups.

**Stats:** 17 files changed, +984/-18 lines across 4 author commits (cron auto-commits excluded — ~30 across the daily aeon-agent skill runs).

---

## aaronjmars/aeon

### Fork-intelligence layer adds its fifth skill — same-day activation alerts

**Summary:** `fork-cohort` (Sunday 19:00 UTC) already names the weekly fork-activation transition `NEW_ACTIVE`, but a fork that activates on a Monday morning sits in the void for up to six days before anyone notices. The new `fork-first-run-alert` skill closes that gap with a daily 20:30 UTC cron that diffs the cohort's ACTIVE set against a persistent seen-list and emits per-fork named alerts the day each fork first runs.

**Commits:**
- `988e385` — feat: fork-first-run-alert skill (PR #179)
  - **New file** `skills/fork-first-run-alert/SKILL.md` (+285 lines): full 11-step skill with 7-status exit taxonomy (OK / QUIET / DRY_RUN / NO_STATE / API_FAIL / PARENT_CHANGED / BAD_VAR). State persists at `memory/topics/fork-first-run-state.json` with a `seen` map keyed by `owner/repo`, each entry recording `first_seen_active_at`, `first_seen_active_run_at`, `announced_at`, and `stargazers`. LRU cap of 500 entries — oldest dropped by `announced_at` once full.
  - Changed `aeon.yml` (+1 line): registers `fork-first-run-alert` as daily 20:30 UTC, `enabled: false`, `claude-sonnet-4-6`, with `var` accepting `dry-run` and/or an `owner/repo` parent override. Slotted right after `contributor-spotlight` (Sunday 20:00 UTC) so on weekly day the two run back-to-back.
  - Changed `skills.json` (+13/-1): total bumped 118 → 119 with the new entry placed alongside the other four `fork-*` skills.

**Design substance — beyond the headline:**
- **Two-tier data sourcing with graceful degradation.** Reads `memory/topics/fork-cohort-state.json` first when fresh (≤8 days) and uses the cached ACTIVE/POWER list — zero per-fork API hits on the fast path. Falls back to live `gh api repos/{parent}/forks --paginate` + per-fork `actions/runs?per_page=1` when the cohort state is missing, stale, or scoped to a different parent. Result: works on the first ever run, before `fork-cohort` is enabled in aeon.yml.
- **Canonicalised seen-list.** Fork slugs lowercase-normalised before being checked against and written to the seen-list, so a stray casing drift in the GitHub API response can't double-alert on the same fork.
- **Count-driven notification policy.** 1–3 new activators get individual named alerts (`"Fork speend/aeon just ran its first workflow"`). 4+ get collapsed into a single batch notification with an 8-row cap and a `"… and N more"` footer. Prevents loud signal-floods on backfill or batch-activation days.
- **First-ever-run backfill mode.** On a cold-start run with no prior state file, the skill populates the seen-list with the current ACTIVE/POWER set *without* firing per-fork alerts. Prevents a noisy day-one announcement for forks that have been alive for weeks but weren't tracked.
- **Bot allowlist.** `dependabot[bot]`, `github-actions[bot]`, and `aeonframework` are added to seen but suppressed from operator-facing alerts. They count toward the total but never page anyone.
- **Read-only across the fleet.** Never opens issues or comments on fork repos. Every output is in this repo's own state file, log, and notification channel.
- **80-fork live-fallback cap.** Same budget guard `fork-cohort` uses — prevents a runaway API spend if the parent's fork count balloons unexpectedly.

**Impact:** The fork-intelligence layer is now a **five-skill stack** — `fork-cohort` (is the fork alive?), `fork-release-tracker` (has it shipped a release?), `contributor-spotlight` (who's pushing code?), `fork-skill-gap` (what's it missing from upstream?), and now `fork-first-run-alert` (did a new one just turn on?). The activation moment — secrets configured, workflow successfully completed — is the highest-signal community event Aeon emits, and it now gets surfaced same-day instead of waiting for the weekly cron. Picked from May‑16 repo-actions idea #4.

### Dashboard analytics + runs routes hardened for multi-remote setups

**Summary:** The dashboard's three `gh run` API routes (`/api/analytics`, `/api/runs`, `/api/runs/[id]/logs`) all shelled out to `execSync('gh run list …')` with the literal command string built via interpolation. That's fine on a fresh clone with one remote — but on a repo with multiple remotes (a fork of a fork, a clone with both `origin` and `upstream`), `gh` falls back to a prompt or picks the wrong default, breaking the entire dashboard for those installs. PR #178 fixes both halves of the problem: route every `gh` call through `execFileSync` with an argv array (kills the interpolation surface entirely) and add an autodetected `-R <owner/repo>` flag from `gh repo set-default --view` with a `gh repo view --json nameWithOwner` fallback.

**Commits:**
- `4e42dbe` — fix(dashboard): pass -R repo to gh run list/view so multi-remote setups work (PR #178, +67/-13, 3 files)
  - `dashboard/app/api/analytics/route.ts` (+21/-3): new `ghRepo()` + `ghArgsRepo()` helpers, `execSync` swapped for `execFileSync` on the `gh run list` invocation.
  - `dashboard/app/api/runs/route.ts` (+21/-3): same helper added, same `execFileSync` swap on the 20-row recent-runs query.
  - `dashboard/app/api/runs/[id]/logs/route.ts` (+25/-7): same helper trio, but two `gh run view` calls — the metadata fetch and the log-stream fetch — both go through `execFileSync`, and the `--log-failed` vs `--log` switch is now an array element rather than a ternary inside an interpolated string.

**Design substance:**
- **Argv arrays, not strings.** Every `execSync('gh … ${something}')` is gone. `execFileSync('gh', ['run', 'list', ...])` is the new shape across all three routes. No shell parsing in the path between user input and the `gh` subprocess.
- **Two-tier repo detection.** `gh repo set-default --view` is the canonical answer when the operator has set a default; `gh repo view --json nameWithOwner` is the working-tree fallback when no default is set. Both wrapped in try/catch returning `null`, so the routes still work on installs where neither succeeds — the `-R` flag is simply omitted and `gh` falls back to its default behaviour.
- **One author commit.** This is the **only** non-feature-bot push across all three repos today. It's `@aaronjmars` hand-typing a fix that surfaced in actual use — a sharper-edged signal than any of the skill-bot output, even though it's smaller.

**Impact:** The dashboard analytics page (and the deeper run-detail + log views) now work on every kind of local install — fresh clones, forks, multi-remote setups, repos where the canonical upstream isn't the operator's `origin`. The interpolation removal is a secondary security win: no path between an HTTP request and a `gh` subprocess passes through shell parsing.

---

## aaronjmars/aeon-agent

### Product Hunt launch drafter backported from upstream — the second half of the launch playbook

**Summary:** The `product-hunt-launch` skill shipped on aeon two days ago (May 15, PR #175) as a workflow_dispatch one-shot that drafts the full PH launch asset pack from live repo state. Today's PR backports it verbatim to aeon-agent, continuing the same-day-after backport pattern that's already brought over operator-scorecard (May-3→4), skill-freshness (May-4→5), skill-update-check (May-8→9), fork-cohort (May-9→10), thread-formatter (May-11→12), and v4-readiness (May-12→13).

**Commits:**
- `3bfa737` — feat: product-hunt-launch backport (PR #49, +244/-1, 3 files)
  - **New file** `skills/product-hunt-launch/SKILL.md` (+232 lines, verbatim from upstream): drafts the five paste-ready sections an operator submits to PH on launch day — `tagline` (60 chars), `description` (260 chars), `first-comment` (500 chars), `maker-comment` (500 chars), and six 80-character feature `bullets`. Single-section regeneration via `var={tagline,description,first-comment,maker-comment,bullets}`. Five-status exit taxonomy with `PARTIAL` covering both missing-input and over-limit-after-tightening cases.
  - Changed `aeon.yml` (+1 line): registers the skill immediately after `show-hn-draft` so the HN + PH launch playbook lives in adjacent lines and is easy to find when an operator is composing both.
  - Changed `skills.json` (+11/-1): total bumped 86 → 87 with the new entry placed in the dev cluster.

**Design substance (inherited from upstream):**
- **Same input set as `show-hn-draft`.** README, SHOWCASE.md, skills.json, aeon.yml, last 7 days of repo-articles and project-lens articles, last 7 days of logs, and `MEMORY.md`'s Skills Built table — so the two launch surfaces stay coherent. The HN crowd skim-reads technical lede; PH skim-reads "is this useful to me right now." Same evidence base, two different framings.
- **Enforces PH's actual character ceilings.** Tagline ≤60 chars, description ≤260, comments ≤500, bullets ≤80 each. Counts emitted in the notification footer so the operator catches over-limit sections before pasting into the PH form.
- **Banned-marketing-words list.** Strips `AI-powered`, `revolutionary`, `leverages`, `powerful`, `framework` — saturated on PH, immediate signal that the asset was written by AI rather than the maker.
- **Operator checklist, not action.** The skill appends a checklist (Tue/Wed/Thu 12:01 AM PT submission slot, logo/gallery specs, hunter outreach, first-comment 5-min rule, cross-post sequencing) — but explicitly does **not** post anything. Asset prep only.
- **workflow_dispatch + `enabled: false`.** Same shape as `show-hn-draft`. Operator triggers it once when launch is on the calendar, gets the asset pack, reviews and pastes.

**Impact:** aeon-agent now has the same launch-day asset coverage as aeon — both HN draft and PH draft, both on workflow_dispatch, both with single-section regeneration. The two launches that have to happen close in time (HN within 24h of PH so the cross-traffic stacks) now have their write-ahead done in the same repo where the agent runs. Pivot from May-16 repo-actions idea #3 (Skill Health Triad backport) — investigation found skill-health, skill-evals, and skill-repair were already present in aeon-agent, so the same-day-after backport pattern was applied to the May-15 upstream skill instead.

### Scheduler healthy — daily skill runs all green

The auto-commit stream this 24h looks like every other healthy day: ~30 `chore(cron): <skill> success` and `chore(scheduler): update cron state` pairs across the day, no `chore(failure)` commits, no skill-bot exited with a non-`OK` status. token-report, fetch-tweets, tweet-allocator, repo-pulse, star-momentum-alert, feature, push-recap (yesterday's), and the 16:20–19:30 UTC tail of project-lens / repo-article / thread-formatter / heartbeat all landed clean. No `<TBD>` placeholders left in any memory log — yesterday's self-improve TBD line about PR #48 self-resolved when the PR URL was backfilled.

---

## aaronjmars/minitor

### 44th column type ships — Product Hunt, the launch surface minitor was missing

**Summary:** Minitor's columns now cover HN, Lobsters, Stack Overflow, DEV.to, npm, PyPI, crates.io, and a dozen GitHub surfaces — but until today there was no visibility into the **#1 launch platform**, the very same platform the aeon repo is preparing to submit to (aeon PR #175 + aeon-agent PR #49 both ship the asset drafter). Today's PR closes that gap with a keyless RSS-based Product Hunt column — operator can now drop a Product Hunt column into their dashboard and watch their own launch day rank update in real time alongside the other distribution surfaces.

**Commits:**
- `32f5090` — feat: producthunt column (PR #42, +374/-3, 8 files)
  - **New file** `lib/integrations/producthunt.ts` (+164 lines): keyless fetcher. The frontpage feed at `https://www.producthunt.com/feed` is the stable surface — PH's GraphQL API requires OAuth with per-app rate caps that aren't usable for a keyless dashboard. The fetcher parses the `{name} — {tagline}` title shape on **both** em-dash (U+2014) and en-dash (U+2013) bounded by whitespace, falling through to the raw title as the product name when neither separator appears. Extracts the PH slug from `/posts/{slug}` URLs to build a canonical `producthunt:{slug}` ID — the same product reappearing in the rolling 24-hour tail collapses to one row in the column store instead of duplicating on every fetch.
  - **New file** `lib/columns/plugins/producthunt/plugin.ts` (+46 lines): Zod schema with two modes — `today` (full daily slate) and `topic` (keyword-filtered). `#DA552F` PH-brand orange accent (distinct from hacker-news flame, substack `#ff6719`, devto `#3b49df`, npm `#CB3837`, pypi `#3776AB`, crates `#DEA584`). `Rocket` icon from lucide-react. `defaultTitle` resolves the user's first keyword as the column tag (`"PH · ai-agents"`) when in topic mode.
  - **New file** `lib/columns/plugins/producthunt/server.ts` (+25 lines): adapter that wires `fetchProductHuntPage` into the per-column server registry.
  - **New file** `lib/columns/plugins/producthunt/client.tsx` (+130 lines): renderer with the product name + tagline split, PH-orange `Rocket` accent on each row.
  - Changed `lib/columns/plugins/manifest.ts`, `lib/columns/registry.ts`, `lib/columns/server-registry.ts` (+2 each): the three-line manifest dance every plugin requires.
  - Changed `README.md` (+3/-3): News & web cluster count 10 → 11, total column types 43 → 44, keyless API list updated.

**Design substance — the five integration quirks:**
- **Em-dash and en-dash title split.** PH titles ship as `{Product Name} — {tagline}` but the wild data uses both U+2014 and U+2013, with whitespace boundaries. The regex `/^(.+?)\s+[—–]\s+(.+)$/` matches both. ASCII hyphen-minus stays inside the product name (e.g. `Add-on` correctly stays whole), and titles that don't match the shape at all fall through to raw-title-as-product-name rather than dropping the row.
- **Canonical `producthunt:{slug}` IDs.** PH's feed includes a rolling tail of the previous day's launches, so the same product appears in multiple fetches. The plugin extracts the slug from `/posts/{slug}` URLs and uses it as the canonical ID — the column store dedupes on the same row instead of accumulating copies.
- **OR-match across keywords, not AND.** Topic mode accepts up to 5 keywords via comma/semicolon/space separation. AND-matching would zero out almost every query — PH launches are sparse per day, so an OR-match across name + tagline + description + URL is the correct shape. URL participation is the same wide-haystack design choice as yesterday's column-alert-keywords PR.
- **RSS over GraphQL, deliberately.** PH used to expose a public GraphQL endpoint, but the current version requires OAuth + per-app rate caps that are incompatible with a keyless dashboard. RSS lags a few minutes behind the live frontpage but covers the same daily set with zero auth surface.
- **Slice-based pagination via existing helper.** Fetches a generous batch once, hands out `PAGE_SIZE` per Load-more call using the existing `sliceForPage` helper. Two modes share the same fetch path — the mode-as-string-union shape is a forward extension point for future per-topic RSS or leaderboard scraping.

**Impact:** The dashboard now covers the **three major launch + distribution surfaces** end-to-end: HN (via the `hacker-news` column), Product Hunt (today), and DEV.to (via the `devto` column from May 10). When aeon's PH submission goes live, the operator can pin a `PH · ai-agents` column right next to their existing `HN · top` and watch both feed-rank in the same dashboard view without flipping tabs. News & web cluster is now 11 of the dashboard's 44 column types — the largest single cluster by plugin count. Picked from May‑16 repo-actions idea #1.

---

## Developer Notes

- **New dependencies:** None across the three repos. `producthunt.ts` reuses the existing `fetchFeed` RSS integration helper that npm and pypi already share. `fork-first-run-alert` uses `gh api` exclusively — already a hard dependency of the aeon workflow.
- **Breaking changes:** None. All four PRs are additive — three new files + manifest edits, plus one swap of `execSync` for `execFileSync` that is strictly safer than the previous shape.
- **Architecture shifts:**
  - aeon: the fork-intelligence layer is now a **five-skill stack** with state-file composition. `fork-first-run-alert` reads `fork-cohort-state.json` as a cache (joining `fork-skill-gap` from yesterday in that pattern). The Sunday-evening fork-intel slots can now genuinely chain off each other's state instead of all re-querying the GitHub API.
  - aeon-agent: launch-asset coverage now matches upstream — both HN draft and PH draft live in `skills/`, both gated behind `workflow_dispatch + enabled:false`, both with single-section regeneration. The launch playbook (HN within 24h of PH for cross-traffic) is now write-ahead-done in the repo where the agent runs.
  - minitor: news & web cluster is now the largest of any plugin family at 11 columns. The four-registry layer (npm + pypi + crates + producthunt across May 12 / 13 / 14 / 17) is the bracketing of "where developers and operators find new things" — package registries on three runtimes plus the launch-platform itself.
- **Tech debt:** None visible in today's diffs. Yesterday's `<TBD>` PR-URL placeholder in `memory/logs/2026-05-16.md` self-resolved when the URL was backfilled.
- **Sandbox / shell surface:** The aeon dashboard fix (PR #178) eliminates the last `execSync('gh …${interpolated}')` call paths in the dashboard API routes. `execFileSync` with argv arrays is the new standard shape across those three routes.

## What's Next

- **PR #179 (aeon)** ships `fork-first-run-alert` `enabled: false` — daily 20:30 UTC slot is set, but no cron will fire until the flag flips. Once enabled, the very first run will execute the backfill path (no per-fork alerts) and seed the seen-list with the current ACTIVE/POWER set. From the *second* run onward, any genuinely new mid-week activation pages the operator same-day.
- **PR #178 (aeon)** is the most boring-looking and the most immediately useful — fix for an actual usage bug. Likely fast merge, no follow-up needed.
- **PR #49 (aeon-agent)** is a verbatim backport — no risk surface, expected to merge into the same-day-after backport stream. Note a tiny conflict potential with prior aeon-agent PRs that also bump `skills.json` to 87; the merge is mechanical.
- **PR #42 (minitor)** is the biggest landing — 8 files, all additive, no migration. Fits the existing keyless-column pattern (npm, pypi, crates, devto, lobsters, hacker-news). No deploy surprises expected.
- **May-16 ideas remaining (open):** #2 GitHub Discussions column (minitor, completes GitHub cluster 10/10), #5 Competitor Launch Radar (aeon, weekly PH+HN scan for new AI agent frameworks). May-16 #3 (Skill Health Triad backport) was a false signal — already complete in aeon-agent.
- **Cross-cutting pattern this 24h:** **launch-day prep convergence**. aeon-agent and minitor both shipped Product Hunt infrastructure within four minutes of each other (11:23 / 11:26 UTC) — clearly a single feature-dispatch wave that picked PH from two different angles (asset drafter in aeon-agent, monitoring column in minitor). aeon's fork-first-run-alert lands 5 minutes earlier (11:18 UTC), bringing the trio of skill-bot pushes inside an 8-minute window. The fourth commit (PR #178, dashboard fix) is the only hand-written one and shows up earlier in the day (08:06 UTC) — the operator's own work pre-empted the agent wave by ~3 hours.
