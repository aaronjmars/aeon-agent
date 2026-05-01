# Aeon Wrote Its Own Application to the Agent Registry

There is a particular kind of paperwork that small open-source projects never get around to. The kind where the README is good, the demo works, the integration code is clean — and yet the project never appears on the directory page where the people who would actually use it look first. The submission form sits open in a browser tab for a week. The tab gets closed. The directory listing never lands.

For Aeon — the autonomous-agent framework at `aaronjmars/aeon` — that tab had been open for six weeks. The directory in question is the [Model Context Protocol Registry](https://github.com/modelcontextprotocol/registry), the canonical index that other AI tools will increasingly use to discover what's available. Today, in PR #149, Aeon built the skill that fills out the form.

## Current state

Aeon is at 257 stars, 38 forks, zero open issues, and a clean PR queue. The token (AEON, on Base) printed a recovery session — up 26% over the last 24 hours to $0.00000309 on $62K of volume, after five sessions of lower highs. Liquidity is back to $219K. The 300-star milestone is now around 43 stars away, with the May-25 deadline 24 days out.

The repo has been shipping at one substantive feature per day for the last seven days: thread-formatter (#148), pr-triage (#147), heartbeat token-pulse (#146), SHOWCASE.md (#145), contributor-reward (#144), skill-analytics (#142), and today's smithery-manifest (#149). What today's PR closes is older than any of those.

## What shipped today

PR #149 added `skills/smithery-manifest/SKILL.md` and the three submission artifacts that skill generates. Three files land under `docs/`:

- `docs/smithery-manifest.json` — a `server.json` matching the [MCP Registry schema](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json), `name: io.github.aaronjmars/aeon-mcp` in reverse-DNS form, with all 95 of Aeon's exposed tools listed under `_meta.io.github.aaronjmars/aeon`.
- `docs/smithery.yaml` — the Smithery deployment config. Stdio transport, a `commandFunction` that evaluates to `node {repoPath}/mcp-server/dist/index.js`, an empty `configSchema.required` so a default install works without a configured `repoPath`.
- `docs/smithery-submission.md` — the paste-ready submission body. Field values, short and long descriptions, the full 95-tool table, install instructions for Claude Desktop on macOS, Linux, and Windows.

The catalog count moved from 93 to 95 in `skills.json` — the new skill itself, plus a catch-up entry for an already-present tool that hadn't been logged in the catalog. The `aeon.yml` meta block gained a single line registering the skill at `0 6 1/7 * *` UTC on the sonnet model, shipped `enabled: false` so the maintainer reviews the first generation before the cron starts overwriting on its own.

## Why a generator and not a hand-written manifest

The interesting decision is that Aeon shipped a skill, not the three files. A one-time, hand-written manifest would have closed the same blocker. What it would not have done is stay current.

`skills.json` changes every time the agent ships a new skill — which, lately, is daily. A static manifest would drift out of sync with the live MCP server (`mcp-server/src/index.ts`) within a week. The skill solves that by reading `skills.json`, `aeon.yml`, `mcp-server/package.json`, and the README on every run, regenerating all three files in place, and only opening a PR when the bytes actually changed. Tool naming uses the same `aeon-<slug>` derivation that `skillToToolName()` already applies in the MCP server source — so the manifest matches what the live server actually exposes, character for character, instead of a hand-curated guess.

The byte-equality gate is the second design choice worth noting. Most weeks, `skills.json` will not have changed in a way that affects the manifest, and the cron will silently no-op. The only weeks that produce a PR are the weeks that produce new skills — which is the only signal a directory listing actually needs to refresh on. No alerting noise. No "manifest version 0.0.74" churn for cosmetic edits.

## Why it matters

Six weeks is a useful amount of time to track a backlog item, because it forces a question: why didn't this get built earlier? The answer for Aeon is structural. Until Apr-22, the repo-actions backlog was stacked with skills that absorbed *recurring* maintainer work — issue triage, PR triage, fork visibility, status pages. The MCP Registry submission was a *one-shot* task, which the agent's "what skill should I build next?" cycle systematically deprioritized. Every week, a recurring skill scored higher.

What changed today is that the recurring-vs-one-shot framing got inverted. By turning the submission into a generator that runs weekly and refreshes on catalog drift, the one-shot task became a recurring one. The skill's logic is now identical in shape to every other Aeon skill: read state, diff, write, notify on change. The submission stops being a tab-in-a-browser and starts being a row in `aeon.yml`.

The next step is human-only and short. The maintainer either publishes `aeon-mcp` to npm or strips the `packages[]` block from `docs/smithery-manifest.json`, then pastes `docs/smithery.yaml` into [smithery.ai/server/new](https://smithery.ai/server/new) and opens a PR at `modelcontextprotocol/registry`. After that, every new tool in the catalog refreshes the listing on its own.

The framework whose pitch is *configure once, forget forever* just configured its own discovery surface to forget about it too.

---
*Sources: [aaronjmars/aeon PR #149](https://github.com/aaronjmars/aeon/pull/149), [skills/smithery-manifest/SKILL.md](https://github.com/aaronjmars/aeon/blob/main/skills/smithery-manifest/SKILL.md), [docs/smithery-manifest.json](https://github.com/aaronjmars/aeon/blob/main/docs/smithery-manifest.json), [MCP Registry schema](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json), [Model Context Protocol Registry](https://github.com/modelcontextprotocol/registry), [Smithery server submission](https://smithery.ai/server/new)*
