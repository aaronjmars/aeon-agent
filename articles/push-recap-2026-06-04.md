# Push Recap — 2026-06-04

## Overview

Six substantive PRs across three repos by two distinct human authors picked up where yesterday's recap left off (~14:00 UTC on 6/3 after the Atrium/ecosystem wave). The day was unusually thematic for two reasons: aeon shipped its **first scheduled consumer of the HoundFlow security pack** (the six keyless onchain skills had been `workflow_dispatch`-only since 2026-05-28), and a **new external contributor (Nurstar)** shipped a meta-content skill that turns the framework's own observable features into daily X posts. Aeon-agent extended its same-day-after backport chain to **21 consecutive days** and fixed the 5th site in the `$(date)` runner-hook anti-pattern cleanup. Minitor reached the **6th rung on the per-column UX axis** with column duplicate.

**Stats:** ~13 files changed, +1,278/-9 lines across 6 substantive PRs (aeon=3 / aeon-agent=2 / minitor=1). Plus 24 bot auto-commits (cron state, per-skill auto-commits) excluded as non-substantive.

---

## aaronjmars/aeon

### Theme 1: Wallet-Risk Weekly — the HoundFlow pack finally has a standing runner

**Summary:** `.x402books/wallets.json` (PR #273, merged 2026-05-29) advertises this fork's treasury + deployer addresses; `token-report` already reads it for daily ETH balance (PR #306, merged 2026-05-31). Neither checks whether those wallets are exposed to **drain risk**. The HoundFlow pack shipped six keyless onchain investigation skills (`approval-audit`, `honeypot-check`, `lp-lock-check`, `linked-wallets`, `fund-flow`, `investigation-report`) on 2026-05-28, all `workflow_dispatch`-only — zero scheduled consumers in the week since. PR #340 closes that gap.

**Commits:**

- `07739cc` — `feat(wallet-risk-weekly): first scheduled consumer of the HoundFlow security pack (#340)`
  - **New file** `skills/wallet-risk-weekly/SKILL.md` (+299): Monday 11:15 UTC weekly risk audit of every Base wallet in `.x402books/wallets.json`. Per wallet: scans the last ~24k blocks for `Approval` events (chunked ~1800 newest-first to stay under public-RPC result cap), confirms each grant live via `allowance` `eth_call`, flags `>= 2^255` as UNLIMITED. Per **unique** token with a live approval (deduped across spenders): honeypot simulation via `eth_call` on `transfer(this, balance/2)` with `from = sampled holder` (no funds at risk — read-only simulation).
  - Buckets HIGH (UNLIMITED to non-known-safe spender OR token = LIKELY_HONEYPOT) / MEDIUM (UNLIMITED to Uniswap V2/V3/V4 routers / Permit2 / Aerodrome Router / finite >$10k-equiv) / LOW / CLEAN per wallet. INCONCLUSIVE **never escalates** — false-flagging the operator's own wallets would erode the alert signal everywhere else.
  - **Modified** `aeon.yml` (+1): registered disabled at `15 11 * * 1`, alphabetically inserted between `ecosystem-pulse` (11:00) and `capabilities-map` (11:30) — fits the Monday morning intelligence stack.
  - **Modified** `skills.json` (+13/-1): total 181→182, category `crypto`, declared `capabilities: read_only` (revised mid-PR from the initial `external_api` — the skill uses the keyless public Base RPC by default, so per `docs/CAPABILITIES.md` it's a read-only on-chain reader like its parent `approval-audit`/`honeypot-check` skills; `external_api` is reserved for calls that use a secret).
  - Gated notify (HIGH only / new MEDIUM transition / first-run baseline with ≥1 live approval). Article written every run even when silent — the weekly CLEAN record is proof the surface was checked. State in `memory/topics/wallet-risk-state.json` (atomic .tmp + mv write).

**Impact:** The HoundFlow pack stops being an "in case of fire, dispatch" surface and becomes a recurring self-audit. The skill consumes existing fork infrastructure (the wallets file shipped a week ago, the spender-allowlist constants are in the upstream skills) so there's nothing new to configure — toggling `enabled: true` in `aeon.yml` is the only operator action. The first scheduled run will baseline the live approval set against today's chain state, and subsequent Mondays only notify when something **changed** for the worse.

### Theme 2: Skill of the Day — first external human contributor since the May-29 maintainer-bottleneck framing

**Summary:** A meta-content skill that turns the framework's own observable feature surface into a daily X post cadence. Each run picks one skill from a rotation queue, drafts a paste-ready feature tweet in the `"Aeon skill of the day 🌟"` format (header line is brand-editable for forks with their own handle), sends it to the configured channels, then **dispatches the picked skill so the chosen channel also gets the live outcome** a few minutes later. The operator screenshots that live notify as the `Result ⤵️` body of the tweet.

**Commits:**

- `d2252c3` — `feat(skill-of-the-day): daily skill feature with paste-ready tweet + live outcome (#341)` — **by Nurstar** (new external contributor)
  - **New file** `skills/skill-of-the-day/SKILL.md` (+146): two-notification pattern — tweet draft + live outcome, both deliverable to Telegram or any configured channel. Strict cadence on the "How it works behind the scenes" bullets (`"✴️ It {verb}."`) so the series visually compounds across days. Voice defaults to terse + neutral; reads `soul/` if populated.
  - **New file** `memory/topics/skill-of-the-day.md` (+136): operator-owned config — a queue (~12 starter entries, three weeks of daily posts), a 30-day covered window (auto-pruned), and a blocklist of meta/internal skills that don't read as user-facing features.
  - **Modified** `aeon.yml` (+1): registered disabled with `workflow_dispatch` only. Recommended cron once enabled is `"0 8 * * *"` (morning slot, lets the dispatched skill complete before midday). `var=<skill-name>` overrides the queue for a one-shot feature.
- `8965bd2` — `chore(skill-of-the-day): drop duplicate skill-evals blocklist entry` — by aaronjmars
  - **Modified** `memory/topics/skill-of-the-day.md` (-1): `skill-evals` was listed twice in the `Never feature` blocklist. Removed the second occurrence under the meta-internal section. Tiny housekeeping landed ~4 minutes after #341 — caught on review.

**Impact:** Two-fold. **Operationally:** the framework's distribution problem has been one of *consistency*, not capability — there are 181 skills and most outsiders only ever hear about the ~5 the maintainer happens to tweet. A rotation queue with a 30-day suppression window guarantees coverage breadth without manual scheduling. **Politically:** Nurstar is a new contributor whose first PR shipped a content-stack skill, not a backport or a fix — the kind of feature build that historically came from the maintainer's own queue. The cadence (queue + covered + blocklist) is operator-editable, so a fork with a different focus can swap the queue without touching the SKILL.md.

---

## aaronjmars/aeon-agent

### Theme 3: Same-day-after backport chain hits day 21 + runner-hook anti-pattern cleanup hits site 5

**Summary:** Two PRs from the daily aeon-agent cron stack landed within 25 minutes of each other in the 15:16–15:41 UTC window. PR #80 is the 21st consecutive same-day-after backport of an upstream aeon merge (the chain has gone unbroken since May 3, including 4 days that were original feature builds not backports). PR #81 fixes the 5th site of the `$(date)` runner-hook anti-pattern in the existing skill stack — same constraint that drove PR #63 (weekly-shiplog), PR #67 (push-recap), PR #71 (heartbeat), and PR #77 (repo-pulse).

**Commits:**

- `1ab2257` — `feat(narrative-convergence): backport upstream aeon PR #272 (#80)`
  - **New file** `skills/narrative-convergence/SKILL.md` (+227): verbatim copy of upstream `skills/narrative-convergence/SKILL.md` from aeon PR #272 (merged 2026-05-29 — the same general-ops batch that brought `spend-monitor` over on Jun-01 and `follow-up-patrol` over on Jun-02).
  - **What it does:** daily 13:00 UTC cross-skill convergence detector. Lists `.outputs/*.md` + last 2 days of memory logs, maps each output to a signal category via the operator-editable `memory/topics/signal-categories.md` seed, builds an entity/theme → `[{skill, category}]` map, scores each entry on `(# distinct skills × # distinct categories × operator-interest match from soul/SOUL.md when present)`, suppresses anything an article already covered in the last 7 days, surfaces the top 5 with a one-line hook each. Notifies only when ≥2 strong signals survive suppression — the high-confidence "this is breaking in 3+ independent lanes" write opportunities the daily content stack (`repo-article`, `project-lens`, `thread-formatter`) was previously inferring by hand.
  - **Three adaptations vs upstream** (inline backport-note at top): (1) `./notify` call style — upstream uses `./notify -f .pending-notify-temp/<file>`, aeon-agent's `./notify` reads its argument as positional `$1`, so step 7 rewrites the call as `./notify "$(cat .pending-notify-temp/<file>)"` — same temp-file contents, same gating, same body, single argv; (2) signal-categories seed kept verbatim **plus additive** — native aeon-agent skills (`repo-pulse`, `repo-article`, `push-recap`, `project-lens`, `repo-actions`, `token-report`, `star-momentum-alert`, `star-milestone`, `thread-formatter`) added to their natural categories so first-run output is useful without operator edits; (3) `.outputs/` is sparse on aeon-agent (chain-runner staging only fills for chained skills, most aeon-agent skills run standalone) → memory-logs fallback is the **primary** path until chains are configured, called out explicitly in SKILL.md so the operator's mental model matches what the skill actually does.
  - **Modified** `aeon.yml` (+1): registered disabled at `0 13 * * *` (same slot upstream uses), alphabetically inserted between `monitor-kalshi` and `onboard` in the `# --- Upstream sync` section.
  - **Modified** `skills.json` (+11/-1): total 98→99, category `research` (first non-`crypto` / non-`dev` / non-`productivity` addition in 4 backports).

- `cf78fdb` — `improve: repo-article $(date) → literal ${today}-derived SINCE (#81)`
  - **Modified** `skills/repo-article/SKILL.md` (+11/-2): step 1 `since="$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ ...)"` → literal `SINCE=YYYY-MM-DDT00:00:00Z` computed from `${today}` minus 7 days. Crucially, the PR went through a **mid-review hardening pass**: the second commit (`harden(repo-article): isolate SINCE cutoff into its own step`) pulled the literal-date cutoff into a dedicated `compute FIRST — critical` step with the placeholder in its own bash block, **separate from the gh api call**, plus an explicit `"never leave YYYY-MM-DD literal"` guard in prose — closes the residual risk that the agent copies the placeholder verbatim and silently queries an empty window.
  - **Why mid-review hardening landed:** the initial fix matched PR #77's shape (single substitution). Adding the dedicated step + the explicit guard is structurally safer because the gh api call no longer **contains** the date placeholder — it references `$SINCE` defined two blocks above, so a sloppy edit can't accidentally leave a literal `YYYY-MM-DD` in the URL.
  - **Modified** `.outputs/self-improve.md`, `dashboard/outputs/self-improve-2026-06-04T13-42-21Z.json`, `memory/MEMORY.md`, `memory/logs/2026-06-04.md`, `memory/token-usage.csv`: the routine artifacts the self-improve skill writes alongside the SKILL.md fix.
  - **Two sites remain unfixed** (carry-list for future runs): `repo-actions:29` (14d window, even days 14:00 UTC — single substitution, same shape) and `star-momentum-alert:69` (3 expansion sites in one `for D in $(seq 13 -1 0); do DATE=$(date ...)` block — bigger fix requiring 14-row literal date table or loop unroll).

**Impact:** The backport chain is now long enough that its breakage would be a measurable signal — the bot fleet observers reading `memory/MEMORY.md` would notice a gap, and the upstream-gap skill (PR #72) is specifically designed to detect lag. The anti-pattern cleanup wave has converted 5 of 8 known sites; the remaining 3 are all on lower-frequency cadences (14-day even-day cron for `repo-actions`, alert-only daily for `star-momentum-alert`) so the marginal benefit of fixing them is smaller. The mid-review hardening on #81 is the **first time** in the cleanup wave that a follow-up commit landed structural improvement over a verbatim shape-match — worth keeping in mind for the remaining sites.

---

## aaronjmars/minitor

### Theme 4: Per-column UX axis — 6th rung lands as `Duplicate`

**Summary:** The deck-density UX work hit its 6th consecutive rung in 7 days. The sequence is now: tab groups (May-29 PR #53) → collapse (May-30 PR #55) → JSON export (May-31 PR #56) → quick-search (Jun-02 PR #58) → pin-to-front (Jun-03 PR #59) → **duplicate (today, PR #60)**. The common operator move it serves: maintain two CoinGecko columns for BTC and ETH, two GitHub repo columns for two different repos, two RSS columns with different include filters. Before this PR the operator had to add a brand-new column and re-enter every config field — after, one click + an optional tweak in the existing Configure dialog.

**Commits:**

- `43b848b` — `feat(columns): per-column duplicate — clone a column with all its settings (#60)`
  - **Modified** `app/actions.ts` (+83): new `duplicateColumn(sourceId, newId, newTitle): Promise<ImportedDeckColumn | null>` server action. Captures a deck snapshot before mutation (same reversibility contract as `createColumn` / `deleteColumn` / `reorderColumnsInDeck` — version history catches an accidental duplicate). Shifts every column with `position > src.position` right by 1 so the duplicate lands at `src.position + 1` without renumbering the whole deck. **Wrapped in `db.transaction()` mid-PR** (second commit `fix(columns): wrap duplicate shift+insert in a transaction; copy config`) because the position-shift UPDATE and the INSERT were two separate awaited statements — a crash between them would leave later columns shifted right with no duplicate filling the gap. Mirrors `importDeck`'s transaction wrap. Inherits `notifyWebhookUrl` (same-install copy, secret stays inside the trust boundary it was configured within); sets `pinned: false` (pinning is the operator's explicit "primary column" decision, mirrors PR #59's "DnD across pin/unpin no-op" rule).
  - **Modified** `lib/store/use-deck-store.ts` (+71): new `duplicateColumn` zustand action. Locates the owning deck by scanning `decks[*].columnIds` (columns are a flat map across decks — no parent-deck field on the column itself). Optimistic state inserts the new column right after the source in `decks[deckId].columnIds[]` so visual order matches where it lands server-side. Returns `{ id, ready } | null` so callers can decide whether to surface the new column on creation (consistent with `addColumn`'s shape). **Shallow-copies `config`** in the optimistic store insert so the clone never shares the source's config object reference (caught in the same mid-PR fix commit as the transaction wrap).
  - **Modified** `components/column/column-card.tsx` (+14): `Duplicate` dropdown entry between `Rename` and `Download (item)` — natural ordering: rename in place, then a structural action that creates a new column with the existing config, then the read-only export. Lucide-react `Copy` icon imported alongside the existing pin / download / settings glyphs. Toast on success names the new column so the operator can spot which row appeared mid-deck.
  - Title format `"<source> (copy)"` not `"Copy of X"` — same as Finder + most cloud doc apps, postfix reads better mid-deck because the column header shows the original title first and the disambiguator second. `.trim().slice(0, 256)` cap matches `renameColumn`. **No DB schema change, no migration, no `DECK_EXPORT_VERSION` bump** — a duplicated column is just another column row, round-trips through export/import/share-link/snapshot identically.
  - Could NOT run Next 16 build/typecheck (offline sandbox — established constraint since PRs #49/#50/#51/#52/#53/#55/#56/#58/#59). Manual review only.

**Impact:** The per-column UX axis is starting to look intentional rather than incremental — six PRs in seven days, each one structural enough that it could have shipped alone, but each one clearly **completing the previous** rather than introducing a new axis. Pin-to-front (PR #59) was the only one that required a DB migration (`0007_column_pinned.sql`); the rest are either view-state (`collapse`, `quick-search`) or pure server actions reusing the existing columns table. The maintainer's velocity ceiling on minitor isn't column-creation rate — it's the offline sandbox blocking Next 16 build/typecheck, which has been the documented constraint for 9 consecutive minitor PRs.

---

## Developer Notes

- **New dependencies:** none. All four feature PRs reuse existing infrastructure (Base RPC + `eth_call`, gh CLI, lucide-react, db.transaction). minitor's `Copy` icon and aeon's `wallet-risk-weekly` skill rely entirely on already-imported libraries.
- **Breaking changes:** none. All four feature additions land disabled in `aeon.yml`; minitor PR #60 doesn't bump `DECK_EXPORT_VERSION`.
- **Architecture shifts:**
  - aeon-agent's narrative-convergence backport admits its primary code path will differ from upstream (memory-logs fallback over `.outputs/` until chains are configured) — first backport in the chain to **document a structural divergence in the SKILL.md itself** rather than carrying the upstream shape and hoping the fallback fires.
  - minitor PR #60's mid-PR transaction wrap on `duplicateColumn` is a small but pointed correctness fix — the kind of issue that wouldn't show up in test until a real crash happened mid-mutation. Worth grepping the rest of `app/actions.ts` for similar two-write patterns that aren't wrapped (`reorderColumnsInDeck`, in particular, also does shift-then-insert-style work).
- **Tech debt:**
  - Two `$(date)` runner-hook anti-pattern sites remain unfixed in aeon-agent (`repo-actions`, `star-momentum-alert`); the latter is the bigger lift.
  - The HoundFlow pack still has 5 other keyless skills (`lp-lock-check`, `linked-wallets`, `fund-flow`, `investigation-report`, plus the meta `approval-audit`) with no standing runner — `wallet-risk-weekly` only consumes 2 of the 6.
  - aeon-agent PR #80's signal-categories seed is verbatim-from-upstream; the operator should trim it to the actually-enabled aeon-agent skill set on first run. Until they do, the skill still runs — fewer outputs map to named lanes.

## What's Next

- **aeon-agent backport queue:** PR #272 still has `mcp-pulse` and `fleet-scorecard` unbackported. `fleet-scorecard` depends on `scripts/prefetch-fleet-scorecard.sh` + `memory/instances.json` which aeon-agent doesn't currently maintain — that's a 2-file prerequisite before the backport can land. `mcp-pulse` is larger and depends on web-fetched npm/GitHub signals — natural target for an upcoming round.
- **aeon's HoundFlow pack consumption:** the operator path of least resistance is one more `*-risk-weekly` skill targeting the 4 unconsumed pack skills as a combined audit (`lp-lock-check` + `linked-wallets` per token, fed back into the `investigation-report` template). The Monday morning stack has slot capacity.
- **Skill-of-the-day cron not yet enabled:** PR #341 landed with `workflow_dispatch` only. Once enabled at `"0 8 * * *"`, the live-outcome screenshot pattern means the **first dispatched skill becomes the test case** for end-to-end visibility — whatever skill is at the head of the queue should be one that produces an interpretable single notification.
- **minitor per-column UX axis:** with duplicate done, the natural next rungs are either column-level metadata (color labels per repo-actions Jun-04 idea #5, drag-handle ergonomics) or moving up the axis to multi-column operations (bulk rename, batch tab-group reassign, deck templates from current state).
- **Open thread:** aeon PR #341 introduced Nurstar as a new contributor with a content-stack skill — first feature build by an external human (non-bot) since the May-29 maintainer-bottleneck framing. Worth watching whether the queue gets edited by Nurstar or by the maintainer as the cadence settles.

---

**Sources:**
- aeon PR #340: https://github.com/aaronjmars/aeon/pull/340
- aeon PR #341: https://github.com/aaronjmars/aeon/pull/341
- aeon-agent PR #80: https://github.com/aaronjmars/aeon-agent/pull/80
- aeon-agent PR #81: https://github.com/aaronjmars/aeon-agent/pull/81
- minitor PR #60: https://github.com/aaronjmars/minitor/pull/60
- HoundFlow pack origin (aeon PR #261, merged 2026-05-28)
- Wallet manifest origin (aeon PR #273, merged 2026-05-29)
- Backport chain anchor (aeon-agent PR #16, merged 2026-05-03 — operator-scorecard backport)
