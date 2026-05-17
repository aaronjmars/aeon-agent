---
name: token-report
description: Daily price performance report for the project's token — price, volume, liquidity, and context
var: ""
tags: [crypto]
---
> **${var}** — Token contract address. If empty, uses tracked token from MEMORY.md.

## Config

This skill reads the token to track from the "Tracked Token" section in `memory/MEMORY.md`.

```markdown
## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e... | base |
```

---

Read memory/MEMORY.md for the tracked token.
Read the last 7 days of memory/logs/ for previous price and volume data to show trends.

## Steps

1. **Fetch token info** from GeckoTerminal (free, no API key needed):
   ```bash
   # Token metadata + price
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/tokens/CONTRACT_ADDRESS"
   ```

2. **Fetch pool data** for the token (top liquidity pools):
   ```bash
   # Top pools for this token
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/tokens/CONTRACT_ADDRESS/pools?page=1"
   ```

3. **Fetch OHLCV data** for trend analysis:
   ```bash
   # Get the top pool address from step 2, then fetch candles
   # Daily candles for the last 30 days
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/ohlcv/day?aggregate=1&limit=30"

   # Hourly candles for the last 24h
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/ohlcv/hour?aggregate=1&limit=24"
   ```

4. **Fetch recent trades** for activity signal:
   ```bash
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/trades"
   ```

5. **Source social signal from the most recent fetch-tweets log** (sandbox-safe — no live curl):
   The direct `curl` to XAI used to live here, but it relied on `$XAI_API_KEY` expanding inside the bash header — which the sandbox blocks. The result was a daily false "XAI_API_KEY not set" line in the report even when the key was set and used by other skills' prefetch.

   Instead, locate the most recent `## fetch-tweets` (or `## Fetch Tweets`) section in `memory/logs/`:
   - Check today's log first — only useful on dispatches where token-report runs *after* fetch-tweets (default order is the reverse: token-report at 06:00 UTC, fetch-tweets at 06:30 UTC).
   - Fall back to yesterday's log. Yesterday's fetch-tweets run is the typical source — its data is ~24h old, which is the same window as the rest of the report.
   - If no `fetch-tweets` section exists in the last 2 days of logs, **omit the Social Pulse section entirely** from step 6's report. Do NOT mention `XAI_API_KEY` — the data source here is logs, not a live key.

   When you do find a section, extract 2-3 representative themes or notable accounts tied to the tracked token (give weight to higher-engagement tweets — those with the most likes / RTs / replies in the logged list). Note the source date inline at the end of the section (e.g. `via fetch-tweets log YYYY-MM-DD`) so a reader can tell how fresh the social read is.

6. **Compile the daily report**:
   ```markdown
   # Token Report — ${today}

   ## $TOKEN Performance

   | Metric | Value | 24h Change |
   |--------|-------|------------|
   | Price | $X.XXXX | +/-Y.Y% |
   | Liquidity | $X.XK | — |
   | 24h Volume | $X.XK | +/-Y.Y% |
   | 24h Buys/Sells | X / Y | — |
   | 24h High/Low | $X.XX / $X.XX | — |
   | FDV | $X.XM | — |

   ## Trend

   **Price**
   - **24h:** [price action summary from hourly candles]
   - **7-day:** +/-X.X% ([rallying, consolidating, pulling back, etc.])
   - **30-day:** +/-X.X% ([context])

   **Volume (daily)**
   - **24h:** $X.XK ([+/-Y.Y% vs prior day])
   - **7-day avg:** $X.XK ([+/-Y.Y% vs prior 7d])
   - **30-day avg:** $X.XK ([context — sustained, spiking, drying up, etc.])

   ## Volume & Liquidity
   [Is volume increasing/decreasing? Any notable large trades? Buy/sell ratio?]

   ## Social Pulse
   [Key mentions, sentiment, notable tweets from the most recent fetch-tweets log, with the source date inline (e.g. "via fetch-tweets log YYYY-MM-DD"). If no fetch-tweets log within the last 2 days, omit this entire section.]

   ## Context
   [1-2 sentences connecting price action to any known events — repo updates, market conditions]

   ---
   *Data: GeckoTerminal | Chain: Base*
   *Contract: CONTRACT_ADDRESS*
   ```

7. **Save** to `articles/token-report-${today}.md`

8. **Send notification** via `./notify`:
   ```
   *$TOKEN Daily — ${today}*

   Price: $X.XXXX (Y.Y% 24h)
   Liquidity: $X.XK | 24h Vol: $X.XK (Y.Y% 24h)
   Buys/Sells: X/Y
   7d: +/-X.X% price, +/-X.X% vol | 30d: +/-X.X% price

   [1-sentence summary]

   Chart: https://www.geckoterminal.com/base/pools/POOL_ADDRESS
   ```

9. **Log** to `memory/logs/${today}.md` including the current price and 24h volume (for price/volume trend comparison in future runs).

**Important:** If the GeckoTerminal API returns no data (token not found, API error, empty response), log "TOKEN_REPORT_NO_DATA" to memory and **do NOT send any notification**. Do not notify about failures or empty results.
