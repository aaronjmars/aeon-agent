# Long-term Memory
*Last consolidated: 2026-03-25*

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

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)

## Next Priorities
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes (blocks status-skill and per-skill-model PRs)
