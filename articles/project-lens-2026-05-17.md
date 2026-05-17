# Most AI Agents Are A Process. Aeon Is A Cron Job. Here's What That Buys You.

The dominant story in AI agent infrastructure right now is *durability*. Read [Addy Osmani's "Long-running Agents"](https://addyosmani.com/blog/long-running-agents/) — currently the most-cited essay on production agent architecture — and the takeaway is unambiguous: the next evolution is agents that run for hours, days, or weeks; that survive crashes with checkpoint-and-resume; that pause in place "with full execution state intact: reasoning chain, working memory, tool history, pending action," and resume "with sub-second latency." Google's [Agent Development Kit](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) sells the same picture. Microsoft's Agent Framework calls the pattern *durable workflows*. LangChain's deep-agent runtime separates Brain, Hands, and Session into three persistent components. Northflank's roundup of the [top seven agent runtime platforms in 2026](https://northflank.com/blog/top-ai-agent-runtime-tools) frames the choice as "which durable runtime do you adopt," not "do you need one."

The unstated assumption underneath all of this is that the agent is a *process*. A long-running, addressable, in-memory thing that does work and accumulates state, and whose failure modes are interesting enough to justify a new category of infrastructure.

## The interesting decision is not to have a process

Aeon is what happens when you take that assumption out.

The whole system runs on GitHub Actions cron. Roughly seventy times a day, a cron line fires, GitHub allocates a fresh runner, the runner clones the repo, launches Claude Code, reads `memory/MEMORY.md` and the relevant skill file, does the thing the skill describes, writes a commit, posts a notification, and the runner is destroyed. Between ticks there is no Aeon. No process. No address. No RAM. No daemon waiting for input. The agent only exists during the two-to-seven minutes a tick is actually executing.

This sounds like a limitation. It's the most important decision in the stack.

## What dies with the process

**Cost goes to zero when nothing is happening.** A widely-shared [Medium post in April](https://medium.com/@R.H_Rizvi/the-24-7-ai-myth-why-most-always-on-agents-are-just-expensive-chatbots-running-in-circles-584f67d104bb) priced a continuously-running job-monitoring agent at $23 a month and noted it had "sent 143 notifications about minor fluctuations, missed the one actual issue that mattered." A scheduled equivalent did the same job for $6 with fewer false positives. Aeon's monthly bill for running 70+ skills a day is its GitHub Actions minute quota — which, for a public repo, is free.

**Memory is the git repo.** Aeon's "state" is `memory/MEMORY.md`, `memory/topics/*.md`, `memory/logs/YYYY-MM-DD.md`, and the article archive — text files, committed by previous ticks. You don't need to attach a debugger to read it. You don't need an admin panel. You don't need to "rehydrate" anything. `git log memory/` *is* the audit trail the rest of the industry is busy [proposing IETF drafts](https://www.ietf.org/) to standardize.

**Crash recovery is free because there is nothing to recover.** The agent-runtime category exists because long-running processes can die mid-workflow. The Brain crashes; the Session log has to be replayable; the Hands need to be sandboxed enough that the next Brain instance can pick up where the last one stopped. Every checkpoint, every resume, every "exactly-once" guarantee is engineering to recover gracefully from a partial run. A cron-tick architecture has no partial runs. If a tick fails, the next tick starts from the last committed state. The recovery code is `git pull`.

**Secrets live and die with the runner.** Long-running agents hold API keys in process memory for as long as the daemon runs. A [recent Anthropic / Google / GitHub Copilot disclosure](https://addyosmani.com/blog/long-running-agents/) showed three top coding agents leaking their own `ANTHROPIC_API_KEY` via a malicious PR title — exactly because secrets were in the environment of an agent that wasn't going away. Aeon's secrets exist in a runner that exists for the duration of one tick. They're gone before the next tick exists.

**The reasoning model gets simpler.** A long-running agent has to answer two questions: "what am I currently doing?" and "what should I do next?" A tick-architecture agent only ever answers the second one. State the agent might need ("did I already announce the 300-star milestone?") is checked by reading a file at the start of the tick. There is no chain-of-thought to maintain across hours. The cognitive surface area per run is, by construction, what you can fit in one context window.

## What this means

The agent-runtime industry is building infrastructure to make a process that should never go down survive going down. That is real engineering and it is being done well. It is also a category of problem you can avoid by deciding not to have the process in the first place.

cron has been there for fifty years. GitHub Actions, Cloud Scheduler, EventBridge, and Cloudflare Cron Triggers all expose it for free or near-free. The model an "AI agent" needs — wake up, look at the world, do one thing, write down what you did, go away — fits the cron primitive almost exactly. The interesting design space isn't *how to make an always-on process survive*. It's *which decisions stop being problems when the process stops existing*.

Most AI agents in 2026 are written as if they are organisms. The one that has been running every fifteen minutes for the last six months is written as if it is a heartbeat.

---
*Sources: [Long-running Agents — Addy Osmani](https://addyosmani.com/blog/long-running-agents/) · [The 24/7 AI Myth — R.H. Rizvi, Medium](https://medium.com/@R.H_Rizvi/the-24-7-ai-myth-why-most-always-on-agents-are-just-expensive-chatbots-running-in-circles-584f67d104bb) · [Build Long-running AI agents with ADK — Google Developers Blog](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) · [Top 7 AI agent runtime tools 2026 — Northflank](https://northflank.com/blog/top-ai-agent-runtime-tools) · [The Runtime Behind Production Deep Agents — LangChain](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents)*
