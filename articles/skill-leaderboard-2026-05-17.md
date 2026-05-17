# Skill Leaderboard — 2026-05-17

*47 active forks scanned (pushed in last 30 days)*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | heartbeat | 47 | 100% | ↑15 forks |
| 2 | token-movers | 7 | 14.9% | ↑4 forks (was 9.4%) |
| 3 | narrative-tracker | 5 | 10.6% | ↑4 ranks (was rank 7 at 6.25%) |
| 3 | token-pick | 5 | 10.6% | NEW |
| 3 | market-context-refresh | 5 | 10.6% | ↑ (was rank 2 at 9.4%) |
| 6 | token-alert | 4 | 8.5% | — (was rank 2 at 9.4%) |
| 6 | token-report | 4 | 8.5% | — (was rank 2 at 9.4%) |
| 6 | skill-health | 4 | 8.5% | — (was rank 2 at 9.4%) |
| 6 | deep-research | 4 | 8.5% | ↑1 rank (was rank 7 at 6.25%) |
| 6 | morning-brief | 4 | 8.5% | ↑1 rank (was rank 7 at 6.25%) |
| 11 | cost-report | 3 | 6.4% | — |
| 11 | monitor-polymarket | 3 | 6.4% | — |
| 11 | hacker-news-digest | 3 | 6.4% | — |
| 11 | github-trending | 3 | 6.4% | ↑ (recovered; was 2 → 3) |
| 15 | defi-monitor | 2 | 4.3% | — |
| 15 | on-chain-monitor | 2 | 4.3% | — |
| 15 | monitor-kalshi | 2 | 4.3% | — |
| 15 | paper-digest | 2 | 4.3% | — |
| 15 | defi-overview | 2 | 4.3% | — |
| 15 | github-monitor | 2 | 4.3% | ↑ (recovered; was 1 → 2) |
| 15 | skill-repair | 2 | 4.3% | — |
| 15 | evening-recap | 2 | 4.3% | — |
| 15 | goal-tracker | 2 | 4.3% | — |
| 15 | monitor-runners | 2 | 4.3% | NEW |
| 15 | idea-capture | 2 | 4.3% | — |
| 15 | polymarket-comments | 2 | 4.3% | NEW |
| 15 | distribute-tokens | 2 | 4.3% | NEW |

*43 additional skills appear in exactly one fork (largely tomscaria's extended configuration).*

## Consensus Skills (>50% of forks)

**heartbeat** remains the sole consensus skill — 47/47 active forks (100%). The number is larger than last week, but the percentage is unchanged: every operator who sets up an instance leaves it on.

The gap between heartbeat and the rest has widened. Last week the runner-up tier sat at 9.4% (3 forks); now the #2 slot is token-movers at 14.9% (7 forks). Still 85+ percentage points below heartbeat. No skill has broken through the "multiple serious operators have to agree" barrier to reach consensus territory.

## Adoption Gaps

Skills shipped upstream with `enabled: false` that no active fork has yet turned on:

**Newer skills (shipped May 3–17, zero fork adoption):**
- **star-milestone** — triggered May 14 on the source repo for the first time; no fork has enabled it
- **star-momentum-alert** — projects next star milestone via 7d rolling avg; shipped May 5
- **operator-scorecard** — weekly Monday synthesis of health + community + economic signals
- **skill-freshness** — walks skill file dependencies, flags stale inputs
- **skill-update-check** — drift detection and priority triage for skill versions across the fleet
- **ai-framework-watch** — weekly competitive-intelligence digest across 9 AI frameworks
- **fork-cohort** — buckets every fork by activation stage (COLD/STALE/ACTIVE/POWER)
- **contributor-spotlight** — recognition post for top POWER fork
- **fork-release-tracker** — celebrates when any fork cuts a tagged GitHub release
- **fleet-state** — Monday synthesis layer over fork-cohort + fork-release-tracker + contributor-spotlight
- **fork-skill-gap** — per-fork upstream skill adoption gap report
- **fork-first-run-alert** — same-day alert the first time a fork completes a workflow run
- **price-threshold-alert** — real-time token alert for ATH and ±20% 1h moves
- **show-hn-draft** — Show HN launch asset drafter
- **product-hunt-launch** — Product Hunt asset pack drafter (shipped May 15)

**Persistent gaps (present since April leaderboards):**
- **repo-scanner** — repo audit tool; never adopted
- **syndicate-article** — cross-posts articles to Dev.to and Farcaster; three active content-operator forks exist, none have enabled it
- **pr-triage** — first-touch external-PR triage; shipped Apr 29, still at zero

The adoption gap across newer skills is structural: skills ship `enabled: false` by design, and operators who forked before a skill landed only pick it up by actively pulling upstream. The highest-leverage unopened skills: **fork-cohort** (gives every operator fleet visibility) and **skill-update-check** (makes the full upstream drift visible at a glance).

## Week-over-Week

Last week (2026-05-10): 32 active forks, 114 total skill slots, 58 unique skills.
This week (2026-05-17): 47 active forks, 170 total skill slots, 70 unique skills.

The fleet grew by 15 forks in 7 days — the largest single-week intake recorded. Five of those new forks arrived with multi-skill configurations, driving most of the slot and unique-skill gains.

**New multi-skill operators (joined since May-10):**

| Fork | Skills | Profile |
|------|--------|---------|
| theipgirl/aeon | 14 | Personal productivity suite — no crypto skills at all |
| itr010038/aeon | 11 | Deep crypto market intelligence (Polymarket + token monitors) |
| Azh1er/aeon | 7 | Token-focused + aixbt-pulse (only fork running this skill) |
| ashneil12/aeon | 7 | Infra + token-movers + proxmox-capacity (only fork running this) |
| madebyshun/blueagent-aeon | 7 | Token-focused + github-monitor + distribute-tokens |

**theipgirl** is the most notable new entrant: 14 skills enabled, none of them crypto. Productivity, research, and workflow skills only. First data point that Aeon operators aren't all running token-monitoring configurations.

**Rising skills (moved up 3+ positions):**
- **narrative-tracker**: rank 7 → rank 3 (↑4 positions) — moved from Boodszw+tomscaria exclusive to a 5-fork cluster including both new crypto-monitor operators
- **token-pick**: NEW at rank 3 — not on last week's list at all; now 5 forks (Azh1er, madebyshun, itr010038, Boodszw, tomscaria)

**Dropouts:**
No skills that had 2+ forks last week dropped to zero this week. The floor held.

| Metric | Last Week (2026-05-10) | This Week (2026-05-17) | Change |
|--------|------------------------|------------------------|--------|
| Active forks | 32 | 47 | +15 |
| Total skill slots | 114 | 170 | +56 |
| Unique skills seen | 58 | 70 | +12 |
| Heartbeat-only forks | 25 | 35 | +10 |
| Multi-skill forks | 7 | 12 | +5 |
| Forks with no aeon.yml | 0 | 0 | — |
| Consensus skills (>50%) | 1 | 1 | — |

The +56 slot gain is spread across new operators rather than concentrated in one fork's config change (unlike last week's -25 swing, which was almost entirely tomscaria's reset). That's a healthier growth signal.

## Fleet Summary

- **Active forks scanned:** 47 (pushed in last 30 days)
- **Total skill slots enabled (across all forks):** 170
- **Unique skills seen:** 70 (68 from standard catalog + 2 custom: github-upstream-tracker from ether-btc, macos-apps from 0xfreddy, proxmox-capacity from ashneil12)
- **Forks with no aeon.yml:** 0

### Fork activation breakdown

| Skills enabled | Forks |
|----------------|-------|
| 1 (heartbeat only) | 35 |
| 2 | 3 (ether-btc, pezetel, 0xfreddy) |
| 3 | 1 (DannyTsaii) |
| 7 | 3 (Azh1er, ashneil12, madebyshun) |
| 11 | 1 (itr010038) |
| 13 | 1 (Boodszw) |
| 14 | 1 (theipgirl) |
| 15 | 1 (maacx2022) |
| 52 | 1 (tomscaria) |

### Most active forks this week

| Fork | Skills enabled | Profile |
|------|---------------|---------|
| tomscaria/aeon | 52 | General-purpose multi-skill |
| maacx2022/aeon | 15 | Content + research + DeFi |
| theipgirl/aeon | 14 | Personal productivity (no crypto) |
| Boodszw/Boodszw_Bread | 13 | DeFi + prediction markets |
| itr010038/aeon | 11 | Crypto market intelligence |
| Azh1er/aeon | 7 | Token-focused + aixbt-pulse |
| ashneil12/aeon | 7 | Infra + productivity + token-movers |
| madebyshun/blueagent-aeon | 7 | Token-focused + distribute-tokens |
| DannyTsaii/aeon | 3 | Digest + capture |
| ether-btc/aeon | 2 | Custom: github-upstream-tracker |
| pezetel/aeon | 2 | github-trending |
| 0xfreddy/aeon | 2 | Custom: macos-apps |

---
*Source: GitHub API — forks of aaronjmars/aeon*
