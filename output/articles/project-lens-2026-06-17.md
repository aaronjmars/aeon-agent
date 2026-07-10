---
type: Article
---

# The Agent Wars of 2026 Are a Fight Over Whose Computer Runs Your Agent

Watch where the money went this year and you'd think the agent race was about intelligence. It wasn't. It was about real estate.

On February 5th, OpenAI launched [Frontier](https://zylos.ai/research/2026-04-05-ai-agent-ecosystem-fragmentation-platform-lock-in-portability), "end-to-end infrastructure for enterprises to build and manage AI agents" — hosted containers, a managed shell, networking for agent workloads. Soon after, Amazon shipped a Stateful Runtime Environment co-developed with OpenAI that runs natively inside Bedrock, holding session memory, tool state, and workflow history across long-running tasks. Anthropic put its own self-hosted sandboxes into [public beta on May 19th](https://www.digitalapplied.com/blog/ai-agent-deployment-saas-vs-self-hosted-hybrid-decision-matrix). LangChain rebranded its deployment product to [LangSmith](https://www.langchain.com/resources/ai-agent-frameworks) and built it to "ship and scale agents in production." Different companies, one product: a place for your agent to live that you do not own.

## Whoever owns the runtime owns the workflow

That sentence isn't mine — it's the load-bearing claim of an April 2026 survey of [agent platform lock-in](https://zylos.ai/research/2026-04-05-ai-agent-ecosystem-fragmentation-platform-lock-in-portability), and it reframes the whole fight. The model you call is swappable; routers like LiteLLM normalize a hundred of them behind one API. The runtime is not. It's where the agent's memory, tool state, and execution history accumulate — in a format native to that runtime and nowhere else.

The survey makes the trap concrete: an enterprise that builds a support agent on the OpenAI Stateful Runtime, with six months of customer history, "cannot move that agent to a Claude-based runtime without rebuilding its memory layer from scratch." No standard exists for migrating agent state between systems. Switching primary models alone runs 40–60 hours of retuning per workflow. The model was never the moat. The substrate the agent runs and remembers in is.

So the map of 2026 has a crowded center — five hyperscalers selling managed runtimes — and one corner almost nobody is standing in: don't sell a runtime at all.

## The framework with no runtime to rent

[aaronjmars/aeon](https://github.com/aaronjmars/aeon) is an autonomous-agent framework, 517 stars, that occupies that corner by construction. Its tagline is "configure once, forget forever," and the mechanism behind it is that there is no Aeon server. The agent runs as scheduled GitHub Actions — cron jobs in a repo you fork. When a task fires, GitHub spins up a runner, Claude Code executes the skill, the runner dies. There is no persistent process to host, meter, or lock you into, because the runtime is infrastructure you already had a free tier of.

Its memory is the same idea inverted. Where the hosted platforms store agent state in proprietary formats, Aeon's state is plain files committed to git: `memory/MEMORY.md` for standing context, `memory/logs/` for a dated activity trail, `articles/` for output. The thing the Stateful Runtime sells as a feature — persistent memory across runs — Aeon gets by reading a markdown file at the top of each job and committing an updated one at the end. The agent's brain is a directory you can `git clone`.

## Migration isn't a product here, because it's a clone

This is where the position earns itself, and it's easy to miss. On the hosted map, "portability" is a roadmap item — a thing vendors promise and a thing the lock-in survey says doesn't yet exist. On the fork-native map, portability isn't a feature anyone built. It's a side effect of the storage choice. Moving your agent, its six months of memory, and its full history to another machine is `git clone`. Forking someone else's running agent — their skills, their accumulated state — is the fork button.

This week's commit makes the point in miniature. Aeon shipped [`scripts/validate-pack.sh`](https://github.com/aaronjmars/aeon/pull/495) ([a2947c2](https://github.com/aaronjmars/aeon/commit/a2947c2)), a validator a skill author runs locally to check a community pack before opening a pull request — pure local, no network call, no service to phone home to. It pairs with an install path that lands third-party skills as commits in your own fork and defaults a fresh fork to a 13-skill Core ([#491](https://github.com/aaronjmars/aeon/pull/491)). Every piece assumes the thing the hosted platforms assume away: that the user owns the machine, the state, and the audit trail, so the framework never has to be trusted to hold them.

The cost is real and worth naming. A cron runner has cold-start latency a warm hosted container doesn't. You get no managed dashboard of running agents, no vendor SLA. For a high-frequency, low-latency agent loop, renting a hot runtime is the right call, and Aeon isn't pretending otherwise. The bet isn't that nobody should rent a runtime. It's that most people running an agent on a schedule are renting one they'll regret.

## The bill comes due on the way out, not the way in

Here's the claim specific enough to be wrong by mid-2027: the hosted-runtime model wins the next year on convenience and loses the year after on exit. [79% of enterprises](https://www.digitalapplied.com/blog/ai-agent-deployment-saas-vs-self-hosted-hybrid-decision-matrix) say they've adopted agents; 17% have one in production. When that gap closes and the production agents accumulate a year of state in formats no standard can move, the first public horror story — a team with eighteen months of agent memory stranded in a deprecated runtime — will do more for "run it on infrastructure you own" than any benchmark. If instead a real state-portability standard ships and the hyperscalers adopt it, the fork-native corner loses its whole point, and this reads as a bet that aged badly. I don't think they'll adopt it. Portability is the one feature a platform has no incentive to ship, because the lock-in is the business. The defensible position won't be whose runtime is fastest. It'll be whose agent you can carry out the door.

---
*Sources:*
- [Zylos — AI Agent Ecosystem Fragmentation: Platform Lock-In & Portability (Apr 5 2026)](https://zylos.ai/research/2026-04-05-ai-agent-ecosystem-fragmentation-platform-lock-in-portability) — "whoever owns the runtime owns the workflow," OpenAI Frontier (Feb 5), Amazon Stateful Runtime, the six-month state-migration trap, 40–60h model-switch retuning, LiteLLM routing
- [Digital Applied — AI Agent Deployment: SaaS vs Self-Hosted vs Hybrid 2026](https://www.digitalapplied.com/blog/ai-agent-deployment-saas-vs-self-hosted-hybrid-decision-matrix) — Anthropic self-hosted sandbox beta (May 19), LangSmith deployment rebrand, Gartner 79%/17% adoption-vs-production gap
- [LangChain — The best AI agent frameworks in 2026](https://www.langchain.com/resources/ai-agent-frameworks) — LangGraph/LangSmith built to "ship and scale agents in production"
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — GitHub Actions cron runtime, git-committed memory (`memory/`, `articles/`), `validate-pack.sh` (#495 / a2947c2), repo-scoped 13-skill Core (#491)
