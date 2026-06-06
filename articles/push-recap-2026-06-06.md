# Push Recap — 2026-06-06

## Overview

11 substantive PRs landed across the three watched repos in the last 24 hours, all merged by aaronjmars (with Claude Opus 4.8 as co-author on the bot-assisted PRs). The day's thrust on **aeon** was a full-stack identity refresh: a load-bearing taxonomy refactor (5→8 categories), a 37-skill catalog bump (156→193) absorbing the Hound onchain pack + 8 ported aeon-aaron skills, fresh CORE.md mechanics documentation, and a new Friday-cadence marketplace watcher. **aeon-agent** continued its 22nd consecutive same-day-after backport (mcp-pulse). **minitor** added the 7th rung on the per-column UX axis (color labels). Three of the four bot-assisted PRs shipped mid-PR structural fixes inside the merge.

**Stats:** ~43 files changed, **+3,878 / −860** lines across **11 commits** in 3 repos.

---

## aaronjmars/aeon

9 substantive PRs (#342–#350) — by raw line count this is the biggest aeon day in the recap window. Six of them stack into one coherent move (a top-to-bottom catalog + taxonomy refresh) and the other three are independent surfaces.

### Theme 1: 5→8 Category Taxonomy + Full Catalog Refresh (the big move)

**Summary:** Aeon's skill catalog had drifted hard. The README claimed 156 skills, skills.json had 193, and 65 of those 193 were sitting in an untyped "other" bucket that no dashboard or mcp-server filter could surface. The category labels themselves no longer matched what the skills actually do: 15 load-bearing self-evolution/fleet/autonomous-action skills were fused into "dev" or "productivity," the Hound onchain forensics pack was scattered across "crypto," and the README-vs-skills.json count gap was widening every week. Today closed all three loops in one stacked push: rebuild the taxonomy, recategorize every skill, update the README, write the deep doc, refresh the banner asset.

**Commits:**

- `1037341` — **README: bump skill catalog 156 → 193, showcase aeon-aaron ports (#344)** (+795 / −660 across 3 files)
  - Changed `README.md`: full category table refreshed with all 37 skills that had shipped since the last update — Hound onchain pack, fleet analytics, PR-triage suite, the 8 aeon-aaron ports from #343; per-category counts corrected (28/44/44/18/19/40 = 193, verified against skills.json). All six stale "156 skills" references bumped to 193 (hero, skills section, repo-structure, FAQ ×2, skill-graph).
  - Changed `generate-skills-json`: category-map entries added for the 8 new skills that had fallen into `other`.
  - Changed `skills.json`: regenerated to 193 entries.

- `4acb4c3` — **generate-skills-json: categorize all 65 'other' skills, align 5 strays (#345)** (+89 / −74 across 2 files)
  - Changed `generate-skills-json`: maps every previously-`other` skill to its README-table category (research +5, dev +13, crypto +18, social +3, productivity +26). Five existing entries that disagreed with the README are realigned: `mcp-pulse` dev→research; `fleet-scorecard`, `fork-first-run-alert`, `fork-skill-gap`, `skill-security-scan` dev→productivity.
  - Changed `skills.json`: regenerated to 28 research / 44 dev / 44 crypto / 18 social / 59 productivity-meta = 193, **zero `other`**, **zero README↔skills.json mismatches**.

- `d358b57` — **Taxonomy: add core, onchain-security, meta categories (5 → 8) (#346)** (+121 / −97 across 4 files)
  - Changed `generate-skills-json`: categories map expanded from 5 keys to 8 (`core`, `onchain-security`, `meta` added); `get_category` restructured so the **core block is matched first**. The 15 load-bearing core skills are now their own row instead of being smeared across dev/productivity:
    - **self-evolution & self-healing (6):** autoresearch, create-skill, skill-health, skill-repair, skill-evals, self-improve
    - **fleet / self-replication (5):** spawn-instance, fleet-control, fleet-scorecard, contributor-reward, distribute-tokens
    - **autonomous real-world action (4):** external-feature, feature, deploy-prototype, vuln-scanner
  - Changed `README.md`: Core row leads the table with the 3-group load-bearing-core blurb; Dev 44→36, Crypto 44→28, new Onchain Security row, Meta 40→35; FAQ updated to reflect 8 categories.
  - Changed `mcp-server/src/index.ts`: category labels + per-category var-hint defaults for the 3 new keys, so MCP tool descriptions now read e.g. `[Aeon - Core] ...`.
  - Changed `skills.json`: regenerated with the new keys. Verified distribution: core 15 / research 28 / dev 36 / crypto 28 / onchain-security 14 / social 18 / productivity 19 / meta 35 = 193.

- `e45c867` — **docs: add CORE.md — the load-bearing 15, per-skill mechanics (#347)** (+129 / −0 across 2 files)
  - New file `docs/CORE.md`: deep mechanics for the core category — the self-evolution/self-healing loop (detect → file → repair → verify → resolve), fleet/self-replication (secret-free spawning, billing isolation, two-phase idempotent on-chain rewards), and autonomous real-world action (unprompted feature PRs, Vercel prototypes, responsible vuln disclosure). Covers exit taxonomies, loop guards, and the money-safety design that the README blurb only gestures at.
  - Changed `README.md`: links the new doc from the Core section.

- `5386ace` — **Port 8 skills from aeon-aaron + fix duplicate-H2 memory drift at the source (#343)** (+1,455 / −2 across 14 files)
  - The largest single commit of the day. Two architectural moves bundled together:
    - **Memory architecture fix (no new skill):** `skills/memory-structural-dedupe/SKILL.md` extended (+22 / −1) to detect + merge duplicate H2 headings (the same section heading appearing 2+ times) — the exact failure mode the skill's description previously excluded. Canonical-span selection, unique-info folding, single-occurrence rewrite. `skills/reflect/SKILL.md` and `skills/memory-flush/SKILL.md` get one-line prevention rules each (+1 each): never prepend a `## heading` that already exists in MEMORY.md; update in place.
    - **8 skills ported from aeon-aaron, de-personalized:**
      - `fear-divergence-scout` (+179): conditional daily scan, fires only when Fear & Greed < 25; consumes `market-context.md`.
      - `beat-tracker` (+204) + `article-queue` (+180): persistent event-level beat counts per storyline + ranked article queue feeding the `article` skill — closes the gap between `topic-momentum`/`narrative-tracker` and `article`.
      - `picks-tracker` (+185): 30-day W/H/L retrospective on token + Polymarket picks vs current prices.
      - `content-performance` (+189): weekly X engagement feedback loop (topics, formats, breakouts); var-override → `soul/SOUL.md` fallback; XAI optional with WebSearch fallback; new `scripts/prefetch-xai.sh` case (+16).
      - `api-health-probe` (+159, from xai-probe): provider-generic pre-batch credit/auth probe via new `scripts/prefetch-api-probe.sh` (+69); dynamic issue filing.
      - `mention-radar` (+99, from project-pulse): external mention tracking for the operator's projects.
      - `thread-writer` (+136): 5–10 tweet thread composer grounded in `soul/` + memory.
  - Changed `aeon.yml` (+15 / −1): all 8 ported skills registered with `enabled: false`.
  - **`skills.json` deliberately left to `generate-skills-json`** — it's a generated artifact, regenerated by #344 the same hour.

- `deb654a` — **README: drop the "New (June 2026)" block, tighten skill-table commas (#348)** (+9 / −19, 1 file)
  - Changed `README.md`: removed the dated showcase section — the ported skills already live in the category table and skills.json after #344. Skill table rows tightened (`a`, `b` → `a`,`b` across 8 rows, narrower table). FAQ self-healing answer updated: `skill-repair`/`self-improve`/`skill-health` are core since #346, not Meta/Agent; link to `docs/CORE.md` added.

- `973244d` — **assets: refresh skills banner for the 193-skill / 8-category catalog (#350)** (+1 / −1, 3 files; 2 binary)
  - Renamed `assets/skills-aeon.jpg` → `assets/skills-aeon-193.jpg` so GitHub's camo CDN cache busts on the new image.
  - Changed `README.md`: image reference bumped to the new filename.

**Impact:** This is the first time in the project's history that aeon's external story (README), internal config (skills.json), and runtime taxonomy (mcp-server tool descriptions + generate-skills-json mapping) all agree on the same numbers and the same buckets. **Zero skills sit in `other` now.** The 15 load-bearing core skills — the ones that make Aeon autonomous rather than just scheduled — get their own row at the top of the table and their own deep doc. The README count is no longer a lie. Catalog drift was a recurring source of contributor confusion; that's now structurally closed by `generate-skills-json` + the locked taxonomy.

---

### Theme 2: New Skill — `atrium-catalog-watcher` (the third weekly marketplace digest)

**Summary:** The third skill installation path (`install-from-atrium`, PR #335, merged Jun-03) had zero standing watcher — operators had no signal when new skills published to the Atrium onchain marketplace. Today's #342 closes that gap and completes the three-weekly digest composition: marketplace arrivals (Atrium) + curated registry health (sparkleware-catalog) + installed-skill drift (skill-update-check), with no overlap.

**Commits:**

- `9cb91a7` — **feat: atrium-catalog-watcher skill — weekly Atrium marketplace diff (#342)** (+320 / −1 across 3 files)
  - New file `skills/atrium-catalog-watcher/SKILL.md` (+306): Friday 12:00 UTC weekly diff of `https://atriumhermes.tech/.well-known/skills/index.json` against the prior snapshot. Reports added / removed / renamed skills with one-click `./install-from-atrium <name>` commands on every added row. Keyed on `skill_id` (canonical onchain id), so a rename or description tweak is `updated` not `add+remove`. `ATRIUM_HOST` env override honored — a host change re-baselines. 56-day prune window. `curl` + WebFetch fallback per CLAUDE.md sandbox pattern 1. 7-state exit taxonomy (OK / QUIET / FETCH_FAIL / BAD_SHAPE / DRY_RUN / STATE_CORRUPT / BAD_VAR).
  - Changed `aeon.yml` (+1): registered disabled at `0 12 * * 5` between `ai-framework-watch` and `competitor-launch-radar`.
  - Changed `skills.json` (+13 / −1): catalog total **182 → 183**, category `dev`.

**Impact:** Aeon now has a passive sentinel watching the marketplace it can install from. New onchain skill publications surface as a notification with a copy-paste install command — the operator's actual next step.

---

### Theme 3: ECOSYSTEM Curation

**Summary:** Curatorial cleanup — 9 new projects added to the ecosystem index.

**Commits:**

- `16a35a9` — **ECOSYSTEM: add 9 projects (#349)** (+9 / 0, 1 file)
  - Changed `ECOSYSTEM.md`: added Aeon City, Charon, CTRL, DarkSol, Hunch, Prism, Sentysis, Venice Deity, XergAI — alphabetized; logos verified live.

**Impact:** Hand-curated ecosystem index grew by 9; the next `ecosystem-entrants` skill run (Monday 11:45 UTC) will diff this snapshot and surface every one of them as a discrete arrival signal.

---

## aaronjmars/aeon-agent

1 substantive PR. The day was otherwise dominated by **22 `chore(cron):`/`chore(scheduler):` auto-commits** from the `aeonframework` bot (token-report, repo-pulse, repo-article, project-lens, thread-formatter, star-momentum-alert, push-recap, star-milestone, heartbeat, feature, self-improve) — those are the scheduled workflow heartbeat, not feature work.

### Theme: 22nd Consecutive Same-Day-After Backport

**Summary:** The same-day-after backport chain that started May-3 reached run 22. Of the five general-ops skills in upstream aeon's PR #272 (spend-monitor / follow-up-patrol / narrative-convergence / mcp-pulse / fleet-scorecard), only `fleet-scorecard` now remains unbackported (and is structurally deferred — depends on `memory/instances.json` + `scripts/prefetch-fleet-scorecard.sh` that aeon-agent doesn't currently maintain). The merge itself shipped with a mid-PR structural fix — a pattern that's been repeating.

**Commits:**

- `20c0fe3` — **feat: mcp-pulse backport — 22nd consecutive same-day-after backport (#82)** (+335 / −1 across 3 files)
  - New file `skills/mcp-pulse/SKILL.md` (+323): verbatim backport of upstream aeon's mcp-pulse — Friday 10:00 UTC weekly Model Context Protocol ecosystem tracker. Queries `modelcontextprotocol` GitHub org for new MCP server repos in a 7-day window, fetches npm `@modelcontextprotocol/sdk` + PyPI `mcp` adoption stats, runs 3 targeted WebSearches for news, scores momentum on a 7-signal rubric, writes a thesis-check line (advancing / holding / stalling / reversing).
  - Three adaptations vs upstream baked into the backport: (1) `./notify` rewritten to positional-`$1` style (`./notify "$(cat .pending-notify-temp/<file>)"`) since aeon-agent's notify reads `MSG=$1`, not upstream's `-f file` flag; (2) the bash `$(date -u -d '7 days ago' ...)` cutoff replaced with a literal ISO timestamp computed from `${today}` minus 7 days — same fix the runner-hook-blocks-`$(...)`-expansion constraint has driven in PRs #63/#67/#71/#77/#81; (3) WebFetch fallback hardened across **every** external endpoint (npm / PyPI / GitHub API) rather than just one, per CLAUDE.md sandbox pattern 1.
  - **Mid-PR structural fix** caught in review: the backport had introduced `${today_minus_7}` as if it were a runner-injected template variable, but no such variable exists and the runner hook blocks `$VAR` expansion — so `CUTOFF` would never have resolved at runtime, and step 3's weekly "new MCP repos" search would have returned nothing every run (the WebSearch fallback was broken the same way). Fixed before merge by substituting the literal date inline, matching the pattern the five sibling skills already use.
  - Changed `aeon.yml` (+1): registered disabled at `0 10 * * 5` between `huggingface-trending` and `monitor-kalshi` (alphabetical, Upstream sync section).
  - Changed `skills.json` (+11 / −1): catalog total **99 → 100**, category research, alphabetical insert between `huggingface-trending` (idx 82) and `monitor-kalshi` (idx 83).

**Impact:** First time aeon-agent has had any signal about MCP tooling momentum (a category the operator is actively evaluating for the agent's own configuration). The PR #272 backport queue is now ≥80% done; only the instance-dependent skill remains.

---

## aaronjmars/minitor

1 substantive PR.

### Theme: 7th Rung on the Per-Column UX Axis (color labels)

**Summary:** The per-column UX axis has been incrementing roughly weekly: tab groups (#53, May-29) → collapse (#55, May-30) → JSON export (#56, May-31) → quick-search (#58, Jun-02) → pin (#59, Jun-03) → duplicate (#60, Jun-04) → **color labels today**. At 10–15 columns per deck, visual scan time becomes the bottleneck; operators were mentally grouping columns (DeFi / dev / news / social) but had no in-app marker for it.

**Commits:**

- `6e81b70` — **feat: per-column color labels (#61)** (+615 / −5 across 10 files)
  - New file `drizzle/0008_column_color.sql` (+1): additive nullable `text` column on `columns` — existing rows backfill to NULL = no color = default brand accent, zero churn.
  - New file `drizzle/meta/0008_snapshot.json` (+365) + `drizzle/meta/_journal.json` (+7): drizzle migration plumbing.
  - Changed `lib/db/schema.ts` (+1): `text("color")` field on `columns`.
  - Changed `lib/columns/types.ts` (+13): `Column.color?: string` with inline doc on the visual semantics + server-side hex-normalization rule.
  - Changed `lib/deck-templates.ts` (+6): `DeckTemplateColumn.color?: string` — starter decks can ship pre-colored lanes.
  - Changed `app/actions.ts` (+71): `COLOR_HEX_RE` + `normalizeColumnColor()` canonical server-side validator (lowercased, 6-hex only — 3-hex shorthand and named CSS colors deliberately rejected, so the stored form is canonical); `updateColumnColor()` server action; `importedColumnSchema` Zod field + `importDeck` re-validates through the normalizer (drop invalid like `notifyWebhookUrl`'s SSRF guard, never abort the import); `exportDeck` emits when set; `duplicateColumn` **inherits color** (unlike `pinned`, which doesn't — color is a labeling decision, pin is a routing decision); `loadSnapshot` maps the field through to the wire shape.
  - Changed `lib/store/use-deck-store.ts` (+30): `updateColor()` optimistic action mirroring server normalization; `importedDeckPatch` + `duplicateColumn` optimistic mirror.
  - Changed `components/column/configure-column-dialog.tsx` (+109 / −1): "Color label" field with 8 preset swatches (orange / green / blue / purple / pink / yellow / cyan / slate) + Clear button + freeform hex input with live invalid-hex error + disabled-Save guard.
  - Changed `components/column/column-card.tsx` (+12 / −4): 10px circular color dot next to title in the expanded header when set; expanded-header + collapsed-strip top accent gradient uses `column.color ?? type.accent` — a collapsed column with color set is instantly identifiable as "that orange one" without reading the rotated title.
  - **Mid-PR structural fix** caught in review: `importedColumnSchema` had validated `color` with `.regex(COLOR_HEX_RE)`, so a single bad color in a hand-edited or shared payload would `safeParse`-fail and throw, aborting the **entire** deck import — the opposite of the documented "dropped, not fatal" contract and inconsistent with how `notifyWebhookUrl` is handled. Fix relaxed the Zod field to `.max(64)` (mirroring `notifyWebhookUrl`) and let the imperative `normalizeColumnColor(c.color)` in `importDeck` drop invalid values to null. Behavior now matches the inline comments and the graceful-degradation contract.

**Impact:** A pinned collapsed orange column stays pinned + collapsed + orange — the three per-column axes (route / density / label) are now fully orthogonal. Color round-trips through export / import / share-links / snapshots identically to any other persisted column attribute (same shape as PR #59's `pinned`). Color is inherited on duplicate; `pinned` is not. The server-authoritative hex regex `/^#[0-9a-f]{6}$/i` means a tampered or hand-edited export can never smuggle a non-canonical color into the DB.

---

## Developer Notes

- **New dependencies:** none — every PR today was pure config / schema / docs / skill additions on existing stacks.
- **Breaking changes:**
  - `aeon` skills.json category vocabulary: `5` keys → `8` keys (`core`, `onchain-security`, `meta` added). Downstream consumers that hard-coded the 5-category list (older dashboard filters, third-party catalog mirrors, AntFleet skill-routing rules) will need to handle the new keys. `generate-skills-json`'s `get_category` now matches the `core` block **first**, so a skill that previously categorized as `dev` may now be `core` if it's in the load-bearing set.
  - `mcp-server` tool descriptions changed — third-party MCP clients that string-match on `[Aeon - Productivity]` etc. will see new labels for the 3 new keys.
- **Architecture shifts:**
  - aeon now has a **first-match-wins core category** in `get_category` — the load-bearing 15 skills are matched before any other rule. This means the taxonomy treats "autonomy" as the primary axis, not "subject domain."
  - The README ↔ skills.json ↔ mcp-server triple is now structurally consistent (zero drift, zero `other` skills). Future drift will be visible to anyone running `generate-skills-json` and diffing.
  - minitor's per-column UX axis now has 7 orthogonal features (tab / collapse / export / search / pin / duplicate / color). The accumulating shape suggests a future consolidated "column config" surface — but each ship has been independently useful.
- **Tech debt:**
  - aeon-agent: `fleet-scorecard` backport from PR #272 still deferred (depends on `memory/instances.json` + a prefetch script aeon-agent doesn't maintain).
  - The pattern of mid-PR structural fixes during merge happened on **both** of the bot-assisted feature/backport PRs today (aeon-agent #82's `${today_minus_7}` and minitor #61's Zod abort). It's been recurring — three of the four substantive bot PRs from the Jun-05 run had the same shape. Worth a future pass on the bot's pre-merge self-review.
  - The 8 ported aeon-aaron skills land disabled-by-default in `aeon.yml`. Enabling decisions deferred to the operator per-skill.

## What's Next

- The next `ecosystem-entrants` run (Mon 11:45 UTC) will diff today's 9 new ECOSYSTEM rows and surface them as discrete arrivals.
- The next `atrium-catalog-watcher` run (Fri 12:00 UTC) will publish its baseline snapshot — it's a new-skill day-0 watcher with no prior state.
- The next `mcp-pulse` run on aeon-agent (Fri 10:00 UTC) will publish its first MCP ecosystem digest for this fork.
- aeon-agent backport chain remaining: only `fleet-scorecard` from PR #272 unbackported (instance-dependent, deferred). The chain is otherwise complete on that batch.
- The mid-PR fix pattern (both #82 and #61 today; same on Jun-05) suggests the bot's pre-merge self-review pass is missing two consistent failure modes: (a) referencing template variables that don't exist (`${today_minus_7}`), and (b) Zod schemas with `.regex` where the imperative drop-invalid path is the documented contract. Worth instrumenting.
- 8 ported aeon-aaron skills landed disabled. The operator's next decision is which of them to enable — `fear-divergence-scout` and `picks-tracker` look like the lowest-config / highest-immediate-signal pair (both depend only on data the framework already collects).
