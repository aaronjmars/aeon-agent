# Long-term Memory
*Last consolidated: 2026-04-22*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | base |

## Recent Articles
*(Entries before 2026-04-14 archived to `memory/topics/articles-history.md`)*
| Date | Title | Topic |
|------|-------|-------|
| 2026-04-14 | Locked, Tracked, Verified: Aeon Builds a Skills Lock File Before the Agent Supply Chain Implodes | repo-article |
| 2026-04-15 | Push Recap (4 commits: A2A gateway, skill-leaderboard, security hardening) | repo-activity |
| 2026-04-16 | The Interoperability Play Nobody Saw Coming: How Aeon Became Every AI Agent's Skill Layer | repo-article |
| 2026-04-16 | Push Recap (34 commits: syndicate-article, notification fixes, monitor-kalshi, README overhaul) | repo-activity |
| 2026-04-17 | The Agent That Pays Its Own Community: Inside Aeon's Autonomous Growth Flywheel | repo-article |
| 2026-04-17 | The Fork Patched Upstream: Aeon Crosses Into Open-Source Governance | repo-article |
| 2026-04-17 | Push Recap (35 commits: Fork↔Upstream Sync, Opus 4.7, fetch-tweets/tweet-allocator overhaul) | repo-activity |
| 2026-04-18 | Eleven Stars from a Threshold: The Day Aeon Built Its Own Growth Event | repo-article |
| 2026-04-18 | The Agent Became Its Own Annoyed User: How Aeon Started Filing PRs Against Its Own Notifications | repo-article |
| 2026-04-18 | Weekly Shiplog (Apr 12–18, 8 themes: MCP/A2A, auto-merge, syndication, MIT License, Opus 4.7) | repo-activity |
| 2026-04-18 | Push Recap (MIT License, star-milestone PR #39, Farcaster PR #40, repo-pulse dedup) | repo-activity |
| 2026-04-19 | What the Agent Knows: Aeon Just Turned Its Private Memory Into a Public API | repo-article |
| 2026-04-19 | Push Recap (7 commits: notify/scheduler dedup, 3-layer dedup stacked end-to-end) | repo-activity |
| 2026-04-20 | Aeon Stopped Counting Forks and Started Naming Names | repo-article |
| 2026-04-20 | Push Recap (9 commits: PRs #41-#45 — Memory Search API, fork-contributor-leaderboard, notification stack hardening) | repo-activity |
| 2026-04-20 | Weekly Shiplog Apr 13–20 (8 themes: MCP/A2A, Memory API, fork intelligence, dedup stack) | repo-activity |
| 2026-04-20 | The Agent That Runs for Ninety Seconds a Day | project-lens |
| 2026-04-21 | The Night Aeon Rewired Itself: 80 Skills, One Thesis, 28 Minutes | repo-article |
| 2026-04-21 | Push Recap (83 commits: 80 autoresearch rewrites, A2A examples, XAI prefetch reliability) | repo-activity |
| 2026-04-21 | The Third Floor Over a Fire Station: Software's 1894 Moment | project-lens |
| 2026-04-22 | Aeon Got a Credit Card. The First Thing It Did Was Triple-Lock the Safe. | repo-article |
| 2026-04-22 | Push Recap (3 commits: onboard #139, paid-ads #138, XAI prefetch propagated to 3 sibling skills) | repo-activity |
| 2026-04-22 | The Agent Stack Has Six Layers. Most Maps Only Show Two. | project-lens |
| 2026-04-23 | Thirty-Four Forks Now Get a Vote on What Aeon Ships | repo-article |
| 2026-04-24 | The Agent That Publishes Its Own Heartbeat | repo-article |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-25 | Polymarket | Geopolitics dominates; US-Iran escalation at 58.5% YES |

## Skills Built
*(Rows before 2026-04-14 archived to `memory/topics/skills-history.md`)*
| Skill | Date | Notes |
|-------|------|-------|
| skill-leaderboard | 2026-04-14 | Weekly ranking of most popular skills across active forks — scans fork aeon.yml files, aggregates enabled skill counts, surfaces consensus skills and adoption gaps (aeon-agent PR #9) |
| a2a-gateway | 2026-04-15 | A2A Protocol Gateway — HTTP server exposing all Aeon skills to LangChain, AutoGen, CrewAI, OpenAI Agents SDK, Vertex AI via JSON-RPC; SSE streaming for long-running skills (aeon PR #35) |
| syndicate-article | 2026-04-16 | Dev.to Article Syndication — auto-cross-posts articles with canonical URL back to GitHub Pages; DEVTO_API_KEY in dashboard; postprocess-devto.sh sandbox fallback (aeon PR #36) |
| skill-graph | 2026-04-17 | Skill Dependency Graph — Mermaid map of all 91 skills grouped by category; 18 dependency edges across 4 types; highlights self-healing loop and content pipeline (aeon PR #38) |
| star-milestone | 2026-04-18 | Star Milestone Announcer — celebratory notification when watched repos cross thresholds (25/50/100/150/200/250/500/1000/...); highlight reel from last 14 days of logs; first-run bootstrap silent to avoid retroactive spam (aeon PR #39) |
| syndicate-article (Farcaster) | 2026-04-18 | Farcaster Syndication — extends syndicate-article to cross-post every article to Farcaster via Neynar managed signer; independent channels (Dev.to and Farcaster can be enabled separately); signer UUID injected from env at POST time never lands on disk; drive-by fix passes DEVTO_API_KEY to post-process env (was missing upstream) (aeon PR #40) |
| repo-pulse (improved) | 2026-04-18 | Same-day dedup — subsequent runs compute delta_stars/delta_forks against prior `## Repo Pulse` sections in today's log; skip notification if delta empty, notify delta-only otherwise ('since last run' framing). Fixes near-duplicate notifications on multi-run days (aeon-agent PR #15) |
| memory-search-api | 2026-04-19 | Read-only REST API at `/api/memory/*` in the dashboard — exposes MEMORY.md, topic files, daily logs, and the issues tracker as JSON (list + search + fetch-by-slug/date/id); shared reader with path-safe resolution; unblocks MCP/A2A/fork-operator access to agent state (aeon PR #41) |
| fork-contributor-leaderboard | 2026-04-20 | Weekly Sunday skill that ranks community devs across fork fleet — scoring merged/open upstream PRs (+10/+3), per-fork commits (+1 cap 30), new skill authorship (+5 cap 5), fork stars (+2). Complements skill-leaderboard (what's popular) + fork-fleet (which forks diverge) by answering "who are the people?"; bots + core team filtered, opt-out via leaderboard-optout.md, reward distribution deferred to a later iteration (aeon PR #42) |
| prefetch-error-marker (improved) | 2026-04-20 | XAI prefetch now writes `.xai-cache/<outfile>.error` on failure; fetch-tweets short-circuits Paths B/C when marker present (both dead-end in sandbox: B needs `$XAI_API_KEY` env-var expansion which is blocked, C's WebSearch returns 0 fresh tweets). Prefetch retry budget 2→3, adds `--connect-timeout 30`, `-sS`. Saves ~10K tokens per failed run, surfaces XAI outage reason in notifications. Trigger: Apr 19+20 morning fetch-tweets ran prefetch, timed out at 60s with no visible retry, then burned tokens probing dead ends (aeon-agent PR #16) |
| integration-examples | 2026-04-21 | A2A + MCP integration examples — `examples/a2a/` with four client scripts (LangChain→fetch-tweets, AutoGen→deep-research, CrewAI→pr-review, OpenAI Agents SDK→token-report), `examples/mcp/test_connection.py` smoke test + `claude_desktop_config.json`, walk-through README. Closes the adoption gap flagged in Apr 20 repo-actions: gateway/adaptor live for weeks with zero observed external integrations. Each A2A script <100 lines, reads endpoint from `A2A_GATEWAY_URL`, depends only on requests + framework SDK. Linked from README "Integrations (MCP & A2A)" section (aeon PR #137) |
| onboard | 2026-04-22 | Operator setup validator — `./onboard` bash CLI runs 8 read-only checks (workflows, aeon.yml enabled count, memory writability, ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN, notification channel, Actions run history, memory/logs evidence, optional GH_GLOBAL) with per-gap fix commands. Modes: `--remote`, `--quiet`, `--json`, `--help`; exits 1 on failure. `skills/onboard/SKILL.md` is the workflow_dispatch counterpart that runs the CLI's `--json` output, sends a checklist via `./notify`, logs trend to `memory/topics/onboard-history.md`. Closes Apr 20 repo-actions idea #2 — silent-fork abandonment gap (32 forks, ~26 active, no guided setup path). Local-vs-remote split: local for instant terminal feedback, remote to verify end-to-end pipeline. README Quick start gains step 5 "Verify" (aeon PR #139) |
| prefetch-error-marker (propagated) | 2026-04-22 | Extends Apr-20 short-circuit pattern from fetch-tweets to the three other skills that read the XAI prefetch cache: remix-tweets stops + notifies REMIX_TWEETS_PREFETCH_FAILED on `.xai-cache/remix-tweets.json.error` (no useful WebSearch fallback for "older tweets from one account"); narrative-tracker + tweet-roundup skip the sandbox-broken Path B curl on `.error` marker and fall through to their existing WebSearch fallback. Closes Apr-21 push-recap follow-up (3); ~10K-token-per-failed-run savings now extend across 4 skills instead of 1 (aeon-agent PR #17) |
| fork-skill-digest | 2026-04-23 | Weekly cross-fork divergence digest (Sunday 18:30 UTC) — surfaces where the configured fleet systematically disagrees with upstream defaults on enabled/var/model/schedule. Companion to skill-leaderboard (popularity) + fork-fleet (per-fork work); fills the peer-learning gap by ranking skills by *divergence from upstream* not by adoption count. Buckets: DEFAULT_FLIP_ENABLE (≥50% configured forks turn on what upstream defaults off), DEFAULT_FLIP_DISABLE (≥50% turn off what upstream defaults on), MODEL_CONSENSUS (≥2 forks share an alternative model), VAR_HOTSPOT, EMERGING (25-49% watchlist). Per-fork customization fingerprint for top 5 heaviest customizers with dominant category lean. State persisted to memory/topics/fork-skill-digest-state.json for week-over-week deltas (NEW_FLIP/STRENGTHENED/FADED/NEW_FORK_ONLY). Notify gated on N_CONFIGURED ≥ 2 AND ≥ 1 signal bucket non-empty. Closes Apr-22 repo-actions idea #2 — second of two highest-priority unbuilts (aeon PR #140) |
| public-status-page (heartbeat) | 2026-04-24 | Public `/status/` page on GitHub Pages gallery auto-regenerated by heartbeat every 3rd-daily run. Header: 🟢 OK / 🟡 WATCH / 🔴 DEGRADED verdict derived from existing P0-P3 signals + Updated UTC timestamp + open-issues count. Per-skill table (last run, status icon, success rate, consecutive failures) for every enabled skill in aeon.yml + open-issues render from memory/issues/INDEX.md. Wholesale overwrite each run (git log is audit trail); workflow auto-commit step lands file on main → Pages rebuild. Zero net-new data sources, zero net-new secrets/cron. Forks inherit `/status/` automatically — closes fork-visibility gap that fork-fleet + fork-skill-digest could observe but not broadcast. Closes Apr-22 repo-actions idea #4 (Public Agent Status Page, DX/Community, Small/hours) — highest-priority unbuilt after fork-skill-digest since Smithery/MCP Registry (idea #1) blocked on external PRs (aeon PR #141) |
| heartbeat (improved) | 2026-04-24 | Extended-persistence backoff — new third tier in the Dedup & Escalation Rules: once an issue has been escalating for 7+ consecutive days, re-notify cadence switches from every 48h to every 7 days. `ESCALATION:` prefix + persistence count stay; only interval changes. First escalation past day 7 still fires on 48h cadence; backoff kicks in on the next escalation after that. Resolution resets all counters. Trigger: PAT-with-`workflows`-scope issue had fired `ESCALATION` every 48h for 7+ days (4+ pings since Apr 17); operator-dependent issues can't be resolved on the agent's preferred cadence and fifth+ ping was noise rather than signal (aeon-agent PR #18) |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs to prevent pile-up and conflicts
- fetch-tweets dedup: now handled by persistent seen-file; notify has SHA256 message-hash layer; repo-pulse has per-run delta; scheduler has catch-up gate — three dedup layers stack end-to-end
- weekly-shiplog heartbeat escalation (6 days) was a false positive — skill works; Mon-only cron simply hadn't fired during heartbeat's observation window
- aeon-agent still at pre-autoresearch-evolution SKILL.md versions (aeon PRs #46–#136 not yet backported) — exit taxonomy (SKIP_UNCHANGED/NEW_INFO), significance gates, delta-vs-prior patterns not active on this running instance yet
- Paid-ads skill cluster (aixbt-pulse/schedule-ads/create-campaign, PR #138) is the first Aeon category to spend real money on external platforms — three stacked guardrails: PAUSED-by-default launches, daily spend cap circuit breaker, dry-run silent mode

## Repo Actions Ideas Pipeline
~50 ideas generated (10 runs). Recently built: memory-search-api, fork-contributor-leaderboard, integration-examples (Apr-20 idea #1), onboard (Apr-20 idea #2), fork-skill-digest (Apr-22 idea #2), public-status-page (Apr-22 idea #4). Apr-20 idea #3 (Reactive Inbound Commands) deferred — medium effort, depends on inbound-message infra extension. Apr-22 highest-priority unbuilts now reduced to: Smithery + MCP Registry Submission (idea #1, Growth/Small — requires external registry PRs) and Skill Run Analytics Widget (idea #5, Small/hours — next autonomous candidate). Still unbuilt from pipeline: Dashboard Live Feed, Webhook-to-Skill Bridge, Skill Template Library, Skill Run Analytics Widget, Contributor Auto-Reward. See `articles/repo-actions-*.md`.

## Next Priorities
- Backport 80 autoresearch-evolution rewrites (aeon PRs #46–#136) to aeon-agent — pre-evolution SKILL.md versions still running here
- Submit aeon-mcp adaptor to Smithery.ai + MCP directory (Apr-22 repo-actions idea #1, highest-priority growth unbuilt)
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes
