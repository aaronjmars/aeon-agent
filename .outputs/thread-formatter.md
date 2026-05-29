*Thread Draft — 2026-05-29*
Topic: fork-health-score — weekly ACTIVE/WARM/STALE/QUIET tiers for every fork in the fleet (aeon PR #271)

1/ Aeon now scores every fork in the fleet — ACTIVE, WARM, STALE, or QUIET — based on push recency, enabled skills, and 30-day PR activity. 138 forks. One health score per fork, every Monday morning.

2/ fork-cohort tracks which forks exist. fork-skill-gap tracks which skills they're missing. fleet-skill-adoption tracks how many forks have each skill enabled. None of those tell you whether a fork is actually alive and actively configured.

3/ Each fork gets a normalized 0-100 score: push recency is 50%, enabled-skill count 30%, 30-day PR throughput 20%. A fork needs at least 2 enabled skills to hit ACTIVE — high-push, low-config placeholders can't claim the tier on score alone.

4/ More than 110 of Aeon's 138 forks have been confirmed running scheduled skills in production. fork-health-score gives the fleet a weekly readout: who's still active, who went quiet, and how the ACTIVE ratio shifted week over week.

5/ fork-health-score — weekly ACTIVE/WARM/STALE/QUIET tiers for every fork in the fleet. aeon PR #271: https://github.com/aaronjmars/aeon/pull/271

(article: articles/thread-2026-05-29.md)
