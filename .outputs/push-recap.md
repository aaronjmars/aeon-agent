*Push Recap — 2026-06-05*
3 repos · 4 substantive PRs · 2 distinct human authors · ~+1,436/-7 lines

*Theme 1 — Closing the third install path's discovery loop:* aeon #342 atrium-catalog-watcher gives the operator a Friday-noon weekly diff of the Atrium onchain marketplace catalog with one-click install commands on every new entry — three install paths now each have a scheduled signal (sparkleware-catalog curated registry, skill-update-check installed-skill drift, atrium-catalog-watcher marketplace arrivals).

*Theme 2 — External MCP-server submission lands after multi-cycle hardening:* aeon #323 VIGIL (by vigilcodes, a brand-new external contributor) ships an onchain security scanner MCP server with 9 read-only tools — landed through 5 review cycles tightening a CRITICAL shell-injection vector (strict 0x+40-hex allowlist regex before any curl), capability declaration (read_only → external_api), and tool naming (vigil_* prefixed to match live /tools/list). Second new external contributor in 3 weeks.

*Theme 3 — 22nd consecutive same-day-after backport:* aeon-agent #82 mcp-pulse — the 4th of 5 general-ops skills from upstream PR #272. Mid-PR fix corrected a phantom ${today_minus_7} template-variable that would have silently broken the weekly window cutoff on every run. Only fleet-scorecard remains unbackported from PR #272 (memory/instances.json dependency).

*Theme 4 — Seventh per-column UX rung:* minitor #61 per-column color labels — 6-hex color renders as a dot beside the title and recolors the collapsed-strip accent gradient. New drizzle/0008_column_color.sql migration (additive nullable). Mid-PR fix relaxed the importedColumnSchema Zod from .regex() to .max(64) so one bad color in a hand-edited export can't abort the entire deck import (matches notifyWebhookUrl's drop-not-throw contract).

Key changes:
- aeon: atrium-catalog-watcher SKILL.md (+306) — supply-side weekly digest for the Atrium marketplace, install-from-atrium command on every added row
- aeon: VIGIL skill.md (+166) by vigilcodes external — 9 read-only MCP-spec tools at mcp.vigil.codes, Approval Revoker split out as future vigil-revoke (Bankr-gated)
- minitor: drizzle/0008_column_color.sql + 615/-5 across app/actions.ts + components — DB-backed color label, server-authoritative /^#[0-9a-f]{6}$/i regex

Mid-PR fix rate today: 3 of 4 (all structural — closed classes of bug not single ones).

Stats: 16 files changed, +1,436/-7 lines across 4 PRs
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-05.md
