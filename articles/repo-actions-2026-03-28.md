# Repo Action Ideas — 2026-03-28

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 131 (aeon) / 4 (aeon-agent) | **Forks:** 15 / 0 | **Language:** TypeScript | **Open Issues:** 2 / 2
**Contributors:** aaronjmars (132 commits), github-actions[bot] (36), Aeon (10)

Aeon is an autonomous background agent on GitHub Actions powered by Claude Code — 47 skills across research, dev tooling, crypto, and productivity. Since the last repo-actions run (Mar 27), the repo gained 6 stars (125→131), shipped 2 more repo-articles, and the agent now runs 12+ skills daily. Two open PRs on aeon-agent: heartbeat timing fix (#1) and per-skill model overrides (#2, ~45% cost savings). The skills marketplace ecosystem has exploded — SkillsMP at 66,500+ skills, SkillHub at 7,000+, and the universal SKILL.md format now works across 11 tools.

## Ecosystem Context (March 28, 2026)

Key developments informing today's ideas:

- **OpenClaw at 250K+ stars** — the fastest-growing open-source project in history, focused on real-time local agents with continuous background tasks. Aeon's differentiator is serverless (GitHub Actions) + background-first design. The gap: OpenClaw has a massive plugin ecosystem; Aeon has better CI/CD native integration but no plugin discovery. ([source](https://skywork.ai/skypage/en/openclaw-ai-agents-automation/2036708876028346368))
- **Claude Code at 5.2M VS Code installs** — leading OpenAI Codex (4.9M) in the VS Code marketplace. Claude Code is Aeon's runtime; this install base is Aeon's addressable market. ([source](https://visualstudiomagazine.com/articles/2026/02/26/claude-code-edges-openais-codex-in-vs-codes-agentic-ai-marketplace-leaderboard.aspx))
- **Multi-provider strategies trending** — OpenRouter and LiteLLM let agents route between providers for cost/latency. Aeon currently locks to one Claude model per skill; multi-provider would unlock Gemini for long-context tasks, DeepSeek for cheap bulk work, and Claude for creative/reasoning. ([source](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks))
- **Trigger.dev for AI agent infra** — production-ready background jobs with tool calling, retries, observability, and human-in-the-loop. An alternative runtime to GitHub Actions that could run Aeon skills with lower latency and real-time streaming. ([source](https://trigger.dev/))
- **Agent market at $7.84B, projected $52.6B by 2030** — 46.3% CAGR. Gartner predicts 40% of enterprise apps will feature task-specific AI agents by end of 2026. ([source](https://aimultiple.com/agentic-frameworks))

Previous runs (Mar 25, Mar 27) covered: skill evals, awesome-continuous-ai listing, agentic workflow templates, SkillsMP publish, A/B testing, cost tracker, security audit, live feed, dependency chains, memory search, marketplace, multi-agent orchestration, interactive builder, skill composition DAG, and community guides. The following 5 ideas are entirely new.

---

### 1. Multi-Model Routing — Use the Right Model for Each Skill Phase

**Type:** Feature / Performance
**Effort:** Medium (1-2 days)
**Impact:** Aeon currently runs each skill on a single model (defaulting to opus). But many skills have distinct phases: research (benefits from long context), reasoning (needs strong logic), and output formatting (cheap model handles fine). Multi-model routing would let a skill use Gemini 2.5 for ingesting a 200K-token codebase, Claude Opus for synthesis and writing, and Haiku for formatting — cutting cost by 60-70% on data-heavy skills like `changelog`, `code-health`, and `push-recap` while maintaining output quality where it matters. The per-skill model override PR (#2) already establishes the pattern; this extends it to intra-skill routing.

**How:**
1. Add a `model_routing` config option in `aeon.yml` that maps skill phases to models: `token-report: { research: "gemini-2.5-flash", synthesis: "claude-opus-4-6", format: "claude-haiku-4-5" }`.
2. Implement a lightweight routing layer in the workflow that splits skill execution into phases based on SKILL.md section headers (e.g., `## Steps` sections marked with `<!-- model: haiku -->`).
3. Start with 3 pilot skills (`push-recap`, `token-report`, `changelog`) and measure token cost + output quality vs. single-model runs.

---

### 2. Skill Forking — Let Users Import and Customize Individual Skills

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** Aeon's `add-skill` command imports entire skill files from GitHub repos, but there's no way for users to discover, preview, and selectively import Aeon's skills into their own agent setup. With 7,000+ skills on SkillHub and 66,500+ on SkillsMP, discovery happens on marketplaces — not by browsing repos. Shipping a `skills.json` manifest that lists all 47 skills with metadata (name, description, category, default var, dependencies) would enable one-command installation (`claude skill install aaronjmars/aeon/token-report`) and make each skill independently forkable. This turns Aeon from a monolithic agent into a skill library — users take what they need without forking 47 skills they don't want.

**How:**
1. Create a `skills.json` manifest at the repo root, auto-generated from all `skills/*/SKILL.md` frontmatter. Include: name, description, category, default var, estimated cost per run, and any required secrets.
2. Add an `export-skill` script that packages a single skill with its SKILL.md + any helper scripts into a standalone directory ready for `claude skill install`.
3. Add "Install this skill" copy-paste commands to each skill's row in the README table, linking to the manifest.

---

### 3. Webhook Triggers — Run Skills on GitHub Events, Not Just Cron

**Type:** Feature / Integration
**Effort:** Medium (1-2 days)
**Impact:** Aeon skills run on cron schedules — but many high-value automations should trigger on events: run `pr-review` when a PR is opened, run `issue-triage` when an issue is created, run `token-alert` when a price API webhook fires. GitHub Actions already supports `issues`, `pull_request`, `push`, and `workflow_dispatch` triggers. Adding event-driven skills would make Aeon reactive, not just periodic — catching a critical issue in minutes instead of waiting for the next cron tick. This is the architecture OpenClaw uses for its real-time responses; Aeon can match it for GitHub-native events without running a daemon.

**How:**
1. Add an `on` field to `aeon.yml` skill config: `pr-review: { enabled: true, on: "pull_request.opened" }`. The workflow dispatcher maps GitHub event types to skill names.
2. Create a new `aeon-events.yml` workflow triggered by `issues`, `pull_request`, `push`, and `release` events. On trigger, it reads `aeon.yml` to find skills subscribed to that event type and dispatches them.
3. Pass event context (issue body, PR diff, push commits) as the skill's `var` input so the skill has full context without needing to re-fetch from the API.

---

### 4. Agent Reputation Dashboard — Public Trust Score for Aeon's Outputs

**Type:** Community / Content
**Effort:** Medium (1-2 days)
**Impact:** Aeon generates articles, token reports, tweet drafts, and repo analyses daily — but there's no way for readers to assess reliability. Did the token prediction hold up? Were the repo-actions ideas actually built? Was the article factually accurate? A reputation dashboard would track Aeon's output accuracy over time: prediction outcomes, idea-to-implementation rate, factual corrections needed, and user feedback. This is a novel concept — no AI agent publishes its own accuracy metrics. Shipping this would differentiate Aeon as a transparent, self-auditing agent and build trust with the growing community (131 stars, 15 forks). It also creates a feedback loop: the agent can prioritize skill types that produce the most accurate/useful outputs.

**How:**
1. Create a `skills/reputation/SKILL.md` that weekly reviews the past 7 days of outputs: checks if token-report price predictions were directionally correct, counts how many repo-actions ideas were implemented (cross-reference with commits/PRs), and flags any article claims that were corrected.
2. Generate a `reputation-report.md` with scores: prediction accuracy %, idea implementation rate %, article correction rate, and an overall trust score.
3. Add a "Reputation" section to the aeon-agent README with a live badge showing the current trust score, updated weekly.

---

### 5. Telegram Skill Store — Browse and Enable Skills via Chat

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Aeon already supports Telegram as a two-way communication channel — users can message Aeon and get responses. But enabling/disabling skills, changing schedules, or configuring vars requires editing `aeon.yml` via the dashboard or git. A Telegram skill store would let users browse available skills (`/skills`), enable them (`/enable token-report`), set vars (`/var token-report solana`), and view recent outputs (`/output push-recap`) — all from chat. This makes Aeon fully mobile-operable: a user on their phone can spin up a new skill, check its output, and disable it without touching a browser or terminal. The messaging infrastructure already exists; this adds structured commands on top of it.

**How:**
1. Add command parsing to the Telegram message handler: recognize `/skills`, `/enable <name>`, `/disable <name>`, `/var <name> <value>`, `/output <name>`, and `/schedule <name> <cron>`.
2. Each command reads/writes `aeon.yml`, commits, and pushes — using the same config sync flow the dashboard uses.
3. Send a formatted skill card in response to `/skills`: name, status (enabled/disabled), schedule, last run time, and a one-line description. Paginate if >10 skills.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-28. Ecosystem data from web searches performed same day.*

Sources:
- [OpenClaw AI Agents & Automation](https://skywork.ai/skypage/en/openclaw-ai-agents-automation/2036708876028346368)
- [Claude Code VS Code Marketplace](https://visualstudiomagazine.com/articles/2026/02/26/claude-code-edges-openais-codex-in-vs-codes-agentic-ai-marketplace-leaderboard.aspx)
- [Best Open Source Agent Frameworks 2026](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks)
- [Trigger.dev — AI Agent Infrastructure](https://trigger.dev/)
- [Agentic AI Frameworks 2026](https://aimultiple.com/agentic-frameworks)
- [GitHub Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)
- [SkillsMP Marketplace](https://skillsmp.com/)
- [SkillHub Agent Skills](https://www.skillhub.club)
- [Continuous AI in Practice (GitHub Blog)](https://github.blog/ai-and-ml/generative-ai/continuous-ai-in-practice-what-developers-can-automate-today-with-agentic-ci/)
