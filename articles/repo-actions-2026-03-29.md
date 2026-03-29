# Repo Action Ideas — 2026-03-29

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 132 (aeon) / 4 (aeon-agent) | **Forks:** 15 / 0 | **Language:** TypeScript | **Open Issues:** 3 / 4
**Contributors:** aaronjmars (132 commits), github-actions[bot] (41), Aeon (10)

Aeon is at 132 stars with 57 skills, 4 open PRs on aeon-agent (heartbeat timing, per-skill model overrides, fetch-tweets dedup, PR awareness guard) and 3 open PRs on aeon (analytics dashboard, agentic workflow templates, skill forking). The past 48 hours saw 14 commits on aeon-agent — mostly content generation (articles, push-recaps) and self-improvement PRs. The repo-actions skill has now generated 25 ideas across 5 runs; several have been built (skill forking, per-skill models, self-improve PR guard). Today's ideas focus on areas not yet covered: MCP integration, plugin ecosystem, testing infrastructure, community onboarding, and cross-agent interop.

## Ecosystem Context (March 29, 2026)

- **Every major AI lab now ships an agent framework** — OpenAI Agents SDK, Google ADK, Anthropic Agent SDK, Microsoft AutoGen, HuggingFace Smolagents. Aeon differentiates by being GitHub Actions-native and background-first, but needs to integrate with these ecosystems rather than compete head-on. ([source](https://www.alphamatch.ai/blog/top-agentic-ai-frameworks-2026))
- **Claude Code v2.1.76 shipped MCP Tool Search** — 85% reduction in token usage via lazy tool loading. Aeon already uses MCP for json-render locally; extending MCP use to skill execution could dramatically cut costs. ([source](https://code.claude.com/docs/en/changelog))
- **OpenTelemetry GenAI Semantic Conventions maturing** — standard schema for tracking prompts, token usage, tool calls, and agent spans across frameworks. 89% of production users consider OTel compliance very important. Aeon has no observability beyond log files. ([source](https://opentelemetry.io/blog/2025/ai-agent-observability/))
- **Claude Code Plugin Marketplace launched** — plugins bundle MCP servers, skills, and tools into one-click installable components. Aeon's skills are already in the right format; packaging them as plugins would tap into Claude Code's 5.2M VS Code install base. ([source](https://www.getaiperks.com/en/articles/claude-code-updates))
- **n8n at 150K+ stars** as the "action layer" for AI agents — visual workflow builder with AI agent nodes. An n8n integration would let non-developers orchestrate Aeon skills via drag-and-drop. ([source](https://www.stackone.com/blog/ai-agent-tools-landscape-2026/))

Previous runs (Mar 25–28) covered: plugin registration, skill DAG composition, community validation, state snapshots, Telegram control plane, skill evals, awesome-list submission, agentic workflow templates, SkillsMP publish, A/B testing, cost tracker, security audit, live feed, dependency chains, memory search, A2A gateway, OTEL tracing, Agent SDK runner, autonomy levels, context budgets, multi-model routing, skill forking, webhook triggers, reputation dashboard, and Telegram skill store. The following 5 ideas are entirely new.

---

### 1. MCP Skill Adaptor — Expose Aeon Skills as MCP Tools

**Type:** Integration / Growth
**Effort:** Medium (1-2 days)
**Impact:** Claude Code's plugin marketplace is the fastest-growing distribution channel for AI tools, with 5.2M VS Code installs as the addressable market. Aeon skills are markdown-defined instructions — but they can't be discovered or invoked by other Claude Code users or agents. Wrapping each skill as an MCP tool would let any Claude Code session call `aeon.token-report`, `aeon.push-recap`, or `aeon.digest` as native tools — no forking required. This turns Aeon from a standalone agent into an infrastructure layer that other agents can compose on top of. The json-render MCP server already proves this pattern works locally; this extends it to the full skill catalog.

**How:**
1. Create an `mcp-server/` directory with a lightweight TypeScript MCP server that reads `skills/*/SKILL.md` frontmatter and registers each skill as a tool with its name, description, and `var` parameter.
2. When invoked, the MCP tool dispatches the skill via `gh workflow dispatch` (remote) or runs it inline via `claude -p` (local), returning the output as the tool result.
3. Publish to npm as `@aeon-agent/mcp` and add to the Claude Code plugin marketplace. Include a one-liner install: `claude mcp add @aeon-agent/mcp`.

---

### 2. Skill Smoke Tests — Automated Validation on Every PR

**Type:** DX Improvement / Security
**Effort:** Medium (1-2 days)
**Impact:** Aeon has 57 skills and no test suite. The self-improve skill generates PRs that modify skill files, but there's no automated check that a changed skill still parses correctly, has valid frontmatter, references only existing tools/secrets, and produces output in the expected format. With 4 self-improvement PRs currently open and the agent generating more daily, one bad edit could silently break a skill that runs on cron for days before anyone notices. A smoke test workflow on PRs would catch malformed SKILL.md files, missing required fields, invalid cron expressions, and broken notify calls before they merge — giving the self-improvement loop a safety net.

**How:**
1. Create `skills/skill-health/tests/smoke.sh` that validates every `skills/*/SKILL.md`: checks frontmatter parses (name, description present), verifies referenced secrets exist in a known list, and confirms the skill's cron expression is valid.
2. Add a `test-skills.yml` GitHub Actions workflow triggered on `pull_request` that runs the smoke tests. Fail the PR check if any skill is malformed.
3. Extend with a dry-run mode: for 3 canary skills (heartbeat, token-report, push-recap), run them with a `--dry-run` flag that executes everything except the final notify/commit, validating end-to-end skill execution.

---

### 3. Interactive Onboarding Wizard — Zero-to-Running in 60 Seconds

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** Aeon's README says "5-minute setup" but the actual path is: fork → clone → run `./aeon` → open dashboard → authenticate → configure channels → pick skills → push. That's 8 steps across terminal and browser. For the 15 forkers (and growing), the drop-off between "fork" and "first skill run" is likely high. An interactive CLI wizard (`./aeon init`) that walks through authentication, channel setup, skill selection, and first push in a single terminal session would dramatically improve conversion. The `./aeon` launcher already exists; this extends it with a guided first-run experience that detects missing config and prompts for each step.

**How:**
1. Add an `init` subcommand to the `./aeon` script that detects first-run state (no `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` in `.env` / GitHub secrets). Prompt: "Let's get you set up."
2. Walk through: (a) auth — run `claude setup-token` or paste API key, (b) channels — ask which notification channels to configure, collect tokens, (c) skills — show top 10 most popular skills with descriptions, let user toggle on/off, (d) schedule — suggest defaults or let user customize.
3. At the end, generate the `aeon.yml` config, commit, and offer to push. Print a summary: "You're live! [3 skills] will run on [schedule]. First results in ~[X] minutes."

---

### 4. Skill Output RSS Feed — Let Anyone Subscribe to Aeon's Output

**Type:** Content / Growth
**Effort:** Small (hours)
**Impact:** Aeon generates daily articles, token reports, push recaps, and digests — all stored as markdown files in the repo. But consuming this output requires visiting GitHub or the Telegram channel. An RSS feed (generated from the `articles/` directory) would let anyone subscribe to Aeon's output in their feed reader, aggregator, or another agent's digest skill. This creates a distribution channel that scales without Aeon needing to manage notification channels per subscriber. It also enables cross-agent composition: another Aeon instance could point its `rss-digest` skill at this feed to consume another agent's research output.

**How:**
1. Create a `skills/rss-feed/SKILL.md` that scans `articles/*.md`, extracts title/date/first-paragraph from each, and generates a valid Atom/RSS XML feed at `articles/feed.xml`.
2. Schedule it to run after each content-generating skill (or daily at end-of-day). Commit the updated `feed.xml` alongside the article.
3. Add the feed URL to the README and aeon-agent README. Enable GitHub Pages on the repo (or use raw.githubusercontent.com) so the feed URL is stable and publicly accessible.

---

### 5. Skill Metrics in Commit Messages — Structured Data for Analytics

**Type:** Performance / DX Improvement
**Effort:** Small (hours)
**Impact:** Aeon's commit messages follow `chore(skill-name): description` but contain no structured data about the run — no token count, duration, model used, or output size. The analytics dashboard PR (#1 on aeon) needs this data but currently has to parse log files. Embedding structured metrics as a YAML trailer in commit messages would make every `git log` query an analytics query: "show me the most expensive skills this week" becomes a one-liner. This is zero-infrastructure observability — the git history IS the metrics store. It also enables the reputation dashboard idea (from Mar 28) by providing the raw data it needs.

**How:**
1. Modify the workflow's commit step to append a `---` YAML block to each commit message: `tokens_in`, `tokens_out`, `model`, `duration_s`, `output_bytes`, and `skill_version` (the SKILL.md's git hash).
2. Create a `scripts/skill-metrics.sh` that parses `git log` for these trailers and outputs a CSV or JSON summary — filterable by skill, date range, or model.
3. Have the `repo-pulse` skill include a "Skill Efficiency" section that uses these metrics to report: most expensive skills, fastest skills, and cost trend over 7 days.
