# Repo Action Ideas — 2026-05-10

Generated from analysis of aaronjmars/aeon (284⭐, 45 forks), aaronjmars/aeon-agent (7⭐, 1 fork), and aaronjmars/minitor (8⭐, 1 fork, 39 column types).

Context: May-8 ideas (arxiv, devto, ai-framework-watch, contributor-spotlight, skill-update-check) all shipped by May-10. Open unbuilt backlog: Auto-Merge Agent PRs, Dashboard Live Feed, Webhook-to-Skill Bridge. This run focuses on the token monitoring gap, CI visibility in minitor, and the autonomous merge loop.

---

### 1. Price Threshold Alert
**Type:** Feature
**Effort:** Small (hours)
**Impact:** token-report gives a once-daily $AEON snapshot, but there's no skill that fires when something meaningful actually happens — a new ATH, a >20% drawdown in a single candle, or a pre-set operator target. The gap between "daily report" and "real-time alert" is where opportunities and risks live. This skill closes it without replacing token-report.
**How:**
1. Cron every 30 minutes. Fetch current $AEON price from the same DexScreener endpoint token-report uses (curl + WebFetch fallback per sandbox rules).
2. Read `memory/topics/price-alert-state.json` for last-known ATH and last-emitted alert timestamp. Compare current price: if new ATH → notify "New ATH: $X"; if 1h change >20% → notify "Sharp move: ±X% in 1h"; if price crosses any operator-configured `target_price` var → notify once.
3. Write updated state (new ATH, alert timestamps) back to state file. Dedup: no re-alert for the same event within 4h. Five-status taxonomy: OK / ATH / SHARP_MOVE / TARGET_HIT / ERROR.

---

### 2. GitHub Actions Status Column
**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** minitor has 39 column types covering GitHub stars/issues/PRs, news, social, and AI content — but no CI visibility. Engineering teams that already use minitor to monitor their repos have to open a second tab for GitHub Actions. A GitHub Actions column makes minitor the single dashboard for repo health, not just community health. No API key needed for public repos.
**How:**
1. New plugin `lib/columns/plugins/github-actions/` (3 files: plugin.ts, server.ts, client.tsx). Fetcher hits `GET /repos/{owner}/{repo}/actions/runs?per_page=N` (public endpoint, no auth). ConfigForm: repo (owner/repo), workflow name filter (optional), branch filter (optional), limit.
2. ItemRenderer: status icon (✅ success / ❌ failure / 🔄 in_progress / ⏩ skipped), workflow name, branch, commit SHA, duration, link to run. Color-code by conclusion (green/red/yellow). Badge for "last N runs" pass rate.
3. Three registry edits (manifest.ts, registry.ts, server-registry.ts). README: GitHub cluster count up, new row. Accent: #2088FF GitHub Actions blue. Count 39 → 40.

---

### 3. Auto-Merge Agent PRs
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Every feature/self-improve run opens a PR that sits unmerged until the operator manually approves it. With the workflows-scope PAT now in place (rotated 2026-05-06), the merge loop can close automatically. Currently aeon has 1 open PR (ai-framework-watch #164) and aeon-agent has 2 (fork-cohort #36, tweet-allocator error-marker #37) — all waiting for a human click. Eliminating that click is the last step to fully autonomous feature shipping.
**How:**
1. Skill reads its own repo's open PRs via `gh pr list --author "aeonframework" --json number,title,mergeable,statusCheckRollup`. Filter: PR opened by the agent user, all required checks passing (statusCheckRollup all SUCCESS), no requested human reviewers, no blocking labels (e.g., `hold`, `do-not-merge`).
2. For each eligible PR: `gh pr merge {number} --squash --auto` (auto waits for checks if still running). Log merge outcome. If merge fails (e.g., conflicts), flag in notification but do not force.
3. Run daily on a schedule after the last expected skill run (e.g., 18:00 UTC). Notify with a summary: "Merged N PRs: {title list}. Skipped M (checks pending / hold label)." Exit taxonomy: OK / NOTHING_TO_MERGE / PARTIAL / ERROR.

---

### 4. Fork Release Tracker
**Type:** Community
**Effort:** Small (hours)
**Impact:** fork-cohort tracks whether forks are alive (workflow runs in last 7 days). contributor-spotlight recognizes top POWER fork operators. But neither skill answers: "has any fork shipped an actual product?" — a tagged GitHub release, a versioned artifact, a real deployment. The first fork to cut a release is a milestone worth announcing publicly. It's also a signal that the platform is being treated as infrastructure, not just a toy.
**How:**
1. Weekly scan. For each fork in the cohort (fetched via `gh api repos/aaronjmars/aeon/forks --paginate`), call `gh api repos/{owner}/aeon/releases --jq '.[0]'` and check if a release exists and its `published_at` is within the last 7 days.
2. Read `memory/topics/fork-release-state.json` for previously-announced releases. For any new release not yet announced: extract tag name, release body (first 200 chars), fork owner. Format a celebration notification.
3. If no new releases this week: skip notify (QUIET exit). State file tracks announced releases by (fork, tag) tuple, capped at 50 entries. Five-status exit: OK / QUIET / NEW_RELEASE / MULTI_RELEASE / ERROR.

---

### 5. npm Trends Column
**Type:** Integration
**Effort:** Small (hours)
**Impact:** minitor's audience is predominantly TypeScript developers (aeon, minitor, and most active forks are all TypeScript repos). npm is the canonical discovery layer for that audience. The npm registry's download-stats API is fully public and keyless — no setup friction. A "trending packages" column closes the gap between what devs see on npmtrends.com and what they can surface in their own minitor dashboard. Natural fit alongside the DEV.to column (also developer-content-focused, landed May-10).
**How:**
1. New plugin `lib/columns/plugins/npm/` (3 files). Fetcher: `GET https://api.npmjs.org/downloads/point/last-week/{package}` for stats; for discovery, use `GET https://registry.npmjs.org/-/v1/search?text={query}&size=N&quality=0.5&popularity=0.8` (keyless, no auth). ConfigForm: search query (required), sort mode (popularity / quality / maintenance / combined), limit.
2. ItemRenderer: package name, description, weekly downloads (formatted with K/M suffix), version badge, npm link. Color accent: #CB3837 npm red. Icon: Package from lucide-react.
3. Three registry edits. README: Tools & Dev cluster (new row or existing), count 40 → 41.
