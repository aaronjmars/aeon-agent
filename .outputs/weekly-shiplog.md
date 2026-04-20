*Weekly Shiplog — 2026-04-20*

Aeon closed its loops this week — three independent dedup layers (per-skill, per-scheduler, per-message) now stack end-to-end after a crescendo of new surfaces (MCP + A2A + 25 fork-merge skills + MIT License) and ended with memory exposed as a public REST API.

Shipped:
- Memory Search API (PR #41 open) — read-only REST at /api/memory/* unblocks MCP/A2A access to agent state
- Three-layer notification dedup stack — repo-pulse same-day (PR #15), scheduler catch-up gating, notify SHA256 hashing
- Star Milestone + Farcaster syndication merged just before the imminent 200-star crossing (aeon at 195)

Stats: ~100 meaningful commits, 19 PRs merged, ~+15,000/-3,500 lines. AEON +48.62% 24h snapback.
Full update: https://github.com/aaronjmars/aeon-agent/blob/main/articles/weekly-shiplog-2026-04-20.md
