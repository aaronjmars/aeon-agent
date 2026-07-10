---
type: Article
---

# Push Recap — 2026-06-15

## Verdict
> SHIPPING — first-party skill packs ship; the dashboard now opens on a curated Core set, not 180+ skills.

**Shape:** 7 user-visible commits · 6 internal · 1 infra · 26 bot-filtered
**Volume:** 271 files changed, +3,998/−5,823 lines across 14 commits by 1 author (net −1,825 — a prune-heavy day)
**Merged PRs:** 14 (aeon #467–#481 minus gaps; aeon-agent #99; minitor #73)

---

## Top impact today
1. `9bd9ed7` — **feat: first-party skill-pack system + dashboard Packs view (#474)**. Adds `packs.config.json` (a curated 13-skill `core` allowlist + 8 opt-in packs) and a generated `packs.json` the dashboard reads; new `GET/PATCH /api/packs` and a `PacksPanel` UI. This is the foundation a forker sees first. (11 files, +816/−7)
2. `e263a6b` — **chore: prune 20 redundant/one-shot skills, 202→182 (#473)**. Merges 16 duplicate skills into survivors (e.g. `token-report`→`token-movers`, `write-tweet`→`thread-writer`) and hard-deletes 4 one-shots. The big deletion that made the catalog packable. (26 files, +39/−3,765)
3. `fbc8616` — **feat: category in SKILL.md frontmatter + author-into-pack (#475)**. Retires a 60-line hardcoded slug→category map; a skill's pack is now a one-line `category:` edit in its own frontmatter, backfilled across all 182 skills, with a `--category` CLI flag and a dashboard Pack dropdown. (100 files, +366/−97)

---

## aaronjmars/aeon

### Skill packs — the catalog becomes navigable

**What this is:** The framework shipped 202→182 skills today *and* the system to make that many skills usable. A "pack" is a visibility lens: a fresh clone now shows only the 13-skill **Core** pack everywhere (sidebar + HQ), and enabling a pack reveals its skills in context. It never changes what *runs* — that's still the per-skill `aeon.yml` toggle. This is the priority-zero fork-friction fix: a forker lands on 13 skills, not a wall of 180+.

**Shipped to users**
- `9bd9ed7` — first-party skill-pack system + Packs view (#474)
  - `packs.config.json`: hand-authored source of truth — a curated `core` allowlist plus 8 packs (fleet, research, dev, markets, hound, social, productivity, agent-ops), demoting the 9 fleet/replication skills out of Core (+816/−7 across the PR)
  - `generate-packs-json` + `packs.json`: derives the catalog and asserts every skill lands in exactly one pack (no dup/unknown/unassigned)
  - `PacksPanel` + `/api/packs`: pack-card grid, plus a Lab catch-all so importing a skill with no declared pack never breaks the `ci-packs-json` gate
- `fbc8616` — category in SKILL.md frontmatter (#475)
  - backfills `category:` into all 182 SKILL.md frontmatters (byte-for-byte preserved — `skills.json` unchanged but for its timestamp), deletes `get_category()` from the generator
  - `new-from-template --category` + dashboard upload Pack dropdown: you can now author a skill straight into a pack (+366/−97 across 100 files)
- `88125d1` — sidebar defaults to enabled skills only (#477): the roster starts focused on the active team with a "No skills on duty / Show all skills" empty state, so the default never looks broken (+32/−1)
- `2a911e9` — packs are a browse lens, enable per-skill (#478): drops the bulk "Enable all" PATCH; each pack expands to per-skill on/off toggles; sidebar + HQ now group by pack instead of category (+114/−121, 11 files)
- `f7dfed7` — packs are a *visibility* lens, Core-only by default (#479): enabling a pack reveals its skills rather than bulk-enabling them; enabled-pack selection persists per-browser in localStorage, Core always on (+74/−41)
- `8a6a331` — rename pack "Hound — Onchain Security" → "Onchain Security" (#481): display-name only, pack key stays `hound`, no data migration (+6/−6)
- `ece56ea` — fold packs into README/CONTRIBUTING + `ci-skill-category` gate (#476): README catalog is now pack-organized (corrected a stale 178 count to 182/9 packs); a new CI gate fails any PR whose SKILL.md lacks a valid `category:` so a typo can't silently dump a skill into the Lab catch-all (+149/−42)

**Under the hood**
- `e263a6b` — prune 20 redundant/one-shot skills, 202→182 (#473): 16 merges where the capability survives in another skill + 4 hard deletes of migration one-shots; regenerates `skills.json`, trims `aeon.yml` and the README catalog. The −3,765 lines that made the pack reframe coherent.
- `4c0b845` / `3c762b6` — code-quality cleanup across 8 dimensions + round-1 follow-ups (#467, #468): consolidates `SkillKeyRef`/`SkillMcpRef`/`McpServer` types into `lib/types.ts`, dedupes error-response/REPO_ROOT/file-save/skill-dispatch helpers across API routes, and adds validation on untrusted request bodies (+489/−304 combined)
- `dc2c0a7` — single gateway-provider registry (#469): one `lib/gateway-registry.ts` now feeds the provider union, `GATEWAY_PROVIDERS`, `AUTH_SECRETS`, key-detection, and service-icon domains — adding a provider is now a one-file edit; also stops silently swallowing git-fetch and `.mcp.json` parse failures (+128/−116)

---

## aaronjmars/minitor

### Internal: code-quality cleanup

**What this is:** A multi-pass quality cleanup with no behavior change — `tsc` stays at 0 errors and `next build` compiles clean. Developer-facing only.

**Under the hood**
- `b57f356` — consolidate types, dedupe, prune dead code (#73): moves each `*Meta` renderer-contract interface into its owning plugin; derives `DeckTemplateColumn`/`ImportedDeckColumn` from canonical types via `Omit` instead of hand-maintained duplicates; extracts shared `format.ts`/`pct-change-pill.tsx`/`text.ts` helpers; drops the farcaster paid-tier re-enable scaffolding and a speculative legacy alias (+1,658/−1,212 across 45 files)

---

## aaronjmars/aeon-agent

### Infra: upstream sync fix

**Infra**
- `539eb79` — `fix(sync)`: use GH_GLOBAL + stop pushing dead branches (#99): the upstream-sync workflow failed every run — a bare `GITHUB_TOKEN` can't open PRs ("Resource not accessible by integration") and unrelated histories made the merge a no-op that still pushed a dead `sync/*` branch. Now uses the GH_GLOBAL PAT and gates push+PR on the branch actually advancing. (+19/−4, 1 file)

*(26 `aeonframework` cron/scheduler/auto-commit churn commits bot-filtered — operational, not engineering.)*

---

## Developer notes
- **New dependencies:** none added. One transitive bump: `esbuild` 0.28.0 → 0.28.1 in the dashboard (npm audit fix, #480 — clears GHSA-gv7w-rqvm-qjhr / GHSA-g7r4-m6w7-qqqr; tsx devDependency only, never in the Next production bundle; lockfile-only).
- **Breaking changes for forkers:** SKILL.md frontmatter now **requires** a valid `category:` — the `ci-skill-category` gate fails PRs without one. 20 skills were removed (202→182); forks pinning the deleted skill names in `aeon.yml` will need to remap to the survivor (see #473 merge table).
- **New public surface:** `packs.config.json` / `packs.json`; `GET`/`PATCH /api/packs`; `category:` SKILL.md frontmatter key; `new-from-template --category` flag; dashboard Packs view + per-pack Pack dropdown; two new CI gates (`ci-packs-json`, `ci-skill-category`).
- **Tech debt added:** none surfaced in the diffs — the day was net-subtractive (−1,825 lines) and removed scaffolding rather than adding it.

## Open threads
- **#418** (BEAMR) — stalled, still open.
- **#470** (glim.sh) — external contributor PR, open.
- **#471** (SECURITY.md) — shipped yesterday, open/awaiting merge.
- **minitor #74** (github-commits column) — shipped 06-15, open/awaiting merge.
- Next framework picks once the PR ceiling clears: CODE_OF_CONDUCT.md (last file for green Community Standards), then SHA-pin workflows (needs a workflows-scoped token).

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: not used (commits + PR list sufficient)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 26
- diff-truncated: 0
