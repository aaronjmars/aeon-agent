*Push Recap — 2026-04-28*
aaronjmars/aeon — 1 meaningful commit by @aaronjmars (PR #146); aeon-agent had 31 commits, all autonomous-scheduler bookkeeping (filtered).

*Public status page learns about the token:* The same `/status/` page that already broadcasts agent health now also broadcasts token health — a Price / 24h / Liquidity / Volume(24h) / FDV row read out of the latest `articles/token-report-*.md`. Zero new APIs, zero new secrets, zero new cron entries. Today's heartbeat already populated it: AEON $0.0000032626, -11.16%, $223.4K, $41.3K, $326.3K, verdict SLIDING.

*Why it matters:* Yesterday's PR #145 made the repo pitch itself to inbound traffic; PR #146 makes the destination URL pull double duty. Anyone landing from SHOWCASE.md, MCP directories, or HN gets one URL answering both reliability and market questions.

Key changes:
- `skills/heartbeat/SKILL.md` (+25/−1): tolerant regex extracts both old (`Value | 24h Change`) and new (`Now | 24h Δ`) token-report layouts so forks at different evolution stages keep working with no per-fork conditional
- `docs/status.md` (+6/−2): seeded Token pulse placeholder, updated intro and data-sources footer
- 24h staleness fallback (`_No recent token data..._`) and section-omit when no report exists — token-less forks still get a clean page

Stats: 2 files changed, +31/−3 lines
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-28.md
