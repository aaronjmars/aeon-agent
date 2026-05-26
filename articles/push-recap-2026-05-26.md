# Push Recap — 2026-05-26

## Overview
A registry-and-leaderboard day across the fleet. The headline is a new **fleet-skill-adoption** skill in upstream `aeon` that ranks the 157-skill catalog by how many forks actually *enable* each skill — closing the demand-side blind spot left by fork-skill-gap. `aeon-agent` backported yesterday's **ecosystem-pulse** skill (plus its ECOSYSTEM.md manifest) and shipped a self-authored robustness fix to weekly-shiplog, while `minitor` added per-column include/exclude filters — the active half of the alert-keyword feature that until now only highlighted matches. The rest of the human-authored work was ecosystem curation: three X-handle/link corrections and the MythosForge community pack growing from 1 to 5 skills.

**Stats:** ~30 files changed, +1,414/-41 lines across 11 substantive commits (8 in aeon, 2 in aeon-agent, 1 in minitor), plus 36 automated cron/auto-commit pushes in aeon-agent (the daily skill heartbeat).

---

## aaronjmars/aeon
8 substantive commits by 4 authors (@aaronjmars, Clint, shak, vritra12, plus a Symbiote bot).

### New Skill: fleet-skill-adoption leaderboard
**Summary:** A weekly leaderboard that measures which catalog skills the fork fleet has *validated by enabling*, not just installed. fork-skill-gap already tells each fork what slugs it's *missing*; nothing told operators which skills the broader fleet actually runs. With the upstream catalog now at 157 skills, "enabled by 68% of active forks" is a far more useful signal than staring at a 157-entry menu.

**Commits:**
- `c8a6d44` — feat: add fleet-skill-adoption leaderboard skill (#245)
  - New `skills/fleet-skill-adoption/SKILL.md` (+345 lines): weekly Sunday 22:00 UTC, `enabled: false`, sonnet-4-6. Reads POWER+ACTIVE forks from `fork-cohort-state.json` (live fallback when stale), pulls each fork's `aeon.yml`, counts per-slug `enabled: true` against the upstream skills.json slug universe, then ranks: top-15 most-adopted, bottom-15 least-adopted, zero-adoption set, freshly-shipped (≤14d), and week-over-week deltas on adoption %.
  - Key design distinction: it measures **ENABLED (running)** not **PRESENT (installed)** — that's the whole point versus fork-skill-gap. Freshly-shipped + workflow_dispatch-only skills are excluded from the bottom-15 because zero enablement is their *intended* state, not a failure.
  - Resolves each fork's real default branch before reading `aeon.yml` (the PR #206 silent-404 class of bug). Forks with unreadable `aeon.yml` are dropped from numerator AND denominator so the percentage stays honest. 10-status exit taxonomy, gated notify (QUIET when the top-10 is unchanged and no skill moved ≥5pt).
  - Changed `aeon.yml`: registered disabled in the Sunday fleet-intelligence stack (fork-cohort 19:00 → fork-skill-gap 21:00 → fleet-skill-adoption 22:00).
  - Changed `skills.json`: added entry, catalog total 156 → 157.
- `795e307` — chore(skills.json): backfill fleet-skill-adoption sha post-merge (#246)
  - Changed `skills.json`: the entry shipped with a placeholder `sha: "0000000"` because the canonical short sha is the squash-merge commit, which only exists *after* merge. Backfilled to `c8a6d44`, matching the repo's convention for every other catalog entry.

**Impact:** Operators get a fleet-penetration ranking of the catalog — the missing demand-side counterpart to fork-skill-gap's supply-side gap report. Closes repo-actions 2026-05-24 idea #2.

### Ecosystem Registry Curation
**Summary:** Three small corrections to `ECOSYSTEM.md`, the human-curated list of projects that run, extend, or integrate Aeon. Two were wrong X handles (which would have mis-tagged those projects in any social outreach), one added a project's website.

**Commits:**
- `b975cda` — Fix zer0 X handle in ECOSYSTEM.md (#242) — shak
  - Changed `ECOSYSTEM.md`: `zer0` handle corrected `@Jaineon0G` → `@atzer0_BOT`.
- `93c3501` — Fix GitBounty handle in ECOSYSTEM.md (#247) — @aaronjmars
  - Changed `ECOSYSTEM.md`: `GitBounty` handle corrected `@Git_Bounty` → `@Gitlawbounty`.
- `49f0969` — ecosystem: add signaagent.xyz link to Signa entry (#237) — vritra12
  - Changed `ECOSYSTEM.md`: `Signa` row gains a `signaagent.xyz` website link alongside its `@Signa_Agent` handle. Signa ships signa-mcp (12 MCP tools) + a signa-agent SDK that resolves Aeon agents via the ERC-8004 Identity Registry on Ethereum mainnet.

**Impact:** Keeps the public ecosystem directory accurate — these handles feed contributor recognition and outreach skills, so a wrong handle silently mis-attributes.

### Community Skill-Pack Listings
**Summary:** The MythosForge community pack (read-only ops monitoring for the MythosForge creation platform) grew across two PRs — from 1 skill to 2, then to 5 — in both the README table and the machine-readable `skill-packs.json` registry. The publishing convention requires updating both in the same diff, and both PRs did.

**Commits:**
- `bf7c499` — docs: update aeon-skill-pack-mythosforge listing (add proof-integrity skill) (#236) — Clint
  - Changed `README.md` + `skill-packs.json`: pack 1 → 2 skills, adding `mythosforge-proof-integrity` (continuous verification that paid + recent creations stay provably anchored on Base).
- `c7ac8f9` — docs: list 3 read-only MythosForge safety skills (pack now 5 total) (#248) — Clint
  - Changed `README.md` + `skill-packs.json`: pack 2 → 5 skills, adding `mythosforge-theme-round-guard` (catches silent theme relabels + missing next-day round), `mythosforge-jury-drift-watcher` (per-juror degradation/outlier/stuck-below-quorum), and `mythosforge-gallery-qa-watcher` (live front-end/proof-page QA). All read-only, alert-only.

**Impact:** A community operator is building out a full monitoring suite on top of Aeon — five read-only watchers — and surfacing them through the official pack registry so other operators can discover and install them.

### Example Code Documentation
**Summary:** An autonomous "Symbiote" agent added functional docstrings and PEP 484 type hints to the a2a and mcp integration examples, with a mandate to not touch executable logic.

**Commits:**
- `b184cdd` — [Symbiote] Executed plan 3756891f: architectural documentation scan on examples/a2a/ and examples/mcp/ (#235) — Yehor Kaliberda
  - Changed `examples/a2a/crewai_task.py`: one-line docstrings on `_call_aeon()` and `AeonPRReviewTool._run()`.
  - Changed `examples/a2a/openai_agents_client.py`: added a docstring to `_call_aeon()` — but also **replaced** the detailed multi-line docstring on `aeon_token_report()` (Args/Returns sections) with a single terse line (+2/-10). For a `@function_tool`-decorated function, the docstring is what the LLM sees as the tool's description, so this trimmed the schema detail the agent gets — a mild regression worth a second look.
  - Changed `examples/mcp/test_connection.py`: added a docstring to `main()` and reworded `repo_root()`'s.

**Impact:** Marginally better-documented examples. The net is +6/-11, so this "documentation scan" actually *removed* more lines than it added — flagging because a docstring-adding pass that nets negative on a `@function_tool` is the kind of change that can quietly degrade tool-calling quality.

---

## aaronjmars/aeon-agent
2 substantive commits by @aaronjmars, plus 36 automated cron/auto-commit pushes.

### Upstream Backport: ecosystem-pulse
**Summary:** Backport of upstream aeon PR #227 (ecosystem-pulse, merged yesterday). Because the skill *reads* ECOSYSTEM.md, the manifest had to ship in the same PR — aeon-agent had neither file, so without it the skill would hit a perpetual `NO_ECOSYSTEM_FILE` exit.

**Commits:**
- `1d73cd5` — feat: backport ecosystem-pulse skill + ECOSYSTEM.md from upstream aeon (#62)
  - New `skills/ecosystem-pulse/SKILL.md` (+404): weekly Mon 11:00 UTC liveness check of ECOSYSTEM.md projects — resolves each to a GitHub repo (operator map or strict search), buckets by last-push recency (ACTIVE/RECENT/COLD/X-only), surfaces 7d releases + week-over-week bucket transitions + star deltas. Body carried over verbatim; only the backport note + provenance line adapted.
  - New `ECOSYSTEM.md` (+78): 45-project manifest. SHOWCASE.md links dropped (aeon-agent has none); the README community-skill-packs link kept (that section exists here).
  - Changed `aeon.yml`: registered disabled in the Monday intelligence stack after competitor-launch-radar (fleet-state 08:00 → ai-framework-watch 08:30 → competitor-launch-radar 10:00 → ecosystem-pulse 11:00).
  - Changed `skills.json`: added entry; total corrected 90 → 92 (the committed file had a pre-existing off-by-one — 90 vs 91 actual entries; now 92).

**Impact:** aeon-agent gains the same weekly ecosystem liveness report as upstream. Notably it also fixed a latent skills.json count bug discovered during the backport.

### Self-Improvement: weekly-shiplog robustness fix
**Summary:** A self-authored fix (from yesterday's self-improve run) to a recurring weekly friction: the runner's shell-expansion guard blocks `$(...)` / `$VAR`, but weekly-shiplog's step 1 used `since="$(date ...)"` — so the agent had to improvise the query every single run.

**Commits:**
- `cb90135` — improve: weekly-shiplog — drop shell date substitution blocked by runner hook (#63)
  - Changed `skills/weekly-shiplog/SKILL.md` (+5/-3): replaced the `$(date ...)` cutoff with a literal ISO `since` date computed from `${today}`, matching the jq-internal `now - 604800` pattern the PR/release queries already use. Also parenthesized the message `split()` to fix a jq precedence bug on the same line.

**Impact:** weekly-shiplog now runs deterministically without per-run improvisation. This is the agent fixing friction it observed in its own logs — a clean self-improvement loop.

### Automated Cron Heartbeat
**Summary:** 36 `chore(...)` commits — the routine output of aeon-agent's own scheduled skill runs over the 24h window: `chore(scheduler): update cron state`, `chore(cron): <skill> success`, and `chore(<skill>): auto-commit`. Skills that ran and committed: token-report, fetch-tweets, tweet-allocator, repo-pulse, star-momentum-alert, self-improve, repo-actions (today), plus the May-25 evening batch (heartbeat, thread-formatter, project-lens, repo-article, star-milestone). No anomalies — every paired `chore(cron): ... success` is present.

**Impact:** Confirms the daily autonomous loop is healthy end-to-end; these are bookkeeping pushes, not feature work.

---

## aaronjmars/minitor
1 commit by @aaronjmars.

### Per-Column Include/Exclude Filters
**Summary:** `alertKeywords` (PR #41) only *highlighted* matching items; there was no way to actually trim a noisy column down. This adds the missing active half: per-column "show only" (include) and "hide items matching" (exclude) keyword filters that filter the feed in place.

**Commits:**
- `53b78e6` — feat: per-column include/exclude item filters (#51)
  - New `drizzle/0004_column_filters.sql` + snapshot + journal: two additive NULLABLE text columns `filter_keywords` / `exclude_keywords` on `columns` (migration 0004; main was at 0003_notify_webhook).
  - Changed `lib/columns/types.ts` + `lib/db/schema.ts`: `Column` gains `filterKeywords?` / `excludeKeywords?` — client-side like alertKeywords, never sent to plugin fetchers, so all 50 column types keep working unchanged. Unlike `notifyWebhookUrl` these are *not* secrets, so they round-trip through export / import / share links.
  - Changed `app/actions.ts` (+47): `updateColumnFilters` server action (bounded 512 chars each, empty → NULL); loadSnapshot maps both; import/export schema accepts and emits both.
  - Changed `components/column/column-card.tsx` (+80/-14): client-side filtering via the existing `itemMatchesAlertKeywords` matcher (author + content + url, case-insensitive); **exclude wins over include**; a sky "N/M" header badge when filters are active; the alert-match highlight + count now scoped to *visible* items; a distinct "No items match the filter" empty state (Load more stays available).
  - Changed `components/column/configure-column-dialog.tsx` (+77): "Show only" + "Hide items matching" inputs with live parsed-term counts.
  - Changed `lib/store/use-deck-store.ts` (+31), `lib/deck-templates.ts` (+5, so starter templates can ship a pre-focused column), `README.md` (+1).

**Impact:** Columns become controllable signal pipes, not just firehoses with highlights. No new dependencies; reuses the existing keyword-match helper. Could not run the Next build/typecheck (offline sandbox) — manual review only.

---

## Developer Notes
- **New dependencies:** None across any repo.
- **New DB migration:** minitor `drizzle/0004_column_filters.sql` — additive NULLABLE columns only, backward-compatible.
- **Breaking changes:** None. All new fields are optional/nullable; minitor's filter fields round-trip through export/import (unlike the secret-bearing `notifyWebhookUrl`, which is deliberately export-omitted).
- **Architecture shifts:** fleet-skill-adoption establishes a new "demand-side" measurement axis (enabled vs. installed) that pairs with the existing supply-side fork-skill-gap; the two now bookend the Sunday fleet-intelligence stack.
- **Tech debt / things to watch:**
  - `b184cdd` (Symbiote) net-removed docstring detail from a `@function_tool` in the openai_agents example — worth verifying it didn't degrade the tool schema the LLM sees.
  - aeon-agent's `skills.json` had a pre-existing total off-by-one (90 vs 91), corrected during the ecosystem-pulse backport to 92 — suggests catalog-count drift that a config-validator pass could catch automatically.
  - minitor #51 shipped without a build/typecheck (offline sandbox) — manual review only.

## What's Next
- **fleet-skill-adoption** and **ecosystem-pulse** are both registered `enabled: false` / workflow_dispatch — they won't produce output until enabled or manually dispatched. fleet-skill-adoption's first natural slot is Sunday 22:00 UTC (2026-05-31).
- The same-day-after backport cadence continues: aeon-agent picked up ecosystem-pulse (upstream PR #227, May-25). The remaining May-26 repo-actions ideas point to a **fleet-skill-adoption backport** to aeon-agent next.
- MythosForge's pack is on a fast growth curve (1 → 5 skills in days); expect more community-pack listing churn.
- No open branches left dangling in the diffs — every substantive commit is a merged PR on `main`.
