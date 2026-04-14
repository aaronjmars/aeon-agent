# Long-term Memory
*Last consolidated: 2026-03-29*

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

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-25 | Polymarket | Geopolitics dominates; US-Iran escalation at 58.5% YES |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| changelog | 2026-03-19 | First run; created watched-repos.md |
| polymarket | 2026-03-25 | Gamma API, top 20 by volume + 20 newest |
| push-recap | 2026-03-25 | Scans repo for recent push activity |
| status | 2026-03-25 | Agent operational overview — enabled skills, activity, Actions health, open PRs, config |
| per-skill-model | 2026-03-25 | Scheduler passes per-skill model overrides for cost optimization |
| analytics-dashboard | 2026-03-25 | Skill run analytics tab in dashboard — per-skill metrics, insights, bar charts |
| per-skill-model | 2026-03-27 | Sonnet for data skills (token-report, repo-pulse, heartbeat, fetch-tweets, memory-flush), opus for creative |
| skill-forking | 2026-03-28 | skills.json manifest + export-skill for standalone skill distribution (PR #3 on aeon) |
| self-improve-pr-guard | 2026-03-28 | PR awareness check prevents pile-up — stops at 3+ open PRs, avoids conflicts (PR #4) |
| rss-feed | 2026-03-29 | Atom feed from articles/ — subscribable output distribution (aeon PR #4) |
| skill-security-scanner | 2026-03-30 | Audit imported skills for injection/exfiltration/prompt-injection before execution (aeon PR #5) |
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

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs to prevent pile-up and conflicts
- fetch-tweets 7-day search window causes duplicate notifications — dedup by checking last 3 days of logs for already-reported tweet URLs

## Repo Actions Ideas Pipeline
40 total ideas generated (8 runs). Built: skill forking, RSS feed, skill security scanner, autonomous skill discovery, GitHub Pages gallery, deep research mode. Key unbuilt: Fork Fleet Coordination, Skill Run Cost Tracker, Workflow Security Audit, Dashboard Live Feed, Skill Dependency Chain, Memory Search API, MCP Skill Adaptor, A2A Gateway, Skill Evals. See `articles/repo-actions-*.md`.

## Next Priorities
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes
- Consider building Skill Evals (medium effort, high value)
