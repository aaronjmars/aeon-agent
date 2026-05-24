# Skill Leaderboard — 2026-05-24

*86 active forks scanned (pushed in last 30 days)*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | heartbeat | 85 | 98.8% | +38 forks (fleet nearly doubled) |
| 2 | token-movers | 9 | 10.5% | ↑2 forks |
| 3 | morning-brief | 8 | 9.3% | ↑4 forks, ↑3 positions |
| 3 | narrative-tracker | 8 | 9.3% | ↑3 forks |
| 5 | market-context-refresh | 7 | 8.1% | ↑2 forks |
| 6 | cost-report | 6 | 7.0% | ↑3 forks, ↑5 positions |
| 6 | skill-health | 6 | 7.0% | ↑2 forks |
| 8 | on-chain-monitor | 5 | 5.8% | ↑3 forks, ↑7 positions |
| 9 | token-pick | 4 | 4.7% | ↓1 fork |
| 9 | deep-research | 4 | 4.7% | — |
| 9 | monitor-polymarket | 4 | 4.7% | ↑1 fork |
| 9 | token-report | 4 | 4.7% | — |
| 9 | evening-recap | 4 | 4.7% | ↑2 forks, ↑6 positions |
| 14 | defi-monitor | 3 | 3.5% | ↑1 fork |
| 14 | monitor-runners | 3 | 3.5% | ↑1 fork |
| 14 | token-alert | 3 | 3.5% | ↓1 fork |
| 17 | distribute-tokens | 2 | 2.3% | — |
| 17 | refresh-x | 2 | 2.3% | NEW |
| 17 | weekly-review | 2 | 2.3% | NEW |
| 17 | write-tweet | 2 | 2.3% | NEW |
| 17 | self-improve | 2 | 2.3% | NEW |
| 17 | polymarket-comments | 2 | 2.3% | — |
| 17 | skill-repair | 2 | 2.3% | — |
| 17 | aixbt-pulse | 2 | 2.3% | NEW |
| 17 | monitor-kalshi | 2 | 2.3% | — |
| 17 | research-brief | 2 | 2.3% | NEW |
| 17 | goal-tracker | 2 | 2.3% | — |
| 17 | hacker-news-digest | 2 | 2.3% | ↓1 fork |

*67 additional skills appear in exactly one fork.*

## Consensus Skills (>50% of forks)

**heartbeat** remains the only consensus skill — 85 of 86 active forks (98.8%). The single exception is jonathanjoseph20/aeon, which has a valid aeon.yml but zero skills enabled; it may be a recently initialized or transitional fork.

The gap between heartbeat and everything else has not narrowed. The fleet doubled in size since last week (47 → 86 forks), but the runner-up tier barely moved in fork count: token-movers went from 7 to 9 forks, still below 11% of the fleet. No second skill has broken through the consensus threshold. Heartbeat is structural — it ships enabled by default. Every other skill requires a deliberate operator decision.

## Adoption Gaps

Skills present in the source repo with `enabled: false` that no active fork has yet turned on:

**Fleet-intelligence skills (high-leverage, zero adoption):**
- **fork-cohort** — buckets every fork by activation stage (COLD/STALE/ACTIVE/POWER); the one skill that would tell each operator where they stand relative to peers
- **fork-skill-gap** — per-fork upstream skill adoption gap report; answers "what's in upstream you haven't adopted yet?"
- **fleet-state** — weekly synthesis over fork-cohort + fork-release-tracker + contributor-spotlight
- **skill-update-check** — drift detection across the fleet; would surface which forks are running outdated skills
- **operator-scorecard** — weekly health + community + economic synthesis

**Content skills (persistent gaps since April):**
- **repo-article**, **repo-actions**, **project-lens**, **push-recap** — all zero fork adoption despite being among the most active skills in the source instance
- **star-milestone**, **star-momentum-alert** — never adopted upstream despite triggering on the source repo
- **syndicate-article** — cross-posting to Dev.to and Farcaster; three active content operators in the fleet, none have enabled it

**Infra / maintenance skills:**
- **auto-merge** — automated PR merge; enabled in source, zero forks
- **skill-security-scan**, **skill-evals** — health triad skills; only skill-health and skill-repair have any fork adoption
- **huggingface-trending** — one of the most informative content skills in the source; zero forks

The structural reason is unchanged: skills ship `enabled: false`. Operators who forked before a skill landed must actively pull upstream to even see it. The highest-leverage skills still sitting at zero: **fork-cohort** and **skill-update-check** — together they close the "I don't know what I'm missing" loop that affects every fork.

## Week-over-Week

| Metric | Last Week (2026-05-17) | This Week (2026-05-24) | Change |
|--------|------------------------|------------------------|--------|
| Active forks | 47 | 86 | +39 (+83%) |
| Total skill slots | 170 | 254 | +84 (+49%) |
| Unique skills seen | 70 | 95 | +25 (+36%) |
| Heartbeat-only forks | 35 | 66 | +31 |
| Multi-skill forks | 12 | 19 | +7 |
| Zero-skill forks | 0 | 1 | +1 |
| Forks with no aeon.yml | 0 | 0 | — |
| Consensus skills (>50%) | 1 | 1 | — |

The fleet grew by 39 forks in 7 days — the largest single-week expansion on record. Most new arrivals came in at the heartbeat-only baseline (31 of 39 new forks), consistent with prior intake patterns. Seven new multi-skill operators joined, adding most of the +84 slot gain.

**New multi-skill operators (joined since May-17):**

| Fork | Skills | Profile |
|------|--------|---------|
| enzoonchain/aeon | 7 | DeFi + token-movers + cost-report |
| forge-executive/forge-executive | 9 | Content + market-context + morning-brief |
| VibeSan7/aeon | 6 | Research + deep-research + skill-health |
| cersei420/aeon | 3 | Custom: crypto-research + fitness-tracker |
| 0xMal0u/aeon | 8 | Crypto + competitor radar + PH launch |
| damo-nu11/aeon-minebean | 2 | Custom: mine-bean |
| anomit/aeon | 2 | Custom: powerloom-bds |

**cersei420** is notable: a custom `crypto-research` skill alongside a `fitness-tracker`, with no standard market monitoring. First data point of a fitness-skill operator in the fleet.

**0xMal0u** is the only fork besides the source instance running both `competitor-launch-radar` and `product-hunt-launch` — suggesting an operator actively tracking launch-surface intelligence.

**Rising skills (moved up 3+ positions):**
- **on-chain-monitor**: rank 15 → rank 8 (↑7 positions) — 2→5 forks; newly adopted by enzoonchain, itr010038's existing count, and Boodszw
- **evening-recap**: rank 15 → rank 9 (↑6 positions) — 2→4 forks
- **cost-report**: rank 11 → rank 6 (↑5 positions) — 3→6 forks; the "what did this cost to run?" feedback loop gaining traction across crypto-focused operators
- **morning-brief**: rank 6 → rank 3 (↑3 positions) — 4→8 forks; now tied with narrative-tracker

**New entries at rank 17+ (not on last week's list):**
- **refresh-x**, **weekly-review**, **write-tweet**, **self-improve**, **aixbt-pulse**, **research-brief** — all crossed into the two-fork tier for the first time

**Dropouts from the top tier:**
- **github-trending**: 3 forks → 1 fork (moved to one-fork tier; pezetel remains the only adopter)
- **hacker-news-digest**: 3 forks → 2 forks (slight pullback)
- **paper-digest**, **defi-overview**, **github-monitor**, **idea-capture**: all dropped from 2-fork to 1-fork tier

No skill with 2+ forks last week dropped to zero this week.

## Fleet Summary

- **Active forks scanned:** 86 (pushed in last 30 days)
- **Total skill slots enabled (across all forks):** 254
- **Unique skills seen:** 95 (includes 8 custom skills not in the source catalog)
- **Forks with no aeon.yml:** 0

### Custom skills in the fleet (not in source catalog)

| Skill | Fork | Domain |
|-------|------|--------|
| lawb-pool-monitor | lawbworld-tech/aeon | Custom pool monitoring |
| mine-bean | damo-nu11/aeon-minebean | Custom |
| powerloom-bds | anomit/aeon | Web3 infrastructure |
| crypto-research | cersei420/aeon | Custom research |
| fitness-tracker | cersei420/aeon | Health/fitness |
| hermesos-growth-desk, hermesos-finance-risk-review, hermesos-backup-restore-watch | ashneil12/aeon | Business ops suite |
| proxmox-capacity, fleet-sweep | ashneil12/aeon | Infrastructure monitoring |
| perps-scan, perps-brief, morning-macro | Azh1er/aeon | Perps trading intelligence |
| github-upstream-tracker | ether-btc/aeon | Custom GitHub tracking |
| token-call | Azh1er/aeon | Custom |

8 custom skill domains visible across the fleet — signals real specialization beyond the standard catalog.

### Fork activation breakdown

| Skills enabled | Forks |
|----------------|-------|
| 0 | 1 (jonathanjoseph20 — aeon.yml present, no enabled skills) |
| 1 (heartbeat only) | 66 |
| 2 | 6 (lawbworld-tech, damo-nu11, anomit, ether-btc, pezetel, and 1 more) |
| 3 | 1 (cersei420) |
| 6 | 2 (VibeSan7, DevZenPro) |
| 7 | 2 (enzoonchain, madebyshun) |
| 8 | 1 (0xMal0u) |
| 9 | 1 (forge-executive) |
| 11 | 1 (Azh1er) |
| 12 | 1 (ashneil12) |
| 13 | 2 (taekwonv89, Boodszw) |
| 14 | 1 (theipgirl) |
| 17 | 1 (itr010038) |
| 52 | 1 (tomscaria) |

### Most active forks this week

| Fork | Skills enabled | Profile |
|------|---------------|---------|
| tomscaria/aeon | 52 | General-purpose (nearly full catalog) |
| itr010038/aeon | 17 | Deep crypto market intelligence |
| theipgirl/aeon | 14 | Personal productivity suite (no crypto) |
| taekwonv89/aeon | 13 | Crypto + market-context + weekly-review |
| Boodszw/Boodszw_Bread | 13 | DeFi + prediction markets |
| ashneil12/aeon | 12 | Custom infra + token-movers |
| Azh1er/aeon | 11 | Token-focused + perps + aixbt-pulse |
| forge-executive/forge-executive | 9 | Content + market intelligence |
| 0xMal0u/aeon | 8 | Crypto + competitor radar + launch tracking |
| enzoonchain/aeon | 7 | DeFi + on-chain + cost-report |
| madebyshun/blueagent-aeon | 7 | Token-focused + distribute-tokens |
| VibeSan7/aeon | 6 | Research + skill-health |
| DevZenPro/aeon | 6 | Token-monitors + aixbt-pulse |

---
*Source: GitHub API — forks of aaronjmars/aeon*
