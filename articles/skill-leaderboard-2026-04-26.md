# Skill Leaderboard — 2026-04-26

*24 active forks scanned (pushed in last 30 days)*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | heartbeat | 24 | 100% | — |
| 2 | github-trending | 3 | 12.5% | ↑ (solo rank 2) |
| 3 | morning-brief | 2 | 8.3% | ↑1 |
| 3 | hacker-news-digest | 2 | 8.3% | ↑1 |
| 3 | paper-digest | 2 | 8.3% | ↑1 |
| 3 | github-monitor | 2 | 8.3% | ↑1 |
| 3 | token-alert | 2 | 8.3% | ↑1 |
| 3 | token-movers | 2 | 8.3% | ↑1 |
| 3 | token-report | 2 | 8.3% | ↑1 |
| 3 | defi-overview | 2 | 8.3% | ↑1 |
| 3 | market-context-refresh | 2 | 8.3% | ↑1 |
| 3 | deep-research | 2 | 8.3% | ↑1 |
| 3 | skill-health | 2 | 8.3% | ↑1 |
| 3 | skill-repair | 2 | 8.3% | ↑1 |
| 3 | evening-recap | 2 | 8.3% | ↑1 |
| 3 | article | 2 | 8.3% | ↑1 |
| 3 | startup-idea | 2 | 8.3% | ↑1 |
| 3 | digest | 2 | 8.3% | NEW |
| 3 | idea-capture | 2 | 8.3% | NEW |

## Consensus Skills (>50% of forks)

**heartbeat** remains the only consensus skill — enabled in all 24 active forks (100%). It's the liveliness check that runs three times daily; every operator who gets past initial setup leaves it on.

The 12.5% ceiling on everything else tells the same story as last week: the fleet is still infrastructure-first. Operators stand up the plumbing and leave most content and intelligence skills off by default. The exception is tomscaria/aeon, which runs the full suite at 94 skills — a single fork that now accounts for 69% of all enabled skill slots across the fleet.

## Adoption Gaps

Five skills exist in the source repo but have zero fork enables. These are the newest additions — recently merged skills the fleet hasn't had time to propagate:

- **repo-scanner** — repo audit tool; no forks have pulled this yet
- **syndicate-article** — cross-posts articles to Dev.to and Farcaster; impressive zero-adoption given how many content forks exist
- **skill-analytics** — fleet-wide skill run analytics; meta-skill useful for operators with multiple skills running
- **vercel-projects** — Vercel deployment tracker
- **contributor-reward** — closes the fork-contributor-leaderboard → token distribution loop; just shipped Apr 26

These are discoverability gaps, not quality gaps. Operators who enabled content skills (article, push-recap, repo-article) would benefit directly from syndicate-article — the pairing isn't surfaced in the onboarding flow.

## Week-over-Week

Last week (2026-04-19): 26 active forks, 42 total skill slots, 17 unique skills.  
This week (2026-04-26): 24 active forks, 137 total skill slots, 95 unique skills.

The jump — 42→137 slots, 17→95 unique skills — is almost entirely attributable to one fork: **tomscaria/aeon** joined the active window with 94 skills enabled, the highest any single fork has run. That one operator accounts for the entire broadening of the leaderboard tail this week.

**github-trending** broke out to rank 2 with 3 forks (pezetel/aeon added it), separating from the pack of 2-fork skills. It's the first skill since heartbeat to hold a unique rank position.

**New entries:** digest (2 forks — DannyTsaii + tomscaria), idea-capture (2 forks — DannyTsaii + tomscaria). Both entered directly at rank 3 because DannyTsaii's fork had them enabled alongside heartbeat.

**Dropout:** maacx2022/aeon is still active but pushed before the last-30-days cutoff — it dropped out of the window this week, taking its 15-skill profile with it. This explains why the fork count fell from 26→24 while the skill count surged: one power-user exited the window, one larger one entered.

| Metric | Last Week | This Week | Change |
|--------|-----------|-----------|--------|
| Active forks | 26 | 24 | −2 |
| Total skill slots | 42 | 137 | +95 |
| Unique skills seen | 17 | 95 | +78 |
| Forks with no aeon.yml | 0 | 0 | — |
| Consensus skills (>50%) | 1 | 1 | — |

## Fleet Summary

- **Active forks scanned:** 24 (pushed in last 30 days)
- **Total skill slots enabled (across all forks):** 137
- **Unique skills seen:** 95 (94 from aaronjmars/aeon catalog + 1 custom: macos-apps)
- **Forks with no aeon.yml:** 0

### Fork activation breakdown

| Skills enabled | Forks |
|----------------|-------|
| 1 (heartbeat only) | 18 |
| 2 | 2 (0xfreddy, pezetel) |
| 3 | 2 (DannyTsaii, davenamovich) |
| 15 | 1 (maacx2022) — last seen Apr 18 |
| 94 | 1 (tomscaria) |

### Most active forks this week

| Fork | Skills enabled |
|------|---------------|
| tomscaria/aeon | 94 |
| maacx2022/aeon | 15 |
| DannyTsaii/aeon | 3 |
| davenamovich/aeon | 3 |
| 0xfreddy/aeon | 2 (incl. custom: macos-apps) |
| pezetel/aeon | 2 |

---
*Source: GitHub API — forks of aaronjmars/aeon*
