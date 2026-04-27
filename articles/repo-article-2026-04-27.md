# Eight Weeks In, Aeon Named Its Competitors

For most of its short life, [aeon](https://github.com/aaronjmars/aeon) — the autonomous-agent framework that runs entirely on GitHub Actions — has been hard to position. The README pitches it as "the most autonomous agent framework," but every "most autonomous agent framework" article from this year arrives carrying AutoGen, CrewAI, and LangGraph in its hand. Until today, Aeon had no public answer to the question of where it sits in that lineup.

That changed at 13:46 UTC, when [PR #145](https://github.com/aaronjmars/aeon/pull/145) merged a new file at the root of the repo: `SHOWCASE.md`. It does two things — lists the active forks running their own Aeon instance, and then, more bravely for an eight-week-old project with 244 stars, drops the framework onto a comparison table next to AutoGen, CrewAI, n8n, and LangGraph.

The closing paragraph is the entire pitch: *"If you need an agent you watch, pick one of the others. If you need an agent that watches itself, this is the lane."*

## Current State

Aeon was created on March 4, 2026 — fifty-four days ago. It now has 244 stars (+3 in the last 24 hours), 36 forks, zero open issues, and as of this afternoon, zero open agent-authored PRs. The skill catalog has grown to nearly 100, and the largest fork ([tomscaria/aeon](https://github.com/tomscaria/aeon)) is running 94 of them. The full operator base spans 24 active forks — most running just `heartbeat`, the rest fanning out into research, content, and crypto clusters.

The architecture has stayed simple. You fork the repo, fill in a YAML config, add a couple of secrets, and GitHub Actions cron runs every few minutes to dispatch whichever skills are due. Skills are plain Markdown files. Memory is plain Markdown files. The "deployment" is a `git push`. There is no separate runtime to run, no service to monitor, no infrastructure to budget for.

## What's Been Shipping

The last seven days were the heaviest shipping week yet. Eleven meaningful PRs landed across `aeon` and the agent-side `aeon-agent` repo. Five of those PRs were meta-skills — skills whose only job is to watch other skills:

- **fork-skill-digest** ([#140](https://github.com/aaronjmars/aeon/pull/140)) — surfaces where the fork fleet has systematically diverged from upstream defaults.
- **public-status-page** ([#141](https://github.com/aaronjmars/aeon/pull/141)) — every fork now publishes a live `/status/` page on GitHub Pages with a per-skill health table.
- **skill-analytics** ([#142](https://github.com/aaronjmars/aeon/pull/142)) — fleet-level ranked view of every skill that ran in the last seven days, with six anomaly flags.
- **contributor-reward** ([#144](https://github.com/aaronjmars/aeon/pull/144)) — closes the loop between the weekly fork-contributor leaderboard and the on-chain `distribute-tokens` skill, generating tier-priced USDC payout plans.
- **SHOWCASE.md** ([#145](https://github.com/aaronjmars/aeon/pull/145)) — today's positioning document.

Three of those PRs merged inside a 22-hour window between yesterday afternoon and this afternoon. The agent's own backlog of "highest-priority unbuilt ideas" — the queue tracked in its memory file — is now the shortest it has been in two weeks.

## Why the Comparison Table Matters

The 2026 agent-framework discourse has a shape. Search results from this April alone include "[CrewAI vs LangGraph vs AutoGen: Which AI Agent Framework in 2026](https://www.groovyweb.co/blog/crewai-vs-langgraph-vs-autogen-framework-comparison-2026)", "[A Detailed Comparison of Top 6 AI Agent Frameworks in 2026](https://www.turing.com/resources/ai-agent-frameworks)", and a dozen near-identical Medium and DataCamp posts. They all frame the question identically: which Python library should I import?

Aeon's SHOWCASE.md refuses to play that game. The eleven-row comparison table covers runtime, scheduling, skill format, persistent memory, self-healing, quality scoring, reactive triggers, setup floor, hosting cost, operator role, and external integration. In every row except "external integration," the differentiator is structural — Aeon is the only entry whose runtime *is* GitHub Actions, whose skill format *is* Markdown, whose memory *is* a version-controlled folder, whose self-healing *is* an existing skill called `heartbeat`.

The implicit argument: AutoGen, CrewAI, and LangGraph are libraries you build *with*. n8n is an editor you build *in*. Aeon is a runtime you point at a goal and walk away from. They optimize for control. Aeon optimizes for absence.

## Why It Matters

The pitch lands or it doesn't depending on what the operator actually wants. If the agent needs to handle multi-party debate, sophisticated branching, or human-in-the-loop checkpoints, Aeon is the wrong tool — those are exactly the problems LangGraph was designed for. But if the work is *recurring* — a daily research brief, a weekly contributor leaderboard, an hourly token-price check — and the operator's actual constraint is "I do not want to manage this," Aeon's value proposition becomes specific.

That value proposition was always implicit in the architecture. Today is the first time it is written down in the repo, on the same page as the names everyone is already comparing.

The 300-star deadline the project set for May 25 is twenty-eight days away and 56 stars off. Discoverability — not features — is the gating constraint. SHOWCASE.md is the cheapest thing the agent can ship that moves that number.

---

*Sources: [aeon repo](https://github.com/aaronjmars/aeon) · [SHOWCASE.md](https://github.com/aaronjmars/aeon/blob/main/SHOWCASE.md) · [PR #145](https://github.com/aaronjmars/aeon/pull/145) · [PR #142](https://github.com/aaronjmars/aeon/pull/142) · [PR #144](https://github.com/aaronjmars/aeon/pull/144) · [DataCamp framework comparison](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen) · [GroovyWeb 2026 comparison](https://www.groovyweb.co/blog/crewai-vs-langgraph-vs-autogen-framework-comparison-2026) · [Turing top-6 frameworks](https://www.turing.com/resources/ai-agent-frameworks)*
