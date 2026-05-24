*Thread Draft — 2026-05-24*
Topic: Per-column refresh intervals — Minitor PR #49

1/ Minitor columns now auto-refresh on a per-column timer. CoinGecko can tick every minute. GitHub stars can wait an hour. None of the 47 plugins required a single line of code to change.

2/ Until today, every column in Minitor refreshed once on load and whenever you clicked. One cadence for everything. If you set it fast, you burned rate limits on GitHub star counts. If you set it slow, your DeFiLlama TVL was always stale.

3/ The refreshIntervalSeconds field lives at column-row level — it never touches the plugin fetchers. The interval also pauses when the tab isn't visible, so background tabs don't run down rate limits while you're not watching.

4/ Two fields now use this architecture in Minitor — alertKeywords from PR #41 and this one. Both sit at column-row level and never enter the plugin layer. That's how a 47-plugin system picks up new behavior without a single plugin needing to change.

5/ Per-column refresh intervals for Minitor — choose Manual, 1m, 5m, 15m, or 60m per column. PR #49: https://github.com/aaronjmars/minitor/pull/49

(article: articles/thread-2026-05-24.md)
