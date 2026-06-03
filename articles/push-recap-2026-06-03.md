# Push Recap — 2026-06-03

## Overview

Nineteen substantive PRs across three repos by seven distinct authors in the window from yesterday's recap (2026-06-02 16:00 UTC) through today. The dominant story is **ECOSYSTEM.md crossing from a name-only list into a visual catalog**: the Logo column landed (aeon PR #327), seven batched PRs backfilled logos for the full table, five X-handle corrections rode along, Careful Finance got pulled, and four fresh entries (VIGIL, Reppo, Atrium, Sparkleware) joined. Layered on top: a new weekly diff skill (`ecosystem-entrants`, aeon PR #339) so the next burst of new entrants is a structured signal instead of PR-queue archaeology, and an `install-from-atrium` CLI (aeon PR #335) that closes the loop on the onchain skill-marketplace pack merged yesterday.

**Stats:** ~19 substantive PRs · ~2,400 net lines added · 7+ distinct authors across aeon, aeon-agent, and minitor.

---

## aaronjmars/aeon — 15 substantive PRs

### Theme 1: ECOSYSTEM.md gets a Logo column and the catalog is visual end-to-end

**Summary:** The ecosystem table on the README has been a name-and-handle list since launch. In a single evening on 2026-06-02 (19:10–19:31 UTC) aaronjmars added a Logo column to the table, backfilled the first 10 logos as a proof-of-concept, then chained six more "logos batch N" PRs that walked the table alphabetically until every row has a 36×36 square avatar. Most logos point at Twitter's `_400x400` profile-image URL (stable, hotlink-safe); the Autonomopoly row uses the CoinGecko image because GeckoTerminal's `_next/image` proxy is hotlink-protected. Five X-handle corrections (Clerk, Liq, RootAi, Gitlawb Terminal, Precog) and one project rename (USIC → MANAGR) rode along — these were detected in the same scan that pulled the avatars, and shipping them together kept each row's commit history honest.

**Commits:**
- `f982004` — *docs(ecosystem): add Logo column with first batch of logos (#327)* by @aaronjmars (+55/-55 on `ECOSYSTEM.md`)
  - Added a `Logo` column header + divider row to the markdown table
  - Backfilled logos for aeonbook, AgentBounty, Amper, AntFleet, Autonomopoly, Bankr, Bankrsynth, BaseHouse, Baseline, Bean — first 10 rows alphabetically
  - Every other row left empty (`| | Name | … |`) ready for the batch follow-ups
- `cd97623` — *docs(ecosystem): remove Careful Finance, add logos batch 2, fix Clerk handle (#328)*
  - Removed the Careful Finance row entirely
  - Added logos for Blue Agent, Capacitr, Claw Harbor, ClawBank, Clerk, Cobot, Echo Oracle, GitBlock, GitBounty, GitKernal
  - Fixed Clerk's X handle: `@clerk` → `@agent_clerk` (the bare `@clerk` was always going to be a different account)
- `95bad27` — *docs(ecosystem): logos batch 3 + update Liq handle (#329)*
  - Logos for LawbWorld, LiquidPad, Liq, Mei, MiroShark, MythosForge, Noctel
  - Liq handle: `@_proxystudio` → `@liquid_launcher`
- `e2857dd` — *docs(ecosystem): logos batch 4 + update RootAi handle (#330)*
  - Logos for RootAi, SAM, Signa, Solvr, Spoon
  - RootAi handle: `@rootaichad` → `@root_edge`
- `0785b81` — *docs(ecosystem): logos batch 5 + update Gitlawb Terminal handle (#331)*
  - Logos for Gitlawb Terminal, HivemindOS, Hound Flow, NoelClaw, PancakeSwap, Powerloom, ResearchSwarm, Revault
  - Gitlawb Terminal handle: `@Gitlawbterminal` → `@terminalgitlawb`
- `75a5c4e` — *docs(ecosystem): logos batch 6 + rename USIC to MANAGR (#332)*
  - Logos for Venice Kernel, Vexor, VIGIL, Wake, x402Books, zer0, MANAGR
  - USIC → MANAGR rename (X handle `@USICAI` unchanged), and the row moved to its new alphabetical slot (before Mei)
- `d2975f1` — *docs(ecosystem): logos batch 7 + update Precog handle (#333)*
  - Logos for Precog, Reg Terminal, Reppo, SyntheticsAI, Tachi — completes 100% logo coverage
  - Precog handle: `@precog` → `@precogmarkets`
- `bfded77` — *docs(ecosystem): document Logo/PFP column in Add your project (#334)*
  - Updated the "Add your project" section so new contributors know the three-column row format and where to source a square avatar (X profile `_400x400` URL pattern)
  - Worked example showing the full row with `<img>` tag

**Impact:** The README ecosystem table now functions as a visual catalog — at-a-glance recognition for 40+ projects instead of a scroll-through name list. Every future ecosystem PR ships with a logo by convention because the docs in #334 lock in the row template. The handle corrections (5) silently fix the otherwise-permanent error where the table linked to wrong accounts.

---

### Theme 2: Atrium onchain marketplace closes its loop — install-from-atrium CLI lands the day after their skill-pack

**Summary:** Yesterday Atrium-Hermes/aeon-atrium-skills joined `skill-packs.json` as the 8th community pack (aeon PR #316). Today the other half landed: `install-from-atrium`, a Bash CLI that fetches skills directly from `atriumhermes.tech/.well-known/skills/` and runs them through Aeon's own security scanner. The two PRs (#316 yesterday, #335 today) compose: #316 registered Atrium as a known publisher; #335 is the install path that pulls a single skill from their onchain marketplace by name or by canonical `0x…` skill_id. Crucially, the CLI never bypasses the scanner — `--force` is supported (mirroring `./add-skill`) but defaults to BLOCK on findings, and forced installs append to `memory/logs/security.log`. Provenance is written to `skills.lock` with the onchain CID stored where `commit_sha` normally lives.

**Commits:**
- `fa80970` — *Add `install-from-atrium` — install skills from the Atrium onchain marketplace (#335)* by Atrium Hermes (+94, new file `install-from-atrium`, mode 100755)
  - `--list` flag pulls and pretty-prints the marketplace index from `$ATRIUM_HOST/.well-known/skills/index.json` (default `https://atriumhermes.tech`, overridable via env)
  - Install by name (`./install-from-atrium <skill-name>`) or by canonical 64-hex skill_id (`./install-from-atrium 0x<64-hex>`)
  - Fetches `SKILL.md`, parses frontmatter `name` + `cid` + `skill_id`, runs `skills/skill-security-scan/scan.sh` against the temp file before write
  - Records onchain provenance via `jq` into `skills.lock` with `source_repo: "atrium:<skill_id>"`, `source_path: "<wellknown>/by-id/<id>/SKILL.md"`, `branch: "base-mainnet"`, `commit_sha: <cid>` — same schema as `./add-skill`, so existing skill-update audits don't have to special-case Atrium
  - `--force` parity with `./add-skill` for scan-override (logs to `memory/logs/security.log` so forced installs are auditable forever)
- `a92b775` — *Adds **Atrium** to the ecosystem (#337)* by Atrium Hermes (+1 ECOSYSTEM.md row)
  - Added the `Atrium` row with logo, X handle `@atriumhermes`, and `atriumhermes.tech` link — registered as an ecosystem project alongside the install CLI

**Impact:** Aeon is the first agent framework whose skill registry has both a curated community list AND a paid onchain marketplace as installable peers. Operators can `./install-skill-pack <gh-repo>` for free community skills or `./install-from-atrium <skill-name>` for skills with onchain provenance — both pipelines go through the same security scanner, both record provenance in `skills.lock`. The split is intentional: install is free, paying (via the `atrium-scout` skill / `atrium invoke`) is opt-in and orthogonal.

---

### Theme 3: ecosystem-entrants skill — surfacing new arrivals as a discrete weekly signal

**Summary:** The static `ECOSYSTEM.md` table is now getting two-to-three new rows per week (this week alone: HivemindOS #320, Echo Oracle #321, VIGIL #326, Reppo #325, Atrium #337, Sparkleware #338, plus the SyntheticsAI link refresh in #324). At that velocity, new entrants buried in the PR queue is the failure mode — nobody scrolls the table looking for what's new. `ecosystem-pulse` (Monday 11:00 UTC) measures *liveness* of projects already in the table; it can't surface the appearance of new rows because its job is the per-project repo-stat delta. `ecosystem-entrants` fills the gap: a separate Monday 11:45 UTC skill whose only job is the structural diff of `ECOSYSTEM.md` against the prior week's snapshot.

**Commits:**
- `99a9dee` — *feat: add ecosystem-entrants skill (#339)* by @aaronjmars (+303, new `skills/ecosystem-entrants/SKILL.md` +289 / `aeon.yml` +1 / `skills.json` +13)
  - **289-line skill file** with 7-state exit taxonomy (`OK` / `QUIET` / `NO_ECOSYSTEM_FILE` / `NO_PROJECT_TABLE` / `DRY_RUN` / `STATE_CORRUPT` / `BAD_VAR`)
  - Parses `ECOSYSTEM.md` table rows: pipe-delimited markdown → `{name, logo_url, links[], primary_url, raw_row}` records
  - **Deterministic `primary_url` resolution order**: first `github.com/<owner>/<repo>` → first `x.com/<handle>` → first non-empty URL → lowercased project name fallback. A row that swaps which link appears first still maps to the same entry, so link reorders don't generate fake add+remove pairs
  - **28-day prune window**: an entry whose `last_seen` is more than 28d old is dropped from state. A project that was added, removed, then re-added later is treated as a fresh entrant (the operator's question on re-add is "what is this project?" not "did it come back?")
  - **Gated notify**: only fires on added/removed entries. Updates (e.g. an X-only project that added a GitHub repo) surface in the article, never the notification — a swapped logo URL is cosmetic
  - **Baseline run**: first execution doesn't fire N notifications — entries already existed, the skill just hadn't been measuring; emits a one-liner watermark instead
  - **State corruption recovery**: corrupted `memory/topics/ecosystem-entrants-state.json` backs up to `.bak` and resets to empty; next run re-notifies every currently-listed project as a fresh entrant (the safer post-corruption outcome than swallowing a real arrival)
  - Best-effort PR attribution via `gh api search/issues` (14-day window — handles 8d-old PRs since the skill runs weekly, but caps at 14d so a year-old PR can't be falsely matched to a re-added project name)
  - Read-only against `ECOSYSTEM.md` — curation stays a human PR decision per the file's own "Add your project" rules
  - Registered disabled in `aeon.yml` at `45 11 * * 1` (between `competitor-launch-radar` and `ecosystem-pulse` in the Monday-morning intelligence stack)
  - Skills count: `159 → 160` in `skills.json` (alphabetical insert), category `research`

**Impact:** Aeon now has matched-pair coverage on the ecosystem layer: `ecosystem-pulse` watches the living projects, `ecosystem-entrants` watches the door. Next Monday a single 45-minute window writes both digests. If a project is added Monday morning between 11:00 and 11:45 UTC, the pulse run won't include it (it ran first), but the entrants run will — same Monday, two complementary artefacts.

---

### Theme 4: Two new ecosystem entries land alongside the Logo overhaul

**Commits:**
- `952c6ab` — *docs(ecosystem): add Reppo (#325)* by @aaronjmars — Reppo, "AI training data using prediction markets," `reppo.xyz` / `@reppo`
- `4b03658` — *docs(ecosystem): add VIGIL (#326)* by @aaronjmars — VIGIL, "Onchain security scanner for Base," `vigil.codes` / `@vigilcodes`. The ecosystem listing was extracted from a larger PR #323; the `skills/vigil/SKILL.md` half of that PR stays open pending live-endpoint verification
- `b071425` — *docs(ecosystem): add Sparkleware (#338)* by sparkleware — Sparkleware, `sparkleware.fun` / `@sparklewarefun`

**Impact:** Three more ecosystem rows in one window. The cadence supports the case for `ecosystem-entrants` — these would otherwise be buried in the merge stream.

---

### Theme 5: Test infrastructure unblocked — TypeScript test files now run via tsx loader

**Commits:**
- `c9c33d5` — *test(dashboard): widen test glob to include .test.ts via tsx loader (#336)* by Raeli Savitt (+585/-1, mostly `package-lock.json`)
  - `dashboard/package.json`: `"test": "node --test lib/*.test.mjs"` → `"test": "node --import tsx --test 'lib/**/*.test.mjs' 'lib/**/*.test.ts'"`
  - Adds `tsx` (^4.22.4) as a `devDependency`
  - Two changes in one: (1) the glob now recurses into subdirectories (`**`) instead of just `lib/*`, (2) `.test.ts` files are picked up via `--import tsx` so they don't need to be pre-built to `.mjs`

**Impact:** Test files can now be authored in TypeScript directly, alongside the existing `.test.mjs` files. The recursive glob means dashboard tests can sit next to the code they cover (e.g. `lib/feature/widget/widget.test.ts`) instead of all living under a flat `lib/` root.

---

## aaronjmars/aeon-agent — 3 substantive PRs (plus auto-commits)

### Theme 6: 20th consecutive same-day-after backport — pr-merge-queue arrives one day after upstream

**Summary:** Yesterday upstream aeon shipped `pr-merge-queue` (PR #318) — daily 09:45 UTC operator-facing digest of every open PR on a target repo, bucketed by touched-file risk tier. Today aeon-agent's PR #79 backports it verbatim. Twentieth consecutive same-day-after backport in the chain (anchor: operator-scorecard May-3→4; most recent prior links follow-up-patrol May-29→Jun-02). Each backport runs the same playbook: inline backport-note block citing the upstream PR + each adaptation, registration in `aeon.yml`, skills.json count increment, optional minor adaptation for the fork's local conventions.

**Commits:**
- `ae6f304` — *feat: backport pr-merge-queue (upstream aeon PR #318) (#79)* by @aaronjmars (+327, new `skills/pr-merge-queue/SKILL.md` +315 / `aeon.yml` +1 / `skills.json` +11)
  - Daily 09:45 UTC digest of every open PR on `aaronjmars/aeon-agent` (default; `${var}` overridable to any other repo)
  - 6-tier file-bucket precedence: `CORE_REVIEW` (touches `aeon.yml` / `install-skill-pack` / `add-skill` / `notify` / `chain-runner.yml` / `CLAUDE.md` / `generate-skills-json`) > `INFRA_REVIEW` (`.github/workflows/*` + root `package.json` + `Dockerfile*`) > `SKILL_WARN_OR_BLOCK` (touches `skills/*/SKILL.md` AND scan returned WARN or BLOCK) > `SKILL_PASS` (skill PR + every scan PASS) > `FAST_TRACK` (docs/assets/data only) > `UNKNOWN` (files API failed OR no rule matched)
  - **Reuses `skills/skill-security-scan/scan.sh` verbatim** — no forked scan patterns, same scanner pr-skill-triage already uses
  - First-match-wins on tiers so a PR touching both `aeon.yml` AND `skills/x/SKILL.md` is `CORE_REVIEW`, never silently routed to `SKILL_PASS`
  - Re-notify gated on head SHA, not on date — a queue that grows by one PR/day doesn't re-notify yesterday's whole backlog every morning
  - Operator-facing only: no merge action, no PR comments, no labels
  - **Three adaptations vs upstream**: (1) default target swapped from `aaronjmars/aeon` to `aaronjmars/aeon-agent`, (2) `./notify` style already aligned (positional `$1`, no `-f` flag rewrite needed), (3) scan.sh shape matches upstream (May-18 PR #186 + May-20 PR #197 hardening intact)
  - Registered disabled in `aeon.yml` between `pr-skill-triage` and `pr-triage`; skills.json `97 → 98`

**Impact:** aeon-agent now has the morning operator brief that upstream got yesterday. Same gating, same scanner, same precedence rubric — the backport contract holds. Three PR #272 skills remain unbackported (narrative-convergence, mcp-pulse, fleet-scorecard); natural targets for upcoming rounds.

---

### Theme 7: Self-improve — repo-pulse joins the $(date)-removal cleanup wave

**Commits:**
- `48f4f95` — *improve: repo-pulse date-shell guard → literal ${today}-derived CUTOFF (#77)* by @aaronjmars (+149/-10)
  - `skills/repo-pulse/SKILL.md` step 2: `CUTOFF=$(date -u -d '24 hours ago' ...)` → literal `CUTOFF=YYYY-MM-DDT00:00:00Z` computed from `${today}` minus 1 day
  - Runner hook blocks `$(...)` shell substitution ("Contains simple_expansion"); the agent had been improvising this cutoff on every single daily 10:00 UTC run
  - Same constraint PR #63 fixed in `weekly-shiplog` (May 26), PR #67 fixed in `push-recap` (May 28), PR #71 fixed in `heartbeat` (May 30). Repo-pulse is the 4th anti-pattern site fixed in the chain
  - Semantic trade: cutoff goes from "exactly 24h ago" to "midnight UTC of yesterday" (10–34h window on a 10:00 UTC run); the same-day dedup in step 5b (parses prior `## Repo Pulse` sections in today's log to compute deltas) is unchanged and absorbs the overlap
  - Three skills with the same anti-pattern remain unfixed (left for future runs): `repo-article` (7d window, daily 16:00 UTC), `repo-actions` (14d window, even days 14:00 UTC), `star-momentum-alert` (3 expansion sites in one `for D in $(seq 13 -1 0); do DATE=$(date ...)` block — bigger fix)

**Impact:** Daily 10:00 UTC repo-pulse runs stop quietly hand-rolling the cutoff timestamp. One fewer per-run improvisation that future skill audits would have to recognize as "the agent worked around the hook" instead of "the skill is correct."

---

### Theme 8: Daily content shipped on schedule

**Commits:**
- `06bd866` — *repo-article(2026-06-02): The Skill Built To Find Six Gaps Was Going To Report Six (#78)* by @aaronjmars (+230, new `articles/repo-article-2026-06-02.md` +43 + supporting log/output entries)
  - The repo-article skill's daily 16:00 UTC artefact for yesterday's run — about PR #319 (capabilities-map UNDECLARED_BASELINE fix) catching the silent six-gap regression before the next Monday cron run

**Impact:** Daily content pipeline running clean. Repo-article shipped yesterday's notable build on schedule, no manual intervention.

---

## aaronjmars/minitor — 1 substantive PR

### Theme 9: Per-column pin-to-front — 5th rung on the deck-density UX ladder

**Summary:** Minitor's per-column UX has been climbing one rung per day for a week: tab groups (May-29 PR #53), collapse-to-strip (May-30 PR #55), JSON export (May-31 PR #56), quick-search (Jun-02 PR #58), and today pin-to-front (Jun-03 PR #59). Today's add answers a question the prior four don't: *"how do I keep one column always visible regardless of the active tab?"* Pinning is the explicit affordance for crossing tab-group boundaries — a pinned column renders before every unpinned column AND appears on every tab, regardless of the column's stored `position` or its tab-group label.

**Commits:**
- `0b96440` — *feat: per-column pin-to-front toggle (#59)* by @aaronjmars (+530/-9, 11 files)
  - **DB schema (additive)**: `drizzle/0007_column_pinned.sql` adds `pinned` BOOLEAN DEFAULT false NOT NULL on `columns`; existing rows backfill safely with the default. Migration 0007 (after 0006 tab_groups from May-29). Snapshot + journal updated
  - **Server actions** (`app/actions.ts` +30): new `updateColumnPinned(id, pinned)` action; `loadSnapshot` mapping; Zod schema field added to `importedColumnSchema`; `importDeck` coerces `c.pinned === true` so a hand-edited JSON payload can't smuggle a truthy non-boolean into the DB; `exportDeck` emits the field only for `pinned: true` columns (keeps non-pinned exports clean)
  - **Zustand store** (`lib/store/use-deck-store.ts` +23): `updatePinned` action mirroring server normalization
  - **Configure dialog** (`components/column/configure-column-dialog.tsx` +39): "Pin to front" checkbox in a labeled card; Save persists on change
  - **Deck board** (`components/deck/deck-board.tsx` +34/-8): the `visibleColumnIds` memo now does a **stable two-pass partition** — pinned IDs first (preserving their relative DnD-saved order), unpinned IDs second (preserving theirs). Reads as O(n) and conveys exactly "pinned first, then everything else, both in existing relative order"
  - **DnD across pin/unpin is intentionally no-op**: the drag handler checks `columns[active.id]?.pinned !== columns[over.id]?.pinned` and bails. Auto-flipping the pinned flag on drag would be surprising; landing the column silently in an unexpected slot once the visual order re-sorts is the alternative. The Pin checkbox is the only affordance for crossing the boundary
  - **Column-card chrome** (`components/column/column-card.tsx` +21): Pin badge in the expanded header (between refresh-interval and Search) + brand-coloured Pin icon in the collapsed-strip indicator stack — a pinned column folded mid-session keeps its visual marker
  - **Templates** (`lib/deck-templates.ts` +5): `DeckTemplateColumn.pinned?: boolean` so future starter templates can ship pre-pinned
  - Pinning **survives reloads** (DB-backed, unlike `collapsedColumnIds` / `searchByColumn` / `selectedTabByDeck` which are view-state). The author's note in the PR makes the contrast explicit: pin is a persistence choice about *which columns are primary*, view-state would re-create the problem the feature exists to solve
  - Pinning **trumps tab grouping**: the deck-board's filter logic now reads `col?.pinned || !col || !col.tabGroup || col.tabGroup === selectedTab` — a pinned column in tab "DeFi" still appears on every tab
  - Deck export / import / share-link fragments all round-trip the new field backward-compatibly (decks without it default to "not pinned")

**Impact:** Minitor's column-density story is now stratified: tabs decide *which columns am I looking at*, pinning decides *which one I always want visible regardless of tab*, collapse decides *how prominent within the visible set*, and search/keywords decide *what content inside each column matters*. Five complementary axes shipped in 6 days. Could not run Next 16 build/typecheck (offline sandbox — same constraint as PRs #49/#50/#51/#52/#53/#55/#56/#58); manual review only.

---

## Developer Notes

- **New dependencies:** `tsx ^4.22.4` (devDependency in `aeon/dashboard/package.json`) — enables `.test.ts` files to run via `node --import tsx` without precompile
- **Breaking changes:** None. `ECOSYSTEM.md` row format added a Logo column — every old row was rewritten to include it (or an empty cell) in #327, so consumers parsing the table by column index will need to re-index. The `docs(ecosystem)` PR #334 documents the new format for human contributors
- **New environment variables:** `ATRIUM_HOST` (default `https://atriumhermes.tech`) — overridable for `install-from-atrium`, useful for self-hosted Atrium nodes
- **New skills:** `ecosystem-entrants` (aeon, weekly Mon 11:45 UTC, disabled), `pr-merge-queue` (aeon-agent backport, daily 09:45 UTC, disabled)
- **New CLIs:** `install-from-atrium` (aeon, Bash) — fetches skills from the Atrium onchain marketplace through the same scan-then-install pipeline as `./add-skill`
- **New ecosystem entries:** Reppo, VIGIL, Atrium, Sparkleware (4 rows added to `ECOSYSTEM.md`). Careful Finance removed (1 row)
- **X-handle corrections:** Clerk, Liq, RootAi, Gitlawb Terminal, Precog — 5 rows fixed
- **Project rename:** USIC → MANAGR (X handle unchanged, row repositioned alphabetically)
- **Architecture shifts:** Aeon's skill-install surface area now spans three protocols — direct `./add-skill` (GitHub raw URL), `./install-skill-pack` (community curated GitHub repos via skill-packs.json registry), and `./install-from-atrium` (onchain marketplace via well-known endpoint). All three go through the same `skills/skill-security-scan/scan.sh` and all three write provenance to `skills.lock` with the same schema
- **DB migrations:** minitor `drizzle/0007_column_pinned.sql` — additive nullable-with-default boolean column on `columns`. No data migration needed
- **Tech debt:** Three remaining `$(date ...)` anti-pattern sites in aeon-agent skills (`repo-article`, `repo-actions`, `star-momentum-alert`) explicitly carried for future self-improve runs

## What's Next

- The Atrium onchain pipeline is half installed (#316 yesterday + #335 today). Natural next step: enable `install-from-atrium` for first real Atrium pull, or `./install-skill-pack Atrium-Hermes/aeon-atrium-skills` for the curated path. The two install paths converge on the same scanner + lockfile, so the choice is about provenance preference
- `ecosystem-entrants` ships disabled. Its first natural run is Monday 2026-06-08 at 11:45 UTC; the prior-week baseline will fire on first execution (already 40+ entries), then the cadence settles into added/removed-only notifications
- Three PR #272 backports remain in the aeon-agent queue: `narrative-convergence`, `mcp-pulse`, `fleet-scorecard` — the chain has shipped one per day since May 29, on track to complete on or before Jun-06
- minitor's column-density UX ladder has consumed every May ideas-cycle entry tied to it. Next steps for minitor are either deeper into a specific column type (plugin-level features) or up a level (deck-level features beyond columns) — the surface is open
- Three remaining `$(date ...)` anti-pattern sites in aeon-agent skills (repo-article 26, repo-actions 29, star-momentum-alert 69 — the third needs a `for` loop refactor not a single substitution swap)
