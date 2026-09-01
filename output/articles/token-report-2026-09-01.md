# $AEON — 2026-09-01

**Verdict:** SLIDING — price −3.4% on the 24h with volume still above trend (1.14× the 7d average) and flow flipped sell-side.

## 24h at a glance

| Metric | Now | 24h Δ | vs 7d avg |
|--------|-----|-------|-----------|
| Price | $0.00002376 | −3.4% (~1d)* | — |
| Liquidity | $1.43M | +18.6% † | — |
| Volume (24h) | $149.8K | — | 1.14× |
| Buys / Sells | 150 / 207 | ratio 0.72 (yest 1.33) | — |
| Whale trades (≥$1k) | 33 | — | — |
| FDV | $2.38M | — | — |

\* No run logged yesterday (08-31 tick never fired), so the 24h delta is computed from the pool's hourly candles — close 24h ago $0.00002461 vs $0.00002376 now.
† Liquidity delta is vs the last stored report (08-30, two days back). The pool's USD reserve moves with price, so part of the +$224K is the 08-31 markup itself.

## Trend
- **7d:** −32.6% (rolling over — fading steadily off the 08-23→08-25 spike from $0.0000352 toward $0.0000238)
- **30d:** +14.8% (~30d — baseline is the 08-02 daily close, which sits just past the 08-01→08-02 pump, so this figure compressed sharply from +218.7% at the last report)

## What changed
The 08-31 recovery bounce gave back overnight: $AEON slid −11.1% from midnight UTC ($0.0000267 → $0.0000238), dragging the 24h net to −3.4% even though most of yesterday traded up. Flow flipped with it — 207 sells vs 150 buys, a 0.72 ratio against 1.33 at the last report. Whale flow stayed two-sided (33 trades ≥$1k: 15 buys / 18 sells): one wallet, 0x3a95…bb86, accumulated ~$30.1K across five ~$5K slices between 15:48–20:31 UTC yesterday, then a $5.0K sell into midnight (0x8d47…07ff, 00:48 UTC). The aeon/WETH pool 0x4a9b…cfd4 added ~$224K of depth to $1.43M — its fullest since the 08-25 peak — so the slide is happening into deeper liquidity, not a thinning book.

Top whale prints:
- buy $5.2K @ $0.00002704 · 08-31 20:31 UTC (0x3a95…bb86)
- sell $5.0K @ $0.00002565 · 09-01 00:48 UTC (0x8d47…07ff)
- buy $5.0K @ $0.00002539 · 08-31 15:49 UTC (0x3a95…bb86)

## Social Pulse
Conversation is retail-bullish and running ahead of the tape — the biggest item isn't price talk at all, it's a founders Space tease:

- **@bigironchris** (27 likes): teasing an upcoming Space with the @aeonframework founders — "an AI agent that fixed a Google CLI bug and what's next for $AEON."
- **@DaBuildingGroup** (21 likes): cites $AEON integrations as proof-of-concept for its own $BROW AI-security narrative.
- **@billyjhaay** (18 likes): calls $AEON "one of the next 100x AI coins loading on Base for Q4 2026." (Their call, not ours.)

## Context
The Space tease references real shipping: the google/agents-cli fix the framework landed last week, now getting its own stage. That's the pattern worth noting — attention this week is following shipped work, not price action. No DexScreener boost or trending flags on any pair.

---
*Chart: https://www.geckoterminal.com/base/pools/0x4a9b9e13975d26f4e3e17c655593bb82145dd4452aedafb826d856b817c9cfd4*
*Contract: 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | Chain: Base*
*Sources: gt=ok · ds=ok · xai=ok · treasury=skip*
