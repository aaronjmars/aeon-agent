# Push Recap — 2026-06-20

## Verdict
> SHIPPING — Litebeam in MCP catalog, auth-secret one-click install unlocked

**Shape:** 3 user-visible commits · 0 internal · 0 infra · 30 bot-filtered  
**Volume:** 4 files changed, +24/−2 lines across 3 commits by 2 authors (aaronjmars, logbookbase)  
**Merged PRs:** 3 (#507 ecosystem: add logbook; #508 feat(mcp): add Litebeam; #509 fix(mcp): Litebeam avatar)

---

## aaronjmars/aeon

### MCP Catalog — auth-secret servers now first-class

**What this is:** The dashboard's one-click MCP install gained the ability to handle bearer-auth servers. Before today every featured entry was public, OAuth, or x402 — none needed a static API key wired into headers. Litebeam (an AI-microservice routing layer) ships as the first entry requiring a bearer token, and the installer now handles it.

**Shipped to users**

- `bb7077b` — feat(mcp): add Litebeam as a featured MCP template (#508)
  - `apps/dashboard/lib/mcp-catalog.ts`: Added `transport?: 'http' | 'sse'` and `authSecret?: string` to `McpCatalogEntry`. Litebeam entry uses `transport: 'sse'` and `authSecret: 'LITEBEAM_API_KEY'` (+16/−0)
  - `apps/dashboard/components/McpPanel.tsx`: `installFeatured()` now reads `f.transport ?? 'http'` (was hardcoded `'http'`) and — when `f.authSecret` is set — wires `Authorization: Bearer ${LITEBEAM_API_KEY}` into the server's headers object. The per-row paste-token box in the panel collects the key; runs skip that MCP with a warning until the secret is set. Both new fields are optional, existing entries unaffected. (+7/−2)

- `0d0fd15` — fix(mcp): use Litebeam's X avatar for the catalog logo (#509)
  - `apps/dashboard/lib/mcp-catalog.ts`: Swapped Litebeam's logo from `litebeam.xyz/litebeam.svg` (didn't render at 36px) to the X/Twitter profile image (400×400 JPEG), matching the convention of every other featured entry. (+1/−1)

### Ecosystem Growth — logbook self-lists

**What this is:** A new Aeon instance operator, logbook, added themselves to the public ecosystem registry.

**Shipped to users**

- `9a97ae9` — ecosystem: add logbook (#507) — external contributor PR from logbookbase
  - `ECOSYSTEM.md`: Added logbook ([@logbookonbase](https://x.com/logbookonbase) · [signedlogbook.com](https://signedlogbook.com)) to the live-instances table. (+1/−0)

---

## Developer notes

- **New dependencies:** none
- **Breaking changes:** none — `transport` and `authSecret` fields on `McpCatalogEntry` are optional; all existing catalog entries unchanged
- **New public surface:** `McpCatalogEntry.transport?: 'http' | 'sse'` and `McpCatalogEntry.authSecret?: string` in `apps/dashboard/lib/mcp-catalog.ts` — catalog contributors can now declare bearer-auth MCP servers with one-click install support
- **Tech debt added:** none

## Open threads

- PR #512 open — `apps/mcp-server/README.md` quickstart (shipped today by feature skill, pending merge)
- PR #511 open — Charon AEON skill pack (external contributor, flagged by repo-actions as top priority)
- PR #510 open — external contributor skill pack (review pending)
- PR #418 open — BEAMR gateway (stalled >72h per heartbeat)

## Sources

- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok (30 commits, all bot-filtered — aeonframework automation chore/cron/scheduler)
- aaronjmars/minitor: ok (0 commits in window)
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 30
- diff-truncated: 0
