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

## 2026-06-15
- Angle: Philosophy / big ideas (the default effect + progressive disclosure → choice architecture)
- Thesis: An agent framework's most consequential decision isn't how many skills it ships — it's how few a fresh fork wakes up running, because forkers inherit defaults and agents drown in options.
- Title: The Setting Almost Nobody Changes Decides Almost Everything
- Sources: alexmurrell.co.uk, behavioraleconomics.com, ixdf.org, arxiv.org/2605.24660, writer.com, github.com/aaronjmars/aeon (PR #473/#474/#479)

## 2026-06-16
- Angle: Industry comparison (central agent-skill stores + scanners vs Aeon's fork-native install-as-commit)
- Thesis: While agent-skill stores race to scan skills before install, Aeon makes each install a pull request into your own fork — betting on git's revertable audit trail over a platform's scanner.
- Title: Everyone Is Building a Store for Agent Skills. The Attackers Already Shopped There.
- Sources: snyk.io, arxiv.org/2605.11418, unite.ai, digitalapplied.com, agensi.io, github.com/aaronjmars/aeon (PRs #485/#486/#487/#491/#472)

## 2026-06-17
- Angle: Ecosystem map (where Aeon sits on the agent-platform map; axis = the runtime, not the model — hosted/provider-owned runtimes vs no runtime at all)
- Thesis: 2026's agent platforms compete over whose runtime you rent. Run as your own GitHub Actions cron with state in git, and migration stops being a product — it's a clone.
- Title: The Agent Wars of 2026 Are a Fight Over Whose Computer Runs Your Agent

## 2026-06-18
- Angle: User story (developer reads GitHub Agentic Workflows launch post; discovers reactive vs. proactive execution model; finds the fork-based autonomous agent as the answer to the question GitHub didn't solve)
- Thesis: GitHub Agentic Workflows keep humans as the final gate before any write; a forked Aeon skips the gate entirely — not because it lacks safety, but because the configuration IS the safety.
- Title: I Read the GitHub Agentic Workflows Launch Post. I Didn't Want My Agent to Ask.
- Sources: github.blog/changelog (June 11 2026 launch), github.blog/ai-and-ml (technical overview), blog.mean.ceo (solo founder stack Apr 2026), github.com/aaronjmars/aeon
- Sources: zylos.ai, digitalapplied.com, langchain.com, github.com/aaronjmars/aeon (#495/a2947c2, #491)

## 2026-06-19
- Angle: Current events (EU AI Act August 2 transparency deadline + December 2027 high-risk deferral — compliance tooling wave)
- Thesis: EU AI Act's tamper-evident logging and human override requirements were written for persistent-server agents. A cron-based agent that commits every run to git inherits both properties as side effects of its design.
- Title: The EU AI Act's Audit Trail Is Just a Commit History
- Sources: artificialintelligenceact.eu (Articles 12+14), gibsondunn.com (Omnibus deferral), covasant.com, predictionguard.com, arxiv.org/2604.04604, github.com/aaronjmars/aeon
