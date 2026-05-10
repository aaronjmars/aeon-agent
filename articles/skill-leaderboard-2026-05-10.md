# Skill Leaderboard — 2026-05-10

*32 active forks scanned (pushed in last 30 days)*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | heartbeat | 32 | 100% | ↑4 forks |
| 2 | token-alert | 3 | 9.4% | ↑1 rank (was 7.1%) |
| 2 | token-movers | 3 | 9.4% | ↑1 rank |
| 2 | token-report | 3 | 9.4% | ↑1 rank |
| 2 | market-context-refresh | 3 | 9.4% | ↑1 rank |
| 2 | skill-health | 3 | 9.4% | ↑1 rank |
| 7 | cost-report | 2 | 6.25% | NEW |
| 7 | defi-monitor | 2 | 6.25% | NEW |
| 7 | deep-research | 2 | 6.25% | — |
| 7 | defi-overview | 2 | 6.25% | — |
| 7 | evening-recap | 2 | 6.25% | — |
| 7 | github-trending | 2 | 6.25% | ↓2 ranks (was rank 2 at 10.7%) |
| 7 | hacker-news-digest | 2 | 6.25% | — |
| 7 | monitor-kalshi | 2 | 6.25% | NEW |
| 7 | monitor-polymarket | 2 | 6.25% | NEW |
| 7 | morning-brief | 2 | 6.25% | — |
| 7 | narrative-tracker | 2 | 6.25% | NEW |
| 7 | on-chain-monitor | 2 | 6.25% | NEW |
| 7 | paper-digest | 2 | 6.25% | — |
| 7 | skill-repair | 2 | 6.25% | — |

*38 additional skills appear in exactly one fork (tomscaria's extended configuration).*

## Consensus Skills (>50% of forks)

**heartbeat** is the sole consensus skill — 32/32 active forks (100%). Every operator who sets up an instance leaves it on. No other skill comes within 90 percentage points: the next tier tops out at 9.4%.

The 100% rate isn't surprising. Heartbeat is the first skill any operator enables and the last they'd turn off — it's the liveliness signal that makes everything else interpretable. What's interesting this week is that the tier just below it reshuffled toward DeFi and analytics rather than content discovery.

## Adoption Gaps

Skills with **zero fork enables** across 32 active forks (catalog entries shipped `enabled: false` that no operator has yet flipped):

**Persistent gaps (present since April leaderboards):**
- **repo-scanner** — repo audit tool; present since early catalog, still at zero
- **syndicate-article** — cross-posts articles to Dev.to and Farcaster; zero adoption despite ~3 active content-operator forks
- **vercel-projects** — Vercel deployment tracker
- **pr-triage** — first-touch external-PR triage; shipped Apr 29, zero operators have enabled it

**New gaps (shipped May 3–10, not yet adopted):**
- **skill-freshness** — walks skill file dependencies, flags stale inputs; shipped May 4/5 to both repos
- **star-momentum-alert** — projects next star milestone via 7d rolling avg; shipped May 5
- **operator-scorecard** — weekly Monday synthesis of health + community + economic signals; shipped May 3/4
- **contributor-spotlight** — recognition post for top POWER fork; shipped May 9
- **skill-update-check** — drift detection and priority triage for skill versions; shipped May 9
- **ai-framework-watch** — weekly competitive-intelligence digest across 9 AI frameworks; shipped May 10
- **fork-cohort** — buckets forks by activation stage (POWER/ACTIVE/STALE/COLD); shipped May 10

**Newly dropped to zero:**
- **article** — was at 1 fork (tomscaria only) last week; tomscaria's configuration reset removed it. First skill to transition from active → abandoned across the fleet.

The adoption gap has grown from 11 to ~18 entries. The pattern is consistent: skills ship `enabled: false` by design; operators who forked before the skill landed only pick it up if they actively pull upstream changes. The highest-value unopened skills for operators running content workflows: **syndicate-article** (pairs with article/push-recap to cross-post) and **skill-update-check** (makes all 80+ upstream skill drifts visible with priority tiers).

## Week-over-Week

Last week (2026-05-03): 28 active forks, 139 total skill slots, 95 unique skills.
This week (2026-05-10): 32 active forks, 114 total skill slots, 58 unique skills.

The headline number is counterintuitive: more forks, fewer total skill slots. The driver is **tomscaria**, who trimmed their configuration from 94 → 52 enabled skills — a -42 slot reduction that more than offsets the +4 new forks and Boodszw's +13 new slots. Unique skill count dropped from 95 to 58 for the same reason: most of the skills that appeared "in the fleet" last week were tomscaria-exclusive entries that are now disabled.

**Rising skills (moved up 3+ positions):**
None cleared the ↑3 threshold this week — the main mover was the tier reshuffle driven by Boodszw's activation.

**New entries to the 2-fork tier** (all from Boodszw joining as a multi-skill operator):
cost-report, defi-monitor, monitor-kalshi, monitor-polymarket, narrative-tracker, on-chain-monitor — all previously tomscaria-only, now at 2 forks.

**Dropouts from the 2-fork tier:**
- **github-trending**: 3 → 2 (was rank 2; tomscaria removed it, now maacx2022 + pezetel only)
- **github-monitor**: 2 → 1 (tomscaria removed it; maacx2022 only)
- **digest**: 2 → 1 (tomscaria removed it; DannyTsaii only)
- **idea-capture**: 2 → 1 (tomscaria removed it; DannyTsaii only)

**Notable new fork:** Boodszw/aeon entered the fleet this week with 13 skills enabled — the most skills of any fork that isn't tomscaria or maacx2022. Configuration is DeFi-and-prediction-market-heavy: all five on-chain/DeFi trackers, both prediction market monitors, three analytics skills, and heartbeat. No content skills. A clear second archetype emerging alongside maacx2022's "content + research + DeFi" profile.

| Metric | Last Week (2026-05-03) | This Week (2026-05-10) | Change |
|--------|------------------------|------------------------|--------|
| Active forks | 28 | 32 | +4 |
| Total skill slots | 139 | 114 | −25 |
| Unique skills seen | 95 | 58 | −37 |
| Forks with no aeon.yml | 0 | 0 | — |
| Consensus skills (>50%) | 1 | 1 | — |
| Adoption gaps | 11 | ~18 | +7 |

The -25 slot drop and -37 unique skill drop are almost entirely tomscaria's config reset. Strip that single fork and the fleet is stable to growing.

## Fleet Summary

- **Active forks scanned:** 32 (pushed in last 30 days)
- **Total skill slots enabled (across all forks):** 114
- **Unique skills seen:** 58 (56 from standard catalog + 2 custom: github-upstream-tracker from ether-btc, macos-apps from 0xfreddy)
- **Forks with no aeon.yml:** 0

### Fork activation breakdown

| Skills enabled | Forks |
|----------------|-------|
| 1 (heartbeat only) | 25 |
| 2 | 3 (ether-btc [github-upstream-tracker+hb], 0xfreddy [macos-apps+hb], pezetel [github-trending+hb]) |
| 3 | 1 (DannyTsaii [digest+idea-capture+hb]) |
| 13 | 1 (Boodszw — DeFi/prediction market suite) |
| 15 | 1 (maacx2022 — content + research + DeFi) |
| 52 | 1 (tomscaria — general-purpose multi-skill) |

### Most active forks this week

| Fork | Skills enabled | Profile |
|------|---------------|---------|
| tomscaria/aeon | 52 | General-purpose multi-skill (trimmed from 94) |
| maacx2022/aeon | 15 | Content + research + DeFi |
| Boodszw/aeon | 13 | DeFi + prediction markets (NEW this week) |
| DannyTsaii/aeon | 3 | Digest + capture |
| ether-btc/aeon | 2 | Custom: github-upstream-tracker |
| 0xfreddy/aeon | 2 | Custom: macos-apps |
| pezetel/aeon | 2 | github-trending |

---
*Source: GitHub API — forks of aaronjmars/aeon*
