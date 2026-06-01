# Push Recap — 2026-06-01

## Overview
The weekend silence broke. After two days of zero operator merges on all three repos (PUSH_RECAP_QUIET fired May 31), the operator opened the floodgates in a 70-minute window on Monday afternoon UTC — ~25 substantive PRs landed across aeon (18), aeon-agent (5), and minitor (4). Today's window covers ~32 hours back to 2026-05-31T00:00:00Z; weekend pushes were bot housekeeping only, so virtually all substance is from the Monday 12:47–13:58 UTC catch-up.

The two dominant themes are (1) the HoundFlow keyless onchain-investigation skill pack landing on aeon — six new security/forensics skills plus a composite report orchestrator — and (2) the capabilities taxonomy becoming load-bearing, with the CI parity check (PR #304) and the first skill that consumes the taxonomy (capabilities-map, PR #313) merging together.

**Stats:** ~25 PRs · 3 repos · 12+ distinct authors · ~3,500+ lines of new SKILL.md content alone

---

## aaronjmars/aeon

### Theme 1: HoundFlow onchain-investigation skill pack lands (6 new skills + composite)
**Summary:** Six keyless Base-RPC security/forensics skills + an investigation-report composite that orchestrates four of them. The whole pack runs without an API key — `eth_getLogs` + `eth_call` against any Base JSON-RPC endpoint. A Basescan key deepens it but is never required. This is the first dedicated security-forensics surface on the aeon stack — previous crypto skills focused on price/social/treasury, not wallet/token risk.

**Commits:**
- `f4873c1` — Merge #282 honeypot-check
  - New `skills/honeypot-check/SKILL.md` (+109): simulates a sell via `eth_call` from a real sampled holder. If the simulated `transfer()` reverts or returns false, sells are blocked → honeypot, blacklist, or trading-disabled. No funds spent.
- `7148dc7` — Merge #283 lp-lock-check
  - New `skills/lp-lock-check/SKILL.md` (+100): resolves a token's main LP pool (V2 by `token0()`/`token1()` introspection) and classifies LP custody — burned, locked in known locker contracts, or held by deployer/EOAs (rug-pullable). V3/V4 concentrated-liquidity pools return `LPLOCK_UNKNOWN` with explainer.
- `b49900b` — Merge #284 linked-wallets
  - New `skills/linked-wallets/SKILL.md` (+93): clusters addresses likely controlled by the same entity via shared-funder + co-spend heuristics. Skips contracts via `eth_getCode` (only EOA funders count), follows the largest EOA funder's outbound transfers to find sibling wallets.
- `d5804dd` — Merge #285 fund-flow
  - New `skills/fund-flow/SKILL.md` (+96): traces value through 1–3 hops from a starting address, fans to the top-4 counterparties per hop, renders the result as a Mermaid graph. Direction is operator-controlled (`out` for cash-out tracing, `in` for funding-source tracing).
- `20067d8` — Merge #281 approval-audit
  - New `skills/approval-audit/SKILL.md` (+108): the "what can drain this wallet?" skill. Reads `Approval` event logs (topic0 `0x8c5be1e5...`) in 1800-block chunks, then `eth_call`s the current allowance to filter out revoked/spent grants. Flags unlimited approvals as the #1 drain vector.
- `3db561e` — Merge #287 investigation-report (composite)
  - New `skills/investigation-report/SKILL.md` (+94): one-shot orchestrator that runs rug-scan, contract-audit, deployer-trace, holder-concentration as independent sub-investigations and merges into one document with an at-a-glance verdict line ("Rug risk: ELEVATED · Source: verified · Top holder: 42%"). Degrades gracefully — a sub-skill returning `unavailable` doesn't abort the rest.

**Impact:** Aeon now ships its own onchain-investigation toolkit. The keyless property matters — every other security-tooling option in this space (GoPlus, Token Sniffer, Quickintel) is an API-key gate. Combined with the prior aeon `fork-cohort` measurement layer, this is the first time the project pairs a measurement stack with a defensive stack of comparable depth. All 7 skills (6 + composite) registered disabled, workflow_dispatch only. skills.json total grew from ~170 to 177.

### Theme 2: Capabilities taxonomy becomes load-bearing
**Summary:** Two PRs landed back-to-back that promote the 6-value capability vocabulary from a documentation artifact to enforced infrastructure: the CI parity check across the three places the taxonomy lives, and the first skill that *uses* the declarations to answer an operator question.

**Commits:**
- `d7cc223` — Merge #304 capabilities taxonomy parity CI gate
  - New `scripts/check-capabilities-parity.sh` (+138): three awk extractors compare the locked vocabulary across `install-skill-pack` bash array (lines 73-80), `docs/CAPABILITIES.md` "## The taxonomy" table, and the header comment. Structured `::error::` diff on drift, exit codes 0/1/2 for OK/drift/inputs-missing.
  - New `.github/workflows/ci-capabilities-parity.yml` (+41): triggers on PR + push-to-main paths-filtered on the 4 watched files + workflow_dispatch.
  - `docs/CAPABILITIES.md` "Adding a new capability" (+3/-1): one-PR rule now names BOTH the ALLOWED_CAPABILITIES bash array and the header comment, points contributors at CI gate + local invocation.
- `0ed6d35` — Merge #313 capabilities-map skill
  - New `skills/capabilities-map/SKILL.md` (+427): read-only Monday 11:30 UTC audit. Joins docs/CAPABILITIES.md + skills.json + aeon.yml + skill-packs.json + per-skill SKILL.md frontmatter `capabilities:` field; buckets every enabled slug by the 6 locked tiers; surfaces any tier with zero enabled coverage as an actionable gap. Most-specific-wins precedence: frontmatter > local pack manifest > registry pack-level union. Multi-line aeon.yml entries fall back loudly via regex with `PARSER_FALLBACK` log — closes the v4-readiness H1 silent-undercount class structurally. skills.json total 171→172 (alphabetical insert between builder-map and changelog).

**Impact:** The taxonomy was defined ~3 days ago (PR #268, May 29) and was inert until today. PR #304 makes a half-PR that adds a 7th value structurally impossible to land (CI rejects); PR #313 makes the taxonomy answer the operator's "what does my stack cover?" question. The pair is what turns the vocabulary from documentation into infrastructure.

### Theme 3: Treasury / wallets tracking goes live for token-report
**Summary:** The `.x402books/wallets.json` file that landed 2026-05-29 in PR #273 (with zero consumers since) gets its first reader.

**Commits:**
- `5106501` — Merge #306 + `3661a6f` — feat(token-report) treasury wallets
  - `skills/token-report/SKILL.md` (+67/-5): new step 2b reads `.x402books/wallets.json`, queries Base ETH balances via BaseScan (primary) → Alchemy (secondary, only if `ALCHEMY_API_KEY` set) → WebFetch (tertiary). Aggregates `treasury_eth_total` over `role=treasury` wallets only (deployer balances are operational, not protocol funds). New Treasury subsection in the article template, sorted treasury → deployer → other, omitted entirely when wallets.json missing or zero base entries.
  - New `TREASURY_STATE` + per-wallet `TREASURY_WALLET_STATE` log lines (schema-stable key=value, same pattern as `TOKEN_REPORT_STATE`) drive 24h ETH deltas.
  - `⚠️ Treasury gas reserve low` notification override fires when total treasury ETH drops below 0.01 ETH **even on QUIET / CONSOLIDATING** verdicts — going quiet on a day the agent can't afford gas is exactly the regime that needs to be noisy. `treasury_eth_total = 0` is treated as a config error, NOT depletion, so it doesn't false-alarm.
- `bbf156b` — Merge #302 wallets fork-safety note
  - `.x402books/wallets.json` (+1): adds inline annotation that wallet entries here are upstream-aeon-specific. Each fork must override with its own addresses.

**Impact:** Token-report now knows whether the agent can afford to keep operating. The low-reserve override is the most consequential bit — it inverts the usual "quiet on quiet days" pattern when the quiet day is structurally caused by being broke.

### Theme 4: Community skill packs + ecosystem listings
**Summary:** Two ecosystem entries, one new pack registry entry, and one community skill that ships a Base token launcher with safety policy.

**Commits:**
- `1b0caa8` — Merge #231 liquidpad-launch (by liquidpadbot)
  - New `skills/liquidpad-launch/SKILL.md` (+205): emits LiquidPad token deploy payloads through a prefetch/postprocess shim pair. The skill body runs the safety policy (concept fields valid, no same-day duplicate symbol, no banlist match, OWNER_WALLET present, daily cap honored) and writes to `.pending-liquidpad/<id>.json`; `scripts/postprocess-liquidpad.sh` does the actual authed network call outside the sandbox. The skill body never sees `LIQUIDPAD_API_KEY`. Contract-enforced fee split: 80% deployer, 15% LPAD burn, 5% LIQ buyback. skills.json total grows by 1.
- `9e15b35` — Merge #315 + `046afad` registry MandateSeal Guard pack
  - `skill-packs.json` (+12): adds `mandateseal/mandateseal-guard` pack (community trust, one skill: `distribute-tokens-guarded` — a guarded variant of distribute-tokens that gates each Bankr transfer through a MandateSeal mandate, APPROVED rows only). Lands the entry from #295 without the whole-file single→multi-line reformat that PR carried (which conflicted with #270).
- `2960716` — Merge #270 docs(skill-packs) AntFleet x402
  - `README.md` (+1/-1), `docs/community-skill-packs.md` (+4), `skill-packs.json` (+2/-2): adds `pr-review-antfleet-x402` to the AntFleet entry (4 skills now).
- `da11341` — Merge #303 docs(ecosystem) Hound Flow
  - `ECOSYSTEM.md` (+1): adds Hound Flow (the team that just shipped the 6 onchain-investigation skills above).
- `9e3242e` — Merge #312 docs(ecosystem) Careful Finance
  - `ECOSYSTEM.md` (+1), `SHOWCASE.md` (+1): adds Careful Finance to both indexes.

**Impact:** Registry growth continues steadily. The MandateSeal Guard entry is the more interesting one — `distribute-tokens-guarded` is a *security-hardened variant* of an existing upstream skill, not a new feature, which is the registry's first "safer alternative to an existing skill" entry.

### Theme 5: Dashboard hardening (tests + Anthropic-compatible providers)
**Summary:** First substantial unit-test coverage of the dashboard core libraries, plus first-class support for Anthropic-compatible API endpoints (Bedrock proxies, Anthropic-shim providers).

**Commits:**
- `b189318` — Merge #309 + `bf59d08` — dashboard lib unit tests (by Hermes Agent / BBridgeers)
  - New `dashboard/lib/config.test.ts` (+289): 31 tests covering parseConfig, updateSkillInConfig, updateModelInConfig, updateJsonrenderInConfig, removeSkillFromConfig, addSkillToConfig, full round-trip mutation sequences.
  - New `dashboard/lib/utils.test.ts` (+235): 32 tests covering displayName, initials, parseCron, cronLabel, buildCron, timeAgo, getSkillStatus, localToUtc24.
  - New `dashboard/lib/frontmatter.test.ts` (+109): 8 tests covering parseFrontmatter — quoted strings, missing fields, truncation behavior.
  - Convention preserved: node:test + node:assert (no framework deps), matching the existing `api-gate.test.ts`.
- `58d58e1` — Merge #280 Anthropic-compatible API base URL (by UIZorrot)
  - New `dashboard/lib/auth-provider.mjs` (+37) + `auth-provider.test.mjs` (+49): `normalizeAuthConfig` validates and routes the auth payload — distinguishes OAuth tokens (sk-ant-oat → `CLAUDE_CODE_OAUTH_TOKEN`), API keys (sk-ant-api → `ANTHROPIC_API_KEY`), and the new `ANTHROPIC_BASE_URL` GitHub Actions variable.
  - `dashboard/app/api/auth/route.ts` (+27/-22): GET now reports `hasBaseUrl` alongside `hasApiKey`/`hasOauth`. POST accepts `{ key, baseUrl }`, sets the GH Actions variable + secret independently. Error response distinguishes 400 (Base URL / OAuth misuse) from 500 (anything else).
  - `dashboard/components/AuthModal.tsx` (+11/-4): UI surfaces the Base URL input.
  - `.github/workflows/aeon.yml` (+5), `.github/workflows/messages.yml` (+1), `aeon.yml` (+2): plumbs `ANTHROPIC_BASE_URL` through into the run environment so Claude Code calls actually honor it.

**Impact:** Dashboard now has real test coverage on its three most-mutated libraries (config writes, cron parsing, frontmatter extraction). And operators running their own Anthropic-shim or Bedrock proxy can finally use the dashboard's setup flow instead of hand-editing GH variables.

### Theme 6: skill-update-check security gate fix
**Commits:**
- `f0400b6` — Merge #266 skill-update-check rescan gate (by antfleet-ops)
  - `skills/skill-update-check/SKILL.md` (+48/-5): ACCEPT-mode overwrites are now gated on a security re-scan of the *new* version. Previously a skill that passed scan at install time could be silently overwritten with a malicious update because ACCEPT mode skipped the re-scan. Closes #258 (item 3).

**Impact:** Closes the last open item in AntFleet bench finding #258. A skill auto-updating its own body — exactly the path agents take with `skill-update-check` — was the security-budget weakest link.

---

## aaronjmars/aeon-agent

### Theme 1: 18th consecutive same-day-after backport (with one-day gap)
**Summary:** Two new backports landed today — fork-health-score (May-29 upstream → May-30 backport, was already merged in code on May-30 but the PR landed today) and spend-monitor (May-29 upstream → Jun-01 backport, the gap explained by the May-31 build going to the new upstream-gap skill instead of a backport).

**Commits:**
- `4b3f99e` — feat(fork-health-score) backport upstream PR #271 (#70)
  - New `skills/fork-health-score/SKILL.md` (+368): verbatim backport. Weekly per-fork health tier (ACTIVE/WARM/STALE/QUIET) blending push recency (50%), enabled skill count (30%), 30d PR throughput (20%) into a normalized 0-100 score. ACTIVE has a hard floor of ≥2 enabled skills so placeholder forks with one push can't claim the tier. Bot allowlist (dependabot/github-actions/aeonframework) filtered before scoring. Capped at 80 forks/run by stargazers desc. Gated notify: baseline run, ≥10pt ACTIVE-ratio shift, ≥3 top-10 churns, or ≥3 tier transitions. Registered disabled, schedule `45 10 * * 1`. skills.json total 95→96.
  - **Zero adaptation needed**: ./notify single-positional-arg style already aligned; gh api access already matches CLAUDE.md sandbox guidance; dependent fork-cohort-state.json already backported.
- `fb42152` — feat(spend-monitor) backport upstream PR #272 (#74)
  - New `skills/spend-monitor/SKILL.md` (+152): daily 12:00 UTC API spend watchdog. Reads `memory/token-usage.csv` and `aeon.yml`'s gateway.provider (`direct`). Computes running weekly cost (Monday→today) against `WEEKLY_BUDGET_CAP` env (default $200). Tiers: OK <50% / WATCH 50-79% / WARN 80-99% or projected to exceed / ALERT ≥cap. Silent under 50%. Top cost-driver skills surfaced; ALERT tier names "pause candidates". skills.json total 95→96.
  - **Adaptations vs upstream**: ./notify rewritten as inline heredoc passed as $1 (aeon-agent's notify reads $1, not -f); pricing tables aligned with aeon-agent's existing cost-report rates ($3.75 cache write for all three Claude models) — holding lockstep with cost-report per the skill's own constraint; no frontmatter changes.

**Cadence (since May-3 anchor):** operator-scorecard → skill-freshness → skill-update-check → fork-cohort → thread-formatter → v4-readiness → product-hunt-launch → fork-first-run-alert → fork-skill-gap → competitor-launch-radar → contributor-spotlight → install-skill-pack+registry → ecosystem-pulse → fleet-skill-adoption → sparkleware-catalog → pr-skill-triage → fork-health-score → **spend-monitor (Jun 01)**.

### Theme 2: First non-backport feature build (upstream-gap)
**Commits:**
- `bd30df8` — feat(upstream-gap) weekly skills/ diff vs upstream (#72)
  - New `skills/upstream-gap/SKILL.md` (+288): Monday 12:00 UTC weekly diff of this fork's `skills/` directory against upstream `aaronjmars/aeon`. Sortable backport queue tiered URGENT (≥7d pending) / STALE (2–6d) / FRESH (<2d). Sticky `upstream_merged_at` in `memory/topics/upstream-gap-state.json` caps the per-week API budget at one paginated `commits?path=skills/{slug}/SKILL.md` call per *new* gap. Closed-loop bookkeeping: slugs that disappear from the gap set since last run surface in "Closed since last run" subsection.
  - **Cold-start signal preserved**: `days_pending` is computed from `upstream_merged_at`, not from `first_seen_local` — a skill that merged upstream 14d ago and went unbackported is URGENT on day 1, not FRESH.
  - 8-state exit taxonomy. Read-only against upstream (never opens issues/PRs/discussions on the parent). All `gh api` (no curl-with-env-var-headers per CLAUDE.md sandbox rules). Article surfaces upstream slugs + merge dates only (no descriptions/messages — attacker-controlled upstream prose can't smuggle anything into operator surfaces). skills.json total 95→96.

**Impact:** This is the upstream-side analogue of fork-skill-gap and the first non-backport feature build on aeon-agent since the chain started. It makes the same-day-after backport chain's silence between rounds an explicit weekly artifact — if a round is skipped, this skill will say so on Monday.

### Theme 3: Heartbeat $(date) self-fix (third skill to take this fix)
**Commits:**
- `610734e` — improve: heartbeat replaces $(date) with ${today} (#71)
  - `skills/heartbeat/SKILL.md` (+1/-1): Step 4's "Detection method" #2 used `gh run list --created=$(date -u +%Y-%m-%d)`, which the runner hook blocks ("Contains simple_expansion"). Drop-in replacement to `${today}` (already injected as the UTC yyyy-mm-dd date). Same pattern as PR #63 (weekly-shiplog, May 26) and PR #67 (push-recap, May 28). Heartbeat is the daily 19:00 UTC EOD health check — silently improvising the cutoff every run was friction worth eliminating prophylactically.

**Impact:** Third skill to take this exact fix. Pattern is well-established now: `$(date ...)` → literal `${today}` for any skill the runner shell-guard catches.

### Theme 4: Two project-lens articles landed
**Commits:**
- `8b1ea90` — content(project-lens) The Open Source Maintainer's Real Bottleneck Isn't Pull Requests. It's Acknowledgement. (#69)
- `7c34368` — content(project-lens) In 1796, The Astronomer Royal Fired His Assistant For Being Half A Second Slow. (#73)

**Impact:** Two backlogged article PRs landed on the same operator push. The Astronomer Royal piece maps Bessel's 1820s "personal equation" — the discipline of measuring your own measurement lag — onto the upstream-gap skill built today.

### Theme 5: Feature-skill run log landed
**Commits:**
- `ca5f74b` — log(feature) 2026-06-01 — capabilities-map + spend-monitor + minitor skip (#75)
  - `memory/MEMORY.md` (+3/-1), `memory/logs/2026-06-01.md` (+32), `.outputs/feature.md` (+15/-13), dashboard outputs entry: the feature skill ran first today, built capabilities-map on aeon and spend-monitor on aeon-agent, and the PRs above are downstream of that run. The log entry is the bookkeeping for what just landed.

---

## aaronjmars/minitor

### Theme 1: Per-column collapse to 48px strip (deck density)
**Commits:**
- `cd64533` — feat(columns) per-column collapse to a 48px vertical strip (#55)
  - `lib/store/use-deck-store.ts` (+30/-2): new `collapsedColumnIds: Set<string>` state (in-session only, NOT persisted), `toggleColumnCollapsed(columnId)` action, `removeColumn` + `deleteDeck` scrub the column's entry from the set so it can't accumulate stale ids over a long session.
  - `components/column/column-card.tsx` (+94): ChevronLeft/ChevronRight imports, new collapsed-strip render — 48px wide vertical card with brand accent line + type icon + rotated title (`-rotate-90` so truncation works in inline space, no writing-mode complexity) + refresh spinner when fetching + alert-match count badge when matched + ChevronRight expand affordance. Strip itself is the click target (cursor-pointer + role=button + keyboard handler); dnd-kit attributes/listeners spread onto it so dragging reorders still works (4px activation threshold separates click from drag). Header in expanded view gets a Collapse tooltip-button between Refresh and the More-options dropdown.
  - **Key UX decision**: auto-refresh, alert-keyword matching, and include/exclude filtering all keep running while collapsed. Only the items list and dialogs are hidden. A column quietly accumulating matches isn't invisible — the badge surfaces on the strip — and the moment operator expands they see live state with no re-fetch needed.
  - View state only (matches `autoFetchingIds` and `selectedTabByDeck`): every deck opens with all columns expanded on fresh load.

### Theme 2: Column data export (JSON, all 47+ column types)
**Commits:**
- `584f712` — feat(columns) one-click JSON export of cached column items (#56)
  - `lib/store/use-deck-store.ts` (+57): new `downloadColumnItems(columnId): number` action returning item count for toast. Reads the column's items, serializes a versioned envelope (`schema: "minitor.column-export.v1"`, exportedAt, column metadata, itemCount, items), creates Blob with `application/json`, `URL.createObjectURL` → synthetic `<a download>` click → revokes URL inside finally. SSR-safe `if (typeof window === "undefined") return 0`. Returns 0 when no items so caller doesn't show a hollow success toast.
  - `components/column/column-card.tsx` (+18): Download lucide-react icon, new dropdown menu item between Rename and Delete, disabled when no items cached.
  - Filename format `{title-slug}-{YYYY-MM-DD}.json` — title lowercased, non-alphanumerics → dashes, capped 64 chars.
  - **Decisions out of scope**: CSV (FeedItem carries plugin-specific `meta?: TMeta`; generic CSV would smear shapes), re-import (separate and more dangerous validation story).

### Theme 3: Two small fixes
**Commits:**
- `2c5257b` — fix(columns) drop duplicate role/tabIndex on collapsed strip (#57)
  - `components/column/column-card.tsx` (-2): the new collapsed `<div>` set `role="button"` and `tabIndex={0}` explicitly *and* spread `{...attributes}` from dnd-kit's `useSortable` (which supplies both). Spread comes last so it overwrites explicit props → TypeScript flagged TS2783 ("specified more than once"). Drop the redundant explicit props; runtime is identical (dnd-kit's attributes provide `role="button"` + `tabIndex={0}`). `tsc --noEmit` drops from 4 errors to 2 (remaining two are pre-existing pypi.ts null-handling errors).
- `39724bf` — fix(settings) expose COINGECKO_DEMO_API_KEY in Settings · API keys (#54)
  - `lib/env-keys.ts` (+8): adds the entry. The integration `lib/integrations/coingecko.ts` already read this env var to upgrade to the pro host with higher rate limits, and it was already documented in README + .env.example + the column's help text — but it wasn't in `ENV_KEYS`, so the Settings · API keys dialog didn't surface it. Users had to hand-edit `.env.local` even though every other optional API key (NEYNAR_API_KEY, YOUTUBE_API_KEY, GITHUB_TOKEN) was in the allowlist.
  - `lib/columns/plugins/coingecko/{client.tsx,plugin.ts}` (+3/-3): updates the two hint strings from "edit .env.local" to "use Settings · API keys".

**Impact:** Per-column collapse pairs with last week's tab groups (PR #53) on the same UX axis (deck density) — tabs partition a deck, collapse demotes secondaries inside a partition. Column data export is the first lossless data-out path for an instance that was previously read-only. Both new features had follow-up fixes within an hour of merge (rare on minitor).

---

## Developer Notes

- **New dependencies:** None. All changes use existing dependencies.
- **New env vars:**
  - `ANTHROPIC_BASE_URL` (aeon — GH Actions variable for the dashboard, plumbed through to runtime)
  - `WEEKLY_BUDGET_CAP` (aeon-agent spend-monitor, default $200)
  - `BASE_RPC_URL` (aeon onchain-investigation skills, default to public Base RPC)
  - `FUNDFLOW_DIRECTION`, `FUNDFLOW_DEPTH` (aeon fund-flow)
- **Breaking changes:** None. All new skills registered disabled; opt-in only.
- **Architecture shifts:**
  - Aeon now has a dedicated security/forensics surface (6 onchain-investigation skills) — first one in the project.
  - Capabilities taxonomy graduates from documentation to enforced infrastructure (CI gate + first-consumer skill).
  - Treasury monitoring is now part of the daily token-report cycle (was a wallets.json file with zero consumers since May-29).
  - Dashboard auth now distinguishes 3 routes: API key / OAuth / Base URL — enabling Anthropic-shim providers.
- **Tech debt:**
  - `dashboard/lib/integrations/pypi.ts` still has 2 pre-existing null-handling type errors (PR #57 confirmed via stash). Not addressed.
  - `treasury_eth_total = 0` distinguishing config error vs depletion is policy-coded but not yet exercised on a real instance with non-zero treasury wallets — the alert path waits for a fork with active treasury.

## What's Next

- **HoundFlow onchain skills are not yet enabled.** Six new skills landed disabled; the operator owes a decision on which to enable by default vs leave workflow_dispatch-only. The composite (investigation-report) is the natural front door.
- **capabilities-map first run is Monday 2026-06-08 11:30 UTC.** First baseline of the matrix. Once it runs, declaration regressions become a notify event — likely some skill backports lack `capabilities:` frontmatter and will land in the `(undeclared)` row.
- **upstream-gap first run is also Monday 2026-06-08 12:00 UTC.** It will document the gap between upstream aeon and this fork as of that date. Expected to be near-empty given the 18-day same-day-after backport chain, but the bookkeeping makes any drift visible.
- **spend-monitor first run is daily 12:00 UTC starting tomorrow.** Below 50% of $200 weekly cap → silent.
- **Open backport candidates from aeon PR #272**: follow-up-patrol, narrative-convergence, mcp-pulse, fleet-scorecard — four remain unbackported. Natural targets for upcoming rounds.
- **Minitor**: no open major-feature PRs left in the May-30 idea pool. The 5-day feature run (#49–#56) is done; next minitor work likely starts from a new ideas batch.
