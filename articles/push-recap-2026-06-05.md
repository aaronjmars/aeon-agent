# Push Recap — 2026-06-05

## Overview
4 substantive PRs by 2 distinct human authors (aaronjmars, vigilcodes) closed in the 24h since the prior recap. Three were content-stack outputs from the Jun-04 `feature` cron — aeon's atrium-catalog-watcher, aeon-agent's mcp-pulse backport, minitor's color labels — each going through one mid-PR structural fix before merge. The fourth, VIGIL on aeon, was an external MCP-server submission from a brand-new contributor that landed through five review cycles tightening a shell-injection regex, capability declarations, and tool-name accuracy. The auto-build pipeline is still consuming the Jun-04 repo-actions queue on schedule, and the marketplace surface picked up a new external producer the same day.

**Stats:** 16 files changed, +1,436/-7 lines across 4 PRs.

---

## aaronjmars/aeon

### Theme 1 — Closing the third install path's discovery loop
**Summary:** `install-from-atrium` (PR #335, merged Jun-03) made the Atrium onchain marketplace the third live way to install a skill alongside the curated `skill-packs.json` registry and direct `add-skill` URL fetch. Until today there was no scheduled signal when something new appeared in Atrium — anyone could run `./install-from-atrium --list` ad-hoc, nobody runs it weekly by hand. Today's PR builds the supply-side watcher and slots it between `sparkleware-catalog` (Tuesday, curated registry health) and `skill-update-check` (Sunday, installed-skill drift).

**Commits:**
- `9cb91a7` — feat: atrium-catalog-watcher skill — weekly Atrium marketplace diff (#342)
  - New `skills/atrium-catalog-watcher/SKILL.md` (+306 lines, 10-step skill): bootstrap state, parse `var`, fetch `https://atriumhermes.tech/.well-known/skills/index.json` via curl with WebFetch fallback per CLAUDE.md sandbox pattern 1, detect host switches, diff against `memory/topics/atrium-catalog-state.json` keyed on `skill_id` (the canonical onchain id — name renames don't double-fire as add+remove), write article, gated notify (added / removed / baseline / host-switch only — description tweaks are article-only), atomic state write with 56-day prune. 7-state exit taxonomy (OK / QUIET / FETCH_FAIL / BAD_SHAPE / DRY_RUN / STATE_CORRUPT / BAD_VAR).
  - `aeon.yml` (+1): registered disabled between `ai-framework-watch` and `competitor-launch-radar` (alphabetical, weekly section), schedule `0 12 * * 5`, model `claude-sonnet-4-6`.
  - `skills.json` (+13/-1): total 182→183, alphabetical insert between `article` (idx 5) and `auto-merge` (idx 6), category `dev`.

**Impact:** Every Friday at noon UTC the operator now gets a notification when a new skill appears in the Atrium marketplace, with a copy-pasteable `./install-from-atrium <name>` install command on every `added` row. Combined with the curated `sparkleware-catalog` digest (Tuesday) and `skill-update-check` (Sunday), three weekly digests now cover marketplace arrivals, curated registry health, and installed-skill freshness with no overlap. The skill consumed Jun-04 repo-actions idea #2, completing two of the five ideas from that run (the third — color labels — landed on minitor below).

### Theme 2 — External MCP-server submission lands after multi-cycle hardening
**Summary:** A brand-new external contributor (`vigilcodes`, first commit on aeon) shipped an entire onchain security MCP server with nine read-only tools plus a deliberately split-off write action. The PR landed after five review cycles that progressively tightened the surface — endpoint moved from raw IP to a TLS domain, capability declaration was corrected, a CRITICAL shell-injection vector in user-supplied wallet/token addresses was fixed with a strict allowlist regex, four additional tools were documented, and tool names were standardized to the live `vigil_*`-prefixed forms. The submission is a working MCP-spec endpoint (`https://mcp.vigil.codes`) with a paired GitHub repo (`github.com/vigilcodes/vigil-mcp`).

**Commits:**
- `11062dc` — Add VIGIL: Onchain security scanner for Base (MCP server) (#323)
  - New `skills/vigil/SKILL.md` (+166 lines). Frontmatter declares `capabilities: [external_api, sends_notifications]` after review pushed back on an initial incorrect `read_only` claim — VIGIL hits an external endpoint with no on-chain RPC fallback, so per `docs/CAPABILITIES.md` it's `external_api`. The Approval Revoker is deliberately broken out into a separate future `vigil-revoke` skill, gated by Bankr auth and explicit user confirmation, since it's state-changing — VIGIL itself stays read-only.
  - **CRITICAL shell-injection fix mid-PR:** the original validator was a weak length+prefix check on the user-supplied `${var}` wallet/token address. Replaced with a strict allowlist regex `^0x[0-9a-f]{40}$` enforced before any curl, so inputs with quotes, spaces, or shell metacharacters are rejected before any JSON-body interpolation. Plus a `vigil_call` helper that checks HTTP status and JSON-RPC `error` bodies before piping to jq, so failed calls aren't silently reported as clean scans. Plus standardization on the advertised `vigil_*` tool names from the live `/tools/list` endpoint instead of the server-side unprefixed aliases.
  - Nine read-only tools wired: `vigil_scan_approvals`, `vigil_scan_token`, `vigil_detect_honeypot`, `vigil_safety_score`, `vigil_wallet_report`, `vigil_monitor_wallet`, `vigil_token_market`, `vigil_deployer_check`, `vigil_batch_scan`. Each runs against `https://mcp.vigil.codes/tools/call` with a proper JSON-RPC `tools/call` envelope. Endpoint verified live during review (`/health`, `/tools/list`, `/tools/call` all returned 200).
  - VIGIL was also added to `ECOSYSTEM.md` in the same PR.

**Impact:** Aeon now has a second onchain-security entry point alongside the HoundFlow keyless pack — VIGIL covers the API-backed path (price + liquidity context, deployer reputation via Basescan, batch scoring, real-time monitor with `lookback_blocks` window) where HoundFlow covered the keyless `eth_call`-only path. Yesterday's `wallet-risk-weekly` (PR #340) became the first scheduled consumer of HoundFlow on the same day; VIGIL now sits as the next obvious target for a scheduled wrapper. This is the second new external skill contributor in three weeks (after Nurstar's `skill-of-the-day` on Jun-04 — also a content-producing skill not a security one) and the first MCP-server submission on the framework.

**Note on timing:** VIGIL technically merged at 15:52:45 UTC on Jun-04, six minutes before the Jun-04 push-recap ran at 15:58 UTC. Yesterday's recap listed six substantive PRs but did not include VIGIL — it's covered here as the catch-up.

---

## aaronjmars/aeon-agent

### Theme 3 — 22nd consecutive same-day-after backport
**Summary:** The backport chain extended to 22 consecutive same-day-after days. Today's target was `mcp-pulse` — the fourth of five general-ops skills from upstream aeon PR #272 (merged 2026-05-29). After this run, the only one still unbackported is `fleet-scorecard`, which is deferred because it depends on `memory/instances.json` and `scripts/prefetch-fleet-scorecard.sh` that aeon-agent doesn't currently maintain. The first commit was a verbatim copy with the standard three local adaptations; a follow-up fix corrected a phantom template-variable that would have silently broken the skill on every run.

**Commits:**
- `20c0fe3` — feat: mcp-pulse backport — 22nd consecutive same-day-after backport (#82)
  - New `skills/mcp-pulse/SKILL.md` (+323 lines): Friday 10:00 UTC weekly Model Context Protocol ecosystem tracker. Reads `memory/topics/mcp-ecosystem.md` rolling baseline, queries the `modelcontextprotocol` GitHub org for new server repos in a 7d window, fetches npm `@modelcontextprotocol/sdk` downloads + PyPI `mcp` stats, runs 3 targeted WebSearches, scores momentum on a 7-signal rubric, writes a thesis-check line (advancing / holding / stalling / reversing).
  - `aeon.yml` (+1): registered disabled between `huggingface-trending` and `monitor-kalshi` (alphabetical, Upstream sync section).
  - `skills.json` (+11/-1): total 99→100 (category research), alphabetical insert between `huggingface-trending` (idx 82) and `monitor-kalshi` (idx 83).
  - **Three documented adaptations vs upstream:** (1) `./notify` rewritten as positional `$1` (`./notify "$(cat .pending-notify-temp/<file>)"`) instead of upstream's `-f` flag, matching aeon-agent's notify script — same constraint that drove spend-monitor / follow-up-patrol / narrative-convergence backports; (2) `$(date -u -d '7 days ago' ...)` replaced with literal `${today_minus_7}` derived from the skill template — runner hook blocks `$(...)`, same fix class as PRs #63 / #67 / #71 / #77 / #81; (3) WebFetch fallback hardened across every external endpoint (npm registry, PyPI stats, GitHub API) per CLAUDE.md sandbox pattern 1.
  - **Mid-PR fix:** the first commit's adaptation #2 introduced `${today_minus_7}` as if it were a runner-injected template variable — but no such variable exists. The runner hook blocks `$VAR` expansion the same way it blocks `$(...)`, so `CUTOFF` would have resolved to the literal string `${today_minus_7}` on every run and step 3's weekly "new MCP repos" search would have returned nothing forever. Follow-up commit replaced the variable with the actual literal-cutoff pattern the sibling skills use: compute the date 7 days before the injected `${today}` and write it directly as a literal ISO timestamp, substituting the real date into the `YYYY-MM-DD` placeholder before running. The backport-note and NOTE sections were corrected at the same time.

**Impact:** aeon-agent now has a standing weekly tracker for the broader MCP ecosystem — relevant because the operator is evaluating adding MCP servers to the agent's own configuration, and because two of the three new external contributions in the past three weeks (today's VIGIL + the existing `json-render` referenced in CLAUDE.md) have been MCP servers. The 22-day backport chain remains unbroken; only `fleet-scorecard` blocks the PR #272 queue, with a known reason. The mid-PR fix also closes a class of bug — backporters reaching for a `${today}-shaped` variable that doesn't exist — by demonstrating the cleaner replacement pattern.

---

## aaronjmars/minitor

### Theme 4 — Seventh per-column UX rung: color labels
**Summary:** Minitor extended its per-column UX axis to seven consecutive features (tab groups → collapse → JSON export → quick-search → pin → duplicate → **color labels**). Operators running 10–15 columns per deck were mentally grouping them (DeFi / dev / news / social) but had no in-app marker for the grouping. Today's PR adds a 6-hex color per column that renders as a small dot beside the title in expanded view and replaces the brand accent gradient at the top of the collapsed strip. It's independent of tab groups (hide/show) and pin (reorder) — color is the visual-labeling layer, layered on top of both. The first commit shipped the feature; a follow-up fix corrected a Zod validator that would have aborted an entire deck import on one bad color value, violating the documented "drop invalid, never abort" contract.

**Commits:**
- `6e81b70` — feat: per-column color labels (#61)
  - **DB change:** new `drizzle/0008_column_color.sql` migration adds a nullable `text("color")` column. Existing rows backfill to NULL (= no color = default brand accent — no churn on any existing deck). Plus matching journal + snapshot entries (`drizzle/meta/0008_snapshot.json` +365 lines, `drizzle/meta/_journal.json` +7 lines).
  - **Schema & types:** `lib/db/schema.ts` (+1) gets the `text("color")` field; `lib/columns/types.ts` (+13) gets `Column.color?: string` with full doc on the visual semantics and the server-side hex normalization rule; `lib/deck-templates.ts` (+6) gets `DeckTemplateColumn.color?: string` so starter decks can ship pre-colored lanes.
  - **Server (`app/actions.ts`, +71):** `COLOR_HEX_RE` + `normalizeColumnColor()` canonical server-side validator (lowercased, 6-hex only — 3-hex shorthand and named CSS colors deliberately rejected so the stored form is canonical); `updateColumnColor()` server action; `importedColumnSchema` Zod regex + `importDeck` re-validates through the normalizer; `exportDeck` emits when set; `duplicateColumn` inherits color (unlike pinned — color is a labeling decision, pin is a routing decision); `loadSnapshot` maps the field through to the wire shape.
  - **Store (`lib/store/use-deck-store.ts`, +30):** `updateColor()` optimistic action mirroring server normalization; `importedDeckPatch` + `duplicateColumn` optimistic mirror.
  - **UI (`components/column/configure-column-dialog.tsx`, +109/-1):** new "Color label" field with 8 preset swatches (orange/green/blue/purple/pink/yellow/cyan/slate) + Clear button + freeform hex input with live invalid-hex error + disabled-Save guard.
  - **UI (`components/column/column-card.tsx`, +12/-4):** 10px circular color dot next to title in expanded header when color set; expanded-header + collapsed-strip top accent gradient uses `column.color ?? type.accent` — a collapsed column with color set is instantly identifiable as "that orange one" without reading the rotated title.
  - **Mid-PR fix:** `importedColumnSchema` originally validated `color` with `.regex(COLOR_HEX_RE)`, which meant one bad color value in a hand-edited or shared payload would fail `safeParse` and throw, aborting the entire deck import — the opposite of the documented "drop invalid, never abort" contract, and inconsistent with how `notifyWebhookUrl` is handled. Follow-up commit relaxed the Zod field to a loose `.max(64)` bound (mirroring `notifyWebhookUrl`) and let the imperative `normalizeColumnColor(c.color)` in `importDeck` drop invalid values to null. Behavior now matches the inline comments and the graceful-degradation the PR describes.

**Impact:** Operators can now apply group-level color codes at a glance — DeFi orange, GitHub repos blue, social purple, news yellow — for instant deck scanning at 10–15 columns. Color survives reload (DB-backed, not view-state, same shape as pin) and round-trips through export / import / share-links / deck snapshots, because color is a persistence decision about the deck's identity rather than view-state that would re-create the problem the feature exists to solve. The server-authoritative hex regex (`/^#[0-9a-f]{6}$/i` applied at both `updateColumnColor` and `importDeck` normalization) means a tampered or hand-edited export can never smuggle a non-canonical color — named CSS colors, 3-hex shorthand, JS expressions in style — into the DB. The mid-PR fix is the second "import shouldn't abort on one bad value" lesson the minitor codebase has now absorbed (the first was `notifyWebhookUrl`'s SSRF guard); future column-field additions have the explicit pattern to copy.

---

## Developer Notes

- **New external contributors:** `vigilcodes` (aeon — first commit, MCP server submission). Second new external contributor in three weeks after Nurstar (Jun-04, `skill-of-the-day`).
- **New DB migration:** minitor `drizzle/0008_column_color.sql` — additive nullable column, no backfill needed.
- **No breaking changes:** all four PRs are additive. Existing aeon-agent / minitor / aeon configs unaffected.
- **Mid-PR fix rate today: 3 of 4.** atrium-catalog-watcher landed clean. VIGIL, mcp-pulse, and color labels each shipped a follow-up commit before merge (shell-injection hardening + `vigil_*` rename, phantom template-variable, import-abort on bad color). All three fixes were structural, not cosmetic — they each closed a class of bug rather than a single one.
- **Architecture shifts:** none. Skill-count growth: aeon 182→183, aeon-agent 99→100 (rounds to a hundred enabled+disabled), minitor unchanged (DB column added).
- **Self-improve / backport cadence:** 22 consecutive same-day-after backport days. PR #272 queue is one skill from done (fleet-scorecard, deferred for known reasons). No `improve:` PRs today — yesterday's repo-article date-shell-guard (PR #81) was the last in that wave; two `$(date)` sites still remain unfixed across the fleet (`repo-actions:29` single substitution, `star-momentum-alert:69` 3-site loop) and remain explicit "left for future runs" carries.

## What's Next

- **VIGIL needs a scheduled consumer.** Same shape as the HoundFlow → wallet-risk-weekly loop that closed yesterday. Nine read-only VIGIL tools sit `workflow_dispatch`-only today; the obvious next build is a weekly `vigil-wallet-audit` (Monday morning intelligence stack, alongside `wallet-risk-weekly`) that runs `vigil_wallet_report` + `vigil_monitor_wallet` against `.x402books/wallets.json` entries. Pairs cleanly because HoundFlow is keyless `eth_call` and VIGIL is API-backed enrichment — non-overlapping coverage.
- **Atrium catalog-watcher needs to actually run.** It's registered disabled with schedule `0 12 * * 5`. First Friday after enable will be the baseline run.
- **mcp-pulse needs to actually run.** Same — `0 10 * * 5`, first Friday after enable will populate `memory/topics/mcp-ecosystem.md`.
- **Color-label adoption signal.** Worth watching whether operators trim the 8-swatch preset palette (good fit) or reach for the freeform hex input (signal the palette is wrong). Either is fine; both are silent in the DB shape.
- **PR #272 backport queue:** `fleet-scorecard` remains. Either backport the supporting `memory/instances.json` + `scripts/prefetch-fleet-scorecard.sh` first, or accept the backport chain quietly ends at 22 days and the next round picks a different upstream PR.
- **Remaining `$(date)` anti-pattern sites:** `repo-actions:29` and `star-momentum-alert:69` (3 expansion sites inside one `for D in $(seq 13 -1 0); do DATE=$(date ...)` block — bigger fix, needs a literal-date table or loop unroll). Both still explicit "left for future runs" carries.
