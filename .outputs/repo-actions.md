*Repo Action Ideas — 2026-06-02*
Generated from analysis of aaronjmars/aeon (475⭐, 153 forks), aeon-agent, and minitor (49 column plugins).

1. ecosystem-entrants (Feature, Small)
   Weekly diff of ECOSYSTEM.md git history to notify on newly-joined projects — two arrived today (HivemindOS, EchoOracle) with no automated signal.

2. wallet-risk-weekly (Integration, Medium)
   First consumer of HoundFlow's 6 keyless onchain investigation skills — weekly approval-audit + honeypot-check scan of wallets in .x402books/wallets.json, 72h after the skills shipped with zero downstream use.

3. pr-merge-queue backport (DX, Small)
   20th consecutive same-day-after backport of upstream aeon PR #318, adapting the daily open-PR risk-tier digest to aaronjmars/aeon-agent.

4. column-pinning-to-top (Feature, Small)
   Per-column pin toggle in minitor — writes pinned boolean to DB so priority columns stay left-anchored across page reloads, complementing tab groups and collapse on the deck-density UX axis.

5. skill-health-digest (Feature, Medium)
   Weekly RED/YELLOW/GREEN skill performance ranking from memory/cron-state.json — surfaces which specific skills are quietly degrading before they warrant filing an issue.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-06-02.md
