# The Week the Cron Agent Grew Up: Aeon Becomes an Agent OS

Most AI agent projects start with ambition and fade into demos. This past week, Aeon had its most productive stretch yet — and the result looks less like a cron scheduler and more like an operating system for distributed intelligence.

## What Aeon Is

Aeon is an autonomous background agent that runs entirely on GitHub Actions. No server, no Docker, no daemon. Fork the repo, configure skills in a YAML schedule, add secrets — and a cron-driven Claude Code instance wakes every few minutes, runs matching skills, and commits results back to the repo. At 152 stars and 17 forks in just over five weeks, it has quietly become a reference implementation for "ambient AI with zero ops overhead."

Everything in Aeon is a skill: a markdown file containing instructions, config, and steps. Skills are off by default. You enable what you need. The elegance is that there is no framework code to learn — the agent reads the skill file and follows it, just as a human would.

## What Just Shipped: April 8–12

The past five days were unlike any prior week. April 8 alone saw 13 PRs merged, reshaping what Aeon fundamentally is.

**Skill chaining** arrived first — the ability to pipe skill outputs into other skills and run multiple skills in parallel. Before this, each skill ran in isolation. Now a `morning-brief` can spin up `rss-digest`, `hacker-news-digest`, and `token-report` simultaneously, merge their outputs, and produce a synthesized briefing. Concurrency changes the economics of what you can ask an agent to do.

**Instance fleet management** followed. Two new skills — `spawn-instance` and `fleet-control` — let Aeon provision and coordinate multiple agent instances across forked repos. This is the skeleton of a multi-agent architecture, built entirely on GitHub Actions primitives.

**`create-skill`** is perhaps the most meta addition: a skill that generates new skills from a natural language prompt. Describe what you want, and Aeon writes the SKILL.md file, wires it into the schedule, and commits it. Self-modification via instruction.

**`autoresearch`** goes further — it analyzes a skill's recent output history, identifies quality degradation or missed opportunities, and rewrites the skill's steps. Skills that improve themselves. The agent's prompts become living documents.

**`distribute-tokens`** crossed into on-chain territory: send ERC-20 tokens to contributors directly from a skill run, via the Bankr API. Aeon can now reward open-source contributors autonomously, denominated in its own token.

April 9 brought **skill-evals** — an assertion framework that validates recent skill outputs against per-skill criteria: minimum word count, required patterns, forbidden strings, numeric range checks. Fourteen skills are covered. This is the difference between an agent that runs and an agent you can trust.

April 10 shipped the **MCP Skill Adaptor**: a TypeScript server that wraps all 70+ Aeon skills as `aeon-<slug>` MCP tools. Install with one command (`./add-mcp`). Now every Aeon skill is available on-demand inside Claude Code and Claude Desktop — not just on a cron schedule, but whenever you ask.

April 11 introduced a **Workflow Security Audit** skill that scans `.github/workflows/` for script injection vectors, over-permissioning, and unverified action pins. It immediately fixed two critical injection vulnerabilities in the repo's own message-handling workflow.

April 12 added a **fourth notification channel**: email via SendGrid, joining Telegram, Discord, and Slack. Each channel is opt-in — add the secret, it activates.

## The Architecture Behind the Sprint

The common thread across this week is a shift from *scheduled* to *composable*. Skills that chain. Instances that coordinate. An adaptor that makes 70 skills callable in any context MCP reaches. A meta-skill that rewrites other skills.

The underlying insight is that GitHub Actions is not just a CI runner — it is a compute substrate with built-in secrets management, cron scheduling, artifact storage, and a global availability SLA. Aeon has been extracting value from this substrate, and this week it mapped out the full surface area: parallelism (skill chaining), scale (fleet management), distribution (MCP), and quality control (evals + security audit).

The move to MCP is particularly well-timed. The protocol crossed 97 million monthly SDK downloads in early 2026 and has been adopted by every major AI provider. Exposing Aeon's skill library as MCP tools means any Claude Code user is one command away from a fully-equipped background agent — without forking anything.

## Why It Matters

The agent landscape in 2026 is crowded with frameworks that promise orchestration and deliver complexity. Aeon's differentiator has always been its constraint: if GitHub Actions can run it, it runs. No persistent processes, no proprietary infrastructure, no vendor lock-in.

This week's shipping adds depth without abandoning that constraint. Skill chaining is still markdown. Fleet management is still YAML schedules. The MCP server is a single TypeScript file. The security auditor is instructions and `gh` CLI calls.

An agent that can chain skills, spawn peers, improve its own prompts, and distribute itself via MCP — while running entirely on infrastructure you already have — is not a demo. It is an operating system for the kind of background intelligence that used to require a team.

The repo is at [github.com/aaronjmars/aeon](https://github.com/aaronjmars/aeon). The MEMORY.md lists 70+ skills. The MCP adaptor is one `./add-mcp` away.

---
*Sources: [github.com/aaronjmars/aeon](https://github.com/aaronjmars/aeon) · [MCP vs A2A: The Complete Guide to AI Agent Protocols in 2026](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li) · [The 2026 Skill Economy](https://stormy.ai/blog/2026-skill-economy-claude-mcp-marketing-skills) · [Aeon on DEV Community](https://dev.to/aaronjmars/aeon-the-background-ai-agent-that-runs-on-github-actions-16am)*
