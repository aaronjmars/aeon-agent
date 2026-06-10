# Repo Action Ideas — 2026-06-10

*Generated from analysis of aaronjmars/aeon (503⭐, 166 forks), aaronjmars/aeon-agent (26-backport chain, ecosystem-entrants just landed), and aaronjmars/minitor (11 UX rungs, refresh-all + r/Shift-R shipped yesterday).*

---

## Context

**aeon** just crossed 500⭐ (now at 503). The star-milestone→show-hn-draft auto-dispatch wired by PR #358 (Jun-8) fired — no operator intervention required. The 14-day window saw the largest single build sprint the repo has run: MCP-inbound runtime enabling skills to call MCP servers during runs (PR #372, #378), dashboard MCP provisioning UI (PR #381–#385), STRATEGY.md as a @-imported north-star every skill reads (PR #370), apps/ restructure grouping sub-apps under `apps/` (PR #376), four new LLM gateways added (OpenRouter, UsePod, Venice, Surplus — PR #409), Fable 5 model (PR #394), and the Phase 2 automated capabilities sweep skill (PR #416, #417). Three external skill packs merged (signa-20, careful-finance, mneme). No open issues.

**aeon-agent** completed its 25th consecutive same-day-after backport today: ecosystem-entrants (PR #91). The backport chain is in its cleanest state yet — all Jun-08 ideas burned, the last explicit deferred item was `atrium-catalog-watcher` (upstream PR #342, blocked on missing `install-from-atrium`). That dependency landed Jun-09 as PR #90, making `atrium-catalog-watcher` the natural 26th link in the chain. No new CLAUDE.md runner-hook issues since PR #83+#89 closed the entire known site list.

**minitor** shipped its 11th UX rung yesterday: deck-level refresh-all button (r/Shift-R keyboard shortcut, PR #68). The per-column and per-deck color labeling system (PRs #61, #62) is now in place but has no filtering layer — color tags create visual groups that operators can't selectively show. No open issues.

---

### 1. `atrium-catalog-watcher` Backport (aeon-agent)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** The 26th consecutive same-day-after backport, explicitly flagged as the natural next link in both PR #87 (Jun-08) and PR #90 (Jun-09). `install-from-atrium` — the one missing dependency — landed Jun-09 as PR #90. With it in place, `atrium-catalog-watcher` (upstream aeon PR #342, Jun-05) is a clean verbatim copy: weekly Friday 12:00 UTC diff of the Atrium marketplace catalog, reports added/removed/renamed skills with one-click `./install-from-atrium <name>` commands on every new entry. Operators currently have no signal when new skills appear in the Atrium onchain marketplace — this closes the gap the install-from-atrium script opened.
**How:**
1. Verbatim copy of `skills/atrium-catalog-watcher/SKILL.md` from upstream aaronjmars/aeon (PR #342). Add backport-note block citing PR #342 + each adaptation. Key adaptations to verify: (a) `./notify` call style — check whether upstream uses positional `$1` or `-f file` style; (b) any `$(date ...)` shell substitutions per the anti-pattern chain closed by PR #83; (c) WebFetch fallback for the Atrium catalog fetch (public endpoint, pattern 1 in CLAUDE.md).
2. Register in `aeon.yml` disabled at `0 12 * * 5` (same slot as upstream, Friday 12:00 UTC) between `ai-framework-watch` and `competitor-launch-radar` (alphabetical). Add to `skills.json` (total 102→103, category dev).
3. Open PR. The install-from-atrium + atrium-catalog-watcher pair closes the Atrium integration on aeon-agent in two consecutive PRs.

---

### 2. Show HN Response Monitor Skill (`hn-monitor`) (aeon)
**Type:** Community / Growth
**Effort:** Medium (1-2 days)
**Impact:** aeon just crossed 500⭐ and the Show HN draft auto-fires via the star-milestone→show-hn-draft chain (PR #358). The launch generates community response on Hacker News — but there's no skill tracking the thread: upvotes, top comments, recurring questions, new GitHub spikes from referrals. Without a monitor, the operator sees the launch notification and nothing after it. A daily `hn-monitor` skill for the first week post-launch (then weekly) closes the loop: fire → land → measure → respond. Given that 503⭐ came fast and the Show HN hasn't shipped yet on aeon-agent's fork, this is a forward-looking gap the upstream fork should build now.
**How:**
1. New `skills/hn-monitor/SKILL.md`. Step 1: WebSearch `"Show HN" aeon site:news.ycombinator.com` to find the thread ID. Step 2: WebFetch the thread page and extract: points, comment count, top-level comment themes (curiosity, praise, criticism, "how do I" questions, comparisons to other frameworks). Step 3: Check GitHub stars delta since the thread went live (gh api repos/aaronjmars/aeon --jq .stargazers_count vs. last cached value in state).
2. Output: (a) Thread stats (points, comments, top 3 themes), (b) star delta since launch, (c) top 2 comments worth addressing with a short reply suggestion. Write to `articles/hn-monitor-${today}.md`. State in `memory/topics/hn-monitor-state.json`.
3. Schedule: daily at 08:00 UTC for 7 days post-launch detection, then weekly. Register `workflow_dispatch` initially; add schedule after the thread is confirmed live. Notifications gated: only when points > prior run OR new comments surfacing a recurring question.

---

### 3. STRATEGY.md Weekly Alignment Check Skill (`strategy-check`) (aeon)
**Type:** Feature / Meta-Agent
**Effort:** Medium (1-2 days)
**Impact:** STRATEGY.md landed Jun-8 as a @-imported north-star in CLAUDE.md. Every skill sees it in base context. But no skill checks whether weekly output actually aligns with the stated strategy dimensions — drift accumulates silently until it's chronic. A weekly `strategy-check` skill reads STRATEGY.md + last 7 days of `.outputs/*.md` and memory logs, scores each signal category against stated priorities, and surfaces the top 3 most-aligned and 1 most-drifted skill. Operators who customize STRATEGY.md (the dashboard editor landed with PR #371) want automated validation that customizations are actually changing behavior, not just sitting in a file.
**How:**
1. New `skills/strategy-check/SKILL.md`. Step 1: Read `STRATEGY.md` + last 7 days of memory logs from `memory/logs/`. Step 2: Map each skill run to a STRATEGY.md priority by title/content match. Build a score matrix: (skill → how many of its recent outputs reference a strategy priority). Step 3: Identify the top 3 skills most aligned with stated priorities and 1 with the widest gap vs. its stated category in STRATEGY.md.
2. Write weekly report to `articles/strategy-check-${today}.md`. Notify only when drift score crosses a threshold (e.g. the most-drifted skill has been off-strategy for 3+ consecutive weeks) — avoid noise on healthy weeks.
3. Schedule: weekly, Sunday 08:00 UTC (pairs with memory-flush which also runs Sunday). Register disabled at `0 8 * * 0` in aeon.yml. Category meta in skills.json.

---

### 4. `capabilities-sweep` Backport to aeon-agent (aeon-agent)
**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** The Phase 2 automated capabilities sweep just landed on upstream as `skills/capabilities-sweep/SKILL.md` (aeon PR #416, Jun-10). It iterates all skills missing `capabilities:` frontmatter, infers tags from content patterns (WebFetch/curl → `external_api`, `./notify` → `sends_notifications`, `gh api` writes → `writes_github`, onchain calls → `onchain_writes`, memory writes → `writes_memory`), and opens a single PR with all declarations. aeon-agent has ~100 skills with the same undeclared-capabilities gap. Backporting this skill lets the fork self-audit and close the gap without waiting for individual per-skill PRs.
**How:**
1. Verbatim copy of `skills/capabilities-sweep/SKILL.md` from upstream aaronjmars/aeon (PR #416). Add backport-note block. Key checks: (a) any absolute path references that differ between upstream and aeon-agent's directory layout (both use `skills/` at repo root — likely clean); (b) `./notify` call style; (c) no `$(date ...)` substitutions expected in this skill.
2. Register as `workflow_dispatch` only in aeon.yml (not scheduled — this is a one-shot fix tool, not a recurring report). Add to `skills.json` (total 103→104 after atrium-catalog-watcher lands, category meta). Insert between `capabilities-map` and `competitor-launch-radar` alphabetically.
3. Open PR. After merge, dispatch once (`gh workflow run aeon.yml -f skill=capabilities-sweep`) to generate the capabilities declarations PR for the aeon-agent skill catalog.

---

### 5. Color-Label Filter Toggle (minitor)
**Type:** Feature / UX
**Effort:** Medium (1-2 days)
**Impact:** Column color labels (PR #61) and deck color labels (PR #62) give operators a visual grouping system — orange columns = crypto, blue = dev, green = social. But there's no way to filter the deck grid to show only one color group. At 15+ columns per deck, tagged columns are still found by scrolling. Adding a color filter pill row above the deck grid (one chip per color used in the deck + "All" default) lets operators single-click to isolate a group — same ergonomics as GitHub label filters. View-state only, no DB migration, wires directly into the existing `visibleColumnIds` path that collapse/tabs/search already use.
**How:**
1. In `lib/store/use-deck-store.ts`, add `activeColorFilter: string | null` per-deck (view-state, not persisted, cleared on deck switch). Add `setColorFilter(deckId, color | null)` action. In `visibleColumnIds` selector, add a final filter step: when `activeColorFilter` is set, keep only columns whose `color === activeColorFilter`.
2. In `components/deck/deck-board.tsx`, compute `usedColors: string[]` by collecting distinct `column.color` values across the deck's columns. Render a compact filter bar above the grid: "All" pill (clears filter) + one pill per used color (rendered as a small colored dot + label, or just the dot if space is tight). Active pill gets a brand-ring border. Hide the bar entirely when `usedColors.length < 2` (no filtering needed with 0 or 1 color in use).
3. Scope clearly: this filters the currently-visible deck's column grid only. Cross-deck filter is out of scope. No DB schema change, no export/import change, no version bump. Same lifecycle as `collapsedColumnIds`/`widthByColumn` — cleared when the column is removed.

---

*Jun-08 ideas FULLY CONSUMED (all 5 built: show-hn-draft prompt refresh aeon PR #380, install-from-atrium aeon-agent PR #90, deck keyboard nav minitor PR #66, ecosystem-entrants backport aeon-agent PR #91 landed today). OAuth credential write-back (Jun-06 #1) remains intentionally deferred as CORE-files-risky.*
