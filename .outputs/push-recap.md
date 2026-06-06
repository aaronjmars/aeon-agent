*Push Recap — 2026-06-06*
11 substantive PRs across 3 repos, ~43 files, +3,878/-860 lines, 1 author (aaronjmars).

*Taxonomy refresh (aeon):* 6 stacked PRs rebuilt the catalog top-to-bottom — 5→8 categories adding core/onchain-security/meta, 65 untyped other skills recategorized, README count corrected 156→193, new docs/CORE.md documenting the load-bearing 15 self-evolution/fleet/autonomous-action skills. First time README ↔ skills.json ↔ mcp-server all agree on the same numbers and buckets.

*New skill (aeon):* atrium-catalog-watcher (#342) — Friday 12:00 UTC weekly diff of the Atrium onchain marketplace. Closes the three-weekly digest loop: marketplace arrivals + curated registry + installed-skill drift, no overlap.

*Continuity (aeon-agent + minitor):* 22nd consecutive same-day-after backport — mcp-pulse (#82); only fleet-scorecard from PR #272 remains. minitor #61 added per-column color labels (7th rung on the UX axis: tab/collapse/export/search/pin/duplicate/color).

Key changes:
- generate-skills-json get_category restructured to match the load-bearing core block first; skills.json regenerated to 0 other (aeon #346)
- 8 aeon-aaron skills ported in one PR (fear-divergence-scout, beat-tracker, article-queue, picks-tracker, content-performance, api-health-probe, mention-radar, thread-writer) + memory-structural-dedupe extended to merge duplicate H2 headings (aeon #343, +1455 lines)
- mcp-pulse backport caught a mid-PR structural fix: nonexistent template var today_minus_7 referenced — would have silently returned zero results every run (aeon-agent #82)

Stats: ~43 files changed, +3,878/-860 lines
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-06.md
