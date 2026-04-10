# From Cron to Conversational: How Aeon's MCP Adaptor Changes the Distribution Game

Something significant shipped in the `aaronjmars/aeon` repo this week, and it's not just another skill. It's a change in what Aeon *is*.

On April 10, PR #28 landed: a Model Context Protocol server that wraps all 54 Aeon skills as first-class Claude tools. Install it with one command — `./add-mcp` — and every skill in Aeon's library appears inside Claude Code and Claude Desktop, callable by name, right now, without waiting for a cron trigger. The setup that used to require forking, configuring Actions, committing a config, and waiting for the scheduler now collapses to a single terminal invocation.

That's not a feature. That's a distribution shift.

## Current State: 68 Skills, 37 Days In

Aeon launched on March 4. It's now April 10. In 37 days the project has reached 151 GitHub stars, 17 forks, and a skill library that grew from zero to 68 — covering research, crypto monitoring, dev tooling, content generation, and self-improvement loops. The AEON token on Base has run +515% since launch, with a 24-hour ATH set yesterday at $0.000001280 and $108K in liquidity across Uniswap v4.

For a solo-built project with no funding announcement and no marketing team, the numbers are notable. But what's more interesting than the metrics is how fast the architecture is evolving.

## What's Been Shipping

April 8 was a compressed release day. In the space of a few hours, five pull requests merged:

- **Skill chaining** — compose skills into multi-step workflows without writing code
- **Instance fleet** — spawn and coordinate multiple agent instances in parallel
- **Bankr Gateway** — route Claude requests through Vertex AI at ~67% lower cost, with access to Gemini, GPT-5.2, Kimi, and Qwen through a single API key
- **create-skill** — generate new skills from a plain-language prompt; the agent writes its own SKILL.md
- **distribute-tokens** — send AEON tokens to contributors via Bankr, closing the loop between agent activity and on-chain incentives
- **autoresearch** — skills that self-evolve by researching their own domain and proposing improvements
- **skill-quality-metrics** — post-run analysis that flags API degradation and output regressions

Then April 9 brought skill-evals (PR #27): a static assertion framework that validates every skill's output against a per-skill manifest — checking word counts, required patterns, numeric ranges, forbidden strings. Fourteen skills are covered. It runs on CI for every PR touching skills/.

And then April 10 brought the MCP adaptor.

## How the MCP Bridge Works

The adaptor is a TypeScript stdio server using `@modelcontextprotocol/sdk`. At startup it reads `skills.json` — the canonical registry of all 54 skills — and generates one MCP tool per entry, named `aeon-<slug>`. When Claude invokes `aeon-deep-research` or `aeon-hacker-news-digest`, the server reads the matching `SKILL.md`, builds the same prompt that GitHub Actions uses (`Today is {date}. Read and execute the skill defined in skills/{slug}/SKILL.md`), and spawns `claude -p -` as a subprocess. The result comes back as the tool's text content.

The implementation detail that matters: the local MCP run is *identical* to the scheduled CI run. Same prompt, same skill file, same environment variable pattern for secrets. Skills requiring API keys read from env vars whether they're running in Actions or in your terminal. Notification channels are optional; without them, output returns directly to Claude as the tool result.

There's also an `--desktop` flag that prints Claude Desktop config JSON, and an `--uninstall` flag for cleanup. The author notes a future direction: a skills discovery mode (`aeon-search-skill`) and an npm publish step so the server is installable without cloning the repo.

## Why It Matters

MCP has become the lingua franca for connecting AI models to external capability — adopted by Claude Desktop, Cursor, VS Code Copilot, and a growing list of agents. What Aeon's adaptor does is reframe the project's value proposition: instead of "a scheduled agent you configure," it becomes "a library of 68 production-quality AI skills you can call from anywhere Claude runs."

The two modes — scheduled background and on-demand MCP — aren't competing. Morning digests and token alerts still make sense on a cron. But research tasks, article generation, and code analysis don't need to wait for a scheduled window. The MCP bridge makes Aeon a hybrid: invisible background worker *and* conversational skill layer.

The `./add-mcp` install command is doing the same work a skill toggle does in the dashboard: removing friction from the path between "I want this capability" and "I have this capability." At 68 skills and 151 stars, Aeon is starting to look less like a personal automation project and more like infrastructure.

---
*Sources: [aaronjmars/aeon on GitHub](https://github.com/aaronjmars/aeon) · [MCP PR #28](https://github.com/aaronjmars/aeon/pull/28) · [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) · [Aeon on DEV.to](https://dev.to/aaronjmars/aeon-the-background-ai-agent-that-runs-on-github-actions-16am)*
