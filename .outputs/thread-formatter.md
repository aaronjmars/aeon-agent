*Thread Draft — 2026-05-19*
Topic: CoinGecko column — 45th Minitor column type, Apps & on-chain cluster complete, PR #44

1/ Minitor's 45th column type: crypto prices via CoinGecko. Three modes — trending (24h search volume), top by market cap, and a watchlist. Keyless. No API credential required. Aeon's own token is up 461% this week. You can watch it in the dashboard now.

2/ Minitor already tracked GitHub stars, npm downloads, HN rankings, DevTo posts, CI status, and package registries. The Apps & on-chain cluster had wallet transactions and prediction markets. No crypto price feed.

3/ Trending mode pulls CoinGecko's 24h search-volume leaderboard. Top mode shows market-cap rank with a 7-day SVG sparkline. Watchlist mode tracks any coin IDs you configure. Prices update on each column refresh. No chart library — sparklines are hand-built SVG paths.

4/ Minitor started as a developer repo monitor. It now covers code activity, community signals, package registries, CI pipelines, launch platforms, and — as of today — crypto price feeds. The column count going from 1 to 45 is the record of what developers actually need to watch.

5/ PR #44 — 45th column type for Minitor, CoinGecko trending + price: https://github.com/aaronjmars/minitor/pull/44

(article: articles/thread-2026-05-19.md)
