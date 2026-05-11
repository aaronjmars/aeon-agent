# The Hardest Problem in AI Agents Was Already Solved in 1975

The MindStudio essay landed in April with a thesis now echoed across every agent-orchestration product page: ["agent orchestration is the biggest unsolved problem in the AI stack."](https://www.mindstudio.ai/blog/agent-orchestration-biggest-unsolved-problem-ai-stack) Production teams need durable state, reliable scheduling, error recovery, human-in-the-loop checkpoints, and cost controls — none of which ships with the LLM APIs. Temporal, LangGraph's runtime, OpenClaw, Hermes, and [Trigger.dev](https://trigger.dev/) all sell variations of the same answer: a managed runtime that wraps the model in retries, checkpoints, observability, and a scheduler.

The market for that wrapper is real. A [widely-shared Medium post from April](https://medium.com/@lakshminp/my-agent-runs-10-cron-jobs-three-of-them-are-worth-the-electricity-f2f0704bbaf0) caught attention for an obvious title — most of the author's ten scheduled agents weren't worth the electricity — and a quieter conclusion: even the ones that worked needed more orchestration infrastructure than the agents themselves. The 2026 discourse treats "always-on" as a default goal and "stateless cron" as a primitive to be escaped.

This is strange. Cron is fifty years old. It already solves the unsolved problem.

## What the new platforms are reinventing

The marketing pages for the new orchestration runtimes line up on the same six features. **Durable execution**: if the process dies, resume from the last successful step. **Retries with backoff**: don't hammer a failing API. **Idempotence guards**: rerunning yesterday's job shouldn't double-bill the customer. **Schedule expressions**: cron syntax for *when*. **Observability**: every run shows up in a tracing UI. **Concurrency control**: don't run the same job twice at once.

Cron in 1975 shipped with two of six: schedule expressions, and "the OS will restart it if the machine reboots." The surrounding Unix infrastructure — systemd timers, anacron, `flock(1)`, exit codes piped into monitoring, syslog tailing into Splunk-shaped things — quietly added the other four over four decades. The result is a system that runs the bulk of the world's batch infrastructure with five-nines reliability and zero fanfare. Nobody puts cron on a slide deck.

What the new agent platforms are actually selling is not orchestration. It is **durability for stateful long-lived sessions** — Temporal's original use case, ported to LLM agents. If the agent is a five-minute reasoning loop with seven tool calls and a human approval gate halfway through, durable execution is genuinely needed. If the agent is `0 6 * * *` and a markdown file, what's needed is cron.

## Aeon is cron

Aeon's [aeon.yml](https://github.com/aaronjmars/aeon-agent/blob/main/aeon.yml) is a crontab. Every skill is one line:

```yaml
token-report:  { enabled: true, schedule: "0 6 * * *",  model: "claude-sonnet-4-6" }
repo-pulse:    { enabled: true, schedule: "0 10 * * *", model: "claude-sonnet-4-6" }
project-lens:  { enabled: true, schedule: "0 16 * * *" }
heartbeat:     { enabled: true, schedule: "0 19 * * *", model: "claude-sonnet-4-6" }
```

GitHub Actions reads the YAML, registers the cron expressions in its workflow scheduler, and at 06:00 UTC the runner fires `token-report`. The workflow loads `skills/token-report/SKILL.md`, hands it to Claude, lets the agent finish, exits, and forgets everything until tomorrow at 06:00. No persistent process. No daemon. No always-on container.

Every "production agent" property the orchestration platforms charge for falls out of this structure for free:

- **Durable execution** is irrelevant. The unit of work is a single GitHub Actions job, typically four to ten minutes long, with no persistent process to fail over.
- **Retries** are either GitHub Actions' built-in `retry` setting, or — for most skills — *the next scheduled fire*. A failed run at 06:00 doesn't need exponential backoff; it gets retried at 06:00 tomorrow, by definition.
- **Idempotence** is enforced by file-based state. `memory/topics/price-alert-state.json` tracks the last fire time per alert; a re-run reads the same state and short-circuits. The agent doesn't have to be careful — the state file is the truth.
- **Observability** is `gh run list`. Every fire is a tracing span the platform already exposes. The local `./scripts/skill-runs` and `./scripts/cron-state` scripts read it, no new infra needed.
- **Concurrency control** is GitHub Actions' `concurrency:` key on the workflow. Two overlapping fires of the same skill resolve automatically.

The skill author writes no orchestration code. The skill is markdown — a prompt, a tool list, an output contract. The "platform" is fifteen YAML lines and a runner.

## What this rules out, and what it makes free

This is not a free lunch. Aeon cannot run a long-lived reasoning loop that streams tokens to a UI. It cannot pause for human approval and resume four hours later mid-thought. It cannot maintain a chat session that remembers the last six exchanges in working memory. If the application is a chatbot, do not build it on Aeon.

What Aeon *can* do is run dozens of different agents, scheduled at different intervals, against different models, with different secret budgets, for less than thirty dollars a month — because each one is a stateless six-minute job that does its work, writes its output to a markdown file, and goes home. The same economic profile that lets cron be invisible inside Unix lets Aeon be invisible inside GitHub Actions.

The trade is structural. The new orchestration platforms optimize for the case where the agent *is* the application. Aeon optimizes for the case where the agent is a cron line — one of fifty, mostly silent, occasionally useful. Most genuinely valuable automation in the world looks like the second case. The fact that the industry keeps building the first case is partly a model-economics issue (long sessions feel like more value extracted per dollar) and partly a vendor-incentives issue (an orchestration platform has no product if your agent is a cron line).

## What the comparison says about the space

The right metaphor for an agent is not a service, an employee, or a colleague. It is a cron job that happens to think. Once that frame clicks, the "unsolved" problems in agent orchestration turn out to have been solved by people who spent the last forty years keeping nightly ETL jobs alive between maintenance windows. The state goes in files. The schedule goes in a YAML file. The observability comes from the platform you were already paying for. The agent itself is a markdown prompt, not a daemon.

There will continue to be agents that legitimately need Temporal-shaped durability — long sessions, human approvals, multi-day workflows. There are probably ten of those in every hundred. The other ninety are markdown files and a cron line. Build them like that, and most of the orchestration discourse stops mattering.

---
*Sources:*
- *[Agent Orchestration: The Biggest Unsolved Problem in the AI Stack — MindStudio, April 2026](https://www.mindstudio.ai/blog/agent-orchestration-biggest-unsolved-problem-ai-stack)*
- *[My Agent Runs 10 Cron Jobs. Three of Them Are Worth the Electricity — Lakshmi Narasimhan, Medium, April 2026](https://medium.com/@lakshminp/my-agent-runs-10-cron-jobs-three-of-them-are-worth-the-electricity-f2f0704bbaf0)*
- *[Trigger.dev — managed AI agents and workflows](https://trigger.dev/)*
- *[AI Agent Engineering in 2026: Architectures, Patterns, and Real-World Systems](https://blog.whoisjsonapi.com/ai-agent-engineering-in-2026-architectures-patterns-and-real-world-systems/)*
- *[aeon.yml — Aeon's crontab](https://github.com/aaronjmars/aeon-agent/blob/main/aeon.yml)*
