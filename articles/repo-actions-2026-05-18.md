# Repo Action Ideas — 2026-05-18

*Generated from analysis of aaronjmars/aeon (370⭐, 78 forks), aaronjmars/aeon-agent (9⭐), aaronjmars/minitor (9⭐). Today's context: AEON token at $7.48M FDV (+1565% 7d), 14 new forks in 24h, May-16 idea pipeline fully consumed.*

---

### 1. Backport fork-skill-gap to aeon-agent
**Type:** Feature (backport)
**Effort:** Small (hours)
**Impact:** Upstream aeon PR #176 (fork-skill-gap) merged to main — per-fork upstream-skill-adoption gap report now exists in aeon but not aeon-agent. Continues the daily same-day-after backport cadence (operator-scorecard May-3→4, skill-freshness May-4→5, fork-cohort May-9→10, v4-readiness May-12→13, product-hunt-launch May-15→17, fork-first-run-alert May-17→18). Closes the fork-intelligence layer for aeon-agent operators who want to know which upstream skills they haven't adopted.
**How:**
1. Copy `skills/fork-skill-gap/SKILL.md` verbatim from upstream aeon main branch.
2. Register in `aeon.yml` under the Upstream sync 2026-05-14 section: Sunday 21:00 UTC, enabled:false, sonnet-4-6 — slots 1h after contributor-spotlight and 1.5h after fork-release-tracker.
3. Bump `skills.json` 88→89.

---

### 2. Fix scan.sh empty-array crash on macOS Bash 3.2 (Issue #182)
**Type:** Bug fix
**Effort:** Small (hours)
**Impact:** With `set -euo pipefail`, Bash 3.2 (macOS default) treats `"${array[@]}"` as unbound when the array has zero elements — causing `add-skill` to report `BLOCKED: has security issues` even when the scan passes cleanly. Confirmed reproduction: `./add-skill powerloom/aeon-skills powerloom-bds` fails despite a clean `[PASS]` scan result. With 78+ forks and 14 new in 24h, operators hitting a broken `add-skill` on first use is a silent churn driver.
**How:**
1. Locate the `warnings` array expansion at `skills/skill-security-scan/scan.sh` lines 280-289.
2. Add a `[[ ${#warnings[@]} -gt 0 ]]` length guard before the `"${warnings[@]}"` expansion so the block is skipped on empty arrays.
3. Open a PR to aeon main (branch `fix/scan-empty-array-bash32`); include a comment noting the Bash 3.2 constraint so the guard isn't accidentally removed.

---

### 3. Extend gateway.provider to support custom API base URLs (Issue #181)
**Type:** Feature / Integration
**Effort:** Medium (1-2 days)
**Impact:** APAC operators (MiniMax at `api.minimaxi.com/anthropic/v1/messages`) and cost-sensitive operators (Together.ai, Groq, etc.) are blocked from using aeon because Claude Code validates model names locally before any API call, rejecting non-Anthropic model IDs. The `gateway.provider` block already handles OpenRouter routing; adding optional `baseUrl` and `authHeader` fields unlocks the Anthropic-compatible third-party ecosystem. Directly addresses Issue #181 with a documented MiniMax example.
**How:**
1. Add optional `baseUrl` (string) and `authHeader` (string, e.g. `"x-api-key"`) fields to the `gateway.provider` schema in `CLAUDE.md` and document the config pattern.
2. Update `.github/workflows/aeon.yml` so when `gateway.baseUrl` is set, the workflow exports `ANTHROPIC_BASE_URL` from that value before launching Claude Code.
3. Add a MiniMax configuration example to the gateway docs section as the canonical reference, covering the `x-api-key` vs `Authorization: Bearer` auth-header difference.

---

### 4. CoinGecko trending + price column for minitor (46th column type)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** No crypto price or trending signal exists in minitor today. Based on skill-leaderboard data, token-movers, token-pick, and defi-monitor are among the most-adopted skills in the active fork cohort — signaling that ~50% of aeon operators are crypto-native. A keyless CoinGecko trending column fills the most obvious monitoring gap for this audience. Three modes: `trending` (keyless `GET /api/v3/search/trending`), `top` (keyless `/coins/markets` by market cap), `watchlist` (comma-separated coin IDs with optional `COINGECKO_DEMO_API_KEY` for higher rate limits). Pairs naturally with wallet-tx column already in the manifest.
**How:**
1. Build `lib/integrations/coingecko.ts` with fetch functions for the three modes; handle rate-limit degradation gracefully (trending + top are keyless, watchlist falls back to top-by-cap on key absence).
2. Create `lib/columns/plugins/coingecko/{plugin.ts, server.ts, client.tsx}` following the crates/pypi/npm plugin pattern; `#8DC647` CoinGecko green accent, `TrendingUp` icon, `{symbol}` + price + 24h % change row format.
3. Register in `manifest.ts`, `registry.ts`, `server-registry.ts`; bump README News & web cluster 10→11 and count 45→46.

---

### 5. IndieHackers RSS column for minitor (47th column type)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** indiehackers.com has a public RSS feed (`indiehackers.com/feed`) covering product milestones, revenue reveals, and maker stories. Fills the bootstrapper/indie gap between ProductHunt (big launches, already a column) and Hacker News (technical discussion, already a column) — IndieHackers targets the founder-as-solo-operator segment that mirrors aeon's own operator profile. Keyless. Completes the "startup launch signal" trifecta for operators monitoring product launches across all three platforms.
**How:**
1. Build `lib/integrations/indiehackers.ts` using the existing RSS fetch pattern (similar to producthunt.ts / rss plugin); two modes: `recent` (latest feed items by publishedAt) and `top` (most-commented in the fetch window, sort client-side on `comments` count).
2. Create `lib/columns/plugins/indiehackers/{plugin.ts, server.ts, client.tsx}`; `#0FA36D` IH green accent, `Seedling` icon (distinct from CoinGecko `TrendingUp` and ProductHunt `Rocket`).
3. Register in `manifest.ts`, `registry.ts`, `server-registry.ts`; bump README News & web cluster 11→12 and count 46→47.

---

*Sources: gh api repos/aaronjmars/{aeon,aeon-agent,minitor}, open issues #181 #182, memory/MEMORY.md skills-built + repo-actions ideas pipeline, skill-leaderboard log 2026-05-17.*
