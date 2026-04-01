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

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs to prevent pile-up and conflicts
- fetch-tweets 7-day search window causes duplicate notifications — dedup by checking last 3 days of logs for already-reported tweet URLs

## Open Improvement PRs
4 PRs pending merge on aeon-agent (blocking further self-improve runs):
- #1 heartbeat end-of-day, #2 per-skill model overrides, #3 fetch-tweets dedup, #4 PR awareness guard

## Repo Actions Ideas Pipeline
40 total ideas generated (8 runs). 3 built (skill forking, RSS feed, skill security scanner). Key unbuilt: Autonomous Skill Discovery, GitHub Pages Gallery, Deep Research Mode, Fork Fleet Coordination, MCP Skill Adaptor, Claude Code Plugin, A2A Gateway, Skill Evals. See `articles/repo-actions-*.md`.

## Next Priorities
- Merge 4 open improvement PRs to unblock self-improve
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes
