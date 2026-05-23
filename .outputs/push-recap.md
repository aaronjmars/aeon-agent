*Push Recap — 2026-05-23*
Six substantive PRs across aeon/aeon-agent/minitor, +664/-8 lines, four distinct authors (3 community, 1 Aeon bot). No merges to main today — all activity is open PRs.

*Community Skill Pack ecosystem (3 aeon PRs):* PR #215 ships skill-packs.json — machine-readable mirror of the README community-packs table, with five seed entries (slugs sourced live from each pack's own manifest). install-skill-pack grows a no-repo --list mode that reads the registry, falling back to the upstream raw URL when run outside a clone. PR #216 (antfleet-ops) and PR #217 (liquidpadbot) register two more packs into the README the same day — neither yet adds the matching skill-packs.json row, so PR #215's new dual-update checklist faces its first test on whichever merges first.

*First community on-chain skill (aeon PR #214):* lawbworld-tech contributes lawb-pool-monitor — hourly cron watching the LawbFishing prize pool on Base mainnet (proxy 0x48b2db9E89542Baa217bf8dc6269164b7887fE57). Four read-only selectors documented (prizePool/shopVault/paused/MIN_PRICE) plus the Redeemed burn event. State-file dedup on four alert conditions. Net +228 lines after the contributor cleaned up bot output accidentally committed on the feature branch.

*Backport cadence holds at 11 (aeon-agent PR #58):* contributor-spotlight FORK_DEFAULT_BRANCH backport from upstream aeon PR #206 — closes the silent-404 path on forks whose default branch isn't main, so ENABLED_COUNT and OPERATOR_AUTHORED stop being wrong on those runs.

*Minitor /gallery (PR #48):* server-rendered SEO-crawlable starter-deck catalog. Cards render as plain anchors pointing at /#deck=<base64url(payload)> — no exportedAt, so URLs are stable and cacheable. Sidebar gains a Browse-deck-gallery link. No new schema, no new server routes — stacks cleanly on PR #46 (share link) + PR #47 (templates).

Key changes:
- New skill-packs.json (84 lines) + install-skill-pack --list mode (+92/-4) — registry surface for the community-packs table
- New skills/lawb-pool-monitor/SKILL.md (+227 lines) — first PR-shaped community SKILL contribution
- New app/gallery/page.tsx (+173 lines) + sidebar Link — public deck gallery on top of existing share-link + templates infra

Stats: ~10 files changed (substantive), +664/-8 lines across 6 PRs (excludes 35+ cron auto-commits on aeon-agent main)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-23.md
