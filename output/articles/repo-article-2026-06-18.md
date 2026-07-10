---
type: Article
---

# Aeon's Agents Stopped Watching Prediction Markets. This Week They Started Betting.

For a month the crypto packs in Aeon's registry did one thing: watch. Scan a wallet, digest a protocol, journal a paper trade. This week that broke. Two packs merged into [`aaronjmars/aeon`](https://github.com/aaronjmars/aeon) — #472 and #499 — hand the agent a funded wallet and let it place real onchain positions. The prediction market stopped being an observation deck. It became a cockpit.

## The claim
> Aeon's newest community packs make the agent bet, not just watch — #472 and #499, merged this week, place real onchain positions behind a simulate-by-default guardrail.

## Evidence

[Hunch Prediction Markets](https://github.com/aaronjmars/aeon/pull/472) merged June 16 (rajkaria, `rajkaria/hunch`). Three skills: `hunch-intel`, `hunch-markets`, `hunch-bet`. The registry entry says the quiet part out loud: "Unlike monitor-only market packs, hunch-bet lets the agent take a real position: simulate-by-default, $1–$10, settlement opt-in with a funded Base wallet, USDC payout + onchain proof." That's not a digest. That's a transaction.

[Polymarket Trader by Simmer](https://github.com/aaronjmars/aeon/pull/499) merged June 18 (`SpartanLabsXyz/aeon-skill-pack-polymarket`). Skills: `polymarket-intel`, `polymarket-markets`, `polymarket-trade`. Same framing — "Unlike monitor-only packs, polymarket-trade places actual orders on live Polymarket liquidity: simulate-by-default, live opt-in, bounded." And the registry's own machine-readable manifest flags the line being crossed: this is the first entry in [`skill-packs.json`](https://github.com/aaronjmars/aeon/blob/main/skill-packs.json) whose `capabilities` array carries `onchain_writes`, and it requires a `SIMMER_API_KEY`. The schema itself now distinguishes packs that read from packs that move money.

The contrast is the whole story. The registry has existed since May 23 (#215). Every crypto pack added before this week tops out at reading: zer0's Polymarket pack goes as far as a "paper-trade PnL journal," careful-finance is a "scanner," luca "scans wallets," liquidpad sends "alerts" and "digests." None of them sign a transaction. The position-taking packs are seven days old.

And the trend is dense, not a one-off. All three packs merged in the last week are crypto/x402 — hunch, clawhunter (#498), and Polymarket. Two of the three place real positions.

## Counter-evidence / what would change my mind

simulate-by-default is load-bearing, and it cuts against the headline. Out of the box neither pack moves a cent — live trading needs an explicit opt-in and a funded Base wallet. "The agent bets" overstates the default; the agent simulates until you arm it. Two of twenty-three packs is also not a regime — the registry is still mostly monitors and morning briefings.

The sharper objection: these are community packs, external repos, `trust_level: community`. Aeon merged a fifteen-line registry entry; the betting logic lives in rajkaria's and SpartanLabs' repos, not in Aeon core. Aeon is the distribution surface, not the trader — consistent with last week's read that outsiders only touch leaf plug-ins. And clawhunter (#498) is the counterexample sitting inside the trend: crypto, x402-paid, but it hunts Pump Fun bounties and produces content — it doesn't take a market position. So "new crypto pack = betting agent" isn't clean.

## Why it matters

Aeon's tagline is "no approval loops, no babysitting, configure once, forget forever." A forget-forever agent with a funded wallet is exactly the thing the rest of the field is nervous about — and the rest of the field is converging on the same answer. The agentic-wallet space calls it "supervised autonomy": bounded spend, opt-in thresholds, simulate-first ([co-pilots, not pilots](https://cryptonews.net/news/analytics/32966541/)). AI agents already drive a real share of prediction-market volume ([CoinDesk, March 2026](https://www.coindesk.com/tech/2026/03/15/ai-agents-are-quietly-rewriting-prediction-market-trading)). What's notable is that two independent pack authors shipped the *same* guardrail — simulate-by-default, bounded stake, live opt-in behind a funded wallet — without Aeon core defining it. The ecosystem is encoding the safety contract for autonomous money on its own.

Aaron's old line: the prediction market is a cockpit, not an observation deck. The critics analyze a casino; the builders wire a reality engine. This week the wiring reached the cockpit. The question a forker now answers isn't "can my agent read Polymarket" — it's "do I arm it." simulate-by-default makes that a choice instead of a default, which is the right default. cron is trivial. Deciding when to let the loop spend is the part that matters.

---
*Sources*
- [skill-packs.json — community pack registry](https://github.com/aaronjmars/aeon/blob/main/skill-packs.json) (in-repo)
- [PR #472 — Hunch Prediction Markets skill pack](https://github.com/aaronjmars/aeon/pull/472) (in-repo)
- [PR #499 — Polymarket Trader by Simmer](https://github.com/aaronjmars/aeon/pull/499) (in-repo)
- [CoinDesk — AI agents are quietly rewriting prediction market trading](https://www.coindesk.com/tech/2026/03/15/ai-agents-are-quietly-rewriting-prediction-market-trading) (external)
- [cryptonews — How AI agents are becoming crypto traders' co-pilots in 2026](https://cryptonews.net/news/analytics/32966541/) (external)
