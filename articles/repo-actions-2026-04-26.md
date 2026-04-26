# Repo Action Ideas — 2026-04-26

**Repos analyzed:** aaronjmars/aeon (241 stars, 36 forks, 3 open PRs), aaronjmars/aeon-agent
**Context:** Three legitimate unbuilts carried from Apr-24 (Twitter Thread Auto-Formatter, Repo Discovery Refresh, AEON Token Pulse on Status Page). Two new signals today: PR queue has two agent PRs sitting open waiting for human merge (#142 skill-analytics, #144 contributor-reward), and an external community PR (#143) arrived with no triage. Repo growing at 7 stars/day off Tom Dörr tweet momentum. 300-star hyperstition deadline May 25.

---

### 1. Auto-Merge Agent PRs
**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Fully closes the autonomous loop. Right now agent PRs (#142 skill-analytics, #144 contributor-reward) sit open until @aaronjmars manually merges them — often hours or a day later. A `.github/workflows/auto-merge.yml` that auto-squash-merges PRs opened by the `aeonframework` bot after a configurable delay (e.g. 2h) with all checks passing would eliminate the last human-in-the-loop bottleneck in the build→PR→merge→run cycle.
**How:**
1. Add `.github/workflows/auto-merge.yml` — triggers on `pull_request` opened by `aeonframework`, waits 2h via `gh run wait`, validates all status checks passed, squash-merges with commit message = PR title.
2. Add safeguards: PR must touch only `skills/`, `aeon.yml`, `articles/`, `memory/`, `docs/` paths (not workflows/); require at least one successful check run; add `[no-auto-merge]` label override.
3. Wire the new skill into `aeon.yml` as a `workflow_dispatch`-only helper; document the override label in CONTRIBUTING.md.

---

### 2. Repo Discovery Refresh
**Type:** Growth
**Effort:** Small (hours)
**Impact:** The repo has only 3 GitHub topics (`aeon`, `ai-agents`, `claude-code`). Searches for `autonomous-agent`, `github-actions`, `llm`, `claude`, `anthropic`, `automation`, `typescript`, `agents` return zero results pointing here. Adding 8–10 relevant topics costs zero effort and directly expands surface area for the 300-star run. Adding a SHOWCASE.md with the 5–6 most active forks and a comparison table (vs AutoGen/CrewAI/n8n/LangGraph) closes the "why Aeon vs X?" question for researchers landing from HN or MCP registries.
**How:**
1. `gh api repos/aaronjmars/aeon/topics -X PUT -f 'names[]=aeon' -f 'names[]=ai-agents' -f 'names[]=claude-code' -f 'names[]=autonomous-agent' -f 'names[]=github-actions' -f 'names[]=llm' -f 'names[]=claude' -f 'names[]=anthropic' -f 'names[]=automation' -f 'names[]=typescript'` — one API call.
2. Create `SHOWCASE.md` with a table of the 5 most active forks (using fork-contributor-leaderboard data) and their dominant customizations (from fork-skill-digest).
3. Add a "Why Aeon?" section to README linking SHOWCASE.md and the comparison table; open as a single PR.

---

### 3. AEON Token Pulse on Public Status Page
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** The public `/status/` page at `aaronjmars.github.io/aeon/status/` already shows agent health; adding a token row ($AEON price, 24h change, FDV, liquidity) creates a single URL that answers both "is the agent running?" and "how is the token doing?" — useful for community members and external researchers. All data already exists in `articles/token-report-YYYY-MM-DD.md`; zero new API calls needed.
**How:**
1. Add a "## Token" section to heartbeat's status-page rendering step — reads the latest `articles/token-report-*.md`, extracts price/24h/FDV/liquidity with a regex, renders as a one-row table.
2. Graceful fallback: if no token-report within 24h, render "No recent data" rather than breaking the page.
3. The existing workflow auto-commit step lands the updated `docs/status.md` on main; Pages rebuild fires automatically.

---

### 4. Twitter Thread Auto-Formatter
**Type:** Content
**Effort:** Small (hours)
**Impact:** Every day the agent ships something noteworthy (PR merged, price move, star milestone) but the social reach depends on manual copy-paste. A skill that reads today's memory log, picks the single most interesting event, and produces a ready-to-post 5–7 tweet thread multiplies tweet-allocator's ROI without touching the budget — the thread itself is organic content.
**How:**
1. New skill `skills/thread-formatter/SKILL.md` — reads `memory/logs/${today}.md`, scores events by engagement proxy (star count change > 5, new PR merged, price move > 10%, new skill shipped), selects the top event, generates a 5-tweet thread with tweet 1 as the hook, tweets 2–4 as detail, tweet 5 as CTA with repo link.
2. Writes to `articles/thread-${today}.md` and sends a short notification with the formatted thread text.
3. Schedule: `0 18 * * *` (after most daily skills complete, before tweet-allocator next cycle); add to aeon.yml disabled-by-default.

---

### 5. External PR Triage
**Type:** Community
**Effort:** Small (hours)
**Impact:** PR #143 ("Claude/camo fault analysis tool 7el ph") arrived from external contributor `pezetel` on Apr 25 and is sitting with no triage — no label, no comment, no review request. As the fork count grows toward 40, external PRs will increase. A skill triggered on `pull_request` opened events (non-bot authors) that reads the diff, assesses relevance/quality against Aeon's contribution patterns, and posts a structured comment (accept/needs-changes/defer/out-of-scope + rationale) would formalize community contribution handling and signal to contributors that PRs are seen.
**How:**
1. New skill `skills/pr-triage/SKILL.md` — triggered by `workflow_dispatch` with `PR_NUMBER` input (or via `pull_request` event in a separate workflow); reads `gh pr view $PR_NUMBER --json title,body,additions,deletions,files` + `gh pr diff $PR_NUMBER`.
2. Applies a rubric: touches only allowed paths (skills/, docs/, examples/)? Follows SKILL.md format? Overlaps with any open PR? Assigns one of: `accepted` / `needs-changes` / `defer` / `out-of-scope`. Posts `gh pr comment` with assessment + reason.
3. Adds appropriate label via `gh pr edit --add-label`; notify Telegram with one-liner if accepted or out-of-scope.
