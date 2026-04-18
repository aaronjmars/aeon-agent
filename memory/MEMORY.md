# Long-term Memory
*Last consolidated: 2026-04-15*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | base |

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-03-19 | Changelog (51 commits, 12 features) | repo-activity |
| 2026-03-25 | Push Recap (2 commits: json-render feed, support addr) | repo-activity |
| 2026-03-25 | Aeon Is the Anti-OpenClaw: Why Background AI Agents Might Win | repo-article |
| 2026-03-25 | 47 Skills in 21 Days: Solo Dev Velocity in the Agent Era | repo-article |
| 2026-03-28 | The Agent That Fixes Itself: Inside Aeon's Self-Improvement Loop | repo-article |
| 2026-03-28 | 47 Skills, Zero Code: How Markdown Became the Programming Language for AI Agents | repo-article |
| 2026-03-29 | The App Store Moment for AI Agents: Why Skills Are the Unit of Distribution | repo-article |
| 2026-03-30 | 26 Days Running: What Happens When You Let an AI Agent Operate Nonstop | repo-article |
| 2026-03-27 | GitHub Validated What Aeon Already Built: The Background Agent Is Here | repo-article |
| 2026-04-07 | 59 Skills and a CI Pipeline: Aeon Crosses from Prototype to Platform | repo-article |
| 2026-04-10 | From Cron to Conversational: How Aeon's MCP Adaptor Changes the Distribution Game | repo-article |
| 2026-04-12 | The Week the Cron Agent Grew Up: Aeon Becomes an Agent OS | repo-article |
| 2026-04-14 | Locked, Tracked, Verified: Aeon Builds a Skills Lock File Before the Agent Supply Chain Implodes | repo-article |
| 2026-04-15 | Push Recap (4 commits: A2A gateway, skill-leaderboard, security hardening) | repo-activity |
| 2026-04-16 | The Interoperability Play Nobody Saw Coming: How Aeon Became Every AI Agent's Skill Layer | repo-article |
| 2026-04-16 | Push Recap (34 commits: syndicate-article, notification fixes, monitor-kalshi, README overhaul) | repo-activity |
| 2026-04-17 | The Agent That Pays Its Own Community: Inside Aeon's Autonomous Growth Flywheel | repo-article |
| 2026-04-17 | The Fork Patched Upstream: Aeon Crosses Into Open-Source Governance | repo-article |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-25 | Polymarket | Geopolitics dominates; US-Iran escalation at 58.5% YES |

## Skills Built
*(Rows before Apr 1 archived to `memory/topics/skills-history.md`)*
| Skill | Date | Notes |
|-------|------|-------|
| skill-discover | 2026-04-01 | Autonomous discovery of trending skills from SkillsMP/GitHub; scores, security-checks, and ranks gap-filling candidates (aeon PR #6) |
| github-pages-gallery | 2026-04-02 | Jekyll-based public gallery at docs/ — publishes articles as browsable posts; update-gallery skill syncs weekly (aeon PR #7) |
| deep-research | 2026-04-04 | Exhaustive multi-source synthesis (30–50 sources, 3K–5K words) using 1M context; shallow/deep modes via --depth flag (aeon PR #9) |
| memory-flush (improved) | 2026-04-04 | Added stale-entry cleanup step: removes resolved PR lists, prunes Next Priorities, archives old Skills Built rows (aeon-agent PR #5) |
| skill-smoke-tests | 2026-04-05 | Static SKILL.md validator + test-skills.yml CI workflow — runs on every PR touching skills/; checks frontmatter, cron, secrets, placeholders (aeon PR #10) |
| cost-report | 2026-04-07 | Weekly API cost breakdown — reads token-usage.csv, computes $ per skill/model (Opus/Sonnet/Haiku pricing), week-over-week trend, top 10 by cost (aeon PR #12) |
| fork-fleet | 2026-04-08 | Weekly fork fleet scan — inventories active forks, scores divergence (+3 new skill, +2 unique commit), deep-reads top 3 forks' unique skills, surfaces upstream candidates (aeon PR #13) |
| skill-evals | 2026-04-09 | Output quality assertion framework — validates recent skill outputs against per-skill manifests (word count, required/forbidden patterns, numeric range checks); covers 14 skills; runs Sunday 6 AM UTC (aeon PR #27) |
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

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs to prevent pile-up and conflicts
- fetch-tweets 7-day search window causes duplicate notifications — dedup by checking last 3 days of logs for already-reported tweet URLs

## Repo Actions Ideas Pipeline
~45 ideas generated (9 runs). Recently built: cost-report, fork-fleet, skill-evals, mcp-skill-adaptor, workflow-security-audit, skill-version-tracking, skill-leaderboard, a2a-gateway, syndicate-article (Dev.to), skill-graph, star-milestone, syndicate-article (Farcaster). Key unbuilt: Dashboard Live Feed, Public Status Page, Memory Search API, Contributor Auto-Reward. See `articles/repo-actions-*.md`.

## Next Priorities
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes
