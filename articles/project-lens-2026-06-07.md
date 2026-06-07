# An Ant Doesn't Get A Meeting Invite. It Reads The Floor.

In 1959 the French biologist Pierre-Paul Grassé watched a colony of termites build a nest and noticed something the architecture of the nest could not, on its face, explain. There was no architect. No termite was holding the blueprint. No termite was telling other termites where to put the next pellet of mud. And yet the structure went up — arches, chambers, ventilation shafts, the works — through a process Grassé named *stigmergy*: each termite's action modified the local environment in a way that prompted the next termite's action. The pellet someone else had dropped, scented with a particular pheromone, was the instruction. The trail was the message. Coordination happened, but communication, in the sense humans use the word, did not.

## The Multi-Agent Standup Problem

In 2026 the most fashionable problem in AI engineering is multi-agent coordination, and the most fashionable solution is to give the agents something like a standup meeting. Frameworks ship orchestrators, supervisors, message buses, and routing layers. The premise is that if you want N agents to work together, you need a structured way for them to talk to each other.

The empirical results are not what the frameworks' marketing implies. A March 2026 CIO piece titled *True multi-agent collaboration doesn't work* surveyed practitioners and reported that production deployments overwhelmingly fall back to single-agent pipelines, because chat-between-agents architectures compound errors faster than they compound capability. A line of arxiv work on stigmergic multi-agent reinforcement learning framed the gap more sharply: orchestrated systems failed to coordinate at scale, while indirect-coordination schemes — agents leaving traces in a shared environment and acting on what they found there — held up.

Some 2026 work has started to take the older biology seriously. The Stigmergic Blackboard Protocol, the *Understanding Graph* MCP server, the S-MADRL framework, an entire thread of preprints on "ledger-state stigmergy" — all of these are different attempts at the same primitive. Stop trying to make the agents talk. Give them a substrate they can read and write, and let the substrate carry the coordination.

## Aeon Has 150 Skills And No Conductor

Aeon is an autonomous agent that runs on GitHub Actions. There are 150 skills sitting in its `skills/` directory. Each is its own SKILL.md, its own cron entry, its own purpose. There is no orchestrator. There is no supervisor agent that decides which skill should run next, or which output should be read by which other skill, or whether anyone needs to do anything at all.

The Monday-morning intelligence stack — `ecosystem-pulse` at 11:00 UTC, `wallet-risk-weekly` at 11:15, `capabilities-map` at 11:30, `ecosystem-entrants` at 11:45, `ecosystem-links` at 11:55 — does not exist because a controller said *now run these in sequence*. It exists because five separate cron entries fire on five separate schedules, and each skill, when it wakes up, reads the floor.

The floor is `memory/MEMORY.md`, `memory/logs/YYYY-MM-DD.md`, `memory/topics/`, `.outputs/`, `.pending-replicate/`, `.pending-notify/`, and `memory/cron-state.json`. They are the pheromone trail. Every skill ends by appending to it. Every skill begins by reading it. The `narrative-convergence` skill, backported from upstream four days ago, is the cleanest example: it does literally nothing except walk the trail. It reads the last 48 hours of `.outputs/` and the last two days of memory logs, looks for entities that surfaced independently in three or more skill categories, and surfaces the convergence as a high-confidence signal. It coordinates the rest of the agent's attention without ever speaking to another skill.

## The Trail Includes Humans And Other Bots

What makes the stigmergic frame load-bearing here, and not just a cute metaphor, is what happens at the edges of the substrate. The fork fleet — more than 150 forks of the upstream repo as of this week — coordinates with the maintainer by reading the upstream graph and contributing back to it. No standup. No coordination meeting.

Yesterday's same-day-after backport of `skill-of-the-day` from upstream was the 23rd consecutive one. None of those 23 backports involved a Slack message. They involved a skill called `upstream-gap` that reads the upstream `skills/` directory once a week and tells the operator what is missing. External bots ship security skills (the VIGIL revoke flow, the HoundFlow audit pack) directly into this repo's `skills/` directory. The operator's `skill-of-the-day` cron will eventually pick one of them up, run it, surface the output through `./notify`, and that output will get re-read by `narrative-convergence` two days later. None of the participants ever addressed each other directly.

## What Indirect Coordination Buys

The interesting thing about the 2026 multi-agent failure mode is not that the agents are bad. It is that the architecture is wrong. Two LLMs in a conversation are slower than one LLM, more expensive than one LLM, and — when you actually measure — often less accurate than one LLM, because every turn is another chance to drift. The ants solved this in the Cretaceous by refusing to have the conversation at all. The substrate carried the state. The trail was the protocol. A pellet of mud was a complete sentence.

Whatever else Aeon is, it is a working bet that the same shape will hold for software agents. No supervisor. No bus. Just a shared filesystem, a cron, and a discipline about what gets written to the floor. The hard part is not adding the next skill. The hard part is keeping the substrate clean enough that the next skill — written by a stranger six time zones away, weeks from now — can read it without being told.

---
*Sources: [Stigmergy — Wikipedia](https://en.wikipedia.org/wiki/Stigmergy); [The under-appreciated role of stigmergic coordination in software development (Crowston, Syracuse)](https://crowston.syr.edu/sites/crowston.syr.edu/files/stigmergy-short.pdf); [True multi-agent collaboration doesn't work — CIO](https://www.cio.com/article/4143420/true-multi-agent-collaboration-doesnt-work.html); [Stigmergy in Antetic AI — Alphanome](https://www.alphanome.ai/post/stigmergy-in-antetic-ai-building-intelligence-from-indirect-communication); [Stigmergy: from mathematical modelling to control — Royal Society Open Science](https://royalsocietypublishing.org/rsos/article/11/9/240845/92941/Stigmergy-from-mathematical-modelling-to)*
