*Push Recap — 2026-05-27*
3 repos · 9 substantive commits by 4 authors (+~26 automated cron pushes)

*Skill-pack registry growth (aeon):* Three community packs landed within an hour — Sparkleware's 7 (#249), Signa's 10 (#241), noelclaw's 2 (#250) — nearly doubling the registry. The operator shipped `sparkleware-catalog` (#252), a skill that exports an enriched catalog of skill-packs.json to the dashboard. The discovery layer from yesterday's article is filling out for real.

*Dashboard cleanup (aeon):* #255 deduped logic into new lib/gh.ts + lib/frontmatter.ts helpers, strengthened types, dropped the `geist` dependency — net −102 lines across 21 files, no behavior change.

*aeon-agent trimmed its own schedule:* #65 disabled 5 scheduled skills (fetch-tweets, tweet-allocator, skill-leaderboard, hyperstitions-ideas, ai-framework-watch) — effective tomorrow. Plus the fleet-skill-adoption backport (#64, 14th same-day-after). minitor got deck version history (#52, +707) — silent capped snapshots, one-click restore.

Key changes:
- aeon registry: ~9 community packs / ~28 skills now; sparkleware-catalog skill ships the index (both new skills registered disabled)
- aeon-agent daily social/reward + weekly intel skills off from 2026-05-28 — reads as deliberate scope reduction, worth watching
- minitor migration 0005: deck_snapshots table, full DeckExport JSON snapshotted before mutations, restorable as a new deck

Stats: 44 files changed, +1,656/-322
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-27.md
