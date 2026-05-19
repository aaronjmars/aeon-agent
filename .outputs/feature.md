*Feature Built — 2026-05-19 — aaronjmars/minitor*

CoinGecko Trending + Price Column (45th column type)
Minitor now has a CoinGecko column with three modes: trending coins (24h search-volume leaderboard), top by market cap (paginated), and custom watchlist (comma-separated CoinGecko ids). Every row shows the coin's price, 24h change with a red/green arrow, an optional 7-day sparkline, market cap, and 24h volume. Keyless by default — works out of the box with no API key.

Why this matters:
The Apps & on-chain cluster had wallet activity (wallet-tx) and prediction markets (polymarket) but no price or trending feed — the most obvious "what's hot in crypto right now" signal. Looking at aeon's skill-leaderboard data, token-movers, token-pick, and defi-monitor are among the most-adopted skills across the fork cohort, signalling that a large share of operators are crypto-native. This column closes the most obvious monitoring gap for that audience and is the natural pair to the wallet-tx column already in the manifest. Picked from May-18 repo-actions idea #4.

What was built:
- lib/integrations/coingecko.ts: 228-line fetcher with three modes; auto-routes between api.coingecko.com (keyless) and pro-api.coingecko.com (when COINGECKO_DEMO_API_KEY is set). Handles two response-shape quirks between the trending and markets endpoints.
- lib/columns/plugins/coingecko/{plugin,server,client}.tsx: 3-file plugin matching the crates/npm/pypi pattern. Brand-green #8DC647 chip, Activity badge icon, TrendingUp plugin icon.
- lib/columns/{manifest,registry,server-registry}.ts: registry parity entries.
- README.md + .env.example: count 44→45, Apps & on-chain cluster 4→5, keyless list + optional COINGECKO_DEMO_API_KEY documented.

How it works:
Three endpoints are routed by mode. Trending hits /api/v3/search/trending — a fixed 7-coin window of the 24h search-volume leaderboard, so it's fast and has no pagination. Top hits /api/v3/coins/markets?order=market_cap_desc with full pagination and sparkline data included. Watchlist hits the same markets endpoint but with ids= filter; input is normalised (lowercased, deduped, 50-id cap, multiple separator support). Two integration quirks are worth flagging: trending returns USD prices as currency-formatted strings ($1,234.56) while markets returns them as plain numbers, and price_change_percentage_24h is a USD-keyed object on trending but a flat number on markets — both are normalised in the mapper so the renderer doesn't have to branch. The sparkline is a pure SVG polyline (no charting library) with green/red colour based on first vs last value.

What's next:
Could add CoinGecko's /coins/{id}/market_chart endpoint for a dedicated single-coin detail column. Or pair with a per-row threshold alert (when watchlist coin 24h change crosses a configurable %). The IndieHackers RSS column from today's repo-actions idea #5 is still open and would round out the launch-signal trio (PH + HN + IH).

PR: https://github.com/aaronjmars/minitor/pull/44
