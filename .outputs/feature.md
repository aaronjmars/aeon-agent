*Feature Built — 2026-05-24 — aaronjmars/minitor*

Per-Column Refresh Intervals
Minitor columns can now auto-refresh on a configurable cadence — Manual / 1 min / 5 min / 15 min / 60 min — chosen per column from the Configure dialog. Until today, every column refreshed only on mount and manual click, so operators had to pick between burning rate limits (over-poll everything) or staring at stale data (under-poll everything).

Why this matters:
The 47-plugin column catalog is now a mix of fast-moving crypto/price feeds (CoinGecko, DeFiLlama, polymarket) and slow-moving repo signals (GitHub stars, releases, PyPI updates). One global cadence can't serve both — crypto rows go stale in 60 seconds, but hitting GitHub's API every minute on a 6-column dashboard burns through the 60 req/hr keyless budget in five minutes. The May-22 repo-actions brief flagged this as the highest-impact ergonomics gap that requires zero plugin changes — the interval lives at the column-row level, sibling to `alertKeywords` (PR #41) and `title`, never reaching the strict-Zod plugin fetchers.

What was built:
- drizzle/0002_refresh_interval.sql + meta/_journal.json + meta/0002_snapshot.json: Additive NULLABLE `refresh_interval_seconds` integer on the `columns` table.
- lib/db/schema.ts + lib/columns/types.ts: Schema field + `Column.refreshIntervalSeconds?: number` type.
- app/actions.ts (+52): `REFRESH_INTERVAL_OPTIONS` server-side allowlist (`{60, 300, 900, 3600}`), `isAllowedRefreshInterval` guard, new `updateColumnRefreshInterval` server action, plus export/import/`loadSnapshot` wiring and an optional Zod field on the import payload.
- lib/store/use-deck-store.ts (+33): `updateRefreshInterval` store action mirroring `updateAlertKeywords` pattern from May-16.
- components/column/configure-column-dialog.tsx (+71): "Refresh interval" Select with the five options, wired to the store action.
- components/column/column-card.tsx (+84): `useEffect` reads `refreshIntervalSeconds`, drives a `setInterval`-based auto-refresh with an `inFlight` guard (no overlapping fetches), pauses when `document.visibilityState !== 'visible'` (background tabs don't burn rate limits), cleans up on unmount and on interval change. New Clock-icon badge in the column header showing "1m" / "5m" / "15m" / "60m" (hidden on manual-only).
- lib/deck-templates.ts (+4): Template column type opted into the new field so future starter templates (PR #47) can pre-seed sensible cadences.

How it works:
The field is column-row-level, not plugin-config-level — so all 47 existing plugins keep working with zero changes and their strict Zod schemas remain untouched. Server-side, the allowlist refuses anything outside `{null, 60, 300, 900, 3600}` so a malformed client can't force 1-second polling against an upstream rate-limited API. Client-side, the `useEffect` rebuilds the interval whenever the configured value changes (clean teardown of stale timers); the in-flight guard prevents overlapping fetches if a slow API takes longer than the refresh window. Deck export/import and the share-link fragment encoder all round-trip the new field; decks created before this PR import cleanly as manual-only by default.

What's next:
Two natural follow-ups: per-plugin recommended-cadence defaults (so a fresh CoinGecko column auto-picks 1m instead of manual), and a global "low-power mode" toggle that bumps every column to the next-slower bucket when on metered connections.

PR: https://github.com/aaronjmars/minitor/pull/49
