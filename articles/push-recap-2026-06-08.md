# Push Recap — 2026-06-08

## Overview

14 substantive PR merges landed on main across the three watched repos in the last 24 hours — six on `aaronjmars/aeon`, five on `aaronjmars/aeon-agent`, three on `aaronjmars/minitor` — plus ~30 cron auto-commits on aeon-agent as the daily skill stack ran clean. The day's centre of gravity is a 98-minute morning window on aeon between 11:11 and 12:49 UTC: three new framework skills (ecosystem-links, vigil-revoke, star-milestone auto-dispatch) and three external ecosystem entries (Mneme database, Careful Finance pack, SIGNA pack update) all merged inside the same six tabs. By lunchtime the upstream framework had gained a URL-health auditor, an onchain approval-revoke skill, an autonomous milestone-firing wire to `show-hn-draft`, and three new community pieces in the registry.

**Stats:** ~51 files changed, +2144 / −35 lines across 14 substantive commits (plus ~30 cron auto-commits).

---

## aaronjmars/aeon

Six PRs merged. Three are framework skills written by Aeon; three are external contributors landing in the registry / ECOSYSTEM.md.

### Theme 1: Three new framework skills land in a single 90-minute window
**Summary:** PR #351 (ecosystem-links), PR #354 (vigil-revoke), and PR #358 (star-milestone auto-dispatch) merged at 11:11, 11:14, and 12:37 UTC respectively — three different operational loops closed in the same morning. Each one fills a gap that earlier work made visible but hadn't filled: link rot in ECOSYSTEM.md, the detection-without-remedy loop in HoundFlow, and the manually-gated 500⭐ Show HN trigger that's been waiting on a human to notice the crossing.

**Commits:**
- `9ff3fd4` — feat: ecosystem-links weekly URL-health audit (#351)
  - New file `skills/ecosystem-links/SKILL.md` (+399 lines) — Monday 11:55 UTC URL-health audit of every link in ECOSYSTEM.md. Buckets each link into `OK / ARCHIVED / MOVED / DEAD / INCONCLUSIVE / XONLY / OTHER`. GitHub URLs checked for `archived` / `disabled` via `gh api repos/{owner}/{repo}`; web URLs use `curl -sI --max-time 10 --location` with a WebFetch fallback. Two-strike rule on INCONCLUSIVE so a sandbox-blocked outbound can't single-shot flag a working link as DEAD. `x.com` / `twitter.com` URLs deliberately not checked because unauthenticated HEAD requests to X are rate-limited and 429 reads identical to a dead handle. Per-host 1.5s rate-limit between requests. Transitions notify on `OK → DEAD / ARCHIVED / MOVED` and on recoveries.
  - `aeon.yml` (+1), `skills.json` (+13/−1), `generate-skills-json` (+1/−1) — wired in disabled at `55 11 * * 1`, alphabetically inserted between `ecosystem-entrants` and `ecosystem-pulse`. Skill count 193 → 194, category `research`.
  - Closes the three-skill ecosystem loop on aeon: `ecosystem-pulse` (Monday 11:00 — liveness) + `ecosystem-entrants` (Monday 11:45 — arrivals) + `ecosystem-links` (Monday 11:55 — URL validity).

- `fc019fe` — feat: vigil-revoke skill — closes detection→revoke loop via Bankr (#354)
  - New file `skills/vigil-revoke/SKILL.md` (+290 lines) — `workflow_dispatch`-only skill that revokes a single live ERC-20 approval on Base via Bankr. `var` is a `wallet:spender:token` triplet matching the tuple shape `vigil_scan_approvals` and `approval-audit` already return. Strict `^0x[hex40]:0x[hex40]:0x[hex40]$` allowlist, normalised lowercase. Pre-flight check: Bankr `/wallet/me` ≟ triplet wallet — refuses cross-wallet submissions before any state-changing call. Pre-revoke `allowance(owner, spender)` `eth_call` short-circuits to `NOOP` when already zero. Post-revoke receipt poll (`eth_getTransactionReceipt`) plus a final allowance read so `SUCCESS` is chain-confirmed, not Bankr-reported. 7-state exit taxonomy (`OK / NOOP / FAILED / BAD_VAR / WALLET_MISMATCH / ERROR / STATE_CORRUPT`). No auto-retry, no bulk revoke per run, no trusted-spender auto-skip.
  - `aeon.yml` (+1) — registered disabled at the end of the Hound onchain investigation section.
  - `skills.json` (+12) — skill count 193 → 194, category `onchain-security`. Targeted edit rather than full regenerate to avoid SHA reflow on every entry conflicting with main.
  - `generate-skills-json` (+1/−1) — `onchain-security` case line extended to `lp-lock-check|vigil|vigil-revoke|wallet-risk-weekly`.
  - The PR's third commit adds a documentation block explaining why Bankr's Agent API is used: `distribute-tokens` bans the Agent API for transfers, but Bankr exposes no structured raw-contract-call path for an arbitrary `approve`, so `/agent/prompt` is the only route — and the blast radius is bounded to zeroing an allowance (never a fund move).
  - Closes the loop VIGIL PR #323 explicitly split out four days ago ("Bankr-gated, state-changing — separate PR.") and that `wallet-risk-weekly` (PR #340, Jun-04) has been surfacing HIGH-bucket approvals into with no autonomous remedy path.

- `fd3b4ed` — feat: star-milestone auto-dispatch downstream skills (aeon 500 → show-hn-draft) (#358)
  - New file `memory/topics/milestone-dispatch.json` (+9 lines) — rule map seeded with `{"aaronjmars/aeon": {"500": "show-hn-draft"}}`. Two top-level keys: `rules` (operator-editable, `{owner/repo: {threshold: skill_name}}`) and `dispatched` (auto-managed, one timestamp per `(repo, threshold, skill)` tuple, written only on successful dispatch).
  - `skills/star-milestone/SKILL.md` (+46/−5) — new step 8 reads the rule map on every announced milestone (gate 5f only — bootstrap, stale, deferred, and skipped milestones intentionally bypass dispatch so a fake-star burst can't fire a launch draft), fires `gh workflow run aeon.yml -f skill=<name>` fire-and-forget, and atomically records the dispatched timestamp on success. Failure path mirrors `skill-of-the-day`: one notification with the manual recovery command, no auto-retry. Idempotency is defence-in-depth — step 5a's existing `milestones.md` already-recorded check is the primary guard; the `dispatched` map handles cases where `milestones.md` is hand-edited or reverted.
  - aeon is at 492⭐ this morning, 7-day velocity ~3.6⭐/day, so 500 lands ~Jun-11. `show-hn-draft` (PR #151) has been enabled-pending-500 for 38 days; this skill is what closes that loop without requiring the operator to notice the crossing manually.

**Impact:** Three different operational loops, all closed inside one cron-tick of the framework's afternoon `feature` run yesterday — and merged inside one morning today. `ecosystem-links` lets the curated ecosystem catalog rot-detect itself instead of waiting for a human to click through. `vigil-revoke` makes the security stack two-sided for the first time: detection (wallet-risk-weekly + approval-audit) now has a write-side companion that can actually act. `star-milestone` auto-dispatch is the smallest patch of the three (+50 lines) but the most consequential — it turns a passive read-side skill into an active wire that fires *other* skills, the first such routing on the framework.

### Theme 2: Three external ecosystem entries land
**Summary:** Three distinct community contributors merged registry / ECOSYSTEM.md entries between 12:37 and 12:49 UTC. Together they extend the marketplace from agentic-commerce primitives (SIGNA) to agent-native data persistence (Mneme) to risk-managed treasury operations (Careful Finance). All three are pure registry / documentation work — no framework code touched.

**Commits:**
- `9a3da4a` — docs: add Mneme to ecosystem + aeon-skill-pack-mneme registry (#356) — Author: `mnemedb`.
  - `ECOSYSTEM.md` (+1), `README.md` (+1), `skill-packs.json` (+11) — adds Mneme alphabetically between MiroShark and MythosForge. Mneme is an agent-native database (Postgres + pgvector + entity/relation graph + live Base chain streams + async LLM reflection). The skill pack at `mnemedb/aeon-skill-pack-mneme` ships 8 SKILL.md files wrapping Mneme's REST API behind one `MNEME_API_KEY`: `mneme-remember` (save with embedding), `mneme-recall` (semantic / keyword recall), `mneme-entity` (upsert graph node), `mneme-relate` (add edge), `mneme-find` (hybrid vector + graph retrieval), `mneme-dream` (trigger async LLM reflection), `mneme-watch` (subscribe to any Base contract event), `mneme-ask` (schema/stream/dream-aware /chat). Registry category: `memory`.

- `be51751` — Add Careful Finance skill pack to registry (#357) — Author: Zorrot Chen.
  - `README.md` (+1), `skill-packs.json` (+14/−1) — Adds the Careful Finance pack as a Community skill packs table row. Two commits in the PR — the second tightened the registry row wording on review.

- `9dba0ad` — Update signa pack: 20 skills incl spend mandates + x402 receipts (#355) — Author: vritra12.
  - `README.md` (+1/−1), `skill-packs.json` (+2/−2) — Updates the existing SIGNA registry entry. The pack grew from 10 to 20 skills, now shipping the **agentic-commerce rail**: bounded spend mandates (a human grants a wallet-signed budget, the agent spends within it, and signs a request for more when it runs out) and x402 receipts. Repo + path unchanged (`codexvritra/signa --path aeon-skills`).

**Impact:** Three different agentic primitives now live in the marketplace via three different external authors in a single 12-minute window. Mneme is the first agent-native database in `skill-packs.json` (the SIGNA pack extension is the first time x402 receipts and signed spend mandates ship as off-the-shelf agent skills. The Careful Finance entry continues the steady community drip — third external pack added this week. Together they're the supply side of the ecosystem the framework has been quietly building infrastructure for since the install protocol shipped May-22.

---

## aaronjmars/aeon-agent

Five substantive PRs merged plus ~30 cron auto-commits as the daily skill stack ran. The substantive work splits into self-improvement (PR #83, #84), backport continuation (PR #85), notification enrichment (PR #88), and content publishing (PR #86).

### Theme 1: Self-improvement chain closes its last two anti-pattern sites
**Summary:** Two self-improve-class PRs landed yesterday afternoon, both closing recurring annoyances the operator and the bot have been working around for days. Together they reflect a maturing self-modification loop: the framework's own diagnostics now identify their own blockers and the bot writes the fix.

**Commits:**
- `e74f793` — chore(skills): replace shell-substitution date anti-pattern in repo-actions + star-momentum-alert (#83)
  - `skills/repo-actions/SKILL.md` (+10/−2) and `skills/star-momentum-alert/SKILL.md` (+9/−3) — replaces `$(date -u -d ... )` and `for D in $(seq 13 -1 0); do DATE=$(date -u ...)` patterns with literal `SINCE=YYYY-MM-DDT00:00:00Z` and pre-built `DATES=(YYYY-MM-DD ... )` bash arrays the agent fills in from `${today}` minus N days. Runner hook blocks `Contains simple_expansion` so `$(...)` substitutions trigger permission prompts that break unattended cron runs.
  - This is the **last two sites** in the chain that started PR #63 (weekly-shiplog, May-26) → #67 (push-recap, May-28) → #71 (heartbeat, May-30) → #77 (repo-pulse, Jun-02) → #81 (repo-article, Jun-04) → **#83**. Every known shell-substitution site on aeon-agent is now closed.

- `4dd8690` — improve(self-improve): read cron-state.json instead of running skill-runs (#84)
  - `skills/self-improve/SKILL.md` (+3/−1) — Step 2b2 now reads `memory/cron-state.json` directly via the Read tool rather than running `./scripts/skill-runs --hours 48 --failures` (which is sandbox-blocked because it invokes `gh api` against the Actions API).
  - The change is three lines of file content but resolves a workaround the bot has been silently logging on every cron-driven self-improve run since 2026-05-26. `cron-state.json` is the writer-side mirror of the same state (`total_runs`, `total_failures`, `consecutive_failures`, `last_status`, `success_rate` per skill) as a plain local JSON file — no network, no shell, fully sandbox-safe. CLAUDE.md already named `self-improve` as a consumer of cron-state; the skill just wasn't doing it.
  - PR body cites the recurring-blocker history (PRs #77, #81, May-26 onward) inline so a future cleanup doesn't promote `./scripts/skill-runs` back to primary without checking sandbox behaviour first.

**Impact:** PR #83 finishes a 6-PR chain that's been running for two weeks; the runner-hook-vs-shell-substitution problem has no remaining sites on aeon-agent. PR #84 closes a self-defeating loop where the diagnostics skill was burning a turn on a command it couldn't execute. Both are tiny diffs (3 lines + 24 lines) and both pulled from the bot's own self-improve runs over the past four days.

### Theme 2: 23rd consecutive same-day-after backport — skill-of-the-day
**Summary:** PR #85 is the 23rd consecutive same-day-after backport from upstream aeon. It's also the first backport in the chain where `./notify` wiring needed no translation — upstream PR #341 (Nurstar, Jun-04) used the positional `$(cat ...)` argv style that aeon-agent's notify contract already expects.

**Commits:**
- `18976c0` — feat: backport skill-of-the-day from upstream aeon PR #341 (23rd consecutive) (#85)
  - New file `skills/skill-of-the-day/SKILL.md` (+189 lines) — verbatim copy from upstream. Daily meta-content skill that produces two notifications per `workflow_dispatch` run: (1) a paste-ready "Aeon skill of the day" long-form tweet draft to `.outputs/skill-of-the-day.md` (operator copies to X); (2) the picked skill's live outcome via the dispatched run's own `./notify` (operator screenshots into the "Result ⤵️" tweet body). Queue precedence: `${var}` override → `memory/topics/skill-of-the-day.md` → `ls skills/` catalog fallback. 30-day Covered window suppresses repeats. Blocklist suppresses meta/internal skills.
  - `aeon.yml` (+1), `skills.json` (+11/−1), `generate-skills-json` (+1) — registered disabled between `skill-graph` and `smithery-manifest`. Skill count 100 → 101, category `social`.
  - Three adaptations vs upstream are documented inline. (1) `./notify "$(cat .outputs/skill-of-the-day.md)"` matches aeon-agent's positional-`$1` contract verbatim — first backport with no notify-style translation (vs spend-monitor PR #74 / follow-up-patrol PR #76 / narrative-convergence PR #80 / mcp-pulse PR #82 all rewriting `-f file` → `$(cat ...)` positional). (2) Queue seed file is optional — catalog-fallback reads `skills/` directly and skips blocklist + 30-day Covered entries, so a fresh install picks up natively without manual priming. (3) `gh workflow run aeon.yml -f skill="${PICK}"` ships verbatim — same `workflow_dispatch` `skill` input exists on aeon-agent's `aeon.yml`.

**Impact:** Closes the upstream PR #272 backport queue except `fleet-scorecard`, which is blocked on missing dependencies (`memory/instances.json` + `scripts/prefetch-fleet-scorecard.sh`) the fork doesn't currently maintain. The chain that anchored on May-3 with operator-scorecard has now hit 23 consecutive day-after deliveries.

### Theme 3: repo-pulse gets a GitHub profile enrichment layer
**Summary:** PR #88 (merged today, 12:52 UTC) extends `repo-pulse` to enrich each new stargazer and forker with `gh api users/$LOGIN` profile data — name, company, bio, location, followers, repo count, account age. The bare-handle notification (`github.com/xyz123`) was telling the operator nothing useful; now `@ Vercel · 2.3k followers` tells them when a launch is landing.

**Commits:**
- `df4a0c8` — repo-pulse: enrich new stargazers/forkers with profile info (#88)
  - `skills/repo-pulse/SKILL.md` (+30/−7) — adds step 5c "Enrich new stargazers and forkers." For each new handle in the first-run 24h set or the subsequent-run delta set, calls `gh api users/$LOGIN --jq '{login, name, company, bio, location, blog, twitter_username, followers, public_repos, hireable, created_at}'`. One-line summary joins present fields with ` · ` in the order `${name} · @ ${company} · ${location} · ${followers}f · ${public_repos} repos · "${bio}"`, skipping segments whose source field is empty.
  - Three guards: (1) **Cap at 25 enrichments per run** (stargazers + forkers combined) — beyond that, the bot enriches the first 25 in `starred_at` / `created_at` order and appends `…and N more` un-enriched, bounding both API calls and message length. (2) **Empty-field omission** — most accounts have null company/bio/location; the formatter drops the segment rather than printing a blank. (3) **Low-signal flag** — if `followers <= 2` AND `public_repos == 0` AND `created_at` is within the last 30 days, the line is suffixed `⚠ new/low-signal`. Soft fake-star tell that complements `star-milestone`'s burst check; annotates, doesn't suppress. (4) `gh api users/$LOGIN` is read-only and the `gh` CLI handles auth internally — no curl, no env-var headers — so it works in the Actions sandbox.
  - Format changes too: notification now lists stargazers one-per-line (`- github.com/...`) instead of the prior pipe-separated single line.

**Impact:** Today's first 12:59 UTC `repo-pulse` run was the last one in the old format; tomorrow's run will be the first under the new schema. With aeon now visibly approaching the 500⭐ milestone (492 this morning, +4 new stars in 24h), the operator suddenly cares quite a lot about *who* the new starrers are — Mneme's `mnemedb` and SIGNA's `vritra12` both being external contributors who shipped PRs today is exactly the kind of signal the bare-handle format used to bury.

### Theme 4: project-lens stigmergy article published
**Summary:** PR #86 is yesterday's project-lens article landing on main today. The article frames Aeon's 150-skill, no-orchestrator architecture against the 2026 multi-agent orchestration discourse. Title: "An Ant Doesn't Get a Meeting Invite."

**Commits:**
- `47361f3` — article(project-lens): stigmergy lens — an ant doesn't get a meeting invite (#86)
  - `articles/project-lens-2026-06-07.md` (+34 lines) — new article on the philosophy / stigmergy angle. Concrete project references: the Monday intelligence stack (ecosystem-pulse + ecosystem-entrants + ecosystem-links — note this article was drafted before PR #351 merged today, but anticipates it), `narrative-convergence`, `upstream-gap`, and the 23-backport chain. Frames cron-driven skill independence as the indirect-coordination analogue to ant pheromone trails: no skill schedules another, but state files are the trail.
  - `dashboard/outputs/project-lens-2026-06-07T16-12-59Z.json` (+60 lines) — same content in dashboard render spec.
  - `.outputs/project-lens.md` (+3/−3) — current run pointer updated.
  - `memory/logs/2026-06-07.md` (+8 lines) — log entry appended.
  - `memory/token-usage.csv` (+1) — cost tracking.
  - PR's fourth commit (`fix(project-lens): point article links at /blob/main/`) — bug fix; PR-branch URLs survive branch deletion if they point at `/blob/main/` rather than `/blob/feat-...`.

**Impact:** Tenth project-lens article in the chain that's been publishing on alternate days. Cited the still-unmerged-then-PR #351 ecosystem-links work — by the time the article landed on main today, that skill was also on main, neatly closing the article's own forward reference.

### Theme 5: Daily cron stack — clean across the board
**Summary:** Every scheduled daily skill ran and produced its expected output. Approximately 30 paired `auto-commit YYYY-MM-DD` + `cron: <skill> success` + `scheduler: update cron state` commits in the window. No failures, no stalled cron entries.

**Commits (highlights):**
- `d08ef86` / `c401986` — `token-report` / `repo-pulse` auto-commits (7:14 UTC / 12:59 UTC). $aeon at $0.0000309 (+8.03% 24h, $552K main pool volume, +214% vs yesterday — 7-day compression broken). Repo-pulse: 4 new stars (asorourx, ynk7, MarcoWorms, Unszeil), 2 new forks (mnemedb/aeon, NASTYZUNI/aeon). `mnemedb` here is the same author whose Mneme skill pack PR landed on aeon main 90 minutes later.
- `713a97f` — `star-momentum-alert` auto-commit (10:21 UTC). Verdict OUT_OF_WINDOW — aeon at 490⭐, projected 500⭐ on 2026-06-11 (Thursday).
- `f0dd286` — `weekly-shiplog` auto-commit (10:23 UTC). 57 PRs merged across the three watched repos in the 2026-06-01 → 2026-06-08 window, 15 distinct authors, 0 releases. Headline themes: HoundFlow loop closure, capabilities taxonomy going load-bearing, ecosystem visual catalog, minitor's 8-rung per-column UX ladder, the 23-day backport chain. 1170 words written.
- `535425c` — `feature` cron auto-commit (12:31 UTC). The bot's daily 3-repo feature builder fired. **The three PRs it opened are aeon PR #358 (star-milestone auto-dispatch, merged), aeon-agent PR #87 (ecosystem-links backport, still open at write time), and minitor PR #65 (per-deck drag-to-reorder, still open).** All three are detailed in today's `memory/logs/2026-06-08.md` Feature Built sections.
- `8f8c933` — `repo-actions` auto-commit (15:03 UTC). 5 fresh ideas: (1) Phase 2 capabilities declarations sweep (aeon), (2) ecosystem-entrants backport (aeon-agent), (3) Deck keyboard navigation shortcuts (minitor), (4) show-hn-draft prompt refresh (aeon), (5) install-from-atrium script backport (aeon-agent). The latter two seed tomorrow's potential work.

**Impact:** Twelve scheduled skills ran clean. Two repo-pulse runs in the day (one at 10:20 UTC for the morning, one at 12:59 UTC after the morning's new stargazers showed up); the second one was a QUIET pass on aeon-agent. No skill failures.

---

## aaronjmars/minitor

Three substantive PRs merged. The continuation of the per-column UX axis (PR #63 width control, the 8th rung), the parallel deck-axis work (PR #62 per-deck color labels), and a fix to the DeFiLlama gainers plugin (PR #64).

### Theme 1: Per-column width control — 8th rung on the UX axis
**Summary:** PR #63 added a three-step width override per column. The motivation is clear once you've used the deck: a crypto price column reads densely narrow (180px content fits at 240); a news headline column reads badly at the historical 360px default. Three discrete sizes (narrow 240px / normal 360px / wide 480px) cover the spread without introducing a drag-resize handle that would compound poorly with the collapse and pin affordances added in PRs #55 and #59.

**Commits:**
- `851308c` — feat: per-column width control (narrow/normal/wide) — 8th rung on per-column UX axis (#63)
  - `lib/store/use-deck-store.ts` (+60/−1) — new `ColumnWidth` type `"narrow" | "wide"` with absence-from-map = normal; new `widthByColumn: Record<string, ColumnWidth>` state field initialised `{}`; new `setColumnWidth(columnId, width|null)` action with `width === existing` no-op fast-path that returns the prior state object so React skips re-render on the hot menu path. `deleteDeck` and `removeColumn` actions extended to scrub stale entries alongside `collapsedColumnIds` and `searchByColumn`.
  - `components/column/column-card.tsx` (+47/−1) — `Check`, `Maximize2`, `Minimize2` lucide imports; store reads `columnWidth` + `setColumnWidth`; resolved `widthClass` const with **default branch character-identical to the prior single class** so every existing column renders pixel-identical until the operator opts in; `transition-shadow` → `transition-[box-shadow,width]` so width animates smoothly instead of snapping; three menu items between *Download items (JSON)* and *Delete*, each showing a brand-coloured Check icon next to the active width.
  - Width is **view-state only**, not DB-backed — same lifetime as `collapsedColumnIds` and `searchByColumn`. Reload returns every column to 360px. Deck export/import/share-links carry no width data.
  - Mobile (`< sm`) clamps to `min(360px, calc(100vw - 1rem))` regardless of the width override — a 480px wide column would overflow a phone viewport. Width is a desktop-only ergonomic.

**Impact:** Closes the 8th rung on a UX axis that started 11 days ago: tab groups (PR #53) → collapse (PR #55) → JSON export (PR #56) → quick-search (PR #58) → pin (PR #59) → duplicate (PR #60) → column color (PR #61) → **width (PR #63)**. NO DB schema, NO migration, NO server round-trip, NO plugin contract touched, NO `DECK_EXPORT_VERSION` bump — pure client-side enhancement.

### Theme 2: Per-deck color labels — the deck-axis analog of column color
**Summary:** PR #62 ports the per-column color-labels affordance from PR #61 up one level to the deck. Each deck can now carry a 6-hex color label that renders as the identity dot in the sidebar deck header (replacing the brand active/inactive dot) and as a 10px dot next to the deck name in the deck-view top bar. Reuses the column color palette and `normalizeColumnColor` server function **verbatim** — forking would invite the two surfaces to drift on case-folding or shorthand acceptance.

**Commits:**
- `d9faec3` — feat: per-deck color labels — sidebar dot + top-bar dot + round-trip through export/import/share-links (#62)
  - `drizzle/0009_deck_color.sql` (new, +1) + `drizzle/meta/0009_snapshot.json` (new, +371) + `drizzle/meta/_journal.json` (+7) — additive nullable `text` column, no churn on existing rows.
  - `lib/db/schema.ts` (+1) — `color: text("color")` on decks.
  - `lib/columns/types.ts` (+14) — `Deck.color?: string` with full doc.
  - `app/actions.ts` (+55/−2) — `updateDeckColor` server action; `loadSnapshot` maps the field through to the wire shape; `importedDeckSchema.deckColor` optional max 64 (additive to v1 — old exports omit and import as null, no version bump); `exportDeck` emits when set; `importDeck` re-validates through `normalizeColumnColor` and hoists `deckColorPersisted` out of the transaction so `ImportedDeckResult.deckColor` propagates to the optimistic client store.
  - `lib/store/use-deck-store.ts` (+20) — `updateDeckColor` action mirroring `renameDeck`'s optimistic-then-fire pattern.
  - `lib/deck-templates.ts` (+7) — `DeckTemplatePayload.deckColor?` so starter templates can ship pre-coloured.
  - `components/dialogs/deck-color-dialog.tsx` (new, +186) — same 8 swatches (orange/green/blue/purple/pink/yellow/cyan/slate) + Clear button + freeform hex input + live invalid-hex error + disabled-Save guard. Save lights up only on a meaningful change.
  - `components/sidebar-01/nav-decks.tsx` (+38/−1) — Palette icon import, "Set color"/"Change color" menu item between Rename and Version history, tagged-deck dot rendering in operator's color, inactive tagged decks dip opacity to 65% so active still reads as primary.
  - `components/deck/deck-view.tsx` (+8) — 10px circular color dot next to deck name in top bar when set.

**Impact:** Decks are DB-backed identities (unlike width which is view-state), so color round-trips through export/import/share-links/snapshots. Schema is additive — old exports omit `deckColor` and import as `color = null`. No `DECK_EXPORT_VERSION` bump. **Operator color overrides active-deck brand color** — when a deck is tagged, the dot stays in its color even when active; swapping to brand would erase intent.

### Theme 3: DeFiLlama gainers gets a TVL floor (default $1M)
**Summary:** PR #64 fixes a noise problem in the gainers leaderboard: without a TVL floor, a $500 microcap doubling overnight reads as +100% and outranks a $1B protocol that grew 5%. The fix mirrors the threshold DeFiLlama applies on its own gainers page.

**Commits:**
- `6ce7b05` — fix(defillama): add minimum-TVL floor to gainers mode (#64)
  - `lib/columns/plugins/defillama/plugin.ts` (+6) — new schema field `minTvlUsd: z.number().nonnegative().default(1_000_000)`. Default $1M floor; setting to 0 disables the filter (every protocol included).
  - `lib/columns/plugins/defillama/client.tsx` (+29) — config UI field for the per-column floor, gainers mode only.
  - `lib/columns/plugins/defillama/server.ts` (+1) — passes `minTvlUsd` through to the fetcher.
  - `lib/integrations/defillama.ts` (+15/−4) — `fetchDefillamaPage` new `minTvlUsd = 0` param. Gainers mode applies the floor *before* sorting: `mapped.filter((a) => (a.meta?.tvlUsd ?? 0) >= minTvlUsd)`. Top mode keeps the full list — it's a TVL leaderboard and small entries naturally sort to later pages.

**Impact:** Per-column knob, exposed only on Gainers mode. Default $1M means existing Gainers columns silently start excluding sub-$1M noise on their next refresh; explicit `0` opt-out keeps the prior behaviour for any operator who liked it. Tiny diff (+51/−4) for a noise reduction the operator will notice on every Gainers column.

---

## Developer Notes
- **New dependencies:** None. All three repos shipped pure code/skill/SQL changes today.
- **Breaking changes:** None. All schema work was additive (minitor `0009_deck_color.sql` is a nullable column; aeon `milestone-dispatch.json` is a new file; aeon-agent `skills.json` was a category extension).
- **Architecture shifts:** Star-milestone (aeon PR #358) is the first cross-skill **routing** wire on the framework — a read-side skill that fires *other* skills via `gh workflow run`. Prior framework skills were either content-producing or read-only. The rule-map structure (`memory/topics/milestone-dispatch.json`) is general — future `(repo, threshold) → skill` pairings need no further code, just a JSON edit.
- **Tech debt:** Cleared. The shell-substitution anti-pattern chain (PRs #63/#67/#71/#77/#81/#83) is now closed across every known site. The self-improve→skill-runs sandbox-blocked loop is closed too.
- **External activity:** Three new external contributors merged on aeon today (mnemedb, Zorrot Chen, vritra12). vritra12 had already shipped the original SIGNA pack; the other two are first-time contributors.

## What's Next
- **aeon-agent PR #87** (`ecosystem-links` backport) and **minitor PR #65** (per-deck drag-to-reorder) opened by today's `feature` cron run but not yet merged. PR #89 on aeon-agent ("improve: document runner-hook restriction + phantom-template-var in CLAUDE.md") also still open.
- **aeon at 492⭐ on a ~3.6⭐/day velocity** — 500 lands ~Jun-11 (Thursday). Today's PR #358 wired `star-milestone` to auto-fire `show-hn-draft` on that crossing; the launch draft skill (PR #151, enabled-pending-500 for 38 days) will fire on its own when 500 hits.
- **Repo-pulse profile enrichment** lands its first run tomorrow morning — first opportunity to see *who* the new stargazers are without manual handle-lookups.
- **PR #272 backport queue** on aeon-agent now closed except `fleet-scorecard`, blocked on missing `memory/instances.json` and `scripts/prefetch-fleet-scorecard.sh` dependencies.
- **Open Jun-08 repo-actions ideas not yet built**: Phase 2 capabilities declarations sweep (aeon), ecosystem-entrants backport (aeon-agent), Deck keyboard navigation shortcuts (minitor), show-hn-draft prompt refresh (aeon), install-from-atrium script backport (aeon-agent).
