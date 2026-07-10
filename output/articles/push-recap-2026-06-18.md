---
type: Article
---

# Push Recap — 2026-06-18

## Verdict
> SHIPPING — two community packs land; heartbeat status page fixed

**Shape:** 4 user-visible commits · 1 internal · 5 infra · 35 bot-filtered
**Volume:** 20 files changed, +238/−111 lines across 10 commits by 3 authors
**Merged PRs:** 7 (#499 Polymarket Trader pack; #498 clawhunter-skills; #497 README one-click; #496 drop non-Claude models; #108 heartbeat status-page fix; #77 minitor CI bump; #76 minitor CI build)

---

## Top impact today
1. `2a4c441` — fix(heartbeat): status-page DEGRADED now reserved for persistently broken skills. The heartbeat SKILL.md redefines 🔴: requires stuck/consecutive_failures ≥ 3/success_rate < 0.5/non-recovered after 2+ failures — a recovered blip maps to 🟡 WATCH instead, so the public fork-facing page stops flashing red on five-minute network hiccups. (6 files, +83/−7)
2. `2e2ff4a` — Remove redundant per-skill model pins from aeon.yml. Drops all explicit `model: claude-sonnet-4-6` overrides that duplicated the new root default, making aeon.yml the single source of truth for model routing. (1 file, +78/−78)
3. `d1e07e8` — Add Polymarket Trader by Simmer to community skill packs (#499). skill-packs.json now lists polymarket-intel, polymarket-markets, and polymarket-trade — real position-taking on Polymarket, simulate-by-default, one `SIMMER_API_KEY` away from live. First execution pack for the venue with the deepest prediction-market liquidity. (2 files, +16/−1)

---

## aaronjmars/aeon

### Community Pack Registry — two external contributors merged

**What this is:** Two external PRs grew the machine-readable community registry today. Both cleared `scripts/validate-pack.sh` (shipped 2026-06-17) with zero warnings. Forkers can one-click install both packs from the dashboard or `./install-skill-pack` immediately.

**Shipped to users**
- `d1e07e8` — Add Polymarket Trader by Simmer to community skill packs (#499)
  - `skill-packs.json`: New entry for SpartanLabsXyz/aeon-skill-pack-polymarket — three skills (polymarket-intel, polymarket-markets, polymarket-trade), SIMMER_API_KEY required, capabilities [external_api, writes_external_host, onchain_writes, sends_notifications]. Simulate-by-default; live opt-in with bounded orders. (+15/−1)
  - `README.md`: New table row documenting the pack with Simmer attribution and deeplink. (+1/−0)
- `7bd1b8d` — Add community skill pack: clawhunter-skills (#498)
  - `skill-packs.json`: New entry for clawhunter/clawhunter-skills — two skills (clawhunter-bounties discovers and vets Pump Fun GO bounties; clawhunter-content-studio generates voice tones, images, and video direction to win them). x402 payments settle on Solana or Base. (+12/−1)
  - `README.md`: New table row. (+1/−0)

**Under the hood**
- `e5e7052` — docs(readme): document one-click dashboard pack install (#497): README's Community skill packs section now shows two install paths side by side — the dashboard's Packs → Install pack button (security-scanned, opens an auto-merging PR) and the `./install-skill-pack` CLI. Clarifies that installed skills land disabled until secrets are set and `enabled: true` is flipped. (+6/−2)

### Internal: Model dropdown cleanup
- `88707ea` — chore: list only Claude models, drop Bankr gateway non-Claude options (#496): Removes gemini-3-pro, gemini-3-flash, gpt-5.2, kimi-k2.5, qwen3-coder from the `workflow_dispatch` model dropdown in `.github/workflows/aeon.yml`, the options comment in `aeon.yml`, and the Bankr Gateway pricing tables in spend-monitor and cost-report SKILL.md. Non-Claude models still route through the gateway at runtime; the dropdown just no longer surfaces them. (+0/−16)

---

## aaronjmars/aeon-agent

### Heartbeat: Public status page stops false-positives

**What this is:** The fork-facing status page was flipping to 🔴 DEGRADED on any `last_status: "failed"` entry — including transient one-off failures the fleet had already recovered from. The 2026-06-17 thread-formatter blip (failed 18:39, recovered 19:13) triggered a false-positive DEGRADED that stayed visible until the next heartbeat. The fix makes the page reflect whether Aeon is *currently broken*, not whether it ever had a bad minute.

**Shipped to users**
- `2a4c441` — fix(heartbeat): don't flag the public status page DEGRADED on a transient, recovered failure (#108)
  - `skills/heartbeat/SKILL.md`: Rewrites the Overall status logic. 🔴 DEGRADED now requires current+persistent breakage: a stuck skill, consecutive_failures ≥ 3, success_rate < 0.5 with ≥ 5 total runs, heartbeat self-check > 36h stale, or a non-recovered failure with consecutive_failures ≥ 2. A recovered failure (last_success > last_failed) maps to 🟡 WATCH. Any non-recovered failure that doesn't clear the 🔴 bar — including a first/isolated failure — also maps to 🟡 WATCH, closing the "green-hole" where a brand-new skill's first failure could fall through to 🟢 OK. P0 operator notifications unchanged. (+6/−4)

### Infra: Model routing — Sonnet default, Opus for high-stakes

**What this is:** Three commits as a set: switched the fleet default from Opus 4.8 to Sonnet 4.6, stripped the now-redundant per-skill Sonnet overrides, then selectively re-pinned Opus on skills that ship code or write flagship content. Net: routine monitoring, digest, and ops skills run on Sonnet; repo-article, self-improve, and feature keep Opus.

**Infra**
- `a3b4a22` — Switch default model to claude-sonnet-4-6: Changes root `model: claude-opus-4-8` → `model: claude-sonnet-4-6` in aeon.yml; per-skill Sonnet pins were already in place so behavior was unchanged at that point. (1 file, +1/−1)
- `2e2ff4a` — Remove redundant per-skill model pins; rely on root default: Drops every explicit `model: claude-sonnet-4-6` from individual skill blocks in aeon.yml — 78 lines in, 78 lines out, single source of truth restored. (1 file, +78/−78)
- `f03a0d8` — Pin Opus 4.8 on high-reasoning enabled skills: Adds `model: claude-opus-4-8` overrides to repo-article, self-improve, and feature in aeon.yml — the skills whose outputs ship to users or directly modify the agent's own code. (1 file, +3/−3)

---

## aaronjmars/minitor

### Infra: First CI workflow

**What this is:** Minitor had no automated build gate before today. These two PRs give every push and PR a build check, and harden the runner actions version.

**Infra**
- `da9c9ca` — ci: add build workflow on push + PR (#76): New `.github/workflows/ci.yml` runs `npm ci` + `next build` on push-to-main and all pull requests. Concurrency group cancels superseded runs on the same ref. No secrets needed: DATABASE_URL unset triggers the PGlite fallback in `lib/db/client.ts`, so the build runs on forks and external PRs too. This is the gate that would have caught the build breaks in #66/#70/#71. (1 file, +32/−0)
- `3565359` — ci: bump checkout/setup-node to v5 + read-only token (#77): Bumps actions/checkout and actions/setup-node from v4 → v5 to clear the Node.js 20 deprecation warning on the runner. Adds `permissions: contents: read` top-level block — least-privilege for a build-only job. (1 file, +6/−2)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none
- **New public surface:** `polymarket-intel`, `polymarket-markets`, `polymarket-trade` skills (Simmer Polymarket pack, community); `clawhunter-bounties`, `clawhunter-content-studio` skills (clawhunter-skills pack, community)
- **Tech debt added:** none

## Open threads
- `aaronjmars/aeon` PR #418 (feat(gateway): add BEAMR as LLM gateway) — contributor PR, last updated 2026-06-16, still stale/open. Only open non-bot PR on the repo.
- repo-actions 2026-06-18 carried forward: "Add A2A server quickstart guide to apps/a2a-server/" — identified as top pick, not yet opened as a PR.

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 35 (aeonframework chore/cron/scheduler auto-commits in aeon-agent)
- diff-truncated: 0
