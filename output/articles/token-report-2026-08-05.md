---
type: Article
title: $AEON — 2026-08-05
description: Daily token report for $AEON — price, volume, liquidity, and market context
tags: [token, aeon, base, crypto]
---

# $AEON — 2026-08-05

**Verdict:** ACCUMULATING — Price flat (−1.0%) at 2.5× volume, buyers outnumber sellers 1.48:1, but whale flow skews sell-heavy (13 vs 6).

## 24h at a glance

| Metric | Now | 24h Δ | vs 7d avg |
|--------|-----|-------|-----------|
| Price | $0.00001481 | −1.0% | — |
| Liquidity | $554.0K | +4.3% (~6d) | — |
| Volume (24h) | $230.5K | — | 2.5× |
| Buys / Sells | 179 / 121 (~9.6h) | ratio 1.48 | — |
| Whale trades (≥$1k) | 19 (6 buy / 13 sell) | — | — |
| FDV | $1.48M | — | — |

## Trend
- **7d:** +140.8% (violent breakout then partial fade)
- **30d:** −22.9% (still below early-July levels despite the spike)

## What changed
AEON round-tripped hard this week: from ~$0.0000064 on 07-31 to a $0.0000207 high on 08-02 (that single day printed $1.86M in volume, ~20× the prior day), then faded back to $0.0000148 — net flat over the trailing 24h (−1.0%). Today's volume ($230.5K) still runs 2.5× the 7-day daily average, and order flow read bullish on count (179 buys vs 121 sells), which is what pins the label at ACCUMULATING. But size tells a different story: the three biggest single trades were all sells — $3.4K @ $0.0000159 (00:10 UTC), $3.4K @ $0.0000163 (08-04 23:25 UTC), $2.5K @ $0.0000167 (02:15 UTC) — and whale trades overall split 13 sells to 6 buys. Read: retail is buying the dip after the spike, a handful of larger wallets are selling into it. 30d is still down −22.9% despite the run-up, so this week's move recovered ground rather than broke new highs.

Note on data continuity: `token-report` didn't run 08-01 through 08-04 (a ~44h GitHub Actions dispatch outage, per the 08-04 heartbeat log), so the prior `TOKEN_REPORT_STATE` snapshot is 6 days old rather than 1. The 24h price delta above is computed from hourly OHLCV (not the stale state line) to stay accurate; liquidity's 24h Δ has no closer baseline available and is marked accordingly.

## Social Pulse
Conversation is amplification-led (news/official accounts recapping listings and partnerships), not organic hype — no grassroots thread caught fire independently.
- **@BSCNews** (70 likes, 7 reposts): flagged AEON's listing on @Aster_DEX alongside other tokens.
- **@Yaki_fomoArt** (31 likes, 3 reposts): bullish take on the @aeonframework × @0xprogrammable Uniswap v4 hooks partnership, citing chart setup and launchpad upside.
- **@AEON_Community** (42 likes, 8 reposts): official July recap covering exchange listings, AI agent integrations, and payment rails.

## Context
No confirmed link between the 08-01/08-02 price spike itself and a specific announcement — it predates the Aug 4 aeonframework × 0xprogrammable partnership post and the Aster DEX listing mention surfaced in Social Pulse, both of which landed after the move had already largely faded. Flagging both as plausible contributors to this week's elevated volume regime, not as confirmed causes of the spike.

---
*Chart: https://www.geckoterminal.com/base/pools/0x4a9b9e13975d26f4e3e17c655593bb82145dd4452aedafb826d856b817c9cfd4*
*Contract: 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | Chain: Base*
*Sources: gt=ok · ds=ok · xai=ok · treasury=skip*
