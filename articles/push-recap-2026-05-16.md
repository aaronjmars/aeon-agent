# Push Recap — 2026-05-16

## Overview

Three substantive commits landed in the last 24h, one in each watched repo, and all three trace back to a single thread: today was completion day for two May‑14 ideas and a self-improvement triggered by five straight days of misleading log output. Two of the three commits close out the fork-intelligence layer and the column-alerting layer respectively; the third is the agent fixing its own daily report after spotting a recurring false-positive in its own logs.

**Stats:** ~15 files changed, +806/-21 lines across 3 author commits (cron auto-commits excluded — ~26 across 13 daily skill runs in aeon-agent, scheduler work, not author work)

---

## aaronjmars/aeon

### Fork-intelligence layer reaches its fourth and final skill

**Summary:** The fork-intel quartet that started with `fork-cohort` (May 10), continued with `fork-release-tracker` (May 12) and `contributor-spotlight` (May 9), now has its fourth corner: `fork-skill-gap`. Each of the first three answers a different fork question — *is the fork alive? has it shipped a release? who's pushing code?* — but none answered the most direct operator question, *what's in upstream that I haven't adopted yet?* This skill closes that gap with a weekly Sunday 21:00 UTC digest.

**Commits:**
- `93b9e4d` — feat: fork-skill-gap skill (PR #176)
  - **New file** `skills/fork-skill-gap/SKILL.md` (+304 lines): full 11-step skill with 8-status exit taxonomy (OK / QUIET / DRY_RUN / NO_ACTIVE / NO_UPSTREAM_MANIFEST / PARENT_CHANGED / API_FAIL / BAD_VAR). State persists at `memory/topics/fork-skill-gap-state.json` keyed by `owner/repo`, with per-fork records of `{missing_count, missing_slugs (cap 50), top_missing_categories, last_seen, classification_source}`.
  - Changed `aeon.yml` (+1 line): registers `fork-skill-gap` as Sunday 21:00 UTC, `enabled: false`, `claude-sonnet-4-6`, with var support for `dry-run` and `owner/repo` parent override.
  - Changed `skills.json` (+13/-1): total bumped 118 → 119 with the new entry slotted between `fork-skill-digest` and `github-issues`.

**Design substance — why this skill is interesting beyond the headline:**
- **Graceful degradation, both directions.** Reads `memory/topics/fork-cohort-state.json` when fresh (≤8 days old) to target only POWER+ACTIVE forks — the audience that actually cares about gaps. When cohort state is missing, stale, or this is the first ever run, it falls back to live `gh api .../actions/runs?per_page=1` per fork and builds its own POWER+ACTIVE list from scratch using the same ≥1-run-in-7d activation rule. Result: works on day one before `fork-cohort` is enabled, accelerates once it is.
- **Manifest-absent ≠ zero adoption.** A fork with no `skills.json` is marked unreadable rather than recorded as "missing 119 skills" — avoids inflating the gap metric on forks that haven't shipped the manifest yet.
- **Inverse view in the article.** The body includes a top-10 rollup of upstream slugs most frequently *unadopted* across the readable fork population — upstream now has a signal for which new shipments are launching into silence, which is exactly the second-order question this skill enables.
- **Quiet-week gate.** Suppresses notify when all readable forks are within 5 skills of upstream AND prior state exists AND no new top-missing slug surfaced — same calm-by-default pattern the other three fork-intel skills use.
- **Read-only across the fleet.** Never opens issues on fork repos, never auto-edits anything. Slug values are JSON-parsed only — no shell interpolation, no description rendering.

**Impact:** Operators of the 56 forks (as of today) now have a single Sunday-evening read on what they're missing from upstream — the first surface in any direction that quantifies skill drift, which is otherwise invisible until someone notices six months later that their agent isn't doing what everyone else's is. Upstream gets the reverse signal: which new shipments are getting picked up by the fleet and which aren't. Picked from May‑14 repo-actions idea #3.

---

## aaronjmars/aeon-agent

### Self-improve: token-report finally tells the truth about its own missing data

**Summary:** For five consecutive days (May 13–16) every `token-report` run has emitted `Social: XAI_API_KEY not set — no social data` even though `XAI_API_KEY` is set and being consumed daily by the `fetch-tweets` and `tweet-allocator` prefetch scripts. The root cause is the same sandbox limitation that's bitten three previous skills: bash inside Claude's sandbox doesn't expand `$XAI_API_KEY` inside curl headers, so the call fails, and the SKILL.md misreads that failure as "key isn't set." `self-improve` caught the pattern this morning and rewrote the broken step.

**Commits:**
- `e0264aa` — improve: token-report social pulse from fetch-tweets log
  - Changed `skills/token-report/SKILL.md` (+10/-14): step 5 rewritten end-to-end. The direct `curl https://api.x.ai/v1/responses ... -H "Authorization: Bearer $XAI_API_KEY"` block is gone. In its place: locate the most recent `## fetch-tweets` (or `## Fetch Tweets`) section in `memory/logs/`, check today's log first (only useful when token-report runs *after* fetch-tweets — default cron order is the reverse: token-report 06:00 UTC, fetch-tweets 06:30 UTC), fall back to yesterday's log, extract 2–3 themes weighted by likes/RTs/replies, and append `via fetch-tweets log YYYY-MM-DD` to mark freshness. If no fetch-tweets section exists in the last 2 days, **omit the Social Pulse section entirely** — explicitly drops the misleading "XAI_API_KEY not set" line from the template.
  - Changed `skills/token-report/SKILL.md` template (step 6): the previous `or "XAI_API_KEY not set, social data unavailable"` fallback string is replaced with explicit "omit this entire section" instructions.
- `4ffd20b` — chore(memory): log self-improve PR #48 + open-PR index update (+2/-1)

**Design substance:**
- **Pattern parallel.** The skill's commit message and the memory log both reference two prior patches of the same shape: aeon-agent PR #43 (May 14, extending `.xai-cache/<file>.truncated` reader to narrative-tracker / remix-tweets / tweet-roundup) and aeon-agent PR #37 (May 10, tweet-allocator `.error` marker contract). All three patches eliminate misleading "key not set" / "cache empty" lines that conflated sandbox limitations with config gaps. The agent is now consistently routing sandbox failures to explicit log markers rather than silent miscategorisation.
- **No new dependency.** Reads memory it already writes daily; the data path was already in place from fetch-tweets' own self-correction last week.
- **Honesty in absence.** Section omission beats a misleading line that survived 5 days of daily runs without an operator noticing because the line was technically syntactically correct.

**Impact:** Once PR #48 merges, the Social Pulse section either contains real social-signal extract or it's silently absent — never again a confidence-eroding "XAI_API_KEY not set" line on a system where that key has been set for weeks.

### Scheduler healthy — 13 daily skill runs auto-committed cleanly

`fa65a24 chore(cron): repo-actions success` and ~25 sibling chore commits show every expected daily skill ran clean: token-report, fetch-tweets, tweet-allocator, repo-pulse, hyperstitions-ideas, star-momentum-alert, feature, self-improve, repo-actions, plus the late-yesterday tail of project-lens, repo-article, thread-formatter, star-milestone, push-recap, heartbeat. No failed runs in the 24h window, no `chore(failure)` commits, no `<<TBD>>` placeholders left in any auto-committed memory log. (The one outstanding placeholder is in the self-improve log entry's PR URL line — the agent self-noted it as TBD because PR #48 was opened in the same run that wrote the log.)

---

## aaronjmars/minitor

### First user-customizable signal layer on top of every column type

**Summary:** Minitor's 43 column plugins all do one thing: fetch a feed, render it, refresh on schedule. They have no concept of "the user cares about this particular row more than the others." PR #41 introduces an optional `alertKeywords` string at the column level — match-on-substring across author/handle/content/URL — that highlights matched rows with a yellow inset ring and surfaces a live match count badge in the column header. Crucially, the value lives as a column-level property (sibling to `title`), never gets sent to server fetchers, so it works with all 43 plugins on day one without touching any plugin's strict Zod schema.

**Commits:**
- `39ac37d` — feat: column-level alert keywords with highlight + badge (+469/-6, 10 files)
  - **Schema + migration** (`lib/db/schema.ts`, `drizzle/0001_alert_keywords.sql`, `drizzle/meta/_journal.json`, `drizzle/meta/0001_snapshot.json`): additive `alert_keywords` nullable `text` column on `columns`. Snapshot version 7, journal idx 1, breakpoints on. Pre-feature decks import cleanly because the column is nullable.
  - **New file** `lib/columns/keyword-match.ts` (+51 lines): exports `parseAlertKeywords(raw)` and `itemMatchesAlertKeywords(item, terms)`. Parser normalises comma/semicolon/whitespace separators uniformly, lowercases everything, dedupes via `Set`, drops terms over 64 chars, and caps the parsed array at 16 terms. Matcher concatenates `content + author.name + author.handle + url` into a single lowercased haystack and does a substring includes check — wide-by-design so `aaronjmars/aeon` matches a GitHub column even when the title's been shortened.
  - **Types + server actions** (`lib/columns/types.ts`, `app/actions.ts`): `Column.alertKeywords?: string` added; new `updateColumnAlertKeywords(id, alertKeywords)` server action truncates to 512 chars and stores `null` for empty. `exportDeck`/`importDeck` round-trip `alertKeywords` with backward compat (Zod schema marks the field `.optional()`, so pre-feature deck JSON imports cleanly). `loadSnapshot` reads the field through.
  - **Store** (`lib/store/use-deck-store.ts`): new `updateAlertKeywords(columnId, alertKeywords)` action mirrors the server-side 512-char clamp, updates the in-memory column atomically, and fires the server action via the existing `fireAndLog` pattern.
  - **UI** (`components/column/column-card.tsx`, `components/column/configure-column-dialog.tsx`): `useMemo` builds a `Set<string>` of matched item IDs whenever `alertKeywords` or `column.items` changes. Each matched item gets wrapped in a `<div data-alert-match="true">` with yellow ring styling; the column header shows a `Bell` icon + tabular-num count chip with a tooltip listing the active terms. Configure dialog gets an "Alert keywords" `Label` + `Input` with the parsed-term preview count and the same 512-char `maxLength` as the server-side clamp.

**Design substance:**
- **Column-level not config-level.** The May-14 idea proposed `BaseColumnConfig.alertKeywords` but no such base interface exists in the codebase — every plugin defines its own strict config schema independently. Lifting `alertKeywords` to the `Column` type itself sidesteps every plugin's Zod schema; the value never travels to the server fetchers at all.
- **Match scope intentionally wide.** Author name + handle + content + URL all participate in the haystack. URL participation is the design choice that pulls weight — it lets `aaronjmars/aeon` highlight rows in a GitHub-flavoured column even when the rendered title was shortened.
- **Honest naming.** The badge is "matches in current visible window" — no new read/unread persistence layer, no notification escalation, no hidden state. What you see in the column is what the badge counts.
- **Capacities documented as code.** `ALERT_KEYWORDS_MAX = 512` on the input; 16-term cap and 64-char-per-term cap in `parseAlertKeywords`; client and server enforce the 512-char clamp independently so a direct server-action call can't bypass UI limits.
- **Forward-compat on export/import.** Unknown `typeId`s already imported cleanly (renders as unknown column); now `alertKeywords` rides along the export JSON v1 without breaking the existing schema — pre-feature deck JSON has no `alertKeywords` key, post-feature import treats absence as `null`.

**Impact:** Every Minitor user can now annotate any column with a watchlist of terms — a project name, a contract address, a Twitter handle, a repo slug — and matching rows surface visually without polling alerts, push notifications, or read-state machinery. This is the first user-customisable signal layer in the app, and because it's column-level it composes with deck export/import (yesterday's PR #40), so a curated deck can ship with pre-filled alert terms attached. Picked from May‑14 repo-actions idea #4.

---

## Developer Notes

- **New dependencies:** None across the three repos. Every diff is pure stdlib / existing-dep work.
- **Breaking changes:** None. `minitor`'s migration is additive (nullable column); aeon's skills.json bump is additive; aeon-agent's self-improve narrows behaviour (less misleading output, no removed step).
- **Architecture shifts:**
  - aeon: fork-intelligence is now a 4-skill stack with composable state files. `fork-skill-gap` is the first member to *read* `fork-cohort-state.json` as a cache, establishing the pattern that the Sunday-evening intel slots can chain off each other's state instead of all re-querying the GitHub API.
  - minitor: first column property that lives outside `config` — `alertKeywords` is a sibling to `title`. Future per-column UX hooks (visibility, pin-state, custom item formatting) now have a paved path to follow.
- **Tech debt:** The `<TBD>` PR-URL placeholder in `memory/logs/2026-05-16.md` self-improve section is the only loose end visible in today's diffs — agent wrote the log before the PR URL existed, didn't backfill. Self-correcting on next memory edit.
- **Self-improve pattern hardening:** Three skills now use the explicit-marker pattern for sandbox-blocked code paths (tweet-allocator `.error`, narrative-tracker/remix-tweets/tweet-roundup `.truncated`, today's token-report fetch-tweets-log fallback). This is congealing into a generalisable contract — sandbox-blocked steps should leave a typed marker rather than silently degrade or emit a misleading config-related line.

## What's Next

- **PR #176 (aeon)** ships `fork-skill-gap` `enabled: false` — first Sunday it could fire is **2026-05-17** (tomorrow). With `fork-cohort` still disabled in aeon.yml, the skill's first live run will execute its API-fallback path; once `fork-cohort` is enabled (still in the URGENT priority list) the two will chain.
- **PR #48 (aeon-agent)** is a small self-improve — likely merges within a day, and the next morning's `token-report` will demonstrate either the new section or its honest absence depending on whether yesterday's `fetch-tweets` log is still in the 2-day window.
- **PR #41 (minitor)** is the biggest landing — 10 files, additive migration, hits every column on the dashboard. Likely needs a manual schema-push step in deploy (`pnpm db:push` or equivalent) once merged. No follow-up PR visible yet for "deck gallery surfaces alertKeywords pre-fills," but the export/import round-trip is wired so that's a future easy lift.
- **May-14 ideas: fully consumed.** Idea #1 (Product Hunt skill, PR #175), #2 (skill-enabler, PR #47), #3 (fork-skill-gap, PR #176), #4 (column-alert-keywords, PR #41), #5 (deck export/import, PR #40) all shipped between May 15 and May 16. May-16 generated the next batch of 5 ideas; May-17+ pipeline starts from there.
- **No open branches with unmerged commits** beyond the three PR branches above. The author-side work this 24h is exactly three PRs, all green, none stalled, all opened today.
