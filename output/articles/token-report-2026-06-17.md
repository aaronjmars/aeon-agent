---
type: Article
---

# $AEON — 2026-06-17

**Verdict:** CONSOLIDATING — price -4.8% on muted 0.4× volume, but four whale buys totaling $7.9K absorbed the slide

## 24h at a glance

| Metric | Now | 24h Δ | vs 7d avg |
|--------|-----|-------|-----------|
| Price | $0.00002775 | -4.8% | — |
| Liquidity | $1,222.3K | -3.3% | — |
| Volume (24h) | $49.3K | — | 0.4× |
| Buys / Sells | 93 / 99 | ratio 0.94 (prev 0.98) | — |
| Whale trades (≥$1k) | 5 | — | — |
| FDV | $2.78M | — | — |

## Trend
- **7d:** -12.9% (~7d from OHLCV, rolling off a $0.000032 peak on June 10)
- **30d:** -75.1% (~30d from OHLCV, full retracement off early-May highs near $0.000112)

## Treasury

| Wallet | Role | ETH | 24h Δ |
|--------|------|-----|-------|
| 0xf1e9…158e | treasury | 6.0000 | +0.0000 |
| 0x6797…e3a2 | deployer | 0.3166 | +0.1776 |

## What changed

Price slid -4.8% against the 06-15 stored state (the 06-16 run wrote no TOKEN_REPORT_STATE to the log). The move fits neither SLIDING nor QUIET: vol at $49.3K is 0.4× the 7-day average of $122.6K — too muted for SLIDING (which requires vol ratio ≥ 1.0×) — but five whale trades disqualify QUIET (which requires whale trades = 0). The directional weight was bullish: four whale buys between $1.1K and $3.0K hit the top pool on 06-16 between 15:03 and 17:26 UTC at prices of $0.00002803–$0.00002992 (totaling $7.9K), against a single $1.4K sell at 03:12 UTC today. Net whale flow: 4 buys to 1 sell. Liquidity in the top aeon/WETH Uniswap v4 pool pulled back $41K to $1.22M. Deployer wallet nearly doubled to 0.3166 ETH from 0.1390 on 06-15 — operationally healthy, likely an ETH top-up between runs.

---
*Chart: https://www.geckoterminal.com/base/pools/0x4a9b9e13975d26f4e3e17c655593bb82145dd4452aedafb826d856b817c9cfd4*
*Contract: 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | Chain: Base*
*Sources: gt=ok · ds=ok · xai=skip · treasury=ok*
