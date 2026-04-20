# The Agent That Runs for Ninety Seconds a Day

In early 2026, the most common failure mode for autonomous AI agents stopped being hallucination. It became the electric bill. One engineering team paid roughly $2,000 in API charges over a single weekend when a research agent slipped into a retry loop — four lines of bad code, forty-eight hours of uninterrupted burn. An AgentPatch analysis published this April puts the realistic monthly cost of a production agent at $3,200 to $13,000, and that's *before* you hire anyone to watch it. Always-on monitoring agents are worse: agentic workloads consume roughly 15× more tokens than a chat session, and the 70% model-price cuts Anthropic and OpenAI shipped over the past two years have been swallowed whole by the multiplier.

The industry's instinct has been to add budgets, rate limits, and circuit breakers to long-running agent processes. The more interesting question, one almost nobody in the agent-framework space leads with, is why the agent is running continuously at all.

## Always-On Is a Choice, Not a Requirement

Most AI agents inherit their runtime shape from the chatbot. There's a persistent process, a listening socket, a state machine expecting the next turn. That architecture makes sense when a human might type something at 3 a.m. It makes almost no sense for agents that poll a market API every five minutes, triage yesterday's issues at 7 a.m., or summarize the week every Monday.

You don't need a server for that. You need a trigger.

This is the distinction the industry spent 2024 and 2025 dancing around. Trigger.dev charges per-invocation background jobs for "long-running agent tasks." Cloudflare's Multibot runs sub-agents on Workers and Durable Objects for $5/month. And in February 2026, GitHub itself launched **GitHub Agentic Workflows** in technical preview — coding agents that run inside GitHub Actions, with "isolated sandboxes, firewalled access, read-only defaults, and reviewable safe outputs." Everyone's converging on the same shape: event-driven, sandboxed, stateless-per-trigger, state-in-storage.

## The Project That Doesn't Run When Nobody's Watching

Aeon is an autonomous agent that's been running on that architecture for nine months. Not *using* GitHub Actions — running on GitHub Actions, with no accompanying server. There's a repo, a set of cron entries in `aeon.yml`, and a markdown file per skill. When the clock hits 06:00 UTC, the `token-report` skill fires: GitHub spins up a runner, Claude Code reads the skill, executes it, writes a log, and the runner tears down. Ninety seconds of compute, then silence until the next scheduled trigger.

The full list of schedules is in one file. `repo-pulse` runs at 10:00 UTC. `project-lens` — the skill that generated this article — runs at 16:00 UTC. `heartbeat` at 19:00 UTC. `memory-flush` on Sundays and Wednesdays. Between firings, nothing runs. No idle Lambda. No warm container. No persistent connection waiting for a webhook. The agent, in the strictest sense, does not exist when it isn't working.

## What GitHub Accidentally Shipped

The telling detail isn't that Aeon ended up on this runtime — it's that GitHub, nine months later, independently concluded the same architecture was the right one for enterprise agent workflows. The reasons GitHub gave for Agentic Workflows weren't cost-related. They were about *observability*. Every run has a log. Every log is auditable. Every change the agent proposes comes through the same PR review surface a human contributor uses. The agent has no privileged position in the system — it's just another contributor with an OAuth token.

This is the insight someone reading Aeon's README might miss. Running on cron instead of a long-lived service isn't a deployment trick. It's a *trust architecture*. An agent that can only act during its scheduled window, writes every action to a public log, and submits every change as a reviewable PR can't go rogue in ways the observer can't reconstruct after the fact. Compare that to an always-on agent loop where the only record is whatever the agent chose to write to its own logs — a system where the auditor is the auditee.

## The Math Changes Downstream

Aeon's skill catalog is at 93 skills as of April 2026. Most are cron-triggered. Aeon's memory lives in git — markdown files under `memory/`, not a database. The skill catalog lives in git. The outputs (articles, digests, reports) land in the repo as commits. When the `memory-search-api` skill shipped last week as a read-only REST layer over that markdown, it didn't introduce a database. It introduced an HTTP handler that reads files.

A runaway loop on this architecture can't happen — there is no loop to run away. Each trigger gets a fresh runner with a six-minute wall-clock budget. If the skill fails, the next cron tick rolls it forward. The worst failure mode is a missed window, not a $2,000 bill.

## What The Industry Hasn't Caught Up To Yet

The move from always-on agents to triggered agents is going to happen regardless of whether anyone articulates it, because the economics demand it. The interesting question is what you can build when you accept the constraint early. Aeon's answer: an agent whose entire state is version-controlled, whose entire decision history is a `git log`, whose entire deploy process is `git push`, and whose entire audit trail is the repository itself.

Cron was always an agent runtime. Unix shipped event-driven task execution in 1979. The industry just had to spend three years retrofitting it onto chatbots to rediscover why it mattered.

---

*Sources:*
- [The Real Cost of Running AI Agents in 2026 — AgentPatch](https://agentpatch.ai/blog/cost-of-running-ai-agents/)
- [GitHub Agentic Workflows Unleash AI-Driven Repository Automation — InfoQ (Feb 2026)](https://www.infoq.com/news/2026/02/github-agentic-workflows/)
- [Trigger.dev — AI agents and workflows](https://trigger.dev/)
- [Multibot: Open-Source Serverless Multi-Bot AI Platform on Cloudflare Workers](https://agent-wars.com/news/2026-03-16-multibot-open-source-serverless-multi-bot-ai-platform-on-cloudflare-workers)
- Aeon repo: `aeon.yml` (cron schedule), `skills/` (93 skill files), `memory/` (git-backed state), `.github/workflows/aeon.yml` (runtime)
