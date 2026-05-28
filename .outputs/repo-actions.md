*Repo Action Ideas — 2026-05-28*
Generated from analysis of aaronjmars/aeon (456⭐, 132 forks), aaronjmars/aeon-agent, and aaronjmars/minitor.

1. capabilities + secrets_required in skill-packs.json (Feature, Small)
   Add capability and secrets declarations to the registry so operators know before installing whether a pack needs secrets they haven't configured — closes open Issue #258.

2. ecosystem-pulse backport (DX, Small)
   16th same-day-after backport: aeon-agent has ECOSYSTEM.md but not the skill that monitors it. Verbatim copy of upstream aeon PR #227.

3. fork-health-score skill (Feature, Medium)
   Weekly per-fork health tier (ACTIVE/WARM/STALE/QUIET) combining push recency + skill count + PR activity — gives a single fleet-health ratio across 132 forks.

4. Farcaster cast feed column — 50th column type (Integration, Medium)
   Uses Neynar's free public API to add Farcaster channel/user feeds, completing the Web3 social set (X + Bluesky + Farcaster) and crossing the 50-column milestone.

5. Column tab groups (Feature, Medium)
   Partition decks into labeled tabs so operators with 8+ columns can navigate without horizontal scrolling — no plugin schema changes required.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-28.md
