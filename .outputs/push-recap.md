*Push Recap — 2026-04-16*
aaronjmars/aeon + aeon-agent — 34 commits by 2 authors (@aaronjmars + aeonframework)

Dev.to Article Syndication: New syndicate-article skill auto-cross-posts articles to Dev.to with canonical URLs back to GitHub Pages. Includes postprocess-devto.sh sandbox fallback and DEVTO_API_KEY dashboard integration — full pipeline from publish to syndicate.

Notification Reliability: Fixed double-notification bug — messages were sent twice (immediate + post-run retry). Added DELIVERED flag tracking and pending file cleanup on successful delivery.

Monitor Kalshi: New prediction market skill covering Kalshi's public API — watchlist-based monitoring with 24h price/volume deltas, >5pp move alerts, and trending event discovery.

README Overhaul: 14 commits restructuring from 768→496 lines. New autonomy comparison table vs Claude Code BG Tasks, Hermes, OpenClaw. Category-based skill listings, visual assets, tighter positioning.

Architecture Sync: aeon-agent brought to full feature parity — A2A server, MCP server, chain runner, 30+ skills, dashboard decomposition (1531-line monolith → 11 components), docs site.

Heartbeat Escalation: Replaced flat 48h dedup with tiered system — persistent 3+ day issues now escalate instead of being silently suppressed. Root cause: dedup checked log entries, not notification records.

Key changes:
- add-skill script fixed for Linux (sed→awk)
- project-lens + repo-article upgraded to daily schedules
- Fork merge added 25 new skills, removed scheduler.yml

Stats: ~200 files changed, +10,500/-2,100 lines
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-16.md
