# Every Agent Platform Promises Faster Restarts. One Framework Made Them Mandatory.

In May, a technical post on AI agent production failures circulated through engineering Slack channels. The line that got quoted most was the bluntest: "The demos are perfect. The deployments are not." What followed was a mathematical argument: if an autonomous agent executes an eight-step workflow and each step succeeds 85% of the time, the probability of completing the full workflow correctly is [27%](https://www.inovabeing.com/blog/ai-agent-reliability-production-failure-2026). Most teams building agents test individual steps. Almost nobody stress-tests compound failure.

The infrastructure industry heard "reliability problem" and concluded "better infrastructure." The leading argument now is that [serverless architecture is fundamentally unsuitable for agents](https://thenewstack.io/serverless-cloud-architecture-is-failing-modern-ai-agents/): AWS Lambda caps execution at 15 minutes, Azure Functions at 230 seconds. Stateful agents lose context when the runtime resets. The proposed fix is [micro-VMs — Firecracker-based sandboxes that resume execution in under 25 milliseconds](https://blaxel.ai/blog/serverless-vs-containers-vs-micro-vms-ai-agents) with in-memory state intact, as if the pause never happened. Better cold start, the argument goes, produces better reliability.

This is the right answer for one specific kind of agent. It is the wrong diagnosis for a different, growing kind — and the distinction matters more than any infrastructure benchmark.

## What persistent state actually costs

The compound failure problem in that reliability analysis is not about cold starts. It is about error propagation. In a persistent-server agent, each step inherits the in-memory state of every step that preceded it. When step three makes a mistaken assumption, step four builds on it. By step eight, the original error has been amplified through five subsequent decisions — each one reasonable given the inherited context, each one wrong given the original mistake.

The infrastructure response — preserve state faster and more reliably across runs — treats this as an execution problem. But the compounding happens precisely because state is continuous. A sub-25ms micro-VM resume delivers the inherited context faster. It does not change what the agent inherits, or whether that context is accurate.

## The inversion

There is a class of agent that sidesteps this failure mode not by preserving state better, but by resetting deliberately.

[aaronjmars/aeon](https://github.com/aaronjmars/aeon) (538 stars, 186 forks) runs on GitHub Actions cron schedules. Every skill fires as a separate job, boots a fresh environment from the repository's current git state, executes, and — if successful — commits its outputs back to the repository. There is no in-memory state between runs. The only state that persists is state that was explicitly committed.

This is enforced by `aeon.yml`, which defines each skill's cron schedule. The cold start is not a performance limitation being tolerated; it is the mechanism that produces the property the reliability industry wants. An agent cannot carry a stale or corrupted assumption forward if it must reload from a committed checkpoint on every run.

The read-before-act instruction in `CLAUDE.md` makes this concrete: at the start of every task, the agent reads `memory/MEMORY.md` and checks `memory/logs/` for recent activity. Those files are committed artifacts. The agent's working context is not what it happened to hold in memory from the previous run — it is the git-committed record of what it reported last time. If a run produced incorrect output, the next run reads incorrect committed memory. But that error is isolated, visible in the diff, and revertable with a single git revert.

## What the commit produces that benchmarks don't capture

Micro-VM benchmarks measure resume time (under 25ms), isolation overhead (Firecracker requires less than 5 MiB per VM), and memory compression (OverlayFS can reduce overhead by 75%). These are real engineering gains for interactive workloads where humans are waiting on responses.

What they do not produce is a run that is independently verifiable after the fact. Each Aeon run produces a git commit. That commit includes the outputs — `memory/logs/YYYY-MM-DD.md`, articles, analysis — alongside a SHA computed from every file the commit touched. Git's content-addressed storage makes retroactive modification structurally impossible without invalidating the hash chain. Two runs that started from identical git trees and executed the same skill can be diffed against each other. Three months from now, it is possible to reconstruct exactly what state the agent operated from, what it produced, and where it diverged.

When logbookbase, an external contributor, registered their live instance this week (`9a97ae9` — "ecosystem: add logbook"), the addition was a pull request into `ECOSYSTEM.md`. The registry of live instances is a committed artifact, not a database entry. Every instance arrived via a commit with an author, a timestamp, and a hash. The record of who's running what is verifiable by the same mechanism as the record of what any single run produced.

## What this implies for the market

The agent hosting market will segment within 18 months along a line most current benchmarks don't track: scheduled autonomous agents versus low-latency interactive agents.

Micro-VM platforms are building the right infrastructure for customer-service workflows, real-time decision loops, and anything where a human is waiting on a response. For that category, sub-25ms resume time is material and state continuity is the correct trade-off.

Autonomous scheduled agents — the category that runs nightly research digests, monitors codebases, executes analysis on a timer, or self-publishes content — have a different cost function entirely. Latency is measured in minutes, not milliseconds. The properties that matter are: can you verify what the agent did? Can you revert a bad run? Can you see, at commit granularity, exactly what state the agent operated from before it produced an output?

The platforms building micro-VM infrastructure will offer audit trails as a premium feature by 2027, because their architecture requires a separate logging layer to produce them. The cron-based framework produces them as a side effect of running. The cold start was never the problem — it was the solution waiting for the right framing.

---
*Sources:*
- [AI Agent Reliability in Production 2026 — INovaBeing (May 15, 2026)](https://www.inovabeing.com/blog/ai-agent-reliability-production-failure-2026) — 27% compound completion rate for 8-step workflows at 85% per-step reliability; "the demos are perfect, the deployments are not"
- [Serverless vs. Containers vs. Micro-VMs for AI Agents — Blaxel (April 20, 2026)](https://blaxel.ai/blog/serverless-vs-containers-vs-micro-vms-ai-agents) — Firecracker resume under 25ms, AWS Lambda 15-minute cap, AWS resets state on timeout, Firecracker memory overhead under 5 MiB
- [Serverless Cloud Architecture Is Failing Modern AI Agents — The New Stack (June 2026)](https://thenewstack.io/serverless-cloud-architecture-is-failing-modern-ai-agents/) — framing of persistent-state agents vs serverless failure modes
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — `aeon.yml` cron schedule enforcement, `CLAUDE.md` read-before-act pattern, `memory/logs/YYYY-MM-DD.md` committed output format, `ECOSYSTEM.md` live-instance registry, commit `9a97ae9`
