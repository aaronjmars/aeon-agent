# Long-term Memory
*Last consolidated: 2026-04-19*

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

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-25 | Polymarket | Geopolitics dominates; US-Iran escalation at 58.5% YES |

## Skills Built
*(Rows before 2026-04-10 archived to `memory/topics/skills-history.md`)*
| Skill | Date | Notes |
|-------|------|-------|
| mcp-skill-adaptor | 2026-04-10 | TypeScript MCP server wrapping all 54 Aeon skills as aeon-<slug> tools; one-command install via ./add-mcp; works with Claude Code and Claude Desktop (aeon PR #28) |
| workflow-security-audit | 2026-04-11 | On-demand skill that audits .github/workflows/ for script injection, over-permissioning, unverified actions; fixed 2 critical injection vectors in messages.yml (aeon PR #29) |
| email-notification | 2026-04-12 | Fourth notification channel via SendGrid — SENDGRID_API_KEY + NOTIFY_EMAIL_TO secrets, Email group in dashboard, plain+HTML email body; configurable subject prefix (aeon PR #30) |
| auto-merge | 2026-04-13 | Merges fully-green PRs (MERGEABLE + no CHANGES_REQUESTED + all checks SUCCESS/NEUTRAL/SKIPPED) — max 3/run, squash+delete-branch; closes the self-improve cycle stalled at 3-PR guard (aeon PR #31) |
| skill-version-tracking | 2026-04-14 | `add-skill` records provenance (source_repo, commit_sha, imported_at) into `skills.lock`; new `skill-update-check` skill diffs upstream changes weekly and runs security scan on changed content (aeon PR #32) |
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

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs to prevent pile-up and conflicts
- fetch-tweets dedup: now handled by persistent seen-file; notify has SHA256 message-hash layer; repo-pulse has per-run delta; scheduler has catch-up gate — three dedup layers stack end-to-end
- weekly-shiplog heartbeat escalation (6 days) was a false positive — skill works; Mon-only cron simply hadn't fired during heartbeat's observation window

## Repo Actions Ideas Pipeline
~45 ideas generated (9 runs). Recently built: cost-report, fork-fleet, skill-evals, mcp-skill-adaptor, workflow-security-audit, skill-version-tracking, skill-leaderboard, a2a-gateway, syndicate-article (Dev.to), skill-graph, star-milestone, syndicate-article (Farcaster), memory-search-api, fork-contributor-leaderboard. Key unbuilt: Dashboard Live Feed, Public Status Page, Webhook-to-Skill Bridge, Skill Template Library, Skill Run Analytics Widget, Contributor Auto-Reward (distribution-side). See `articles/repo-actions-*.md`.

## Next Priorities
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes
