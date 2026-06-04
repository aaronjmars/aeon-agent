*Push Recap — 2026-06-04*
6 substantive PRs · 2 distinct human authors · aeon=3 / aeon-agent=2 / minitor=1

*Wallet-Risk Weekly (aeon #340)*: First scheduled consumer of the HoundFlow security pack — six keyless onchain skills had been workflow_dispatch-only since 2026-05-28. Monday 11:15 UTC weekly audit of every Base wallet in .x402books/wallets.json: scans 24k blocks for Approval events, confirms each grant live via allowance eth_call, flags >=2^255 as UNLIMITED, simulates a sell via eth_call (no funds at risk) to detect honeypots.

*Skill of the Day (aeon #341 by Nurstar)*: New external contributor's first PR — meta-content skill that picks one skill from a rotation queue each morning, drafts a paste-ready "Aeon skill of the day 🌟" tweet, then dispatches the picked skill so the live outcome arrives as the screenshot body. Two notifications per run, 30-day suppression window, operator-editable queue + blocklist.

*aeon-agent backport chain → day 21 + anti-pattern cleanup site 5 (PRs #80 #81)*: narrative-convergence backported from upstream PR #272 (mcp-pulse and fleet-scorecard remain). repo-article $(date) → literal ${today}-derived SINCE — went through mid-review hardening that isolated the SINCE cutoff into its own step with an explicit "never leave YYYY-MM-DD literal" guard, structurally safer than the verbatim shape-match the previous 4 sites used.

*minitor per-column UX axis hits rung 6 (#60)*: Per-column duplicate. Series: tab groups → collapse → JSON export → quick-search → pin-to-front → duplicate. Inherits notifyWebhookUrl (same-install copy stays inside the trust boundary); sets pinned: false. Mid-PR fix wrapped shift+insert in db.transaction() — a crash between the two writes would leave later columns shifted right with no duplicate filling the gap.

Key changes:
- aeon/skills/wallet-risk-weekly/SKILL.md +299 (12-state exit taxonomy, atomic state writes, 100% keyless Base RPC)
- aeon/skills/skill-of-the-day/SKILL.md +146 + memory/topics/skill-of-the-day.md +136 (queue + covered + blocklist)
- minitor/app/actions.ts +83 duplicateColumn server action (db.transaction wrap landed mid-review)

Stats: ~13 files changed, +1,278/-9 lines
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-04.md
