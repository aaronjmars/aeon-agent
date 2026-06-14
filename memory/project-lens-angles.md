# Project Lens — Angle History

Tracks angle categories and theses so they don't repeat within 14 days.

## 2026-06-13
- Angle: Technical deep-dive for non-technical readers (one architectural decision: the CI gate that recomputes a self-modifying agent's capability manifest)
- Thesis: A self-modifying agent can't be trusted to describe itself — so Aeon doesn't ask: a CI gate recomputes its capability manifest from source and rejects any self-authored PR that drifts.
- Title: A Self-Modifying Agent's Most Dangerous Output Is Its Own Capability List
- Sources: thenewstack.io, arxiv.org/2603.10060, arxiv.org/2601.05111, o-mega.ai, github.com/aaronjmars/aeon (PR #457)

## 2026-06-12
- Angle: Contrarian take (challenge the assumption that agent memory = vector database)
- Thesis: While the agent-memory industry standardizes on vector databases, Aeon keeps memory as git-committed markdown — trading millisecond retrieval for what those stores structurally can't offer: a blamable, revertable, forkable audit trail.
- Title: The Agent-Memory Race Is Optimizing the Wrong Thing
- Sources: agentmarketcap.ai, atlan.com, venturebeat.com, mem0.ai, github.com (aaronjmars/aeon)

## 2026-06-11
- Angle: Current events (June 2026 Claude outage / AI provider-concentration) → industry comparison
- Thesis: Multi-provider failover is sold as a gateway problem — but an agent that runs as a cron job gets it nearly free: a dead run just restarts on the next provider.
- Title: The Cheapest Place to Put AI Failover Isn't a Gateway
- Sources: thoughtworks.com, virtido.com, universal.cloud, ardanlabs.com, blog.cybelesoft.com, windowsnews.ai

## 2026-06-14
- Angle: Historical parallel (HTTP 402 "Payment Required" reserved in RFC 2068/1997, dormant ~29 years; concrete mechanism = card-fee arithmetic blocked sub-cent payments until agents + stablecoin rails made the fee smaller than the price)
- Thesis: HTTP 402 sat blank for 29 years because no human payer could afford a sub-cent charge; its first real users are agents paying agents — settling each inference call onchain.
- Title: The Status Code That Waited 29 Years for a Customer Who Wasn't Human
- Sources: developer.mozilla.org, dev.to, coinbase.com, coindesk.com (x2), github.com/aaronjmars/aeon (PR #419)
