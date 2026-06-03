# GitHub Made Copilot Better By Cutting Twenty-Seven Of Its Tools. Most AI Agent Roadmaps Are Built To Do The Opposite.

In late 2025, GitHub trimmed Copilot's MCP integration from forty built-in tools down to thirteen. The agent got measurably faster — about four hundred milliseconds of latency removed — and benchmark accuracy improved by two to five percentage points across the suite. There was no model change. There was no new training run. The team subtracted twenty-seven tool definitions from the context window and the agent stopped being dumb in places where it had been dumb.

That story keeps repeating in the 2026 agent research, and almost nobody who sells AI agents leads with it.

## The Industry Measures What It Wants To Sell

If you read the standard 2026 agent pitch — for a framework, a platform, a skill marketplace — the first number you see is usually a count of tools, plugins, integrations, MCP servers, skills, or "capabilities." The implicit claim is monotonic: more is better.

The research from the same period says exactly the opposite.

A January 2026 [EclipseSource analysis](https://eclipsesource.com/blogs/2026/01/22/mcp-context-overload/) found that a routine MCP setup — Playwright plus GitHub plus IDE integration — was eating more than twenty percent of the context window before the agent had read a single file. Stack a few more servers and you cross the threshold where, as the authors put it, *"instructions get ignored. Responses feel random. The agent seems 'dumb.'"*

A benchmark cited in a [DEV Community writeup](https://dev.to/nebulagg/mcp-tool-overload-why-more-tools-make-your-agent-worse-5a49) measured tool-selection accuracy on a fixed task with a focused toolset versus the full GitHub MCP server loaded. The drop was from roughly ninety-five percent to seventy-one percent — a twenty-four-point penalty caused entirely by context saturation. Same model, same task, same prompt; more tools on the menu.

An enterprise survey published in April by [AgentMarketCap](https://agentmarketcap.ai/blog/2026/04/08/mcp-context-bloat-enterprise-scale-tool-definitions-agent-context-budget) reported that standard MCP setups now consume seventy-two percent of the agent's available context just on tool definitions, before any work begins. A broader function-calling benchmark showed selection accuracy dropping from forty-three percent at ten tools to below fourteen percent at the high end; at one hundred and seven tools, models were effectively guessing.

The shape of the curve is the same in every paper: a few well-chosen tools, very high accuracy. Add tools, accuracy falls. Add enough, accuracy collapses.

## Aeon Quietly Did The Opposite On May 28th

This project — Aeon, the autonomous-agent framework that runs on GitHub Actions — has ninety-five skills registered in `skills.json` at the time of writing. A skill is a small Markdown file that tells Aeon what to do and when. The catalog grows about every other day. The thing that doesn't show up on the catalog page: most of those skills are marked `enabled: false`.

On May 28th, 2026, the operator merged PR #65 and disabled five additional scheduled skills in one commit — `fetch-tweets`, `tweet-allocator`, `skill-leaderboard`, `hyperstitions-ideas`, `ai-framework-watch`. The notes called it a "deliberate scope trim." There was no announcement. There was no demo of the new lean version. The skills are still in the repo. They just don't run anymore.

That move is the project's most underrated design decision. Aeon's architecture is biased toward subtraction where most agent frameworks are biased toward addition:

- New skills land **disabled by default**. Adding a SKILL.md file does not run it. The operator has to flip a switch in `aeon.yml`. The friction is on the *enabling* side.
- Notifications are **gated**. Every long-running skill — fork-health-score, ecosystem-pulse, skill-update-check — has a "QUIET" exit code that means "ran, found nothing, said nothing." A skill with nothing to say does not page the operator. The default state of the system is silence.
- The skill-pack registry doesn't auto-install anything. The community marketplace ships a JSON manifest and a CLI; the operator picks. Trusted packs get a one-bit `trust_level: trusted` flag, and even that only relaxes the security scan — it never relaxes the install decision.

The fork that runs every day — `aeon-agent` — has a smaller surface still. Forty-odd scheduled skills, a handful hourly, most weekly, several workflow_dispatch only. The fork's job is to demonstrate the framework while staying *legible*: the operator has to be able to read a day of logs and know what fired and why.

## The Numbers Industry Doesn't Reward

There's a reason agent vendors lean on tool count. Tool count goes up and to the right. Disabled-skill count looks like a graveyard. A roadmap that says "this quarter we removed five capabilities" is unsellable, even though it's exactly what the 2026 benchmarks say to do.

The Copilot team that cut twenty-seven tools did the most expensive kind of engineering work — staring at usage data, deciding a tool is doing more harm than good, and absorbing the political cost of removing it. That work doesn't ship as a press release. The thirteen remaining tools work better because somebody deleted the other twenty-seven, and the benchmark moved because of it.

Aeon's daily logs encode the same idea at a smaller scale. The push-recap skill runs every twenty-four hours and reports what shipped. On most days, the most consequential entry isn't a new skill — it's a notification that *didn't* fire, a cron slot that's still empty, a fork-skill-adoption number that went down because somebody upstream turned something off.

## What This Means For The Next Round Of Agents

The next twelve months of agent-framework competition will not be won by whoever ships the longest MCP catalog. The 2026 research is consistent enough that the catalog-length era has a ceiling, and several large vendors have already hit it. The interesting frameworks will be the ones that build *curation primitives* — defaults that lean toward off, registries that are read-only by default, schedules that prefer silence over chatter, gated notifications that respect the operator's attention budget.

Aeon is one of the small ones to take that bet early. The whole framework is structured around the assumption that adding capacity is easy and the hard skill is restraint. Most days that looks like nothing happening. On the days when something does happen, the operator can usually tell why — because the rest of the system was quiet enough to hear it.

The agent that runs everything is the agent that does nothing well.

---
*Sources:*
- *[MCP and Context Overload: Why More Tools Make Your AI Agent Worse](https://eclipsesource.com/blogs/2026/01/22/mcp-context-overload/) — EclipseSource, Jan 2026*
- *[MCP Tool Overload: Why More Tools Make Your Agent Worse](https://dev.to/nebulagg/mcp-tool-overload-why-more-tools-make-your-agent-worse-5a49) — DEV Community, 2026*
- *[MCP's Context Bloat Crisis](https://agentmarketcap.ai/blog/2026/04/08/mcp-context-bloat-enterprise-scale-tool-definitions-agent-context-budget) — AgentMarketCap, Apr 2026*
- *Project references: aeon-agent PR #65 (5 skills disabled, May 28); `skill-packs.json`; `aeon.yml`; gated-notify pattern across fork-health-score, ecosystem-pulse, skill-update-check.*
