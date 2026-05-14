*Feature Built — 2026-05-14 — aaronjmars/minitor*

crates.io Column
Minitor's 42nd column type lets users monitor the Rust package registry — trending crates from the last 90 days, all-time download giants, just-published crates, and active-maintenance flags — in the same deck where they already watch npm packages and Python PyPI releases. Picks a crate, drops it into a column, picks a sort axis (Trending / All-time / Recently updated / Newest / A–Z), optionally filters by keyword (tokio, axum, serde, wasm), and the deck refreshes from crates.io's public API with zero configuration.

Why this matters:
After npm (PR #35, May 12) and PyPI (PR #36, May 13 — still open), Rust was the last major package registry without a minitor surface. Rust's audience overlaps heavily with minitor's existing TypeScript + Python user base — the same operators running a `langchain` PyPI column also want to see `tokio`, `axum`, or `polars-rs` activity. This is the natural completion of the registry trifecta the May-13 PyPI PR description explicitly anticipated as the next obvious gap. crates.io's API is fully keyless and well-documented, matching minitor's no-secrets-required design philosophy.

What was built:
- lib/integrations/crates.ts: Keyless `GET /api/v1/crates` fetcher with five documented sort axes (recent-downloads / downloads / recent-updates / new / alpha), optional `q=` search across crate name + description + keywords, User-Agent compliance per crates.io's documented anonymous-request policy (no UA = 403), and pagination via `meta.next_page` with a length-fallback for older mirror deployments. Schema-drift safe — drops rows missing name or version, max_stable_version fallback chain handles pre-release-only crates.
- lib/columns/plugins/crates/: Standard 3-file plugin (plugin.ts / server.ts / client.tsx). #DEA584 Rust ember orange accent (distinct from npm's #CB3837 red, PyPI's #3776AB blue, devto's #3b49df indigo, and lobsters' #ac130d red). `Box` icon visually evokes a crate, distinct from npm's `Package` and PyPI's `Package2`.
- 3 registry edits (manifest.ts, registry.ts, server-registry.ts) — parity check verifies all three stay in sync at server module init.
- README.md: Hero paragraph picks up crates.io, column count 41 → 42, News & web cluster row 8 → 9, keyless-columns list updated.

How it works:
The integration hits `https://crates.io/api/v1/crates?sort={axis}&per_page=N&page=M&q={query}` with the required User-Agent. The five sort axes map directly to documented API values — no client-side ranking, no zombie-package risk. `recent_downloads` is a fixed 90-day window (different from npm's last-week stats, hence the explicit "/90d" label so users aren't confused). The row displays crate slug in mono font, a 3-line description clamp, a brand-coloured pill showing version + relative time, both download badges (recent-90d via Flame icon + all-time via Download icon, formatted with K/M/B suffixes), and up to 5 keyword pills. Pagination uses `meta.next_page` from the API response with a length-based fallback for mirror deployments that omit the field.

What's next:
The natural next layer is a Cargo ecosystem column (deps.rs, lib.rs, or shields.io badges for build status across the top 100 crates) — though that overlaps with the existing github-actions column when crates publish CI badges. A Rust-language version of stack-overflow filtering or a docs.rs documentation-freshness column could also pair well.

PR: https://github.com/aaronjmars/minitor/pull/38
