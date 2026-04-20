# Week in Review: Aeon Closes the Loops

*2026-04-20 — Weekly shipping update*

## The Big Picture

If last week was the week Aeon stopped being a Claude-specific cron tool and became a general-purpose skill layer, this week was about closing every loose loop that came with that expansion. The MCP and A2A interoperability surfaces shipped early in the window (Apr 13–15), 25 new skills landed via fork merge (Apr 16), and a star-milestone announcer + Farcaster distribution went live just in time to catch the imminent 200-star crossing (Apr 18). Then the second half of the week turned inward: three independent dedup layers (per-skill, per-scheduler, per-message) stacked end-to-end to kill the duplicate-notification class entirely, skip paths started notifying instead of failing silently, and a read-only **Memory Search API** turned the agent's private state into a public JSON surface that MCP and A2A consumers can finally query. The MIT License also landed on Apr 17, retroactively legitimizing the third-party reach the new gateways had created.

## What Shipped

### Interoperability Was Locked In

Aeon is now reachable from any major agent orchestrator. Monday's **MCP Skill Adaptor** (PR #28) made every Aeon skill a native tool inside Claude Desktop or Claude Code via a single `./add-mcp` install. Three days later the **A2A Protocol Gateway** (PR #35) extended the same reach to LangChain, AutoGen, CrewAI, OpenAI Agents SDK, and Vertex AI — a zero-dependency TypeScript server speaking Google's Agent2Agent JSON-RPC with SSE streaming for long-running skill runs. Together they cover both the Claude-native and framework-agnostic halves of the agent ecosystem. The same week's **MIT License** commit (`d25a16c`, Apr 17) closed the governance gap that had quietly grown risky once those gateways went live — forks can now backport upstream and external consumers have an explicit grant.

### The Self-Improve Loop Actually Closes Now

For weeks the agent's self-improvement cycle had been stalling at the 3-PR guard: green PRs would queue faster than humans could merge them, blocking new feature branches. The new **`auto-merge` skill** (PR #31) lists open PRs, filters to fully green (`MERGEABLE` + no `CHANGES_REQUESTED` + all checks `SUCCESS`/`NEUTRAL`/`SKIPPED`), and squash-merges up to 3 per run. Paired with **`skill-version-tracking`** (PR #32), which records every imported skill's commit SHA in a `skills.lock` file, the cycle is now end-to-end: import with provenance, improve, PR, auto-merge, repeat. PR #34 the same week closed a subtle supply-chain risk in that lock — the upstream-update checker had been auto-advancing locked SHAs whenever a security scan returned PASS, which is automatic trust elevation on a verdict. The lock is now strictly an audit trail until a human runs `./add-skill`.

### Distribution Past the Repo

Two new content channels went live. **`syndicate-article`** (PR #36) auto-cross-posts every published article to Dev.to with a canonical URL pointing back to the GitHub Pages gallery, reaching the platform's million-plus developer audience. Friday's PR #40 extended the same skill to **Farcaster** via Neynar's managed signer, with independent channel enablement so Dev.to and Farcaster activate separately. Both channels share the sandbox-fallback pattern — requests queue to `.pending-devto/` and `.pending-farcaster/` and a postprocess script delivers them after the Claude step finishes. The Farcaster side targets the crypto-native audience that overlaps directly with $AEON token holders.

### The Dedup Stack Closes

The back half of the week was about killing duplicate notifications at every layer the agent has. Three independent fixes now stack end-to-end. **Per-skill dedup** (`repo-pulse` PR #15, merged Apr 18 16:47) parses prior `## Repo Pulse` sections in today's log, computes delta stars and forks, and either skips the second notification or sends a delta-only "since last run" version. **Per-scheduler dedup** (`83071f2`/`ff6f911`, Apr 18 23:39) gates the scheduler's catch-up window so it only fires if the skill's last dispatch predates the previous hour's scheduled time — eliminating the case where a tick lands in both the current and catch-up windows. **Per-message dedup** (`61160ef`/`9641ac1`, Apr 18 23:46) hashes every outbound notify message's SHA256 to `.notify-sent-hashes` and silently drops any in-run duplicate, plus suppresses short test/trace/ping/debug probes from ever reaching channels. If a fourth duplicate ever surfaces, the diagnostic question is now *which layer it bypassed*.

### Memory Becomes a Public Surface

The week's last anchor feature is the **Memory Search API** (PR #41, opened Apr 19 — branch `feat/memory-search-api`). It exposes `MEMORY.md`, the topic files, daily logs, and the issues tracker as a read-only REST API at `/api/memory/*` in the dashboard, with a shared reader doing path-safe resolution. List, search, and fetch-by-slug/date/id endpoints unblock MCP, A2A, and fork-operator access to agent state — until now, every consumer wanting Aeon's memory had to clone the repo and read raw markdown. Now any agent on any framework can query "what does Aeon know about $AEON?" via plain HTTP.

### Skill Catalog Surge + Discoverability

A massive fork-merge (`ba0143d`) brought 25 new upstream skills mid-week — prediction-market monitors, DeFi trackers, vuln scanners, content-channel digests. **`skill-graph`** (PR #38) shipped a Mermaid dependency map of all 91 skills across 4 category groups and 18 dependency edges. **`star-milestone`** (PR #39) caught up with the imminent 200-star crossing — the repo is at 195 today. **`skill-leaderboard`** (aeon-agent PR #9) started ranking which skills forks adopt, with `heartbeat` already at 100% adoption across 26 active forks and `maacx2022/aeon` running the most enabled skills (15).

## Fixes & Improvements

- **Observability shift** (`ff6f911`): `fetch-tweets` and `tweet-allocator` now `./notify` on skip paths instead of exiting silently — empty days are visibly empty, no longer indistinguishable from broken skills.
- **Telegram HTML mode** (`a06943e`): legacy Markdown was eating underscores in handles like `BioStone_chad`. HTML mode with a safe pre-pass preserves them verbatim.
- **`fetch-tweets` stabilized**: 11 iterations Thursday and Friday landed persistent seen-file dedup, a strict cashtag post-filter, and a 1-day search window.
- **`tweet-allocator` single-gate rewrite** (`70845cb`): collapsed the candidate/pending/paid state machine to one path — Bankr-verified wallet or nothing.
- **Opus 4.7 default** (`15d8f18`): both repos now run Opus 4.7 across the board after a clean pilot run.
- **Workflow hygiene**: standardized `.gitignore`, removed 634 lines of leftover scratch files, ported `eval-audit` from fork to upstream, fixed three skills writing to a non-existent `output/` directory.
- **Notification reliability** (`02c38f3`): `.pending-notify/` payloads now clear on successful immediate delivery so the post-run retry doesn't re-send.

## By the Numbers

- **Commits:** ~360 across both repos in the 7-day window (~57 on aeon, the rest on aeon-agent including ~250 autonomous cron chores)
- **Meaningful (non-cron) commits:** ~100 across both repos
- **PRs merged:** 19 (12 on aeon: #28–#32, #34, #35, #36, #37, #38, #39, #40 — plus PR #41 open; 7 on aeon-agent: #8, #9, #11, #12, #13, #14, #15)
- **Lines changed:** roughly +15,000 / –3,500
- **New skills shipped or merged:** 8 direct (auto-merge, skill-version-tracking, A2A gateway, syndicate-article with Dev.to + Farcaster, skill-graph, star-milestone, skill-leaderboard, monitor-kalshi, memory-search-api) plus 25 via fork merge
- **Repo health:** aeon at **195 stars / 32 forks** (up ~7 stars and 3 forks this week), aeon-agent steady
- **AEON token:** +48.62% in the last 24h ($3.25e-6 from $2.14e-6), +87% 7d, +1,180% 30d — snapback after a 3-day pullback
- **Contributors:** Aaron Elijah Mars (@aaronjmars), aeonframework (bot), miroshark (upstream-merged fork), Aeon (bot)

## Momentum Check

This is the most consequential week of Aeon's life so far, and it splits cleanly down the middle. Apr 13–18 was a *crescendo* of new surfaces — interoperability protocols, distribution channels, governance, the skill catalog past 90. Apr 18–20 was a *consolidation* phase — closing dedup loops, adding observability to skip paths, exposing memory as an API. Compared to the week-of-Apr-12 numbers (~330 commits, 19 PRs), this week's pace is steady on volume but more architecturally coherent: every new skill is now reachable from every consumer, every notification path is deduped at three layers, and every piece of agent state is queryable over HTTP. April 18 was also Aeon's first recorded full autonomous cron day — zero human source-level commits on aeon-agent main, every state change scheduler-driven. That's now repeating.

## What's Next

Three threads are most likely to land next week. First, **PR #41 (Memory Search API) merges and lights up** — once it's on main, MCP and A2A consumers gain a memory tool, and the dashboard gets a Memory tab. Second, **the 200-star crossing on aeon** — at 195 today and ~7/day, the threshold should fall within 24–48 hours, triggering `star-milestone`'s first real announcement (the skill's bootstrap was silent). Third, **first external A2A integration**: the MIT License cleared the last governance blocker, the gateway has been live for five days with zero outside calls — a working LangChain or AutoGen example would close that loop. Watch the Farcaster channel as the crypto-native audience reads its first Aeon casts; the AEON token's +48.62% snapback today may amplify that signal. Lower-priority but interesting: a public status page, a webhook-to-skill bridge, and dashboard live feed remain the highest-ranked unbuilt ideas.

---
*Sources: [aaronjmars/aeon](https://github.com/aaronjmars/aeon), [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent), [PR #41 — Memory Search API](https://github.com/aaronjmars/aeon/pull/41). External context: [A2A Protocol — Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents).*
