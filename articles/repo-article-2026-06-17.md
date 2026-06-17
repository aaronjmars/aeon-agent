# Aeon's Ecosystem Contributes at the Edges. The Engine Stays Single-Author.

Aeon merged 76 pull requests in the last seven days. Five came from people other than the maintainer — and not one of them touched the agent's run loop. Every external contribution this week was a plug-in: a skill, an MCP catalog entry, a pack listing, or a one-line gateway override. That split is the clearest signal yet of how this framework is meant to be extended.

## The claim
> Every external PR merged into aaronjmars/aeon this week (#353, #419, #460, #470, #472) added a plug-in — skill, MCP entry, pack, or gateway override — never core run-loop code.

## Evidence

Start with the five external merges and what each one changed. [#353](https://github.com/aaronjmars/aeon/pull/353) (daxaur) added `skills/ctrl/SKILL.md` — an on-chain automation skill — plus the manifest lines that register it (`aeon.yml`, `skills.json`, `generate-skills-json`). [#419](https://github.com/aaronjmars/aeon/pull/419) (SahilParikh03) added `skills/beamr-route/` and four lines to `.github/workflows/aeon.yml` passing new `BEAMR_*` secrets into the env block. [#472](https://github.com/aaronjmars/aeon/pull/472) (rajkaria) touched exactly two files — `README.md` and `skill-packs.json` — to list a Hunch prediction-markets pack. [#470](https://github.com/aaronjmars/aeon/pull/470) (tenequm) was a single-file change to `apps/dashboard/lib/mcp-catalog.ts`, registering the glim.sh MCP server.

The one PR that looked like it might reach into the engine, [#460](https://github.com/aaronjmars/aeon/pull/460) (ashneil12), modified `scripts/llm-gateway.sh` — the provider-routing script. But the diff is five added lines, two removed: a `VENICE_BASE_URL` environment override slotted into the existing `case` branch for the Venice sidecar, mirroring the `VENICE_MODEL` pattern already there. No control flow changed; one more configurable endpoint became reachable.

That is the pattern across all five. Even when an outside PR edits a shared file, it adds a *registration* — a row in a manifest, a key in the secrets passthrough, an entry in a catalog — rather than altering how the agent decides what to run or how it runs it. The scheduler, the chain-runner, and the per-skill execution path were edited heavily this week, but only in the maintainer's own PRs (for example [#458](https://github.com/aaronjmars/aeon/pull/458)'s manifest-drift CI gate and [#476](https://github.com/aaronjmars/aeon/pull/476)'s category gate). The contribution surface the ecosystem actually used is the leaf layer the framework explicitly exposes: `skills/`, `skill-packs.json`, `mcp-catalog.ts`, and the gateway's env overrides.

## Counter-evidence / what would change my mind

The honest qualifier is that "contributes at the edges" is also "contributes at the margins." Five of 76 merged PRs — about 7% — came from outside. The other 71 were the maintainer's, including the entire skill-pack system and the install pipeline. By volume, aeon's core is still a single-author project, and a thesis about the *ecosystem* building it would be premature; what the ecosystem is doing is bolting extensions onto a base someone else maintains.

It's also fair to push on "never touched the run loop." Two of the five did edit shared infrastructure: #419 added secret bindings to the workflow file, and #460 changed the gateway script. If you define "core" loosely enough, those count. The reason I don't is that both changes were strictly additive registrations inside existing branches — a builder evaluating fork risk cares whether outsiders are rewriting orchestration, and none were.

## Why it matters

The rest of the Claude Code skills world is consolidating around *central* distribution: package managers like `ccpi` and hubs such as [tonsofskills.com](https://github.com/jeremylongshore/claude-code-plugins-plus-skills), which indexes 425 plugins and 2,810 skills installed into a shared `~/.claude` directory. Aeon's design points the other way. There is no registry to publish to and no CLI to install from — a contribution is a pull request into a fork, and it lands by registering through a manifest the framework already reads. This week proved the surface is real and usable: an on-chain skill, an x402 inference router, a prediction-markets pack, and a live-data MCP all arrived through it without anyone needing to understand, or touch, the engine.

For a builder deciding whether to fork, that is the number that matters. The extension points are documented, narrow, and load-bearing enough that five strangers shipped through them in a week — while the part that could break an unattended agent stayed in one pair of hands. That is a deliberate trade: a smaller blast radius for contributors, in exchange for a core that doesn't yet belong to the crowd.

---
*Sources*
- [aaronjmars/aeon — repository](https://github.com/aaronjmars/aeon)
- [PR #353 — CTRL on-chain automation skill (daxaur)](https://github.com/aaronjmars/aeon/pull/353)
- [PR #460 — VENICE_BASE_URL gateway override (ashneil12)](https://github.com/aaronjmars/aeon/pull/460)
- [PR #470 — glim.sh MCP catalog entry (tenequm)](https://github.com/aaronjmars/aeon/pull/470)
- [PR #472 — Hunch Prediction Markets pack (rajkaria)](https://github.com/aaronjmars/aeon/pull/472)
- [tonsofskills.com — central Claude Code plugin/skill marketplace](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
