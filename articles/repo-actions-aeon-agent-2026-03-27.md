# Repo Action Ideas — aeon-agent — 2026-03-27

**Repo:** [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 4 | **Forks:** 0 | **Language:** TypeScript | **Open Issues:** 0
**Contributors:** github-actions[bot] (32), aaronjmars (15), Aeon (4)

This is the operational instance of the Aeon framework — the private agent repo that runs 12 enabled skills daily on GitHub Actions, hosts the Next.js dashboard, manages memory/logs, and generates articles. 54+ commits in 14 days, mostly automated skill runs. The dashboard (Next.js + TypeScript) serves as the control plane for skill management, config sync, and output viewing.

## Ecosystem Context (Late March 2026)

- **Next.js 16.2 Agent DevTools** — experimental CLI (`next-browser`) exposes browser-level data and a debugging panel for AI agent calls, streaming responses, tool invocations, and token usage. Enabled via `experimental.agentDevTools: true` in `next.config.ts`. ([source](https://nextjs.org/blog/next-16-2-ai))
- **AI Observability Tools** — Braintrust, Arize Phoenix, Langfuse, and Fiddler offer real-time dashboards for token usage, latency, error rates, and cost tracking per feature/user cohort. Standard patterns emerging for agent monitoring. ([source](https://www.braintrust.dev/articles/best-ai-observability-tools-2026))
- **GitHub Agentic Workflows** — plain Markdown workflow files in `.github/workflows/`, supporting Claude Code as an engine. YAML frontmatter defines permissions/triggers, Markdown body has natural-language instructions. ([source](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/))
- **hackerbot-claw CI/CD Incident** (Feb 2026) — autonomous Claude-powered agent scanned public repos for misconfigured GitHub Actions, achieved RCE in high-profile projects. Highlights need for CI/CD security hardening. ([source](https://windowsforum.com/threads/ai-agent-attack-on-github-actions-hackerbot-claw-exposes-ci-cd-misconfig-risks.404782/))
- **Claude Agent SDK** — renamed from Code SDK, Python + TypeScript. Powers the same agent loop as Claude Code but programmable. Skills follow the open Agent Skills standard across 11 compatible tools. ([source](https://platform.claude.com/docs/en/agent-sdk/overview))

Previous repo-actions run today covered the upstream `aaronjmars/aeon` repo (skill evals, awesome-continuous-ai listing, agentic workflow templates, SkillsMP publish, A/B testing). The following 5 ideas target the **aeon-agent operational instance** specifically.

---

### 1. Skill Run Cost Tracker — Per-Skill Token Spend in Dashboard

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** The aeon-agent instance runs 12+ skills daily on claude-opus-4-6, but there's no visibility into which skills consume the most tokens. The workflow already captures `input_tokens`, `output_tokens`, `cache_read`, and `cache_creation` per run and writes them to `$GITHUB_STEP_SUMMARY`. This data exists but isn't aggregated or visualized. Building a cost tracker would show daily/weekly token spend per skill, identify expensive skills (repo-article and feature likely dominate), and enable informed decisions about which skills to move to cheaper models (sonnet/haiku). With Opus at ~$15/M input tokens, a single feature run can cost $2-5 — tracking this prevents bill shock.

**How:**
1. Add a post-run step in `aeon.yml` that appends token usage to a `data/token-usage.jsonl` file (one JSON line per run: `{skill, model, input_tokens, output_tokens, cache_read, cache_creation, timestamp}`).
2. Add a `/api/token-usage` endpoint in the dashboard that reads the JSONL and returns aggregated stats (daily totals, per-skill breakdown, cost estimates at published API rates).
3. Build a "Cost" tab in the dashboard showing a stacked bar chart of daily spend by skill, a table of per-skill averages, and a "savings simulator" showing projected cost if a skill were switched to sonnet or haiku.

---

### 2. Workflow Security Audit — Harden Against CI/CD Agent Attacks

**Type:** Security
**Effort:** Small (hours)
**Impact:** The hackerbot-claw incident (Feb 2026) showed that autonomous agents can exploit misconfigured GitHub Actions workflows — scanning for overly permissive tokens, write access in pull_request triggers, and secret exfiltration. The aeon-agent instance has broad permissions (`contents: write`, `pull-requests: write`, `actions: write`), uses `secrets.GH_GLOBAL` for cross-repo access, and runs arbitrary Claude-generated commands with shell access. A security audit would identify specific hardening steps: pin action versions to SHAs (not tags), restrict allowed tools list, add network egress controls, validate that `./notify` only calls known endpoints, and ensure `GH_GLOBAL` has minimum required scopes. This is defensive — the repo is public, so attackers can read the workflow.

**How:**
1. Create `skills/security-audit/SKILL.md` that reads all `.github/workflows/*.yml`, checks for known anti-patterns (unpinned actions, over-broad permissions, secret exposure in logs, missing `if` guards), and produces a findings report with severity ratings.
2. Apply immediate fixes: pin `actions/checkout@v5` and `actions/setup-node@v5` to specific commit SHAs, add `--deny-network` or URL allowlist to the Claude Code `--allowedTools` flag, restrict `GH_GLOBAL` permissions documentation.
3. Add a `SECURITY.md` documenting the threat model: what the agent can access, what it can't, and how secrets are scoped.

---

### 3. Dashboard Live Feed — Real-Time Skill Output Streaming

**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** The dashboard currently shows skill outputs after they're committed to the repo — meaning there's a delay of minutes between a skill finishing and its output appearing. Next.js 16.2's Agent DevTools and the AI SDK both support real-time streaming of agent responses. Adding a live feed would let users watch skill runs as they happen: token-report pulling prices, repo-article writing paragraphs, feature building code. This transforms the dashboard from a static log viewer into a live agent control room. It also enables faster debugging — if a skill is stuck or producing bad output, you see it immediately instead of after the commit.

**How:**
1. Add a GitHub Actions workflow annotation step that streams Claude's output to a workflow artifact in real-time (using `--output-format stream-json` in the Claude CLI call).
2. Build a `/api/live-feed` endpoint that polls the GitHub Actions API for in-progress runs, fetches their live logs, and serves them as Server-Sent Events.
3. Add a "Live" tab in the dashboard with an auto-scrolling terminal-style view showing the current skill's output, token counter, and elapsed time. Show a green/amber/red status indicator per active run.

---

### 4. Skill Dependency Chain — Compose Multi-Skill Pipelines in Config

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** CLAUDE.md describes skill composition ("a skill can reuse another skill by reading its file"), but this only works within a single Claude session. There's no way to define in `aeon.yml` that `repo-actions` should run before `feature`, or that `push-recap` should trigger after any other skill commits. Currently the scheduler treats each skill as independent — the only ordering is by cron time, with no data passing between runs. Adding dependency chains would enable pipelines like: `token-report` -> `write-tweet` (tweet about today's price), or `repo-actions` -> `feature` (build the top idea immediately). This turns Aeon from a collection of independent skills into a composable automation platform.

**How:**
1. Add a `depends_on` field to `aeon.yml` skill config: `feature: { enabled: true, schedule: "30 16 * * *", depends_on: "repo-actions" }`. The scheduler checks that the dependency ran successfully today before dispatching.
2. Add an `output` mechanism: after a skill runs, save its key output to `data/outputs/{skill}-{date}.json` (e.g., the top idea from repo-actions). The dependent skill reads this as input context.
3. Update the dashboard to show dependency arrows between skills in the schedule view, and warn when a dependency hasn't run yet.

---

### 5. Memory Search API — Query Agent Memory from the Dashboard

**Type:** Feature
**Effort:** Small (hours)
**Impact:** The agent's memory system (`memory/MEMORY.md`, `memory/topics/`, `memory/logs/`) is append-heavy — 27 days of daily logs across multiple skills, topic files, and the index. When the user asks Aeon a question via Telegram, it reads these files linearly, burning context window on irrelevant entries. The dashboard has no memory view at all. Adding a searchable memory API would let users browse and search memory from the dashboard (find all mentions of a token, see when a skill was first built, trace a decision), and would let skills do targeted memory lookups instead of reading entire files. This also enables a "memory health" view — showing memory size, staleness, and topics that haven't been updated.

**How:**
1. Add a `/api/memory` endpoint that indexes all files in `memory/` (MEMORY.md, topics/*.md, logs/*.md), supports full-text search with keyword highlighting, and returns results sorted by relevance/date.
2. Build a "Memory" tab in the dashboard with a search bar, timeline view of log entries, and a topic explorer showing each topic file with its last-modified date.
3. Add a `memory-stats` section to the heartbeat skill: total entries, oldest/newest, topics by size, and a "stale memory" warning for topic files not updated in 7+ days.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-27, targeting the aeon-agent operational instance. Ecosystem data from web searches performed same day.*

Sources:
- [Next.js 16.2 AI Improvements](https://nextjs.org/blog/next-16-2-ai)
- [AI Observability Tools 2026](https://www.braintrust.dev/articles/best-ai-observability-tools-2026)
- [GitHub Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)
- [hackerbot-claw CI/CD Incident](https://windowsforum.com/threads/ai-agent-attack-on-github-actions-hackerbot-claw-exposes-ci-cd-misconfig-risks.404782/)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Continuous AI in Practice (GitHub Blog)](https://github.blog/ai-and-ml/generative-ai/continuous-ai-in-practice-what-developers-can-automate-today-with-agentic-ci/)
