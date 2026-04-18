# Repo Action Ideas — 2026-04-18 (Run 2)

**Repos:** aaronjmars/aeon (189 stars, 28 forks, 92 skills, 2 open PRs) | aaronjmars/aeon-agent

**Context:** MIT License landed today, opening the repo to formal contributions. The A2A gateway (Apr 15) and MCP adaptor (Apr 10) are live infrastructure with zero observed external integrations — adoption is the outstanding gap. 28 forks active, one proven upstream backport (miroshark, Apr 17). Token +901% 30d. Run 1 today covered Contributor Auto-Reward, Dashboard Live Feed, A2A Client Examples, Public Status Page, and Smithery Listing. This run focuses on the next tier: memory exposure, event-driven architecture, ecosystem depth, and operator DX.

---

### 1. Memory Search API
**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** Agent memory lives in `memory/` as markdown files — queryable only by reading raw text. The MCP adaptor, A2A gateway, and the 28 fork operators who built their own tooling all need programmatic access to what the agent knows: recent logs, topic notes, tracked tokens, watched repos. A REST API at `/api/memory/search?q=` in the Next.js dashboard turns Aeon's memory into a queryable knowledge base for any tool in the stack. It's the missing bridge between the agent's private state and the public interfaces already shipping (MCP, A2A, dashboard).
**How:**
1. Add a `/api/memory/search` Next.js route that reads `memory/MEMORY.md` + all `memory/topics/*.md` files and returns matching excerpts scored by keyword relevance (simple TF-IDF or substring match is sufficient for file-scale data). Add a `/api/memory/logs?date=` route that returns the parsed log for a given day.
2. Add a `/api/memory/topics` route listing all topic files with last-modified timestamps, and `/api/memory/topics/:slug` to return the full content of a topic file.
3. Expose these routes in the MCP adaptor as `aeon-memory-search`, `aeon-memory-log`, and `aeon-memory-topic` tools — so Claude Code operators can ask "what has Aeon been tracking about crypto?" and get a live answer from the running instance.

---

### 2. Webhook-to-Skill Bridge
**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** Every reactive skill (pr-review, issue-triage, github-monitor) runs on a cron schedule — a PR opened at 9:01 AM waits until 9 AM the next day to get reviewed. GitHub webhooks deliver events in seconds. A webhook receiver on the dashboard that maps incoming events (PR opened → `pr-review`, issue labeled `bug` → `issue-triage`, push to main → `push-recap`) and triggers the corresponding GitHub Actions workflow_dispatch would cut skill latency from hours to seconds for every event-driven use case. This is the infrastructure that turns Aeon from a "daily cron agent" into a "real-time reactive agent."
**How:**
1. Add a `/api/webhook/github` POST endpoint to the Next.js dashboard that validates the `X-Hub-Signature-256` header (using `GITHUB_WEBHOOK_SECRET`) and parses the event type and payload.
2. Build an event→skill routing table (configurable in `aeon.yml` under a new `webhooks:` section) that maps `pull_request.opened` → `pr-review`, `issues.labeled` → `issue-triage`, etc. The handler calls `gh workflow run` with the appropriate skill and var.
3. Add a "Webhooks" card to the dashboard Settings panel showing the webhook URL, a one-click copy button, and a log of the last 10 webhook events received — so operators can verify the bridge is wired up correctly.

---

### 3. Fork Contributor Leaderboard
**Type:** Community
**Effort:** Small (hours)
**Impact:** The fork fleet has 28 forks and one proven upstream backport. The tweet-allocator rewards social mentions with $AEON, but code contributors get nothing — no recognition, no economic signal that upstream values their work. A weekly `fork-contributor-leaderboard` skill ranks fork operators by commit activity (commits since fork, PRs opened upstream, new skills added) and distributes $AEON to the top 3, mirroring the tweet-allocator mechanics but targeting developers. This closes the feedback loop: fork → contribute → get paid → fork more. It's the contributor version of the community growth flywheel that the tweet-allocator already runs for social.
**How:**
1. Create `skills/fork-contributor-leaderboard/SKILL.md` as a weekly skill (Sunday, after `fork-fleet`). It reads the fork list from `gh api repos/aaronjmars/aeon/forks`, queries each fork's commits since its creation date (`gh api repos/{fork}/commits?since={fork.created_at}`), and counts upstream PR contributions via `gh api repos/aaronjmars/aeon/pulls?state=all` filtered by fork-owner authors.
2. Score each fork operator: +3 per commit since fork, +10 per merged upstream PR, +5 per new skill file detected in their `skills/` directory. Rank the top 10. Resolve wallet for top 3 via `.bankr-cache/` and write a reward plan to `.pending-distribute/fork-leaderboard-<date>.json`.
3. Send a notification with the weekly leaderboard table and reward plan — publicly naming contributors drives social proof and encourages the next fork operator to contribute upstream.

---

### 4. Skill Template Library
**Type:** DX / Community
**Effort:** Small (hours)
**Impact:** 28 operators have forked Aeon. The most common next step after forking is "now I want a skill that monitors X" — and right now that means reading an existing SKILL.md, copying its structure, and figuring out the right prefetch/postprocess patterns from scratch. A `templates/` directory with 6 pre-built skill starters (crypto tracker, research digest, code reviewer, social monitor, deploy watcher, community manager) reduces activation time from "30-minute exploration" to "copy-paste and edit two fields." Each template is a complete, runnable SKILL.md with secrets listed, sandbox fallbacks noted, and an `add-skill` install command at the top.
**How:**
1. Create `templates/` with six subdirectories, each containing a `SKILL.md` with `[REPLACE: ...]` tokens for the operator-specific parts (topic, schedule, var). Include a `TEMPLATE.md` at the root that explains the template format and lists available templates with one-line descriptions.
2. Add a `./add-template <name>` CLI command (or extend `./add-skill`) that copies the chosen template into `skills/<chosen-name>/`, replaces the `[REPLACE: ...]` tokens interactively, and registers the skill in `aeon.yml`.
3. Link the templates directory from the README under Quick Start: "Need a skill for X? Start from a template." — gives every fork operator a discovery path the first time they look for customization options.

---

### 5. Skill Run Analytics Dashboard Widget
**Type:** Feature
**Effort:** Small (hours)
**Impact:** The cost-report skill generates weekly token-usage breakdowns, but operators have no real-time view inside the dashboard of how their skills are performing. A dashboard analytics widget — showing runs per skill (last 14 days), success rate, and estimated cost from `token-usage.csv` — surfaces degradation before the weekly report catches it and gives operators the data they need to optimize their schedule (disable expensive skills, downgrade model, add caching). All the raw data already exists in `token-usage.csv` and `memory/logs/`; this is a rendering layer, not new instrumentation.
**How:**
1. Add a `/api/analytics` Next.js route that reads `token-usage.csv`, aggregates by skill name and date (last 14 days), and returns per-skill stats: run count, total tokens, estimated cost (Opus/Sonnet/Haiku pricing from cost-report skill), and a 14-day sparkline array.
2. Add an "Analytics" tab to the dashboard (alongside the existing Feed, Skills, and Secrets tabs) that renders a table of skills sorted by cost descending, with color-coded success rate indicators (green ≥90%, yellow 70–89%, red <70%) derived from `memory/logs/` heartbeat entries.
3. Add a "Cost this week" summary card to the dashboard header — always-visible, single number, links to the Analytics tab. Makes cost visible without requiring a separate weekly report run.
