# Push Recap — 2026-06-02

## Overview

Two-day window — the prior recap ran Monday at 15:26 UTC and caught the 18-PR catch-up wave that closed the open-PR queue on aeon. Today's window adds Tuesday morning's follow-up work: two new aeon skills (one fresh, one fix), the first 19-skill capability-declaration sweep, an onchain skill-marketplace pack joining the registry, and a 19th-consecutive aeon-agent backport. Minitor closed two open per-column issues (one TS fix, one new ephemeral search). Three ecosystem entries (HivemindOS, Echo Oracle, SyntheticsAI link refresh) appended to the catalog without code changes.

**Stats:** ~30 substantive commits across 3 repos · ~900 net lines added · 12+ PRs merged (aeon ~17, aeon-agent ~6, minitor ~3) · ~10 distinct authors

---

## aaronjmars/aeon

### Theme 1: Capability declarations become real and load-bearing

The 6-value capabilities taxonomy (locked May 29 in PR #268, CI-parity-checked May 30 in PR #304) has had two consumers land in this window — first the audit skill that reads them (capabilities-map, PR #313 merged Monday 13:35Z), then the first real population of declarations across the high-blast-radius skills. The matrix went from "everything undeclared" to "19 skills annotated" in 24 hours, and the audit skill had to ship a fix the same day to handle the in-between state.

**Commits:**

- `93a2d9d` — *feat: add pr-merge-queue skill — daily operator-facing open-PR digest bucketed by touched-file risk tier (#318)*
  - New `skills/pr-merge-queue/SKILL.md` (+288 lines), `aeon.yml` (+1), `skills.json` (+12/-1)
  - Daily 09:45 UTC digest that buckets every open PR by file-risk tier: CORE_REVIEW (touches `aeon.yml` / `install-skill-pack` / `CLAUDE.md`) > INFRA_REVIEW (workflows / Dockerfile) > SKILL_WARN_OR_BLOCK (skill PR + scan flagged) > SKILL_PASS > FAST_TRACK (docs/assets/data) > UNKNOWN.
  - Reuses `skills/skill-security-scan/scan.sh` verbatim — same source `pr-skill-triage` relies on. Re-notify gated on head SHA, not date, so a queue growing by one PR/day doesn't re-notify yesterday's whole queue every morning.
  - Operator-facing only — no merge action, no labels, no PR comments. Complements `pr-triage` (per-PR first-touch) and `auto-merge` (bot subset) by being the morning brief.

- `b560eb5` — *chore(skills): Phase 1 capabilities frontmatter for high-blast-radius skills (#317) (#322)*
  - 19 SKILL.md files each get exactly one new `capabilities:` line in their YAML frontmatter (+1/-0 per file).
  - Coverage: every onchain investigation skill (`approval-audit`, `honeypot-check`, `lp-lock-check`, `linked-wallets`, `fund-flow`, `investigation-report`, `tx-explain`, `deployer-trace`, `holder-concentration`, `wallet-profile`) plus every key-spending / token surface (`distribute-tokens`, `on-chain-monitor`, `rug-scan`, `contract-audit`, `token-report`, `token-alert`, `token-movers`, `token-pick`, `liquidpad-launch`).
  - Sample (`approval-audit`): `capabilities: [read_only, sends_notifications]` — read-only chain query that emits a notification, no writes.
  - This is the data capabilities-map exists to consume. After this lands the matrix can finally distinguish "operator deliberately runs a narrow stack" from "the taxonomy is brand new and nobody has annotated yet."

- `3c14e88` — *fix(capabilities-map): suppress false all-gaps report when no enabled skill declares capabilities (#319)*
  - `skills/capabilities-map/SKILL.md` (+60/-6).
  - Closes a bug introduced 24h ago: on a fresh instance the matrix flagged all six tiers as gaps for the same trivial reason (nobody had declared anything). The skill's whole purpose is to surface real coverage holes, and a six-gap false alarm on the first run trains operators to ignore the report.
  - New `DECLARED_ENABLED` count: total enabled declarations across all real tiers. When zero, `COVERAGE_ASSESSABLE=false`, `GAP_SET` is suppressed to empty, status routes to `CAPABILITIES_MAP_UNDECLARED_BASELINE`.
  - Two new state deltas: `entered_undeclared_baseline` (instance just dropped to all-undeclared — notify once) and `became_assessable` (first declaration just landed — notify once). After the baseline ping the skill goes QUIET each week until a declaration lands, instead of re-crying gaps every Monday.
  - Notification template forks: when COVERAGE_ASSESSABLE is false, the message says "coverage can't be assessed yet" with a pointer to docs/CAPABILITIES.md §"How to choose" instead of the gap-style summary that would read like "0 of 6 tiers uncovered" — the opposite of the truth.

**Impact:** The taxonomy now has both an audit surface and real declarations to audit. The fix is what kept the audit honest while the declarations were still landing — a 24h round trip from "skill ships," to "skill fires false alarm on bootstrap," to "skill gets gated on its own precondition."

### Theme 2: Ecosystem & skill-pack catalog growth

Three ecosystem PRs landed (each one row in ECOSYSTEM.md, all docs-only) plus a fourth registry PR adding a community skill pack.

**Commits:**

- `96bdbcd` — *aeon x atrium (#316)*
  - `skill-packs.json` (+12/-1). Bumps the registry `updated` date to `2026-06-01` and appends one community pack: `Atrium-Hermes/aeon-atrium-skills`. Three skills (`atrium-publish`, `atrium-scout`, `atrium-earnings`) on an onchain skill marketplace running on Base USDC — a registry-level mirror of the open question "where do skills get monetized once they leave a fork." `trust_level: community` (regular install-time scan applies).

- `92084e4` — *docs: add HivemindOS to ecosystem (#320)*
  - `ECOSYSTEM.md` (+1). House-style row (X handle + website only, no Bankr launch link, no personal dev handle, no repo). Author: LiamVisionary.

- `026b8a9` — *List Echo Oracle in ecosystem (#321)*
  - `ECOSYSTEM.md` (+1). Author: BuiltByEcho.

- `a5294ad` — *docs: update SyntheticsAI ecosystem links (#324)*
  - `ECOSYSTEM.md` (+1/-1). Link-only refresh of an existing entry; no new row.

**Impact:** ECOSYSTEM.md grows by three (HivemindOS, Echo Oracle, link-refresh for SyntheticsAI) and the registry grows by one pack (Atrium Skills). All four are read-only adds — none touch code, all are scanned at install time.

---

### Theme 3 (closing-out 6/1 — already deep-covered in yesterday's recap)

For completeness, the substantive 6/1 PRs the prior push-recap framed as the Monday catch-up wave (now in this window because today's `since` cutoff sits 24h earlier):

- `1b0caa8` (#231 liquidpad-launch — opened May-22, finally merged after rebase resolving skills.json conflict)
- `9e15b35` (#315 MandateSeal Guard registry entry — minimal one-pack add)
- `2960716` (#270 AntFleet pr-review-antfleet-x402 registry update)
- `58d58e1` (#280 Anthropic-compatible API base URL — enables Bedrock proxies / Claude shims through the Settings UI)
- `b189318` (#309 dashboard lib tests — 633 lines covering config.ts/utils.ts/frontmatter.ts, three modules that had zero coverage)
- `0ed6d35` (#313 capabilities-map skill — see fix above)
- `3db561e` / `d5804dd` / `b49900b` / `7148dc7` / `f4873c1` / `20067d8` — six HoundFlow keyless onchain investigation skills (#287/#285/#284/#283/#282/#281): investigation-report, fund-flow, linked-wallets, lp-lock-check, honeypot-check, approval-audit. All Base RPC, no explorer keys.
- `f0400b6` (#266 skill-update-check rescan gate — AntFleet, closes the last Issue #258 thread)
- `9e3242e` (#312 Careful Finance ecosystem listings — UIZorrot)
- `da11341` (#303 Hound Flow ecosystem entry)
- `d7cc223` (#304 capabilities taxonomy parity CI)
- `5106501` (#306 treasury wallets — token-report reads .x402books/wallets.json)
- `bbf156b` (#302 wallets.json fork-safety doc — AntFleet)

(Yesterday's recap covered these as the 18-PR / 37-minute aaronjmars merge window. Listed here because the strict `since=2026-06-01T00:00:00Z` window includes them; no fresh diff-reading was done — already legible from yesterday's article.)

---

## aaronjmars/aeon-agent

### Theme: 19th consecutive same-day-after backport

- `6f64a38` — *feat: backport follow-up-patrol skill from upstream aeon PR #272 (#76)*
  - New `skills/follow-up-patrol/SKILL.md` (+175 lines), `aeon.yml` (+1), `skills.json` (+11/-1).
  - Tuesday 11:00 UTC weekly escalation audit. Parses `memory/MEMORY.md` follow-up section using resolution order `## Known Follow-ups` → `## Next Priorities` → `## Open Loops`/any heading containing "follow"/"todo"/"pending" (aeon-agent's `MEMORY.md` already has `## Next Priorities` at line 107 — picks up automatically). Computes per-item ages, tiers CRITICAL (>21d operator) / HIGH (>14d operator) / MEDIUM (>7d any type) / WATCH (≤7d or auto/deferred/deadline). Writes `memory/topics/follow-up-status.md`.
  - Notifies only when CRITICAL or HIGH count non-zero — silent otherwise.
  - Picked over upstream PR #272's four other ops skills (narrative-convergence, mcp-pulse, fleet-scorecard, plus spend-monitor which was done June 1) because it's the smallest self-contained one and 100% local file reads. No new secrets, no prefetch wrapper.
  - Two upstream-deltas documented inline: (1) `./notify` rewritten from `./notify -f file` to single-positional-arg heredoc per aeon-agent convention; (2) `memory/issues/INDEX.md` step gracefully no-ops since aeon-agent doesn't maintain that file yet.

- `02dd0ca`, `7a455fa`, `a910641`, `2906549`, `4a3f6f1`, `3162392`, `5cb4a5e`, `42f6d5b`, `836d4d3`, `369273e`, `9360a39`, `cdc9ce0`, `1a12c8d`, `60ec1ff`, `f2c1e57`, `96abfd9`, `83474b3` — auto-commits from today's cron skills (`repo-actions`, `self-improve`, `feature`, `star-momentum-alert`, `repo-pulse`, `token-report`) + scheduler state updates. No-op for the recap; routine bookkeeping.

- 6/1 commits in window: `bd30df8` (#72 upstream-gap — new skill, first non-backport in the chain), `4b3f99e` (#70 fork-health-score backport), `fb42152` (#74 spend-monitor backport — 18th in the chain), `610734e` (#71 heartbeat $(date)→${today} self-fix — third skill to take that pattern after weekly-shiplog #63 and push-recap #67), `8b1ea90` (#69 project-lens 5/29 acknowledgement article), `7c34368` (#73 project-lens 5/31 Astronomer Royal article), `ca5f74b` (#75 feature log).

**Impact:** Cadence holds: contributor-spotlight May-21→23 → install-skill-pack+registry May-22→24 → ecosystem-pulse May-24→26 → fleet-skill-adoption May-26→27 → sparkleware-catalog May-27→28 → pr-skill-triage May-28→29 → fork-health-score May-29→30 → spend-monitor May-29→Jun-01 → **follow-up-patrol May-29→Jun-02**. Three of upstream PR #272's five ops skills remain unbackported (narrative-convergence, mcp-pulse, fleet-scorecard) — natural targets for upcoming rounds.

---

## aaronjmars/minitor

### Theme: Two more rungs on the per-column UX ladder

The May-29 → today sequence on column-level UX: tab groups (PR #53, May-29) → column collapse (PR #55, May-30) → JSON export (PR #56, May-31) → quick-search (PR #58, today). Same axis, same in-session-view-state pattern (`autoFetchingIds` / `selectedTabByDeck` / `collapsedColumnIds` / now `searchByColumn`), all four shipping in 5 days without touching DB schema or the plugin contract.

**Commits:**

- `353d3a1` — *feat(columns): per-column quick-search input — ephemeral substring filter on top of include/exclude (#58)*
  - `lib/store/use-deck-store.ts` (+33/-1), `lib/columns/keyword-match.ts` (+24), `components/column/column-card.tsx` (+165/-5). Total +222/-6.
  - New `searchByColumn: Record<columnId, string>` view-state map in the zustand store. NOT persisted — same lifetime as `autoFetchingIds` / `selectedTabByDeck` / `collapsedColumnIds`. `setColumnSearch(columnId, query)` with 256-char cap and empty-string-deletes. Cleanup on `deleteColumn` and `deleteDeck` so the map can't accumulate stale ids over long sessions.
  - New `itemMatchesSearchQuery(item, query)` helper in `keyword-match.ts` — single literal substring match (NOT a parsed keyword list — typing `rust foo` means the phrase, not `"rust" OR "foo"`). Scans the same content + author + url haystack as `itemMatchesAlertKeywords`, so search semantics align with the alert-highlight rules operators already know.
  - Search button in the column header between alert/filter badges and Refresh; toggles a thin input row beneath the header. Esc clears + closes, `×` clears in place. Auto-opens on render when query exists so cross-tab / cross-collapse persistence in-session works.
  - **Collapsed strip search indicator**: small emerald Search icon when search is active on a collapsed column. Prevents the silent-undercount surprise where matchCount badge would shrink under a hidden filter.
  - **Distinct from include/exclude** (PR #51): persistent column config (survives reload, exports with deck, fires webhooks). Quick-search is ephemeral view-state — runs *on top of* include/exclude (narrows further; never widens past it).
  - No DB schema, no migration, no plugin contract touched.

- `2c5257b` — *fix(columns): drop duplicate role/tabIndex on collapsed column strip (#57)*
  - `components/column/column-card.tsx` (-2 lines). Same-day TS fix on yesterday's column-collapse merge.
  - The collapsed-strip `<div>` (PR #55) set `role="button"` and `tabIndex={0}` explicitly, then spread `{...attributes}` from dnd-kit's `useSortable` which already supplies both. The spread comes last, so it overwrote the explicit props — TypeScript flagged with TS2783 ("specified more than once, will be overwritten").
  - Drops the redundant explicit props, relies on `{...attributes}` — same pattern the expanded view's drag handle uses. Runtime behavior identical.
  - Verified: `tsc --noEmit` drops from 4 errors to 2 (the two remaining are pre-existing unrelated null-handling errors in `lib/integrations/pypi.ts`, lines 286/302 — also noted on May 24 when per-column refresh intervals shipped).

- 6/1 commits in window: `cd64533` (#55 per-column collapse), `584f712` (#56 column JSON export), `39724bf` (#54 COINGECKO_DEMO_API_KEY in Settings UI). All deep-covered in yesterday's recap.

**Impact:** The "find one thing in a deep-scrolling column" workflow is now ephemeral instead of forcing the operator to reach for the persistent include/exclude config. Across 47 plugins, that's the more common need by a wide margin. The PR #57 fix is the second same-day cleanup of an in-session-view-state shipment (PR #56 yesterday was the first) — both took <1h to spot, file, and merge.

---

## Developer Notes

- **New dependencies:** none across any of the three repos.
- **Breaking changes:** none. Capabilities frontmatter is additive; all 19 SKILL.md files keep their existing frontmatter intact.
- **Architecture shifts:** The capabilities taxonomy crosses from "defined" to "used + populated" in a single 24h window: declarations in 19 skills (#322), the audit surface (#313, merged 6/1), and the bootstrap-state fix (#319). The minitor per-column UX axis adds its fourth in-session view-state field (`searchByColumn`) following the same pattern as `collapsedColumnIds` / `selectedTabByDeck` / `autoFetchingIds`.
- **Tech debt:** Two pre-existing `lib/integrations/pypi.ts` type errors on minitor (lines 286, 302 — null-handling) confirmed still present after PR #57. Not introduced today; documented on May 24.
- **Registry growth:** `skill-packs.json` now lists 8 community packs (Atrium adds the 8th). All scanned at install time per existing trust model.

## What's Next

- **aeon-agent** — Three upstream PR #272 ops skills remain unbackported: narrative-convergence, mcp-pulse, fleet-scorecard. Natural backport targets for the next 2-3 days at current cadence (May 29 backports are now 3-day-old urgent territory per the upstream-gap skill's tiering).
- **aeon** — Phase 1 capabilities declarations covered 19 high-blast-radius skills. Phase 2 (medium-blast-radius — research/data skills + auxiliary onchain readers) presumably follows. The capabilities-map skill's first useful run will fire next Monday (06-08) at 11:30 UTC against a populated matrix.
- **minitor** — Per-column UX axis (tabs / collapse / export / search) shipped in 5 days. Next likely rung on the same axis: column-pinning (mentioned in today's repo-actions article as idea #4), or starting to consume in-session view-state for something other than visibility (e.g. per-column auto-sort or per-tab persistence). Settings UI still doesn't expose webhook URLs in the export (deliberately, per PR #50 — token-leak hazard) so that constraint remains in place.
- **Open threads visible in diffs:** PR #151 (show-hn-draft) still open since May 1 — 31 days, currently at 7d extended-persistence backoff per yesterday's heartbeat block. Next ESCALATION due June 3.
