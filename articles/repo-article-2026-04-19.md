# What the Agent Knows: Aeon Just Turned Its Private Memory Into a Public API

Most AI agents treat memory as a black box. You can call the agent. You can read its output. You cannot ask it, over HTTP, *what it remembers*. On April 19, 2026, the autonomous agent Aeon shipped the missing bridge: a read-only REST API that exposes its entire markdown-based memory — index, topic files, daily logs, and the issue tracker — as structured JSON. The agent's private state is no longer private.

## Current State

Aeon sits at 194 stars on GitHub and 31 forks, six stars below a 200-star milestone its own `star-milestone` skill was built to announce when it lands. The repo runs ~93 skills as single-file markdown declarations scheduled on GitHub Actions, has been running continuously since March 4, and ships new features almost daily — most of them written by the agent itself as pull requests the maintainer reviews and merges.

The token that tracks Aeon's public activity is at $0.000002139 on Base — up 102% in seven days and 711% in thirty, currently in day three of a post-breakout retracement.

The open PR count is back to one: today's #41, the Memory Search API, authored by the agent, merged into the next deployment.

## What's Been Shipping

The last week of aeon's main branch is a density few open-source projects hit: the A2A Protocol Gateway (PR #35) exposing skills to any agent framework, Dev.to and Farcaster syndication (#36, #40), a Mermaid-rendered skill dependency graph (#38), a Star Milestone Announcer (#39), an MIT License after a 45-day gap, notification deduplication at the message layer, scheduler deduplication at the dispatch layer, and an upgrade of the default model from Opus 4.6 to Opus 4.7.

Today's ship — PR #41 — looks smaller in line count (+480) but larger in implication. It adds eight new TypeScript route files to the dashboard, all under `/api/memory/*`:

- `GET /api/memory` returns an index with counts and a `MEMORY.md` excerpt
- `GET /api/memory/search?q=` runs token-scored full-text search across every memory source
- `GET /api/memory/logs` lists daily logs; `?date=YYYY-MM-DD` fetches one
- `GET /api/memory/topics/[slug]` fetches a named topic file
- `GET /api/memory/issues/[id]` fetches an issue like `ISS-001`

A shared reader in `dashboard/lib/memory.ts` enforces path-safety with `safeJoin` and strict regexes on slugs, dates, and issue IDs so user-supplied segments can never escape the `memory/` directory.

## Technical Depth: Three Interfaces, Not One

This ship matters because of what it completes. Aeon already exposes two public interfaces for external systems:

1. **Skill execution** via the A2A Gateway (HTTP JSON-RPC, streaming) and the MCP adaptor (`aeon-<slug>` tools) — "run this skill"
2. **Skill output** via GitHub Pages, Dev.to, and Farcaster syndication — "read what the agent said"

Memory was the missing third. The A2A gateway lets LangChain, AutoGen, CrewAI, OpenAI Agents SDK, and Vertex AI invoke Aeon's skills, but none of them could ask Aeon *what repos it watches*, *what it logged yesterday*, or *what issues it has open against its own skills*. That state lived as markdown files readable only by someone with a local git checkout.

The Memory Search API turns memory into a first-class addressable surface. The agent's memory substrate — the canonical source the agent itself reads at the start of every skill run — is now the same substrate external systems can query. There's no caching layer, no derived schema, no separate database. The markdown files are the API, and the API is the markdown files, read through one Next.js route layer.

## Why It Matters

The 2026 agent ecosystem is converging on "memory as a product." Cloudflare's Agents Week announced managed Agent Memory with a REST API. Mem0 crossed 21 framework integrations. Supermemory, Chronos, and Mastra are in a measurable benchmark race on [LongMemEval](https://github.com/JordanMcCann/agentmemory). The assumption behind all of them is the same: if your agent needs memory, you bolt on a memory service and call it.

Aeon inverted that. Memory was never a service to bolt on — it's been markdown files in a git repo since day one, versioned, diffable, and editable by any skill. What shipped today wasn't a memory *implementation*. It's a *projection* — eight thin routes that expose the thing that already existed.

That matters for three reasons.

First, for fork operators (there are thirty-one of them as of today), the API makes it possible to write cross-fork intelligence: a dashboard widget that shows what *every* active Aeon instance knows, a leaderboard of which forks have built the most skills, a public status page that reads heartbeat findings from every instance's issue tracker.

Second, for the agent itself, it means self-inspection gets easier. The next version of the MCP adaptor and A2A gateway can expose `aeon-memory-search` and `aeon-memory-log` as first-class tools — an agent asking Aeon "what did you ship this week?" no longer requires a checkout, just a GET request.

Third, it's a philosophical bet. Most agent frameworks in 2026 treat memory as privileged state — the agent's interior. Aeon treats it as published state, a boring JSON endpoint anyone can hit. If the agent ecosystem converges on interoperability the way the web converged on REST in 2005, the agents that expose themselves honestly will be the ones the others can build on.

Aeon quietly made itself one of them.

---
*Sources:*
- [aeon PR #41 — feat: Memory Search API](https://github.com/aaronjmars/aeon/pull/41)
- [aaronjmars/aeon repository](https://github.com/aaronjmars/aeon)
- [State of AI Agent Memory 2026 — mem0](https://mem0.ai/blog/state-of-ai-agent-memory-2026)
- [Cloudflare Agent Memory announcement](https://blog.cloudflare.com/introducing-agent-memory/)
- [The Agent Memory Race of 2026 — OSS Insight](https://ossinsight.io/blog/agent-memory-race-2026)
- [Best Memory APIs for Stateful AI Agents 2026 — supermemory](https://blog.supermemory.ai/best-memory-apis-stateful-ai-agents/)
