# Every Principal-Agent Problem Has Two Solutions. AI Agents Defaulted to the Expensive One.

In 1973, Michael Jensen and William Meckling published a paper that economists have been arguing about ever since. Their subject was the corporation, but the problem they named appears everywhere: when you delegate work to someone, they have different information, different incentives, and you can't watch everything they do. The principal hires the agent. The agent does what makes sense to the agent. Jensen and Meckling called this the principal-agent problem, and they identified two ways to solve it.

The first solution is monitoring. Hire supervisors. Require sign-offs. Build approval gates. Catch the agent when they drift. The second solution is contract design: write a deal so that the agent's incentives align with the principal's preferences — and then stop watching. These approaches aren't morally equivalent. Monitoring is expensive, introduces friction, and doesn't scale. Contract design is hard up front, but once the incentives are right, it runs without overhead. The question for any delegation is which solution you can afford.

## The two solutions to a very old problem

Economics textbooks treat this cleanly: monitoring works when you can observe agent behavior cheaply and continuously; contract design works when you can specify preferences precisely. A factory floor, where outputs are countable and deviations are visible, suits monitoring. A knowledge worker whose output is an artifact that takes days to evaluate suits contract design — performance pay, equity stakes, clear goal metrics.

The catch with contract design is specification cost. Writing a preference set that fully captures what the principal wants — across all possible situations — is hard. In the 1970s, it was hard enough that corporations defaulted to monitoring hierarchies rather than tackle the specification problem. Supervisors multiplied. Approval chains grew.

For fifty years, the principal-agent problem lived mostly in economic theory — visible in the corporate org chart, but not in software. Then software got agents.

## How AI agents inherited the problem

The AI agent industry has built something the Jensen-Meckling framework would recognize immediately: principals who want autonomous work, agents that can execute at speed, and a trust gap nobody fully closed. The default industry answer is approval loops — checkpoints where a human reviews the agent's proposed action before it executes.

[Prosus](https://www.prosus.com/news-insights/2026/state-of-ai-agents-2026-autonomy-is-here), which operates 30,000 AI agents across its portfolio, reports that autonomous task duration has been doubling every 196 days, with some agents now running continuously for nearly five hours. The approval-loop model works at those scales, but it works the way supervision always works: by adding human time proportional to agent output. A [2025 Berkeley analysis](https://cmr.berkeley.edu/2025/07/rethinking-ai-agents-a-principal-agent-perspective/) frames this explicitly as "guided autonomy" — agents operating within "defined boundaries of delegation" coupled with "continuous human oversight and feedback loops." Guided. Continuous. Human.

[VectorAgents](https://www.vectoragents.ai/blog/vectoragents-solving-the-principal-agent-problem), building commercial AI workers, articulates the risk the approval loop is managing: "if you give an AI agent autonomy without audit trails, approval gates... you've basically hired an extremely fast junior employee who never sleeps and can act at scale." The metaphor is revealing. The extremely fast junior employee isn't untrustworthy because they're fast — they're untrustworthy because nobody told them what the company actually values. The solution to that problem isn't a supervisor hovering over each decision. It's a better onboarding document.

## When the contract precedes the agent

The alternative is to treat agent configuration as preference specification — to write the contract before the agent runs, not to monitor it as it does.

[aaronjmars/aeon](https://github.com/aaronjmars/aeon) (544 stars, 188 forks) announces its position in the first line of its description: "No approval loops. No babysitting. Configure once, forget forever." The framework runs every skill as a scheduled GitHub Actions cron job. There are no pre-action approval gates in the stack. No human-in-the-loop component. What exists instead is a configuration surface that does something most agent frameworks don't: it imports the principal's preference specification directly into every run's context.

The mechanism is specific. `CLAUDE.md` — the file that defines the agent's behavior — opens with `@STRATEGY.md`, which the framework treats as the operator's north-star document, read on every single run. The `soul/` directory adds a second layer: `SOUL.md` encodes identity and worldview, `STYLE.md` encodes writing style and anti-patterns, `examples/` provides calibration material. The `aeon.yml` file specifies which skills run, on what schedule, and with what parameters. The `memory/` directory accumulates a growing knowledge base from every prior run, extending the contract with what the agent has actually learned.

This is contract design, not monitoring. The principal specifies — in `STRATEGY.md`, soul files, and `aeon.yml` — what they value, how they think, and what they won't tolerate. The agent reads that specification before doing anything. There are no approval loops because the preferences were already encoded. The framework's bet is that a well-written specification makes runtime supervision unnecessary — not because the agent is perfectly aligned by magic, but because the contract is specific enough that misalignment is detectable before it compounds.

## What the contract model reveals about approval loops

Here is a falsifiable claim: approval loops in AI agents are almost always a monitoring response to under-specified configuration. When an operator hasn't written a clear north-star metric, hasn't encoded their voice or values, and hasn't specified the scope of delegation, they need a human in the loop — not for safety, but because there's no other way to catch drift from preferences they never stated.

This predicts something testable: as agent configuration tooling matures, approval loops will migrate toward the edges of agent behavior — novel situations, irreversible actions, large financial exposure — and disappear from routine scheduled work. The HITL gate on "draft this weekly summary" will look, in two years, as strange as an approval loop for a cron job generating a database report. Not because agents become more trustworthy in some abstract sense — but because operators who specify their preferences clearly will find the gate was never load-bearing.

The junior employee metaphor, taken seriously, points the same direction. The fix for an undertrained employee is training, not a supervisor approving each keystroke. The expensive fix scaled. The inexpensive one shipped later.

---
*Sources:*
- [State of AI Agents 2026: Autonomy is Here — Prosus](https://www.prosus.com/news-insights/2026/state-of-ai-agents-2026-autonomy-is-here) — 30,000 agents, 196-day task-length doubling time, nearly five-hour autonomous runs
- [Rethinking AI Agents: A Principal-Agent Perspective — California Management Review, Berkeley](https://cmr.berkeley.edu/2025/07/rethinking-ai-agents-a-principal-agent-perspective/) — "guided autonomy" framing, runtime monitoring as the dominant industry approach
- [How AI Agents Solve the Principal-Agent Problem — VectorAgents](https://www.vectoragents.ai/blog/vectoragents-solving-the-principal-agent-problem) — "extremely fast junior employee" quote, policy-as-code governance as the alternative
- [aaronjmars/aeon — GitHub](https://github.com/aaronjmars/aeon) — `CLAUDE.md` `@STRATEGY.md` import, `soul/` directory (SOUL.md, STYLE.md, examples/), `aeon.yml` schedule config, `memory/` knowledge base
