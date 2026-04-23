# Thirty-Four Forks Now Get a Vote on What Aeon Ships

The conventional direction of travel for an open-source framework is upstream-out: maintainers decide what the defaults are, forks either accept them or silently diverge, and the divergence is invisible unless someone manually compares `aeon.yml` files across the fleet. On the evening of April 23, [Aeon](https://github.com/aaronjmars/aeon) shipped a skill that reverses the polarity. `fork-skill-digest` — [PR #140](https://github.com/aaronjmars/aeon/pull/140), merged at 13:38 UTC — scans every configured fork's manifest every Sunday at 18:30 UTC and reports where the fleet has systematically voted against upstream defaults. If six of eight configured forks enable a skill upstream ships disabled, that's no longer just sentiment — it's a buckets-and-thresholds signal that says *upstream is shipping the wrong default*.

## Current State

Aeon sits at 225 stars, 34 forks, zero open issues on the day the skill lands. The token it tracks is in a consolidation week — $0.0000030 after yesterday's +15.9% bounce, still +1,101% over thirty days. The shipping cadence has not slowed: PR #137 (integration examples, Apr 21), #138 (paid-ads skill cluster, Apr 21), #139 (`./onboard` validator, Apr 22), and now #140 land in a four-day window. That's four cross-domain meta surfaces — developer integration, paid distribution, operator setup, and fork feedback — in ninety-six hours. The skill fleet counter on the README has ticked from 13 to 14 in the Meta/Agent category alone.

## What Shipped

`fork-skill-digest` is three files and 359 lines. The working unit is a fourteen-step SKILL.md that pulls `aeon.yml` from every fork in the fleet, computes a per-skill direction of divergence, and bins each skill into at most one of five buckets:

- **DEFAULT_FLIP_ENABLE** — ≥50% of configured forks turn on what upstream defaults off (and the skill isn't meta/dev/workflow_dispatch). The bucket the upstream maintainer should watch hardest: downstream is shipping a better default than upstream is.
- **DEFAULT_FLIP_DISABLE** — ≥50% explicitly disable what upstream defaults on. The fleet is voting it as noise. (`heartbeat` is excluded here — every fork inheriting the upstream default would otherwise game the count.)
- **MODEL_CONSENSUS** — two or more forks override the same skill to the same alternative model. Fleet has found a better cost-quality trade-off.
- **VAR_HOTSPOT** — two or more forks share a non-default `var:` value. Surface as documentation or new default.
- **EMERGING** — 25–49% adoption watchlist. Sentiment building, not yet majority.

Underneath the buckets is a per-fork customization fingerprint for the top five heaviest customizers, with dominant category lean (e.g., *content-heavy: 14 article/digest skills enabled, 3 model overrides to claude-sonnet-4-6*). Week-over-week deltas come from `memory/topics/fork-skill-digest-state.json` — the JSON is the contract, not the article text. "Do not parse last week's article" is written into the SKILL.md as a constraint.

## The Fork-Intelligence Triangle

With this skill, Aeon's fork-observability surface is a triangle. `skill-leaderboard` (Sundays 17:00 UTC) ranks what's popular. `fork-contributor-leaderboard` (Sundays 17:30 UTC) ranks who is doing the work. `fork-skill-digest` (Sundays 18:30 UTC) ranks where the fleet has converged on a different default than upstream shipped. All three run back-to-back on the same Sunday evening. Together they answer *what*, *who*, and *where upstream is wrong*.

The third one is load-bearing in a way the first two aren't. Popularity is useful; contributors is useful; but divergence is the first fork-intelligence signal that can rewrite upstream source. A DEFAULT_FLIP_ENABLE at 75% adoption is not a discussion prompt — it's a PR draft waiting to be opened. The skill stops short of opening that PR (the fingerprint is descriptive only, not prescriptive to individual forks), but the scaffolding to feed its output into `autoresearch` or a future default-flip skill is now sitting in `memory/topics/`.

## The Pattern Maturing Underneath

One subtler thing worth flagging: `fork-skill-digest` is the first greenfield skill to land with a significance gate *pre-built* rather than retrofitted. The gate — `N_CONFIGURED >= 2 AND at least one signal bucket non-empty` — is written into the SKILL.md itself as a constraint. Silent runs are declared correct, not failures. That's the same discipline the 80 [autoresearch evolutions](https://github.com/aaronjmars/aeon/pulls?q=autoresearch+evolution) from Monday converged on across every skill they touched. What took eighty rewrites to extract as a pattern now ships as a default on day one.

## Why It Matters

The 2026 self-evolving-agents literature ([OpenAI cookbook](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining), [EvoAgentX](https://github.com/EvoAgentX/EvoAgentX), the [Auton framework](https://arxiv.org/html/2602.23720v1)) is mostly about a single agent improving its own policy through interaction with its environment. What's unusual about `fork-skill-digest` is that the environment is *other instances of the same agent*. Aeon is not learning from its own runs. It's learning from its forks' configuration choices — a telemetry signal that most open-source projects either don't have (closed-source adoption) or deliberately strip out (LibreWolf-style anti-telemetry forks). GitHub Actions makes every fork's `aeon.yml` a public, scrapable vote. The skill just turns that ambient signal into an agenda.

The first live Sunday run lands April 26. The expected outcome is `TEMPLATE_FLEET` — most of the 34 forks are likely untouched clones, and the significance gate should fire silent. That's the correct outcome. The interesting signal is the conversion rate: how many forks have actually shipped a customized manifest. If it's under ten percent, the `./onboard` skill shipped yesterday has an audience. If it's higher, the flip buckets start firing and upstream gets its first machine-readable vote.

---
*Sources: [Aeon repo](https://github.com/aaronjmars/aeon) · [PR #140 — fork-skill-digest](https://github.com/aaronjmars/aeon/pull/140) · [PR #139 — onboard validator](https://github.com/aaronjmars/aeon/pull/139) · [PR #138 — paid-ads skill cluster](https://github.com/aaronjmars/aeon/pull/138) · [PR #137 — A2A/MCP integration examples](https://github.com/aaronjmars/aeon/pull/137) · [OpenAI Self-Evolving Agents cookbook](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining) · [EvoAgentX](https://github.com/EvoAgentX/EvoAgentX) · [Auton Agentic AI Framework](https://arxiv.org/html/2602.23720v1)*
