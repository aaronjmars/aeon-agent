---
type: Article
---

# The Setting Almost Nobody Changes Decides Almost Everything

Print a country's organ-donor form so you're enrolled unless you tick a box to opt out, and roughly **90%** of people end up donors. Print the same form the other way — out unless you tick a box to opt in — and the number collapses to about **15%**. [The gap has been measured across countries for two decades](https://www.alexmurrell.co.uk/summaries/cass-sunstein-and-richard-thaler-nudge). The options are identical. The only thing that changed is which one was already selected.

This is one of the most durable findings in behavioral economics, and it has a name: the default effect. Richard Thaler and Cass Sunstein built a whole discipline — [choice architecture](https://www.behavioraleconomics.com/resources/mini-encyclopedia-of-be/choice-architecture/) — around the fact that the way options are arranged changes which ones get picked. When US employers made 401(k) auto-enrollment the default, [participation jumped from 49% to 86%](https://www.alexmurrell.co.uk/summaries/cass-sunstein-and-richard-thaler-nudge). The mechanism isn't quite laziness. It's a stack of forces: the friction of changing, the implied recommendation in whatever was chosen for you, the discomfort of giving up what you already hold, and the plain fact that most people never register that the choice was theirs to make.

## The real product is the part that ships switched on

Software inherited this physics decades ago. Jakob Nielsen named [progressive disclosure](https://ixdf.org/literature/topics/progressive-disclosure) in 1995: show the few things someone needs now, defer the rest until they ask. The point was never to hide power. It was that a screen with forty options and a screen with four can offer identical capabilities and produce completely different behavior — because the four-option screen tells you what matters, and almost no one digs past what they're shown.

So in any configurable system, the consequential decision isn't the size of the menu. It's the subset that ships already selected. That subset is what the median user actually runs, possibly forever. Everything else is a capability that exists in principle and in nobody's daily life.

## A framework spent a week deciding what its copies wake up doing

Which is why a quiet change in an open-source agent framework this week is more interesting than its commit log suggests. Aeon — a framework for running autonomous agents as scheduled GitHub Actions — spent the week of June 15 on something most projects treat as housekeeping: deciding what a fresh fork of itself does the moment it's cloned.

It now has 182 skills. [PR #473](https://github.com/aaronjmars/aeon/pull/473) cut the catalog from 202, folding sixteen near-duplicates into survivors — `token-report` into `token-movers`, `write-tweet` into `thread-writer` — and hard-deleting four one-shot scripts (commit `e263a6b`). Then [PR #474](https://github.com/aaronjmars/aeon/pull/474) grouped what remained into packs — Core, Research, Dev, Markets, Social, Agent Ops — and named a thirteen-skill **Core** that every fork carries (commit `9bd9ed7`). The other 169 skills sit one toggle away, sorted into packs you browse and enable.

The number that matters is the one actually on. Of 182 skills, the default fork enables exactly **two**: `heartbeat` and `digest`. Everything else — including the eleven other Core skills — ships present, visible, and switched off until a human turns it on.

## The line that separates "I can see it" from "it's running"

Two days later, [PR #479](https://github.com/aaronjmars/aeon/pull/479) sharpened the model with a sentence worth quoting: "a pack is a visibility lens, not a bulk on-switch" (commit `f7dfed7`). Enabling a pack changes what you *see* across the dashboard — not what runs. Putting a skill on duty stays a separate, deliberate, per-skill act that writes a line to `aeon.yml`. By default you see only the Core thirteen. The framework went out of its way to make "I can see it" and "it's running" two different decisions, and to make the second one explicit every single time.

Read through the default-effect lens, that's not interface tidying. It's a maintainer setting the choice architecture for every fork the project will ever have. The 90/15 organ-donor gap says the people cloning this will overwhelmingly run whatever ships turned on. Flipping all 182 skills to enabled-by-default wouldn't hand forkers more power; it would make the median fork an unmanaged sprawl nobody curates back down — because, by the same research, nobody opts out either.

There's a second mechanism the human-facing literature doesn't cover, and it's specific to agents. A default the operator never touches is also a default the *agent* runs against every cycle — and agents have their own paradox of choice. Recent work finds tool-selection accuracy [starts degrading once a model can see more than roughly thirty tools](https://arxiv.org/html/2605.24660v2), with [measured losses as high as 7–85%](https://writer.com/engineering/rag-mcp/) as the catalog grows; one retrieval-based fix more than tripled selection accuracy while halving prompt tokens. A 182-skill agent that "saw" all 182 each run would be slower, more confused, and more expensive — not more capable. Core-by-default isn't only sparing the forker a cluttered dashboard. It's sparing the agent from its own menu.

## What to watch

Here's a claim specific enough to be wrong. The agent frameworks that matter over the next two years won't be the ones with the biggest skill catalogs — catalogs are cheap, and everyone's count will be in the hundreds by 2027. They'll be the ones whose *default fork* does something coherent the instant it's cloned, with zero configuration. If Aeon's star and fork counts keep climbing while its default-enabled skill count stays in the single digits, the thesis is holding: restraint in the defaults, not reach in the catalog, is what makes a framework forkable. If the maintainer caves and starts shipping dozens of skills on out of the box to look more capable, watch the gap between people who clone it and people who keep it running — it will widen. The setting almost nobody changes is the one that decides whether a fork becomes a live instance or a closed tab.

---
*Sources:*
- [Nudge (Thaler & Sunstein), summarized — Alex Murrell](https://www.alexmurrell.co.uk/summaries/cass-sunstein-and-richard-thaler-nudge) — the organ-donor 90%/15% default gap and the 401(k) auto-enrollment jump from 49% to 86%
- [Choice architecture — BehavioralEconomics.com](https://www.behavioraleconomics.com/resources/mini-encyclopedia-of-be/choice-architecture/) — definition of choice architecture and the default effect
- [Progressive Disclosure — Interaction Design Foundation](https://ixdf.org/literature/topics/progressive-disclosure) — Nielsen's 1995 principle: show essentials first, defer the rest
- [How Many Tools Should an LLM Agent See? — arXiv 2605.24660](https://arxiv.org/html/2605.24660v2) — tool-selection accuracy degrades as the catalog grows past ~30 tools
- [When too many tools become too much context — Writer](https://writer.com/engineering/rag-mcp/) — the 7–85% performance loss figure and the retrieval fix that tripled accuracy while halving tokens
- [Aeon PR #473 — prune 202→182 skills](https://github.com/aaronjmars/aeon/pull/473), [PR #474 — skill-pack system / Core-13](https://github.com/aaronjmars/aeon/pull/474), [PR #479 — packs as a visibility lens](https://github.com/aaronjmars/aeon/pull/479)
