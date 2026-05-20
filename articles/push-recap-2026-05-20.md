# Push Recap — 2026-05-20

## Overview

Fourteen substantive commits across three repos in the last 24 hours from two human authors (@aaronjmars, AntFleet) plus the routine cron auto-commits in aeon-agent. The main thrust was **dashboard hardening + silent-failure fixes** on aeon (six dashboard/script-safety PRs landed, four of them sourced from AntFleet's outside-in security review) and **three new minitor columns** rounding out the on-chain + GitHub-discussions surface. aeon-agent kept its same-day-after backport cadence intact (10th consecutive) with `competitor-launch-radar`.

**Stats:** 28 files changed, +2,213 / -167 lines across 14 substantive commits (excluding ~30 aeon-agent cron auto-commits).

---

## aaronjmars/aeon

Nine PRs merged in two clusters six hours apart: a 19:25–22:09 UTC dashboard cluster on May-19, and a 13:23 UTC AntFleet fix-bundle on May-20.

### Theme 1: Dashboard hardening — loopback gate, gh preflight, token reassembly, dep bumps

The `dashboard/` local-UI is the operator's installation surface. It shells out to `gh` for secret-writes and workflow dispatches, and assumes "the OS user owns localhost." Four commits this window all tighten that assumption end-to-end.

**Commits:**

- `fa0adc0` — **security(dashboard): gate /api/* on loopback Host + same-origin write (#188)**
  - New `dashboard/middleware.ts` (+33): runs on every `/api/*` route, calls `gateRequest(req)` from the new security module
  - New `dashboard/lib/security/api-gate.ts` (+199) + test (+188): loopback Host-header allowlist + same-origin check on state-changing methods. Operator escape hatches via `AEON_DASHBOARD_ALLOWED_HOSTS` and `AEON_DASHBOARD_ALLOW_ANY_HOST=1` for trusted reverse-proxy setups
  - README (+13): documents the threat model — DNS rebinding + cross-origin POST to localhost are unauthenticated-write surfaces on `/api/skills/[name]/run`, `/api/secrets`, and `/api/auth` without this gate
  - Largest single commit of the day at +433 lines, all additive

- `ae2e0ca` — **security(dashboard): bump next to 16.2.6 and override postcss >=8.5.10 (#189)**
  - `dashboard/package.json` (+3): adds `overrides.postcss: "^8.5.10"` to pin the transitive postcss version above the vuln floor
  - `dashboard/package-lock.json` (+47, -75): the net package-lock shrink suggests next's own dep tree got tighter on the 16.2.6 bump

- `360dd13` — **fix(dashboard): require gh CLI up front + surface real /api/auth errors (#190)**
  - `aeon` launcher (+35): two preflights — `command -v gh` and `gh auth status`. Without them, the dashboard's failure showed up much later as a confusing 503 in the Authenticate modal. Now exits early with platform-specific install instructions (brew / winget / GitHub Releases)
  - `dashboard/app/page.tsx` (+1/-1): wires the upstream-error surface

- `e777f0a` — **fix(auth): extract only token characters per line during claude setup-token reassembly (#194)**
  - `dashboard/app/api/auth/route.ts` (+14/-12): when the operator pastes the wrapped token output, the first line previously got pushed in whole (trimmed only). Now every line goes through a `^[A-Za-z0-9_\-]+` regex match, stopping at the first contribution-free line. Adds an `sk-ant-oat` prefix validation that returns 400 with a clear paste-the-key-manually hint when extraction misfires
  - AntFleet H5 from `articles/repo-actions-*.md` Issue #184

**Impact:** The local dashboard is now defended against three distinct classes of operator-side failure: DNS rebinding / cross-origin browser attacks (gate), known-CVE deps (postcss/next bump), broken-environment install-time failures (gh preflight), and token-paste corner cases (auth route). Together they close the gap between "launches on my machine" and "launches reliably on every operator's machine," which is the exact friction surface the fleet keeps stubbing toes on.

---

### Theme 2: Silent-failure fixes — POSIX ERE, Slack filter, spend-cap guard

Three independent bugs that all share the same shape: they passed without erroring but silently degraded a safety check. All three are AntFleet H-class findings from Issue #184.

**Commits:**

- `b77b201` — **fix(scan): replace PCRE \s/\b with POSIX equivalents in scan.sh (#197)**
  - `skills/skill-security-scan/scan.sh` (+41, -35): all 28 patterns across HIGH/MEDIUM/LOW arrays rewritten. `\s`/`\s+` → `[[:space:]]`/`[[:space:]]+`; the single `\b` (on `git push -f`) → `($|[^[:alnum:]_-])` so `-fast`/`-force` don't false-positive; forkbomb pattern `:(){.*};:` literal-paren-escaped to `:\(\)[[:space:]]*\{.*\};[[:space:]]*:`; literal-dot escapes added to `~/.ssh`/`~/.gnupg`/`~/.aws`/`~/.config`
  - 4-line header comment names the POSIX-ERE constraint + cites Issue #184 so a future edit doesn't silently drop the guards
  - GNU grep silently extends ERE to accept PCRE escapes; BSD grep (macOS default `/bin/grep`, busybox) treats them as literal `s` and `b`. So `eval\s`, `rm\s+-rf\s+/`, `[Ii]gnore\s+(all\s+)?previous\s+instructions`, `git\s+push\s+-f\b` all silently no-op'd on every macOS operator running `./add-skill`

- `5252cf3` — **fix(messages): correct Slack bot-message filter from string "null" (#196)**
  - `.github/workflows/messages.yml` (+1, -1): a one-line bugfix that quietly changed who could trigger the bot. `BOT_ID="null"` is a literal string check that never matched — `jq -r ".bot_id // empty"` returns `""`, not `"null"`. Replaced with `[ -z "$BOT_ID" ]`. Without this, all bot's own messages were re-processed as user input
  - AntFleet H2

- `48d59fa` — **fix(admanage): validate TODAY_SPEND is numeric before awk spend-cap check (#195)**
  - `scripts/postprocess-admanage.sh` (+9): adds a `^[0-9]+(\.[0-9]+)?$` regex check on `TODAY_SPEND` before the awk comparison. Previously, a malformed AdManage API response → jq returned non-numeric → awk treated `""` as 0 → spend cap silently bypassed → ads launched
  - Fails closed with a notify and `exit 0` — the launch is blocked until spend can be verified
  - AntFleet H8

**Impact:** Same root cause across all three — code that "worked" because its safety-net silently degraded to allow-all. The scan.sh fix in particular is the broadest: every macOS operator running `./add-skill` had quietly-weaker pattern matching for 14+ HIGH/MEDIUM patterns. Cumulative `+51 / -36` lines, all in safety/filter paths.

---

### Theme 3: Catalog & community visibility — Community Skill Packs surface

Three commits, ~20 lines of additive README work that opens a new third-party-skill-pack discovery channel.

**Commits:**

- `31aa9ff` — **docs(readme): add Community Skill Packs section (#187)**
  - README (+18): new section under publishing, with the first listed pack — `aeon-skill-pack-vvvkernel` (Venice AI inference, 9 skills covering onchain/audit/growth/narrative/image-gen/monitoring). Establishes the listing PR-flow contract: own repo, clear license, per-skill `SKILL.md`, no monkey-patching, no private endpoints
  - The lightweight surface gives community packs visibility without coupling them to the core catalog's release cadence — packs install via the existing `add-skill <github-url>` flow

- `03057e2` — **docs(catalog): bump catalog to 121 skills + refresh skill.jpg graphic (#191)**
  - `skills.json`: `total` 120 → 121, `generated` 2026-05-11 → 2026-05-19
  - README (+12, -12), `generate-skills-json` (+3, -2), `assets/skill.jpg` (refreshed), `product-hunt-launch` SKILL.md description tweak

- `d0208d2` — **chore(assets): rename skill.jpg → skills.jpg to bust CDN cache (#192)**
  - The asset graphic refresh in #191 didn't propagate through downstream CDN/social-preview caches because the filename was identical; renaming forces a fresh fetch everywhere README is rendered (GitHub social card, link unfurls)

**Impact:** External skill pack listings are now a first-class README citizen — the marketplace question ("how does my pack get discovered?") has a concrete PR-able answer. Catalog stays in sync with the registry's actual count.

---

## aaronjmars/aeon-agent

One substantive commit; everything else (~30 entries) is routine cron auto-commits and scheduler state-file updates from the runtime.

### Theme: Backport — competitor-launch-radar (10th consecutive same-day-after)

**Commits:**

- `17682e3` — **feat: backport competitor-launch-radar from upstream aeon PR #183 (#53)**
  - New `skills/competitor-launch-radar/SKILL.md` (+442): verbatim port of upstream — Monday 10:00 UTC keyless PH RSS + HN Algolia scan for NEW AI-agent-framework launches outside the 9-framework cohort already tracked by `ai-framework-watch`. 7-status exit taxonomy (OK/QUIET/DRY_RUN/NO_SOURCES/PARTIAL/STATE_CORRUPT/BAD_VAR). Classifies framework/mcp/product. Suppression list of 9 cohort slugs so cohort member updates don't fire here. LRU-200 state, count-driven notify (QUIET on zero, individual 1–3, batched top-8 with overflow at 4+)
  - `aeon.yml` (+1): registered between `aixbt-pulse` and `contributor-reward` in the Upstream sync (2026-05-14) section. `enabled: false, sonnet-4-6, Monday 10:00 UTC`
  - `skills.json` (+11, -1): registry bumped 88 → 89

- ~30 cron auto-commits (`chore(cron): <skill> success`, `chore(scheduler): update cron state`, `chore(<skill>): auto-commit`) — routine fleet runtime writes from token-report, fetch-tweets, repo-pulse, star-momentum-alert, tweet-allocator, heartbeat, weekly-shiplog, repo-article, project-lens, thread-formatter, star-milestone, push-recap, repo-actions, self-improve, feature. Not analyzed in detail — these are the system breathing.

**Impact:** Closes the cohort blind spot — `ai-framework-watch` tracks momentum across a hardcoded 9-framework set (intentionally drift-resistant) and can't answer "did a new framework launch this week?" This skill does. The 10th consecutive same-day-after backport keeps the upstream/agent-fork sync cadence on its established beat (operator-scorecard May-3→4, skill-freshness May-4→5, skill-update-check May-8→9, fork-cohort May-9→10, thread-formatter May-11→12, v4-readiness May-12→13, product-hunt-launch May-15→17, fork-first-run-alert May-17→18, fork-skill-gap May-18→19, competitor-launch-radar May-19→20).

---

## aaronjmars/minitor

Three PR merges between 19:25 May-19 and 13:28 May-20 — `github-discussions` then `coingecko` then `defillama` — bumping the column count 44 → 47 in 24 hours.

### Theme: Three new column types — GitHub Discussions, CoinGecko, DeFiLlama

**Commits:**

- `5cd8b22` — **feat: github-discussions column (45th column type) (#43)** (+534, -4 across 8 files)
  - New `lib/integrations/github-discussions.ts` (+228): GraphQL-only — `api.github.com/graphql` with `repository(owner, name) { discussions(first: 50, orderBy: CREATED_AT DESC) { nodes { ... } } }`. REST doesn't expose Discussions
  - New plugin (3 files: client.tsx +189, plugin.ts +63, server.ts +44): three modes (recent / unanswered / top by upvotes), optional `GITHUB_TOKEN` (5000 vs 60 req/hr), `DiscussionsDisabledError` sentinel for repos with Discussions off, `AnsweredIndicator` only renders on Q&A category discussions
  - 3 registry edits (manifest/registry/server-registry) + README cluster row GitHub 9 → 10
  - `#7C3AED` purple accent (distinct from every other GitHub-cluster colour), `MessageSquare` icon

- `3a524a9` — **feat: CoinGecko trending + price column (46th column type) (#44)** (+649, -5 across 9 files)
  - New `lib/integrations/coingecko.ts` (+299): three keyless modes — `trending` (24h search-volume from `/api/v3/search/trending`), `top` (market-cap leaderboard with sparkline from `/api/v3/coins/markets`), `watchlist` (same markets endpoint with `ids=` filter, 50-id cap)
  - New plugin (3 files: client.tsx +242, plugin.ts +61, server.ts +31): handles two API-shape quirks — trending returns USD prices as currency-formatted strings, markets returns plain numbers; `price_change_percentage_24h` is a USD-keyed object on trending but a flat number on markets. Mapper normalises both. Empty watchlist falls back to top-by-cap so freshly-added column isn't a dead box
  - `.env.example` (+5): documents the optional `COINGECKO_DEMO_API_KEY`
  - 3 registry edits + README cluster row Apps & on-chain 4 → 5
  - `#8DC647` CoinGecko green (distinct from wallet-tx #627eea + polymarket #2D9CDB), `TrendingUp` icon

- `9bc0a1e` — **feat: DeFiLlama TVL column (47th column type) (#45)** (+518, -4 across 8 files)
  - New `lib/integrations/defillama.ts` (+234): three keyless modes via `api.llama.fi` — `top` (top protocols by TVL from `/protocols`), `gainers` (same source re-sorted by 24h TVL change desc with absolute TVL as tiebreaker so a $50M @ 20% beats a $50k @ 20%), `chains` (per-chain TVL leaderboard from `/v2/chains`). Optional category substring filter (Dexs, Lending, Liquid Staking, Restaking, CDP, Yield Aggregator)
  - New plugin (3 files: client.tsx +186, plugin.ts +57, server.ts +31): drops `tvl ≤ 0` to suppress dead protocols but keeps CEXes (Binance CEX, Coinbase Custody) — watching custody concentration is part of the use case
  - 3 registry edits + README cluster row Apps & on-chain 5 → 6
  - `#445ed0` DeFiLlama brand blue (distinct from #627eea Ethereum + #2D9CDB electric + #8DC647 green), `Layers` icon
  - Originally May-18 idea #5 was IndieHackers RSS — all IH RSS endpoints now return SPA HTML (silently deprecated); DeFiLlama replaced it as the highest-impact gap once npm/PyPI/crates (the registry trifecta from May-12/13/14) made the on-chain registry layer the obvious next move

**Impact:** Two patterns visible across the trio. (1) **Cluster completion** — GitHub Discussions closes minitor's last GitHub-monitoring gap (stars/forks/PRs/issues/releases/search/actions/backlinks/trending/discussions = all 10 covered); CoinGecko + DeFiLlama together close the on-chain cluster's "what's the price/cap/TVL?" gap that wallet-tx (transactions) and polymarket (predictions) left open. (2) **Zero-overlap pairs by design** — CoinGecko gives price + market cap, DeFiLlama gives TVL + protocol-level signal. Distinct icons (Package vs Package2 vs Box vs Layers), distinct accent colours specifically chosen to be visually distinct from each other.

---

## Developer Notes

- **New dependencies:**
  - aeon: `postcss` pinned to `^8.5.10` as a transitive override in dashboard/package.json
  - aeon: `next` bumped to `16.2.6`
  - minitor: no new top-level deps across the three new columns — everything reuses existing nanoid/zod/lucide-react/lib helpers

- **Breaking changes:**
  - None at the SDK / public-surface level. The dashboard `/api/*` middleware is additive — it only adds a Host-header check that defaults to loopback-only; non-localhost deployments need the `AEON_DASHBOARD_ALLOWED_HOSTS` or `AEON_DASHBOARD_ALLOW_ANY_HOST=1` escape hatch to keep working
  - The new `OAuth token must start with sk-ant-oat` check in `dashboard/app/api/auth/route.ts` is stricter than the prior reassembly logic — pre-existing valid tokens stay valid; malformed paste-recovered tokens now error out cleanly instead of producing a corrupted secret

- **Architecture shifts:**
  - Dashboard's `dashboard/lib/security/` is a new module path — first time a dedicated `lib/security/` exists in the dashboard tree. Pattern: pure-function gate + middleware wrapper + adjacent unit tests
  - `scan.sh` now carries an inline POSIX-ERE constraint comment naming the BSD/macOS grep quirk — future pattern edits have an explicit invariant to honour
  - minitor's column count is at 47 — the plugin/registry/server-registry/manifest 3-edit pattern stayed stable across all three new types (no migration / no schema-base changes needed for these)

- **Tech debt:** None introduced. Three TODO-style items closed (AntFleet H2/H5/H6/H8).

## What's Next

- **AntFleet Issue #184 still has 5 open Highs** (H1 v4-readiness manifest gaps, H3 undefined `FORK_DEFAULT_BRANCH` in contributor-spotlight, H4 `.bak` rollback in fleet-state, H7 `branch` field in skills.lock ignored by skill-update-check, H9 admanage-create skips `campaignId`-only ad sets) + 13 Mediums + 2 Lows. Today picked H6/H2/H5/H8 — the easiest-to-isolate four. The remaining Highs span skill-level config and state-file handling
- **`competitor-launch-radar` first run** is Monday 2026-05-25 10:00 UTC in upstream aeon (enabled there); aeon-agent's copy stays `enabled: false` per same-day-after pattern
- **Dashboard hardening trajectory** — the security/api-gate test file is the first dedicated security test in the dashboard tree. Likely follow-ups: rate-limit on `/api/secrets`, audit-log surface
- **minitor cluster status post-trio**: GitHub cluster fully covered (10/10), Apps & on-chain at 6 columns. News & web (11) and registry (3: npm/PyPI/crates) remain the biggest clusters. No new May-18 ideas remain in the active pipeline — May-19 self-improve run will need to seed fresh ones
- **PR #54 (aeon-agent) project-lens 14d → 7d rotation** opened today; not yet merged at the time of this recap
