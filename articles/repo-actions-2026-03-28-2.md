# Repo Action Ideas — 2026-03-28 (Run 2)

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 131 (aeon) / 4 (aeon-agent) | **Forks:** 15 / 0 | **Language:** TypeScript | **Open Issues:** 2 / 2
**Contributors:** aaronjmars (132 commits), github-actions[bot], Aeon

Aeon is an autonomous background agent on GitHub Actions powered by Claude Code — 47 skills across research, dev tooling, crypto, and productivity. The agent runs 12+ skills daily, has generated 6 articles this week, and gained 13 stars in 3 days (118→131). Two open PRs on aeon-agent: heartbeat timing fix (#1) and per-skill model overrides (#2, ~45% cost savings).

## Ecosystem Context (March 28, 2026)

Key developments informing today's ideas — distinct from prior runs:

- **Agent-to-Agent (A2A) Protocol emerging** — Alongside MCP (tool/data integration), A2A is forming as a standard for inter-agent communication. Agents can now discover and invoke each other across services. Aeon's skills are isolated; A2A would let external agents call Aeon skills and vice versa. ([source](https://platform.claude.com/docs/en/agent-sdk/overview))
- **OpenTelemetry GenAI semantic conventions** — OTEL now has standardized spans for LLM calls, tool invocations, and reasoning steps. 89% of orgs have implemented agent observability; a single agent generates 10x the trace data of a web service. Open-source stacks (Langfuse, Arize Phoenix, Grafana) cut monitoring costs 70% vs. commercial tools. ([source](https://research.aimultiple.com/agentic-monitoring/))
- **Claude Agent SDK v0.1.48 (Python) / v0.2.71 (TypeScript)** — The renamed Claude Code SDK is now a general-purpose agent runtime with MCP integration, subagent spawning, tool search, and isolated context per child agent. This is the programmatic equivalent of what Aeon does via CLI. ([source](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk))
- **Bounded autonomy as industry pattern** — Gartner and enterprise teams are implementing configurable autonomy levels: clear operational limits, escalation paths, and audit trails per agent capability. 40% of enterprise apps will embed AI agents by end of 2026. ([source](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/))
- **Context engineering as discipline** — Systematic construction and management of context for AI agents is now a recognized field. Long-running agents that manage their own context window (pruning, caching, summarizing) outperform those that don't by 3-5x on complex tasks. ([source](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a))

Previous runs (Mar 25, Mar 27, Mar 28 run 1) covered 20 ideas: skill marketplace, multi-agent orchestration, awesome-list listings, analytics dashboard, interactive builder, plugin registration, composition DAG, community contributions, agent state snapshots, Telegram control plane, skill evals, agentic workflow templates, SkillsMP publish, A/B testing, cost tracker, security audit, live feed, multi-model routing, skill forking, webhook triggers, reputation dashboard, Telegram skill store, and dependency chains. The following 5 ideas are entirely new.

---

### 1. Agent-to-Agent Protocol Gateway — Let External Agents Call Aeon Skills

**Type:** Integration / Growth
**Effort:** Medium (1-2 days)
**Impact:** The A2A protocol is emerging as the standard for inter-agent communication — agents discovering and invoking each other across services. Aeon currently runs in isolation: skills trigger on cron, produce output, and commit. An A2A gateway would expose Aeon's skills as callable endpoints that other agents can discover and invoke. Imagine a user's personal Claude agent asking Aeon for a token report, or a Devin instance requesting a code-health analysis. This transforms Aeon from a standalone agent into a skill service — a node in the growing multi-agent network. With 47 skills already built, Aeon has more to offer than most agents.

**How:**
1. Create a `skills/a2a-gateway/SKILL.md` that generates an A2A-compatible service descriptor listing all enabled skills with their input/output schemas (derived from SKILL.md frontmatter: name, description, var type).
2. Add a `workflow_dispatch` trigger to `aeon.yml` that accepts an A2A-formatted request (skill name + var), runs the skill, and returns the output as a workflow artifact. This is the simplest A2A-compatible invocation path using existing GitHub Actions infrastructure.
3. Publish the service descriptor to the repo root as `a2a-descriptor.json` and document the invocation pattern in the README so other agent builders can integrate.

---

### 2. OpenTelemetry Skill Tracing — Production Observability for Every Run

**Type:** DX Improvement / Performance
**Effort:** Medium (1-2 days)
**Impact:** Aeon runs 12+ skills daily but has zero structured observability — no traces, no latency breakdowns, no error categorization. The industry has converged on OpenTelemetry's GenAI semantic conventions for agent monitoring. Adding OTEL tracing would capture every skill run as a structured trace: start time, model used, tokens consumed, tool calls made, errors encountered, and output quality signals. This data feeds into any OTEL-compatible backend (Grafana, Langfuse, Arize Phoenix) for dashboards, alerting, and cost analysis. With Langfuse at 21K+ GitHub stars and free self-hosting, the infrastructure cost is zero. The payoff is immediate: identify which skills are slow, which fail silently, and which waste tokens on cache misses.

**How:**
1. Add a lightweight OTEL instrumentation wrapper in the workflow: before each skill run, emit a trace span with `{skill_name, model, var, trigger_type}`. After the run, close the span with `{status, duration_ms, input_tokens, output_tokens, cache_read, cache_creation, output_file}`.
2. Write spans to a `data/traces.jsonl` file (one JSON line per span) committed alongside skill outputs. This is the zero-infrastructure approach — no external backend needed initially.
3. Add a `skills/observability-report/SKILL.md` that reads `traces.jsonl` weekly, generates a performance report (p50/p95 latency per skill, failure rate, cost trends, anomalies), and posts it via `./notify`.

---

### 3. Claude Agent SDK Skill Runner — Programmatic Execution Beyond CLI

**Type:** Feature / Integration
**Effort:** Large (3+ days)
**Impact:** Aeon executes skills by piping SKILL.md content to the Claude Code CLI. This works but is limited: no programmatic control over tool permissions mid-run, no subagent spawning for parallel subtasks, no structured output parsing, and CLI stderr parsing for errors is brittle (the recent stderr capture fix in aeon.yml proves this). The Claude Agent SDK (v0.2.71 TypeScript) provides the same agent loop programmatically — with MCP integration, subagent support, tool search (load tools on demand instead of bloating context), and typed responses. Migrating the skill runner from CLI to SDK would unlock: running skill subtasks in parallel via subagents, dynamically loading MCP tools per skill, and structured JSON output instead of scraping markdown. This is the architectural upgrade that unblocks the next generation of complex skills.

**How:**
1. Create a `lib/skill-runner.ts` that uses the Claude Agent SDK to execute a skill: reads SKILL.md, constructs the prompt, configures tools (file read/write, bash, web search, GitHub API via MCP), and runs the agent loop.
2. Add a `sdk-mode` flag to `aeon.yml` skill config. When enabled, the workflow calls `npx tsx lib/skill-runner.ts <skill-name>` instead of the Claude CLI. Migrate 3 pilot skills (token-report, push-recap, heartbeat) first.
3. Expose structured output: the SDK runner returns JSON `{status, output_file, tokens_used, duration_ms, errors}` instead of relying on exit codes and stderr parsing. Feed this into the OTEL traces (idea #2) for end-to-end observability.

---

### 4. Skill Autonomy Levels — Configurable Guardrails Per Skill

**Type:** Security / DX Improvement
**Effort:** Small (hours)
**Impact:** Aeon skills range from read-only data fetches (token-report, fetch-tweets) to write-heavy operations (feature, self-improve) that create branches, write code, and open PRs. But all skills run with the same permissions: full file system access, shell execution, GitHub write access. The "bounded autonomy" pattern — now an industry standard per Gartner — assigns each agent capability an explicit autonomy level with escalation paths. Implementing this for Aeon would mean: `token-report` runs with `read-only` (no file writes, no git operations), `push-recap` runs with `write-files` (can create articles but not branches), and `feature` runs with `full` (can create branches and PRs). This reduces blast radius if a skill hallucinates a destructive command, and makes Aeon auditable for enterprise adoption.

**How:**
1. Add an `autonomy` field to `aeon.yml` skill config with three levels: `read-only` (web search, API reads, file reads only), `write-files` (adds file write + git commit to main), `full` (adds branch creation, PR opening, shell commands). Default to `write-files`.
2. Map autonomy levels to Claude Code `--allowedTools` flags in the workflow dispatcher. `read-only` restricts to `Read,Glob,Grep,WebSearch,WebFetch`; `write-files` adds `Write,Edit,Bash(git commit)`; `full` allows all tools.
3. Log the autonomy level in each skill's trace span (ties into idea #2) and add a "Permissions" column to the dashboard skills table showing each skill's current level.

---

### 5. Context Window Budget — Smart Token Management for Long-Running Skills

**Type:** Performance / Feature
**Effort:** Medium (1-2 days)
**Impact:** Aeon's most expensive skills (feature, repo-article, code-health) consume large context windows — reading multiple files, fetching web pages, processing API responses. But there's no budget or management: skills run until they finish or hit the model's context limit, with no awareness of how much context they've consumed or whether they're wasting tokens on redundant reads. Context engineering — now a recognized discipline — shows that agents with explicit context budgets outperform unmanaged ones by 3-5x on complex tasks. Adding a token budget per skill would: cap runaway costs (a feature skill that reads 50 files could burn $10+ on Opus), force skills to prioritize information (read the most relevant files first), and enable automatic summarization of consumed context when approaching the limit.

**How:**
1. Add a `max_tokens` field to `aeon.yml` skill config (e.g., `token-report: { max_tokens: 50000 }`, `feature: { max_tokens: 200000 }`). The workflow passes this as `--max-tokens` to the Claude CLI (or SDK runner from idea #3).
2. Create a `context-budget` prompt prefix injected before each skill's SKILL.md content: "You have a budget of N tokens for this task. Prioritize the most impactful actions. Summarize large file contents instead of quoting them verbatim. If you approach 80% of your budget, wrap up with what you have."
3. Track actual vs. budgeted token usage in the OTEL traces and surface "over-budget" skills in the weekly observability report as candidates for optimization or model downgrade.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-28 (run 2). Ecosystem data from web searches performed same day.*

Sources:
- [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [AI Agent Observability Tools 2026](https://research.aimultiple.com/agentic-monitoring/)
- [Best AI Observability Tools — Braintrust](https://www.braintrust.dev/articles/best-ai-observability-tools-2026)
- [7 Agentic AI Trends to Watch in 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/)
- [State of AI Coding Agents 2026](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a)
- [GitHub Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)
- [Continuous AI in Practice — GitHub Blog](https://github.blog/ai-and-ml/generative-ai/continuous-ai-in-practice-what-developers-can-automate-today-with-agentic-ci/)
- [Langfuse — LLM Observability](https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse)
