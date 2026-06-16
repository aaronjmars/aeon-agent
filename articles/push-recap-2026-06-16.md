# Push Recap — 2026-06-16

## Verdict
> SHIPPING — one-click community-pack install now lands skills on main and renders them in the dashboard.

**Shape:** 13 user-visible commits · 3 internal · 4 infra · 35 bot-filtered
**Volume:** ~105 files changed (50 from a single em-dash style sweep), +1,341/−469 lines across 19 merged PRs / 19 commits by 4 authors
**Merged PRs:** 19 — aeon ×14 (#470 glim.sh, #471 SECURITY.md, #472 Hunch pack, #482 em-dash sweep, #483 one-click install, #484 catalog decouple, #485 auto-merge, #486 Installed pack, #487 packs.json regen, #488 readme, #489 Robinhood MCP, #490 community roster, #491 per-repo packs, #493 --path forward); aeon-agent ×4 (#101, #102, #103, #104); minitor ×1 (#74)

---

## Top impact today
1. `8d6d2ea` — minitor #74 github-commits column plugin. New TweetDeck-style column streaming a repo's commit feed (the most direct velocity signal) — keyless or token-auth, registered across all three id registries. (8 files, +248/−3)
2. `da0a970` — aeon #483 one-click community pack install. Replaces the copy-only `./install-skill-pack` command on community pack cards with an "Install pack" button that dispatches a new `install-skill` core skill; adds an "Add more" cell to the HQ Packs grid. (8 files, +167/−11)
3. `341c33f` — aeon #490 render installed community packs in the roster. Grouping is now data-driven (`packGroups()`) instead of a hardcoded PACKS list, so a skill installed under an arbitrary community-pack key (e.g. `antfleet-pr-review`) renders in its own always-visible group instead of vanishing. (8 files, +125/−28)

---

## aaronjmars/aeon

### The community-install pipeline got finished end-to-end

**What this is:** Yesterday the skill-pack *system* shipped (Core-by-default, 182 skills behind opt-in packs). Today closed the loop that actually mattered for forkers: a skill you install from a community repo now installs in one click, lands on `main`, and shows up in your dashboard — six separate failure points in that path were each found and fixed. This is the difference between "packs exist" and "packs work on a fresh fork."

**Shipped to users**
- `da0a970` — #483 one-click install + "Add more" packs button
  - `apps/dashboard`: community pack cards swap the copy-only command for a primary "Install pack" button (dispatches via `/api/skills/<name>/run`), keeping the copy-command icon + SITE link; HQ Packs grid gains a final "Add more" cell routing to the Packs view (+167/−11)
  - new `skills/install-skill` (core, `workflow_dispatch`): drives the hardened `./install-skill-pack`, keeps the HIGH-blocking security scan on, regenerates the catalog, opens a PR — skills land **disabled**
- `afd4efe` — #485 zero-touch auto-merge + ensure Actions can open PRs
  - `apps/dashboard`: `ensureActionsCanOpenPRs()` flips `default_workflow_permissions=write` + auto-merge via the operator's admin `gh` before dispatch — a fresh fork has this **off** and the in-Actions token can't set it, so without this the install PR was blocked and skills stranded on an unmerged branch (+76/−14)
  - `skills/install-skill`: squash-auto-merges the PR (`gh pr merge --squash --delete-branch --auto`, with `--no-merge` opt-out)
  - `onboard`: detects the PR-creation setting and prints the one-line fix for the CLI/cron path
- `078eee1` — #486 installed community skills get their own always-visible "Installed" pack
  - `scripts/generate-packs-json`: reads `skills.lock`, pulls installed skills **out** of their category-assigned first-party pack into a synthetic `installed` pack (`kind:community`, carrying `source_repo`); emitted only when `skills.lock` has entries, so upstream packs.json stays byte-identical (+56/−7)
  - `apps/dashboard`: `installed` added to PACKS, locked always-visible like Core
- `341c33f` — #490 render installed community packs in the roster (data-driven groups)
  - `constants.ts`: `FIRST_PARTY_KEYS` + `packGroups()` build the ordered group list from whatever packs skills actually belong to — Core first, then any non-first-party (community) pack, always shown; `constants.test.ts` covers the `antfleet-pr-review` regression (+125/−28)
  - `api/skills`: joins each skill's `packName` from packs.json so groups show "AntFleet PR Review", not a raw key
- `04625ff` — #487 install-skill-pack regenerates packs.json so installs aren't invisible
  - `install-skill-pack`: after a successful install, deterministically regenerates **both** skills.json **and** packs.json itself instead of leaving packs.json to an agent step that got skipped (the bug: a skill reached main in skills.json but not packs.json, so the dashboard never showed it) (+22/−4)
- `fbdcd0e` — #491 scope enabled-packs per repo so forks default to Core-only
  - `apps/dashboard`: pack-visibility selection moves from a single global `aeon.enabledPacks` localStorage key (keyed only by `localhost:5555`, so enabling Dev on one fork bled into every fork) to a per-repo `aeon.enabledPacks:<owner/repo>` key; a fork with no saved selection now defaults to Core only (+16/−4)
- `02d458b` — #493 forward pack `path` as `--path` on install + copy command
  - `apps/dashboard`: the install button + copy command now build `--path <path>` when a pack declares one — community packs whose skills live in a repo subdirectory (hunch, signa, mandateseal-guard) failed to install without it (+19/−12)

**Under the hood**
- `2061478` — #484 decouple skills.json from aeon.yml: `generate-skills-json` stops reading aeon.yml and drops the dead `schedule` field, so an operator schedule edit (or upstream sync) can no longer make the catalog stale and false-fail `ci-skills-json` on a fork (+21/−24, infra)

### New catalog surface — agents that take positions, not just watch

**What this is:** Three external/MCP additions, and the theme is agents acting on money rails: a betting skill pack and two trading/live-data MCP servers join the featured catalog.

**Shipped to users**
- `fe8579f` — #472 Hunch Prediction Markets skill pack (by rajkaria, external): 3 skills (hunch-intel / hunch-markets / hunch-bet), autonomous x402 betting on PlayHunch prediction markets on Base — "the first registry pack where an agent can take a position, not just monitor," simulate-by-default on the money path (+14/−1 registry; skills live in the external repo)
- `271f195` — #470 glim.sh live-data MCP (by tenequm, external): x402 + MPP, added to the featured MCP catalog (+7/−0) — this clears the `#464` glim.sh idea that had sat as the carried-over repo-actions top pick
- `7fd25a2` — #489 Robinhood Agentic Trading MCP: remote HTTP MCP (OAuth) that reads portfolio/positions/order history and places trades from a dedicated Agentic brokerage account (+7/−0)

### Docs & security

**Shipped to users**
- `4414a2e` — #471 SECURITY.md: supported versions, private vuln-reporting flow, documented trust model (CLAUDE.md/SKILL.md trusted, fetched content untrusted), GITHUB_TOKEN/GH_GLOBAL scope split, in/out-of-scope lists — closes the last `code_of_conduct`/`security`=null gap toward green Community Standards (security half) (+141/−0)
- `9d017f3` — #488 align the README packs table (emoji-width-aware padding) and delete the stale `skills-aeon-197.jpg` banner (named for 197 skills; catalog is 182) plus its orphaned 388KB asset (+11/−13)

**Under the hood**
- `470aa90` — #482 style: replace spaced em-dash `" — "` with `" - "` across README + 49 dashboard files — pure 1:1 text substitution, no logic touched (+327/−327, 50 files). Big line count, zero behavior change.

---

## Internal: aaronjmars/aeon-agent (the live operating instance)

**What this is:** The agent tuning its own runner and skills — not framework product, but it explains why some crons went green again today.

- `2397f9f` — #101 disable `operator-scorecard` (aeon.yml `enabled: false`) and enrich `repo-pulse` to profile every new stargazer **and** forker (name, location, company, bio, followers, repos, twitter) into per-actor cards, capped at 10+10 lookups/repo, profile strings treated as untrusted (+36/−12)
- `7166c83` — #102 repo-pulse follow-up on operator feedback: always render the bio line (widened 100→140 chars), hide the follower count when 0/<10, reorder cards so identity leads (+14/−9)
- `a28129f` — #103 unblock the `feature` skill: add `rm/cd/cp/mv` to the run allowlist (it clones each repo into `/tmp/feature-build-<repo>` and `cd`s in — every clone/cleanup was being denied, thrashing ~25 turns/~$0.80) and treat Anthropic content-filter blocks as a clean `exit 0` skip instead of a red-X job failure (+18/−0, infra)
- `b094360` — #104 mirror those two #103 fixes into the Messages & Scheduler workflow, which shares the same allowlist + `claude -p` shape (+16/−0, infra)

---

## Developer notes
- **New dependencies:** none (all additions are skills/catalog/dashboard code, no new packages)
- **Breaking changes:** none for upstream. Catalog generators (`generate-packs-json`, `generate-skills-json`) changed behavior but emit a byte-identical packs.json/skills.json on a repo with no `skills.lock`. Legacy global `aeon.enabledPacks` localStorage key is abandoned (no migration — by design; that stale state was the bug).
- **New public surface:** new core skill `install-skill` (`workflow_dispatch`, var `owner/repo [skill...]`); dashboard "Install pack" / "Add more" buttons + `/api/skills/<name>/run` dispatch path; `installed` synthetic pack key; per-repo `aeon.enabledPacks:<owner/repo>` localStorage key; `packGroups()` + `FIRST_PARTY_KEYS` in dashboard constants; glim.sh, Robinhood, Hunch entries in the featured catalog; SECURITY.md disclosure flow.
- **Tech debt added:** none flagged in the diffs — fixes were deterministic-regeneration and data-driven-grouping (removing hardcoded lists), i.e. debt paid down.

## Open threads
- **PR #418 (BEAMR gateway)** — still stalled (open since 2026-06-10, last touched 06-12); flagged in the 06-15 heartbeat. Not in this window's merges.
- **aeon Community Standards** — SECURITY.md merged (#471); `CODE_OF_CONDUCT.md` remains the last file for a green profile, then SHA-pinning workflows (needs a workflows-scoped token).
- **`feature` cron** — two `feature failed` auto-commits today (12:34, 14:26 UTC) before #103/#104 landed the allowlist + content-filter fixes; next scheduled run should confirm the red-X is cleared.

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 35 (all `aeonframework` automated `chore(scheduler/cron/<skill>)` self-commits on aeon-agent)
- diff-truncated: 0
