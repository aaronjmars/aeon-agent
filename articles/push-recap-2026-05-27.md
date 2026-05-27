# Push Recap — 2026-05-27

## Overview
9 substantive commits by 4 authors across the three watched repos, plus ~26 automated cron/auto-commit pushes in aeon-agent. The day's center of gravity was the **community skill-pack registry**: three external packs landed in `aeon` within an hour (Sparkleware's 7, Signa's 10, noelclaw's 2), and the operator shipped `sparkleware-catalog` — the first-party skill that exports an enriched view of that registry. Around it: a net-negative dashboard refactor in `aeon`, deck version history in `minitor`, and a notable scope trim in `aeon-agent` that **disabled five scheduled skills**.

**Stats:** 44 files changed, +1,656/-322 lines across 9 substantive commits

---

## aaronjmars/aeon — 6 commits

### Community Skill-Pack Registry Growth
**Summary:** Three new community packs were registered in a single afternoon, and the operator added the tooling to surface the registry. This is the discovery layer that yesterday's repo-article described arriving unbidden, now filling out for real.

**Commits:**
- `61c3d11` — Add 7 community skill packs from sparkleware (#249) — *sparkleware*
  - Changed `skill-packs.json` (+78, -1): seven Sparkleware-owned packs appended (`demo-pack`, `aeon-pulse`, `registry-watch`, `arxiv-digest`, `hn-top`, `eth-gas-watch`, `morning-briefing`), each `trust_level: community`, MIT, single-skill. Bumped `updated` 2026-05-23 → 2026-05-26.
  - Changed `README.md` (+7): same seven packs mirrored into the human-readable Community Skill Packs table.
  - This nearly doubles the registry and is self-submitted by the new `sparkleware` org — the storefront populating its own shelves.

- `01e9159` — community: add signa skill pack (10 skills, --path aeon-skills) (#241) — *vritra12*
  - Changed `skill-packs.json` (+12) and `README.md` (+1): registers `codexvritra`'s Signa pack — 10 skills under a non-root `aeon-skills/` subdirectory (uses the `--path` install flag), including agent-to-agent coordination primitives.

- `eff974e` — feat: add noelclaw skill pack (noelvault + noel-swarm) (#250) — *noelclaw*
  - Changed `skill-packs.json` (+12, -1) and `README.md` (+1): registers the noelclaw pack (2 skills: `noelvault`, `noel-swarm`).

- `5f2b595` — feat: add sparkleware-catalog skill — enriched skill-packs.json export (#252) — *aaronjmars*
  - New file `skills/sparkleware-catalog/SKILL.md` (+286): a skill that reads `skill-packs.json`, enriches it, and writes a catalog export to `dashboard/outputs/` for the dashboard feed.
  - Changed `aeon.yml` (+1) and `skills.json` (+13, -1): registered **disabled**, category dev.

**Impact:** The registry went from 6 community packs to ~9 packs / ~28 skills in one day, and `aeon` now has a first-party skill to publish a machine-readable catalog of it. The npm → npms.io discovery pattern is materializing — community supplies the packs, the operator supplies the index.

### Dashboard Refactor & Dead-Code Removal
**Summary:** A consolidation pass on the dashboard — shared logic extracted into new helper modules, types strengthened, a font dependency dropped. Net **−102 lines** across 21 files; a cleanup, not a feature.

**Commits:**
- `e4ec64c` — refactor(dashboard): dedupe helpers, consolidate + strengthen types, remove dead code (#255) — *aaronjmars*
  - New file `dashboard/lib/gh.ts` (+34): centralizes `gh` CLI availability checks and active-repo resolution (`gh repo set-default --view` first, inferred remote fallback), with `REPO_ROOT` resolving one level up from `dashboard/`.
  - New file `dashboard/lib/frontmatter.ts` (+33): single `parseFrontmatter()` for SKILL.md `--- ... ---` blocks, falling back to the first non-heading line (truncated to 120 chars) when `description:` is absent.
  - Changed `dashboard/lib/types.ts` (+38): consolidated shared type definitions.
  - Trimmed eight API routes (`analytics`, `auth`, `import`, `runs`, `runs/[id]/logs`, `secrets`, `skills`, `upload`) — collectively ~150 deletions as duplicated inline logic moved into the new helpers; `dashboard/lib/github.ts` shed 52 lines.
  - Changed `dashboard/package.json` + `package-lock.json`: removed the `geist` font dependency.

**Impact:** Less duplicated `gh`/frontmatter handling, fewer moving parts, one fewer npm dependency. No behavior change intended — the diff is dominated by deletions.

### Ecosystem Curation Fix
**Commits:**
- `8fbbdd2` — fix(ecosystem): correct Amper X handle (#256) — *aaronjmars*
  - Changed `ECOSYSTEM.md` (+1, -1): Amper's X handle corrected `@ampera_xyze` → `@helloamper`.

**Impact:** A one-line accuracy fix so the ecosystem listing points at the live account.

---

## aaronjmars/aeon-agent — 2 commits (+ ~26 automated cron pushes)

### fleet-skill-adoption Backport
**Summary:** The 14th same-day-after backport in the established chain — upstream `aeon` PR #245 (merged May 26) ported into the agent repo the next day.

**Commits:**
- `4e5035f` — feat: backport fleet-skill-adoption leaderboard from upstream aeon PR #245 (#64) — *aaronjmars*
  - New file `skills/fleet-skill-adoption/SKILL.md` (+347): a leaderboard skill that measures which skills forks have **enabled** (not merely present), complementing the existing `fork-skill-gap`.
  - Changed `aeon.yml` (+1) and `skills.json` (+11, -1): registered **disabled**.

**Impact:** Once enabled, gives a "which skills are actually running across the fleet" view rather than "which skills exist in the tree."

### Five Scheduled Skills Disabled
**Summary:** The agent repo trimmed its own scheduled footprint — five `enabled: true` skills flipped to `false` in one commit.

**Commits:**
- `7fb11e3` — chore(skills): disable 5 scheduled skills in aeon.yml (#65) — *aaronjmars*
  - Changed `aeon.yml` (+5, -5): `fetch-tweets`, `tweet-allocator`, `skill-leaderboard`, `hyperstitions-ideas`, and `ai-framework-watch` all set `enabled: false`.
  - Note: `fetch-tweets` (06:30) and `tweet-allocator` (08:00) still ran this morning — the disable landed at 14:04 UTC, after their windows — so the change takes effect from tomorrow. `push-recap`, `token-report`, `repo-pulse`, `feature`, `self-improve`, `repo-actions`, and the content skills remain enabled.

**Impact:** Removes daily social/reward churn (Twitter fetch + $AEON tip allocation) and the weekly competitive-intelligence/leaderboard/idea-generation skills from the agent repo's schedule. Reads as a deliberate scope reduction for `aeon-agent` rather than a failure — worth watching whether more consolidation follows.

---

## aaronjmars/minitor — 1 commit

### Deck Version History
**Summary:** Decks now keep a rolling log of automatic snapshots, restorable in one click as a new deck. Closes the May-26 idea #5. +707/-37 across 9 files, migration 0005.

**Commits:**
- `e9f37b5` — feat: deck version history — auto-captured snapshots restorable as a new deck (#52) — *aaronjmars*
  - New migration `drizzle/0005_deck_snapshots.sql` (+9) + journal + snapshot meta: adds a `deck_snapshots` table (`deck_id` FK with `ON DELETE cascade`, `snapshot_json` text, `captured_at` tz timestamp) with a composite `(deck_id, captured_at)` index.
  - Changed `lib/db/schema.ts` (+20): `deckSnapshots` table — each row is a full DeckExport v1 JSON captured just before a structural mutation (or just after an import/restore), capped to the most recent few rows per deck.
  - Changed `app/actions.ts` (+121, -6): snapshot capture on mutation, per-deck cap enforcement, and a restore action that imports a snapshot as a new deck (reusing the existing `importDeck` contract).
  - New file `components/dialogs/version-history-dialog.tsx` (+133): the history UI listing snapshots with one-click restore.
  - Changed `components/sidebar-01/nav-decks.tsx` (+19, -1) and `lib/store/use-deck-store.ts` (+51, -30): entry point + store wiring.

**Impact:** Operators get an undo/time-machine safety net for deck edits without manual exports — snapshots are silent, capped, and cascade away with their parent deck. Builds directly on the existing export/import/share-link infrastructure (no new validation path).

---

## Developer Notes
- **New dependencies:** none added. `aeon` dashboard **removed** the `geist` font dependency (#255).
- **Breaking changes:** `minitor` migration **0005** (`deck_snapshots` table) must be applied. `aeon-agent` schedule reduced — 5 skills no longer run on cron from 2026-05-28 onward.
- **Architecture shifts:** `aeon` dashboard extracted shared `gh`-CLI and SKILL.md-frontmatter logic into `lib/gh.ts` + `lib/frontmatter.ts`, consuming them across 8 API routes. `minitor` adds a snapshot/version-history layer atop the deck store.
- **Tech debt:** none introduced; #255 was a net deletion and #52 reuses the existing import contract rather than adding a parallel restore path.

## What's Next
- **Enable the two new skills:** both `sparkleware-catalog` (aeon) and `fleet-skill-adoption` (aeon-agent) shipped **disabled** — neither produces output until dispatched/enabled. `fleet-skill-adoption` wants a Monday slot for its first fleet run.
- **Watch the aeon-agent trim:** disabling fetch-tweets + tweet-allocator + 3 weekly skills is a meaningful schedule change. If it's a prelude to consolidating the agent repo's role, expect follow-up commits.
- **Registry curation load:** with three external packs landing in one day, the `sparkleware-catalog` export and the registry's trust model will see more traffic — the canonical install path still resolves through `./install-skill-pack`, not the catalog.
- No branches were left dangling — all 9 substantive commits landed on `main` via merged PRs.
