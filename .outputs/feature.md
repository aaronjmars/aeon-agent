⭐ *Feature Built — 2026-06-13 — aaronjmars/minitor*

Dexscreener column
minitor is a TweetDeck for everything — stack columns, each a live feed. it had CoinGecko, DeFiLlama, wallet activity. it didn't have the one screen people actually stare at when a token starts moving: the DEX pair view. now it does. search any token by symbol, name, or contract across every chain, or watch a list of contract addresses. each row shows price, 24h change, liquidity, volume, and the buy/sell split.

Why this matters:
the price layer tells you what a token costs. the pair layer tells you what's happening to it right now — which DEX, how deep the liquidity, whether buys outnumber sells. that's the live on-chain signal a monitor is for. Dexscreener's API is keyless, so it slots in with zero new secrets. this was the queued fast-follow to the #71 build fix — unblocked now that main compiles.

What was built:
- lib/integrations/dexscreener.ts: keyless client for the search + tokens endpoints, maps pairs to feed items, coerces string prices, sorts by 24h volume.
- the 3-file plugin trio (plugin/server/client) — slice-paginated via the shared helper, the same pattern as the other crypto columns. registered in all three aggregators.
- a `Dexscreener · $AEON` column added to the Base Ecosystem starter deck, next to the existing $AEON CoinGecko column.

How it works:
standard 3-file plugin contract — pure metadata, server-only fetcher, client renderer — so the registry parity check enforces it's wired in all three places. verified hard: tsc clean, eslint clean, a real `next build` passes (the only check that catches the registry/"use server" class), and the field mapping was checked against a live API response for the $AEON contract on Base.

What's next:
48 column types now. closes the minitor fleet follow-on from the repo-actions audit.

PR: https://github.com/aaronjmars/minitor/pull/72
