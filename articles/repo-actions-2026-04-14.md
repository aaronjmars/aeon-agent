# Repo Action Ideas — 2026-04-14

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 153 (aeon) | **Forks:** 17 | **Language:** TypeScript | **Open Issues:** 1
**Contributors:** aaronjmars (192), Aeon (5), aeonframework (4), github-actions[bot] (3)
**Open PRs:** [#32 skill-version-tracking](https://github.com/aaronjmars/aeon/pull/32)

Since the Apr 12 run, four of five ideas were built and merged: PR Auto-Merge (#31), Skill Version Tracking (#32, open), Email Notification (#30), and Workflow Security Audit (#29). The 3-PR guard is now unblocked — auto-merge shipped and the pipeline is clear. The repo sits at 153 stars, 17 forks, and 68+ skills, with a live MCP adaptor, Bankr Gateway, instance fleet, auto-workflow, and distribute-tokens now all merged.

Unbuilt from previous runs: **A2A Protocol Gateway** (Apr 10, Apr 12), **Dashboard Live Feed** (Apr 10), **Skill Analytics Leaderboard** (Apr 10, Apr 12), **Skill Dependency Visualizer** (Apr 12).

Today's run carries forward the two most ecosystem-critical unbuilt ideas (A2A, Live Feed) and introduces three fresh angles enabled by what just shipped: article syndication for growth, skill leaderboard for community, and contributor auto-reward to close the contribution incentive loop that distribute-tokens opened.

---

### 1. A2A Protocol Gateway — Open Aeon to Any AI Agent Framework

**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** The MCP adaptor exposes all Aeon skills to Claude Desktop and Claude Code. But MCP is Claude-specific. Google's Agent-to-Agent (A2A) protocol — now supported by OpenAI Agents SDK, LangChain, AutoGen, CrewAI, and Vertex AI — is the framework-agnostic standard for agent interoperability. An A2A gateway would let any compliant agent invoke Aeon skills by POSTing to a `/tasks/send` endpoint: a GPT-4o research pipeline calling `aeon:deep-research`, a Gemini trading bot calling `aeon:token-report`, a LangChain content scheduler calling `aeon:article`. MCP + A2A together cover the entire landscape of AI agent frameworks. With 68 skills and 17 forks, Aeon is now substantial enough to serve as a "background intelligence" module that other agents delegate to — not just a standalone cron tool. Submission to the A2A protocol directory drives discovery from a completely different audience than GitHub or Claude Desktop users.

**How:**
1. Create `a2a-server/` with a minimal TypeScript A2A-compliant server. Implement `GET /.well-known/agent.json` (agent card) advertising all skills as callable tasks with `var` string input schemas. Implement `POST /tasks/send` to receive task payloads, resolve skill by name, and invoke via `claude` CLI.
2. Implement `GET /tasks/{id}` polling endpoint so calling agents can retrieve output. Each skill invocation writes to `articles/{skill}-{date}.md` — the A2A response body wraps this content. Support SSE via `POST /tasks/sendSubscribe` for long-running skills (`deep-research`, `last30`).
3. Add `./add-a2a` install script parallel to `./add-mcp`. Update README with a "Use with any AI agent" section. Submit to the A2A protocol directory and post in LangChain/AutoGen communities for discovery.

---

### 2. Dev.to Article Syndication — Multiply Article Reach Beyond GitHub Pages

**Type:** Growth / Content
**Effort:** Small (hours)
**Impact:** Aeon generates high-quality articles daily — repo recaps, token analysis, deep research, AI trend pieces — and publishes them to GitHub Pages via the `update-gallery` skill. But GitHub Pages reaches only users who already know the project. Dev.to has 1M+ active developer readers and a free public API (`POST /api/articles`) that accepts markdown directly. A syndication skill would auto-cross-post newly written articles to dev.to with canonical URL pointing back to the GitHub Pages post, capturing organic discovery from developers searching for AI agents, GitHub Actions automation, or crypto tooling. A single well-timed post on dev.to regularly surfaces to 5K–20K readers in its topic tags. The canonical URL preserves SEO attribution. The skill is purely additive — no changes to the existing article pipeline, just a new output destination triggered by the same `notify-jsonrender` hook.

**How:**
1. Create `skills/syndicate-article/SKILL.md` that reads the most recently written article from `articles/` (by modification time), extracts the title, tags (derived from the filename prefix: `repo-article` → `ai, github-actions, automation`; `token-report` → `crypto, defi, base`), and body. Post to `https://dev.to/api/articles` using `DEVTO_API_KEY` with `published: true`, `canonical_url` pointing to the GitHub Pages post URL, and `series: "Aeon"` to group all posts. Log the dev.to URL returned in the response.
2. Add `DEVTO_API_KEY` as an optional secret in `dashboard/app/api/secrets/route.ts` (alongside `SENDGRID_API_KEY`). If key is absent, skip silently. Add `DEVTO_API_KEY` to the dashboard's Secrets panel under a "Distribution" group.
3. Schedule `syndicate-article` in `aeon.yml` to run 30 minutes after `repo-article` and `deep-research` (which produce the highest-quality content). Log the dev.to post URL to the daily log. No notification — this is a background distribution task.

---

### 3. Dashboard Live Feed — Real-Time Skill Run Visibility

**Type:** Feature / DX
**Effort:** Medium (1-2 days)
**Impact:** The dashboard shows historical analytics and per-skill output — but when skills are running right now (fleet-control spawning instances, deep-research pulling 50 sources, the MCP adaptor responding to a Claude query), the dashboard is silent until the output file lands. With auto-merge now closing the self-improve loop autonomously, and the MCP adaptor enabling externally-triggered skill runs, the gap between "what's running?" and "what can I see?" is widening. A live feed shows which skills are currently executing, elapsed time, recent completions with output preview, and a "Skills running: N" badge in the header. This transforms the dashboard from a skill gallery into an operational control plane — and gives new users immediate confirmation that their setup is working without needing to open GitHub Actions logs.

**How:**
1. Create `dashboard/components/live-feed/` component that polls `dashboard/outputs/` every 30 seconds for JSON files. Add `./notify-running "skill-name"` script that writes a running-state stub to `dashboard/outputs/{skill}-running.json` (`{status: "running", skill, started_at}`). The scheduler calls this at invocation start; `./notify` overwrites it on completion.
2. The live feed distinguishes "running" stubs (amber dot, elapsed time counter, last log line pulled from `memory/logs/{today}.md`) from "completed" entries (green dot, duration, output preview). Display the last 10 events as a sidebar panel. Add a "Skills running: N" badge to the dashboard header.
3. Wire the scheduler to call `./notify-running` before each skill invocation and update `./notify` to write a `{status: "done", ...}` completion stub. For MCP-triggered runs, pass a `$AEON_CALLER` env var through the MCP server and display the invoking agent name in the feed entry.

---

### 4. Skill Analytics Leaderboard — Surface the Most-Enabled Skills Across All Forks

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** Aeon has 17 forks — each running a subset of the 68 skills. Fork-fleet already inventories active forks weekly, but there's no aggregated view of which skills are most commonly enabled across the fleet. A leaderboard answers three questions: which skills do operators actually use (adoption signal), which skills are enabled nowhere (documentation gap candidates), and which skills are trending up or down week-over-week. This data benefits three audiences: new users (see which skills others find valuable), skill builders (see adoption of what they built), and the project (a "Community Picks" section in the README). With 17 forks, the sample is small but real — and it grows with each new fork.

**How:**
1. Create `skills/skill-leaderboard/SKILL.md` that fetches all active forks via `gh api repos/aaronjmars/aeon/forks` (filtered to `pushed_at` within 30 days), reads each fork's `aeon.yml` via `gh api repos/{fork}/contents/aeon.yml`, extracts all skill entries where `enabled: true`, and aggregates counts across forks into a ranked list.
2. Output a table: skill name, enable count, percentage of forks, category, and trend column (compare to last week's leaderboard article if present in `articles/`). Flag consensus skills (>50% of forks) and zero-adoption skills (candidates for docs improvement). Write to `articles/skill-leaderboard-{date}.md` and publish to GitHub Pages gallery.
3. Add a `## Community Picks` section to the README that links to the latest leaderboard. Schedule weekly (Mondays) in `aeon.yml`. Send notification with top 5 skills and any week-over-week movement.

---

### 5. Contributor Auto-Reward — Close the Incentive Loop with Bankr Tokens

**Type:** Integration
**Effort:** Small (hours)
**Impact:** The `distribute-tokens` skill can send AEON tokens to contributors via Bankr — but it's a manual skill requiring explicit invocation with target usernames. With 17 forks and occasional external issues/PRs, the project now has a real contributor base that could be recognized automatically. Auto-Reward hooks into GitHub's merge events: when a PR is merged by anyone *other than* aaronjmars or aeonframework (i.e., a community contributor), the skill sends a small fixed AEON token reward to their on-chain address (looked up via Bankr's username-to-address API). This creates a positive flywheel — contributors know they'll be recognized automatically, lowering the bar to contribute. It also makes the AEON token economically meaningful to the community, not just to its creator.

**How:**
1. Create `skills/contributor-reward/SKILL.md` that lists recently merged PRs via `gh api repos/aaronjmars/aeon/pulls --state closed` (filtered to `merged_at` within last 24 hours), extracts the PR author login, and skips `aaronjmars`, `aeonframework`, and `github-actions[bot]`. For each qualifying contributor, resolve their Bankr address via `gh api` or a direct Bankr lookup, and send a fixed reward amount (configurable via `REWARD_AMOUNT_AEON`, default: 100 AEON) using the distribute-tokens skill logic.
2. Add deduplication: before sending, check `memory/logs/` for the past 7 days to see if this PR author was already rewarded for this PR number. Log each reward in the daily log with PR number, contributor username, amount, and tx hash. If Bankr lookup fails (user has no linked address), log as skipped — no error, no notification.
3. Schedule daily in `aeon.yml` (after `repo-pulse`). Send notification only when a reward is actually sent: "Rewarded @{username} {amount} AEON for contributing PR #{number}." Add `REWARD_AMOUNT_AEON` as an optional env var with a dashboard Secrets panel entry alongside distribute-tokens config.

---

## Summary

These 5 ideas address Aeon's post-auto-merge state: the pipeline is clear, the fleet is functional, the MCP adaptor is live, and the article engine is running daily. A2A Gateway is the highest-ROI ecosystem play still outstanding — every week it stays unbuilt is another week Aeon is invisible to LangChain, AutoGen, and OpenAI Agents users. Dev.to Syndication is the cheapest path to 10× article reach with a one-afternoon implementation. Dashboard Live Feed makes the increasingly complex multi-agent, multi-trigger operation legible without GitHub Actions access. Skill Analytics Leaderboard turns the 17-fork fleet into a community discovery signal. Contributor Auto-Reward closes the incentive loop that distribute-tokens opened — making AEON tokens flow automatically to anyone who improves the project. All five are scoped for autonomous `feature` skill implementation with clear inputs, outputs, and no external approvals required.
