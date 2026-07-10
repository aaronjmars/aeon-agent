---
type: Article
---

# Push Recap — 2026-06-19

## Verdict
> MIXED — A2A gateway documented, catalog scrubbed, heartbeat reliability fixed

**Shape:** 6 user-visible commits · 3 internal · 2 infra · ~35 bot-filtered
**Volume:** ~50 files changed, +393/−208 lines across 13 substantive commits by 3 human authors (aaronjmars, adlai88, clawhunter)
**Merged PRs:** 11 (#506 purge dangling refs, #505 skill gallery refresh, #504 remove 4 more dangling refs, #503 remove token-report refs, #501 A2A gateway README, #499 Polymarket Trader pack, #498 clawhunter-skills pack, #497 one-click pack install docs, #108 heartbeat DEGRADED fix, #77 minitor CI hardening, #76 minitor build workflow)

---

## Top impact today

1. `ab15246` — docs(a2a-server): add README quickstart for the A2A gateway (#501). New 116-line `apps/a2a-server/README.md` turns the previously undocumented gateway into a walk-up-and-run resource — LangChain/AutoGen/CrewAI/OpenAI Agents SDK all get a copy-paste path from zero to a fired skill call. (5 files, +127/−9)
2. `2a4c441` — fix(heartbeat): don't flag status page DEGRADED on transient, recovered failure (#108). `skills/heartbeat/SKILL.md` now reserves 🔴 DEGRADED for skills that are currently *and* persistently broken (`consecutive_failures ≥ 3` or `last_failed ≥ last_success`); a single recovered blip drops to 🟡 WATCH, stopping `docs/status.md` from underselling reliability to evaluating forkers. (6 files, +83/−7)
3. `90e8b5f` — docs: refresh skill gallery + prune skill-graph (#505). `docs/index.md` goes from referencing ~10 deleted skills to 180+ live ones; `docs/skill-graph.md` drops 17 dead nodes and 2 broken edges, recomputing all counts to 176 mapped vs 183 live. (2 files, +33/−71)
4. `d1f662d` — chore: purge remaining dangling refs (#506). Final consistency sweep removes 6 dead tool entries from the Smithery manifest/submission, 3 dead rows from `docs/skills.md`, the dead `polymarket` eval block, and repoints 6 cross-references in active SKILL.md files. (10 files, +7/−49)
5. `d1e07e8` — Add Polymarket Trader by Simmer to community skill packs (#499). Three new skills (`polymarket-intel`, `polymarket-markets`, `polymarket-trade`) wired to Simmer's verified execution layer — simulate-by-default, bounded, opt-in live. Registry now covers both watching Polymarket (existing `monitor-polymarket`) and acting on it. (2 files, +16/−1)

---

## aaronjmars/aeon

### A2A Gateway — first user-facing documentation

**What this is:** The A2A gateway (`apps/a2a-server/`) shipped source code and four working framework clients months ago but had no README. Any developer evaluating Aeon from AutoGen, LangChain, CrewAI, or the OpenAI Agents SDK was landing on raw TypeScript with no path to a running task. Today that gap closed.

**Shipped to users**
- `ab15246` — docs(a2a-server): add README quickstart for the A2A gateway (#501)
  - `apps/a2a-server/README.md` (new, +116): documents what the gateway is, how to start it (`./add-a2a`), env vars (`A2A_PORT`, `A2A_URL`), all three endpoints (`/.well-known/agent.json`, `POST /`, `POST /tasks/sendSubscribe`), a complete Python submit+poll client, framework example table (LangChain/AutoGen/CrewAI/OpenAI Agents SDK), and protocol/deployment notes. All commands and endpoint paths verified against `src/index.ts`.
  - `README.md` (+2): one-line pointer from the A2A section pointing to the new server README.
  - `examples/a2a/openai_agents_client.py` (+6/−6): repoints dead `aeon-token-report` skill to `aeon-token-movers` — copy-paste run now works.

### Community Packs — two new entries, one install doc fix

**What this is:** The skill-pack registry grew by two external packs, and the README was updated to surface the lower-friction dashboard one-click install path alongside the CLI.

**Shipped to users**
- `d1e07e8` — Add Polymarket Trader by Simmer to community skill packs (#499, by adlai88)
  - `skill-packs.json` (+15): registers `SpartanLabsXyz/aeon-skill-pack-polymarket` with three skills — `polymarket-intel` (signal read), `polymarket-markets` (market discovery), `polymarket-trade` (position execution via Simmer, simulate-by-default). The registry's first pack enabling actual onchain position-taking on a prediction market.
- `7bd1b8d` — Add community skill pack: clawhunter-skills (#498, by Claw Hunter)
  - `skill-packs.json` (+12): registers `clawhunter/clawhunter-skills` with two skills (`clawhunter-bounties`, `clawhunter-content-studio`) wrapping the clawhunter.fun API for bounty discovery and x402-paid content creation.
- `e5e7052` — docs(readme): document one-click dashboard pack install (#497)
  - `README.md` (+6/−2): splits the Community skill packs section into "One-click (dashboard)" and "CLI" subsections; makes the disabled-until-enabled post-install step explicit.

### Catalog Health — dead skill references cleared in four passes

**What this is:** Four sequential PRs completed a reference cleanup after the 2026-06-15 skill prune (17 skills removed). The four passes covered token-report, then four more slugs, then the catalog docs, then a final sweep of SKILL.md cross-references and eval configs.

**Under the hood**
- `562f78b` — chore: remove dangling references to the deleted token-report skill (#503)
  - `skills/skill-health/tests/smoke.sh` (+1/−1): real bug fixed — `token-report` was in `CANARY_SKILLS`, pointing the dry-run structural check at a deleted dir; repointed to `token-movers`.
  - `docs/smithery-manifest.json` (−4): removes the orphaned `aeon-token-report` tool entry.
  - 7 other files: README, SHOWCASE, syndicate-article, update-gallery SKILL.md cross-refs all repointed.
- `8e70b5a` — chore: remove dangling refs to 4 more skills (#504)
  - Maps `token-alert→price-alert`, `defi-monitor→defi-overview`, `wallet-digest→treasury-info`, `feature→pr-review` across 14 files including `skill-evals/evals.json` (dead eval block removed).
- `90e8b5f` — docs: refresh skill gallery + prune skill-graph (#505)
  - `docs/index.md` (+10/−10): 10 dead skill names replaced with live equivalents; "50 skills" count corrected to "180+".
  - `docs/skill-graph.md` (+23/−61): 17 dead nodes pruned, all counts recomputed to 176 mapped/183 live.
- `d1f662d` — chore: purge remaining dangling refs (#506)
  - `docs/smithery-manifest.json` + `docs/smithery-submission.md` (−30): 6 dead tool entries removed.
  - `skills/skill-evals/evals.json` (−9): dead `polymarket` eval block removed.
  - `skills/contributor-spotlight`, `pm-manipulation`, `pm-pulse`, `self-improve`, `update-gallery` SKILL.md (6 files): 6 cross-references repointed to live successors.

---

## aaronjmars/aeon-agent

### Heartbeat — status page false-positive fixed

**What this is:** The public `docs/status.md` was flipping to 🔴 DEGRADED on any single failed skill run, even one the skill had already recovered from before the next heartbeat. This made the public reliability page an unreliable signal for builders evaluating whether to fork.

**Shipped to users**
- `2a4c441` — fix(heartbeat): don't flag status page DEGRADED on transient, recovered failure (#108)
  - `skills/heartbeat/SKILL.md` (+6/−4): rewrites the "Overall status" verdict mapping. 🔴 DEGRADED now requires `consecutive_failures ≥ 3`, `success_rate < 0.5` (with ≥5 runs), self-check stale >36h, or a non-recovered failure with `consecutive_failures ≥ 2`. A recovered failure (`last_success > last_failed`) or a first/isolated failure (`consecutive_failures ≤ 1`) maps to 🟡 WATCH. P0 notifications are unchanged.
  - Evidence: thread-formatter failed 2026-06-17 at 18:39 UTC, recovered at 19:13 UTC — but the 19:00 heartbeat still wrote `STATUS_PAGE=DEGRADED`.

---

## aaronjmars/minitor

### Infra: first CI build gate

**What this is:** minitor had no CI before today. Two PRs added a full build gate that catches the same class of failure that caused the recent regressions (#66, #70, #71), then hardened the actions versions.

**Infra**
- `da9c9ca` — ci: add build workflow on push + PR (#76)
  - `.github/workflows/ci.yml` (new, +32): single `Build` job running `npm ci && next build` on push-to-main and PRs. `next build` runs the TypeScript checker — exactly the gate that catches `"use server"` export violations and null-narrowing issues. No secrets required (PGlite fallback when `DATABASE_URL` unset).
- `3565359` — ci: bump checkout/setup-node to v5 + drop to read-only token (#77)
  - `.github/workflows/ci.yml` (+6/−2): bumps `actions/checkout@v4→@v5` and `actions/setup-node@v4→@v5` to clear the Node.js 20 deprecation warning; adds `permissions: contents: read` least-privilege block.

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none — docs-only and SKILL.md prompt changes only; no API, config, or schema changes
- **New public surface:** `apps/a2a-server/README.md` (new doc file); `skill-packs.json` gains 2 new pack entries (Polymarket Trader, clawhunter-skills)
- **Tech debt added:** `docs/skill-graph.md` banner notes ~7 newer live skills (176 mapped vs 183 live) still need a full `skill-graph` skill re-run to appear

## Open threads
- #418 (BEAMR, external contributor) — still the only open code PR on `aaronjmars/aeon`; PR #501 merged brings it down to one non-author PR
- `docs/skill-graph.md` — mechanically pruned to 176 nodes; a full `skill-graph` skill run needed to re-add the 7+ newer skills and refresh dependency edges
- `skill-packs.json` has 2 new packs from today — both `default_enabled: false`; operators must set secrets and flip `enabled: true`

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: ~35 (aeon-agent operational auto-commits: chore(cron), chore(scheduler), chore(skill)-auto-commit)
- diff-truncated: 0
