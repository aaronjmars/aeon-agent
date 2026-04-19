# Skill Leaderboard — 2026-04-19

*26 active forks scanned (pushed in last 30 days)*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | heartbeat | 26 | 100% | — |
| 2 | morning-brief | 1 | 4% | — |
| 2 | hacker-news-digest | 1 | 4% | — |
| 2 | paper-digest | 1 | 4% | — |
| 2 | github-monitor | 1 | 4% | — |
| 2 | github-trending | 1 | 4% | — |
| 2 | token-alert | 1 | 4% | — |
| 2 | token-movers | 1 | 4% | — |
| 2 | token-report | 1 | 4% | — |
| 2 | defi-overview | 1 | 4% | — |
| 2 | market-context-refresh | 1 | 4% | — |
| 2 | deep-research | 1 | 4% | — |
| 2 | skill-health | 1 | 4% | — |
| 2 | skill-repair | 1 | 4% | — |
| 2 | evening-recap | 1 | 4% | — |
| 2 | article | 1 | 4% | — |
| 2 | startup-idea | 1 | 4% | — |

## Consensus Skills (>50% of forks)

**heartbeat** is the only consensus skill — enabled in all 26 active forks (100%). This is the liveliness check that runs at 8 AM, 2 PM, and 8 PM UTC, confirming the agent infrastructure is operational.

The dominance of heartbeat reflects how the fleet is composed: most forks are freshly deployed instances that have connected the plumbing (secrets, runners, schedule) but haven't yet selected which content or intelligence skills to activate. The agent stack is live; the programming layer is still to come.

## Adoption Gaps

The vast majority of Aeon's ~90 skills have zero or near-zero fork adoption. Notable underutilized skills that could drive significant value:

**Content & Publishing**
- `article`, `repo-article`, `push-recap` — automated content generation; only 1 fork running `article`
- `syndicate-article` — cross-posts to Dev.to and Farcaster; zero forks enabled
- `rss-feed`, `update-gallery` — builds public feed and Jekyll gallery; zero forks

**Intelligence & Monitoring**
- `repo-pulse`, `github-issues`, `github-monitor` — repo health signals; 1 fork running monitor
- `token-report`, `token-movers`, `token-alert` — token intelligence suite; 1 fork running all three
- `self-improve`, `skill-health`, `skill-repair` — the self-healing loop; 1 fork running health + repair

**Workflow Automation**
- `auto-merge`, `pr-review`, `issue-triage` — CI/CD automation; zero forks enabled
- `fork-fleet`, `skill-leaderboard` — meta-intelligence about the fleet itself; zero forks enabled
- `skill-evals` — output quality assertions; zero forks enabled

The pattern suggests forks are validating infrastructure before enabling intelligence. Skills like `skill-health` and `heartbeat` make a natural pair for an "ops-first" activation sequence.

## Week-over-Week

First leaderboard run — no prior data. All 17 unique skills are new entries. Baseline established for future tracking.

## Fleet Summary

- **Active forks scanned:** 26 (pushed in last 30 days)
- **Total skill slots enabled (across all forks):** 42
- **Unique skills seen:** 17
- **Forks with no aeon.yml:** 0 (all active forks carry the config)
- **Forks with only heartbeat:** 23 (88%)
- **Most active fork:** maacx2022/aeon — 15 enabled skills (full intelligence suite)
- **Second most active:** davenamovich/aeon — 3 enabled skills (article, startup-idea, heartbeat)

### Fork activation breakdown
| Skills enabled | Forks |
|----------------|-------|
| 1 (heartbeat only) | 23 |
| 3 | 1 (davenamovich) |
| 15 | 1 (maacx2022) |

---
*Source: GitHub API — forks of aaronjmars/aeon*
