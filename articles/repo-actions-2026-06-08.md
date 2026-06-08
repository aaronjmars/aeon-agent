# Repo Action Ideas — 2026-06-08

*Generated from analysis of aaronjmars/aeon (493⭐, 166 forks), aaronjmars/aeon-agent (102 skills, 24 consecutive backports), and aaronjmars/minitor (9 UX rungs shipped in 11 days).*

---

## Context

**aeon** is at 493⭐ — 500 arrives in roughly 3 days (v7≈3.6/day). star-milestone auto-dispatch (PR #358, today) means show-hn-draft will fire without a manual gate. The ecosystem loop is fully closed: `ecosystem-pulse` + `ecosystem-entrants` + `ecosystem-links` cover liveness, new arrivals, and URL validity. The 193-skill catalog now spans 8 categories (core, onchain-security, meta added this week). Capabilities Phase 1 declared ~30 high-blast-radius skills; ~150+ remain `(undeclared)` in `capabilities-map`. Three external skill packs merged in the last 14 days (signa-20, careful-finance, mneme). VIGIL + `vigil-revoke` closed the onchain security detection→revoke loop. No open non-PR issues.

**aeon-agent** completed its 24th consecutive same-day-after backport today (ecosystem-links, PR #87). `ecosystem-links` references `ecosystem-entrants` as "the third leg, NOT yet backported" — the ecosystem loop on this fork is 2/3 closed. `install-from-atrium` (the shell script, not a SKILL.md) is absent, which blocked the `atrium-catalog-watcher` backport explicitly in today's notes. OAuth credential write-back remains the one intentionally deferred idea (CORE-files-risky). `repo-pulse` now enriches stargazer/forker profiles (PR #88, today).

**minitor** shipped 9 rungs in 11 days: tab groups, collapse, export, search, pin, duplicate, column color, deck color, width control, deck drag-to-reorder. No open issues. The per-column/deck UX surface is now high enough that cross-deck and keyboard ergonomics become the bottleneck.

---

### 1. Phase 2 Capabilities Declarations Sweep (aeon)
**Type:** DX
**Effort:** Medium (1-2 days)
**Impact:** `capabilities-map` surfaces an `(undeclared)` row covering ~150+ skills that shipped before the Phase 1 sweep (PR #322, May). The CI gate added by PR #304 enforces declarations going forward, but the existing gap makes the map's output noisy — every `capabilities-map` run lumps ~80% of the catalog into one unlabeled bucket. A batch sweep that reads each remaining skill file, infers capability tags from content patterns (external API calls, `./notify` invocations, `gh api` writes, onchain calls, file writes to memory/), and opens a single PR with all declarations would clean the map in one shot and make it a meaningful ops signal immediately.
**How:**
1. New `skills/capabilities-sweep/SKILL.md` (or a self-contained script): iterate `skills/*/SKILL.md` where `capabilities:` is absent in frontmatter. For each, extract patterns: `WebFetch|curl` → `external_api`; `./notify` → `sends_notifications`; `gh api.*POST|PUT|DELETE|PATCH` → `writes_github`; `eth_call|eth_sendRawTransaction|Bankr` → `onchain_writes`; `memory/` write → `writes_memory`. Confidence threshold: require ≥2 matching lines before auto-declaring; flag low-confidence for manual review.
2. Write proposed frontmatter patches to a JSON manifest. Open a single PR adding `capabilities:` to each skill file — keeps the diff reviewable as one commit per skill.
3. Register as `workflow_dispatch` only (not scheduled). Rerun is safe — skills already declared are skipped. Estimated coverage: 150+ skills in one pass; manual cleanup for the ~10 edge cases the regex can't resolve.

---

### 2. `ecosystem-entrants` Backport (aeon-agent)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** The 25th consecutive same-day-after backport. `ecosystem-links` (PR #87, today) landed with an explicit inline note: "ecosystem-entrants is the third leg, NOT yet backported." With `ecosystem-pulse` (Mon 11:00, liveness) and `ecosystem-links` (Mon 11:55, URL validity) both live on aeon-agent, the loop is 2/3 closed. `ecosystem-entrants` (Mon 11:45, upstream PR #339 merged Jun-03) is the demand-side signal: it discovers new aeon-adjacent projects from GitHub trending + community signals before they're curated into ECOSYSTEM.md. The operator currently has no signal on when new agent frameworks, skill packs, or ecosystem integrations are forming around aeon.
**How:**
1. Verbatim copy of `skills/ecosystem-entrants/SKILL.md` from upstream aaronjmars/aeon (upstream PR #339). Add backport-note block citing PR #339 + each adaptation.
2. Key adaptations to verify: (a) `./notify` call style — check whether upstream uses positional `$1` or `-f file` style (last two backports PR #85 and PR #87 needed no translation; check this one); (b) any `$(date ...)` shell substitutions replaced with literal `${today}` per the chain closed by PR #83; (c) WebFetch fallback for any external fetches not already covered.
3. Register in `aeon.yml` disabled at `45 11 * * 1` (same slot as upstream, between ecosystem-pulse and ecosystem-links). Add to `skills.json` (total 102→103, category research). Closes the three-skill ecosystem loop on aeon-agent.

---

### 3. Deck Keyboard Navigation Shortcuts (minitor)
**Type:** DX
**Effort:** Small (hours)
**Impact:** Minitor has no keyboard navigation layer. At 10+ columns per deck, every action is a hunt-and-click — focus a column, open its menu, select an option, dismiss. Four shortcuts cover 80% of the operator's daily workflow: `j`/`k` to move focus between columns, `/` to open quick-search on the focused column, `c` to toggle collapse on the focused column, `Escape` to clear focus/search. These mirror the shortcuts used by Linear, GitHub issues, and most terminal dashboards that operators already have in muscle memory. A single `keydown` listener at the `DeckBoard` level routes events to the focused column's existing actions — no new components, no new DB fields, no state migration. View-state only (which column is focused), same pattern as `collapsedColumnIds`.
**How:**
1. Add `focusedColumnId: string | null` to `lib/store/use-deck-store.ts` (view-state, not persisted) with a `setFocusedColumn(id)` action. In `components/column/column-card.tsx`, render a visible focus ring when `focusedColumnId === column.id` (e.g. `ring-2 ring-primary`). Click on any column sets focus.
2. In `components/deck/deck-board.tsx`, add a `useEffect` with a `keydown` listener: `j` → focus next column in `columnIds` order; `k` → previous; `/` → call `setSearchByColumn(focusedColumnId, true)` to open the quick-search input (same action the search button already fires); `c` → toggle `collapsedColumnIds` for the focused column; `Escape` → `setFocusedColumn(null)`, clear search.
3. Guard the listener: skip when focus is inside an `<input>`, `<textarea>`, or `[contenteditable]` element (standard keyboard shortcut gating pattern) so typing in a search box doesn't accidentally navigate columns.

---

### 4. `show-hn-draft` Prompt Refresh (aeon)
**Type:** Growth
**Effort:** Small (hours)
**Impact:** `show-hn-draft` (PR #151, open since May 1) auto-fires at 500⭐ via the star-milestone dispatch wired today. The SKILL.md prompt was written in early May when aeon had fewer skills, no external contributors, no skill packs ecosystem, and no onchain security layer. At 500⭐ the auto-generated draft is the first impression for thousands of HN readers. Updating the prompt context to reflect the current state — 193 skills across 8 categories, 166 forks, the Atrium marketplace, three install paths, external contributors shipping skill packs, onchain security with VIGIL + vigil-revoke — means the fired draft accurately represents the product rather than an early-May snapshot.
**How:**
1. Read `skills/show-hn-draft/SKILL.md` and locate the prompt context block (the section that describes aeon's current state to the LLM). Update: skill count (→193), categories (5→8 with core/onchain-security/meta), install paths (add `install-from-atrium` as 3rd path), external contributors (Nurstar, vigilcodes, HoundFlow, signa, Careful Finance, Mneme), onchain security layer (VIGIL + wallet-risk-weekly + vigil-revoke).
2. Update the "what makes aeon different" framing from "configure once, forget forever" toward the forks ecosystem angle: 166 forks running autonomous agents means it's not just a framework but a coordination layer — each fork is an autonomous agent operating independently on GitHub Actions.
3. Open PR. No schema changes, no new files — single SKILL.md edit. The PR description should note this is a prompt refresh timed for the 500⭐ auto-fire on ~Jun 11.

---

### 5. `install-from-atrium` Script Backport (aeon-agent)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** `atrium-catalog-watcher` (upstream aeon PR #342, Jun-05) was explicitly skipped in today's backport notes because aeon-agent doesn't have the `install-from-atrium` shell script. The skill's core value is emitting `./install-from-atrium <name>` one-click install commands on every newly-discovered Atrium marketplace entry — backporting it without that command would surface notifications recommending a non-existent tool. `install-from-atrium` is a shell script (not a SKILL.md), straightforward to port. Once live, `atrium-catalog-watcher` becomes the natural 26th consecutive backport, giving aeon-agent a weekly signal when new skills appear in the Atrium onchain marketplace.
**How:**
1. Fetch the `install-from-atrium` shell script from upstream: `gh api repos/aaronjmars/aeon/contents/install-from-atrium` (or read it from the aeon repo directly). It uses `$ATRIUM_HOST` env override + fetches `/.well-known/skills/index.json` + downloads the named skill's SKILL.md into `skills/{name}/`. Adapt any hardcoded paths for aeon-agent's directory structure if they differ.
2. Place the script at the repo root (same location as `add-skill` and `install-skill-pack`). Mark executable (`chmod +x`). Test with a dry-run that prints the resolved URL without writing files.
3. Open PR. Then in a follow-up PR, backport `atrium-catalog-watcher` (upstream PR #342 Jun-05) — this is now unblocked. The two PRs together complete the Atrium integration on aeon-agent (26th consecutive backport).

---

*Jun-06 ideas FULLY CONSUMED (all 5 built: ecosystem-links aeon PR #351, $(date) batch self-fix aeon-agent PR #83, ecosystem-links backport aeon-agent PR #87, vigil-revoke aeon PR #354, show-hn-draft auto-dispatch aeon PR #358). OAuth credential write-back (Jun-06 #1) remains intentionally deferred as CORE-files-risky.*
