# Skill Leaderboard — 2026-05-03

*28 active forks scanned (pushed in last 30 days)*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | heartbeat | 28 | 100% | — |
| 2 | github-trending | 3 | 10.7% | — |
| 3 | morning-brief | 2 | 7.1% | — |
| 3 | hacker-news-digest | 2 | 7.1% | — |
| 3 | paper-digest | 2 | 7.1% | — |
| 3 | github-monitor | 2 | 7.1% | — |
| 3 | token-alert | 2 | 7.1% | — |
| 3 | token-movers | 2 | 7.1% | — |
| 3 | token-report | 2 | 7.1% | — |
| 3 | defi-overview | 2 | 7.1% | — |
| 3 | market-context-refresh | 2 | 7.1% | — |
| 3 | deep-research | 2 | 7.1% | — |
| 3 | skill-health | 2 | 7.1% | — |
| 3 | skill-repair | 2 | 7.1% | — |
| 3 | evening-recap | 2 | 7.1% | — |
| 3 | digest | 2 | 7.1% | — |
| 3 | idea-capture | 2 | 7.1% | — |

## Consensus Skills (>50% of forks)

**heartbeat** is the only consensus skill — enabled in all 28 active forks (100%). Every operator who gets past initial setup leaves it on. It's the liveliness check that runs three times daily; nothing else comes close.

The next tier — github-trending at 10.7% (3 forks), the 15-skill block at 7.1% (2 forks each) — tells the same story as last month: the fleet is infrastructure-first. Operators stand up the plumbing, confirm heartbeat runs, and stop there. The exception is tomscaria/aeon, which runs 94 skills and accounts for 67.6% of all enabled skill slots across the fleet.

## Adoption Gaps

Eleven skills exist in the source catalog but have zero fork enables. Six of these are net-new since the April 26 leaderboard — all shipped `enabled: false` in the last week:

**New additions (shipped April 26 – May 3, zero forks have picked them up yet):**
- **contributor-reward** — closes the fork-contributor-leaderboard → token distribution loop; shipped Apr 26
- **skill-analytics** — fleet-wide skill run analytics; meta-skill useful for multi-skill operators; shipped Apr 25
- **smithery-manifest** — regenerates three Smithery/MCP Registry submission artifacts from skills.json; shipped May 1
- **show-hn-draft** — writes a Show HN body + Reddit variants from today's logs; workflow_dispatch only; shipped May 1
- **fork-cohort** — buckets every fork by activation stage (POWER/ACTIVE/STALE/COLD); shipped May 2
- **operator-scorecard** — weekly Monday synthesis of health + community + economic signals; shipped May 3
- **thread-formatter** — auto-formats the day's top event as a 5-tweet thread; shipped Apr 30

**Persistent gaps (exist for multiple leaderboard cycles):**
- **repo-scanner** — repo audit tool; no forks have pulled this yet
- **syndicate-article** — cross-posts articles to Dev.to and Farcaster; zero adoption despite many content-enabled forks
- **vercel-projects** — Vercel deployment tracker
- **pr-triage** — first-touch external-PR triage; shipped Apr 29

The adoption gap is widening: 5 gaps in April 26's report, 11 now. Every new skill ships `enabled: false` by design (operator opt-in), so the gap is expected to grow until forks begin pulling updates. The high-signal pair for operators who run content skills is **syndicate-article** (pairs with article/push-recap/repo-article to cross-post) and **skill-analytics** (gives a fleet-level pass-rate view once ≥3 skills are running).

## Week-over-Week

Last week (2026-04-26): 24 active forks, 137 total skill slots, 95 unique skills.
This week (2026-05-03): 28 active forks, 139 total skill slots, 95 unique skills.

**Fleet growth:** +4 net forks. Six new forks entered the 30-day window (artlu99, CNZSMJ, eugene-gourevitch, adarshhalan, KingKaonix, yugo-engineer — all heartbeat-only). Two exited: davenamovich/aeon (3 skills) fell outside the window; one more unidentified fork. The net effect is +4 forks but only +2 skill slots — all new entrants are heartbeat-only, so the active operator count is effectively flat.

**Dropouts at rank 3:** `article` and `startup-idea` fell from 2 forks to 1 fork each (tomscaria only). maacx2022/aeon re-entered the window on its April 18 push, but its current config (15 skills) doesn't include those two — likely trimmed at some point. Both remain in tomscaria's full suite.

**No new rising skills:** Every skill in the rank 3 tier held position. The leaderboard structure is stable week-over-week; the main dynamic is headcount, not skill activation.

| Metric | Last Week | This Week | Change |
|--------|-----------|-----------|--------|
| Active forks | 24 | 28 | +4 |
| Total skill slots | 137 | 139 | +2 |
| Unique skills seen | 95 | 95 | — |
| Forks with no aeon.yml | 0 | 0 | — |
| Consensus skills (>50%) | 1 | 1 | — |
| Adoption gaps | 5 | 11 | +6 |

## Fleet Summary

- **Active forks scanned:** 28 (pushed in last 30 days)
- **Total skill slots enabled (across all forks):** 139
- **Unique skills seen:** 95 (94 from standard catalog + 1 custom: macos-apps from 0xfreddy)
- **Forks with no aeon.yml:** 0

### Fork activation breakdown

| Skills enabled | Forks |
|----------------|-------|
| 1 (heartbeat only) | 23 |
| 2 | 2 (0xfreddy [macos-apps+heartbeat], pezetel [github-trending+heartbeat]) |
| 3 | 1 (DannyTsaii [digest+idea-capture+heartbeat]) |
| 15 | 1 (maacx2022) |
| 94 | 1 (tomscaria) |

### Most active forks this week

| Fork | Skills enabled |
|------|---------------|
| tomscaria/aeon | 94 |
| maacx2022/aeon | 15 |
| DannyTsaii/aeon | 3 |
| 0xfreddy/aeon | 2 (incl. custom: macos-apps) |
| pezetel/aeon | 2 |

---
*Source: GitHub API — forks of aaronjmars/aeon*
