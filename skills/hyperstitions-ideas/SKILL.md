---
name: hyperstitions-ideas
description: Generate a hyperstition-style prediction market idea — a fiction designed to make itself real through belief and circulation
var: ""
---
> **${var}** — Theme or domain override (e.g. "AI regulation", "crypto adoption", "autonomous agents"). If empty, scans broadly across current signals.

Today is ${today}.

Read memory/MEMORY.md and the last 7 days of memory/logs/ for context on what's been happening — recent articles, tweets, token activity, and repo developments.

## What is a hyperstition?

A hyperstition is a fiction that makes itself real. In prediction markets, this means: the act of creating the market and people trading on it **changes the probability of the outcome**. The market's existence influences the real world.

## The 5 qualities of a great hyperstition market idea

1. **Reflexivity** — trading on the market plausibly changes real-world behavior (e.g. a CEO sees the market, feels pressure to act)
2. **Engagement bait** — people want to trade AND share the question (it's provocative, contrarian, or touches identity)
3. **Real-world connection** — tied to something happening right now, not hypothetical future speculation
4. **Memetic potential** — the question itself is viral-worthy, screenshot-able, argument-starting
5. **Ambiguity in resolution** — interesting edge cases but still resolvable YES/NO with clear criteria

## Steps

1. **Gather live signals** from the current project and ecosystem:

   a. Read recent repo activity — what's been built, shipped, or discussed in the watched repos (check `articles/` for recent push-recaps, repo-articles, repo-actions).

   b. Read recent tweet data from `memory/logs/` — what's the community talking about? What's trending around the project's domain?

   c. Read recent token data from `memory/logs/` — any price movements, volume spikes, or market shifts?

2. **Fetch live Polymarket data** to understand what markets already exist:
   ```bash
   # Top markets by volume
   curl -s "https://gamma-api.polymarket.com/markets?limit=20&order=volume24hr&ascending=false&active=true" | jq '[.[] | {question, volume24hr: .volume24hr, outcomePrices: .outcomePrices}]'

   # Newest markets
   curl -s "https://gamma-api.polymarket.com/markets?limit=20&order=startDate&ascending=false&active=true" | jq '[.[] | {question, startDate: .startDate, outcomePrices: .outcomePrices}]'
   ```

3. **Identify gaps** — what questions *should* exist on Polymarket but don't? Look for:
   - Topics that are trending in crypto/AI/tech but have no prediction market
   - Events that are being debated online but nobody has put money on it yet
   - Outcomes that would become more likely if people started betting on them (reflexivity)

4. **Use WebSearch** to go deeper on the most promising intersection between your project's ecosystem and current events. Find the specific trigger — a tweet, an announcement, a policy proposal, a product launch — that makes this timely.

5. **Generate ONE market idea** that scores highly across all 5 qualities. Do not generate multiple — pick the single strongest one.

6. **Score it**:
   - Reflexivity: X/5 (how much does the market's existence change the outcome?)
   - Viral potential: X/5 (how shareable is the question?)

7. **If no compelling idea emerges** (both scores below 3/5), log "HYPERSTITIONS_SKIP: no strong idea today" and **do NOT send any notification**.

8. **Send notification** via `./notify`:
   ```
   *Hyperstition Idea — ${today}*

   "[Market question]?"

   Reflexivity: [1-2 sentences on how the market's existence changes real-world behavior — who sees it, who feels pressure, what feedback loop does it create?]

   Why now: [What specific signal triggered this idea — a tweet, a repo update, a price move, a news event? Be specific with names, dates, links.]

   Resolution: [Exact YES/NO criteria — what has to happen, by when, and who judges it]

   Scores: Reflexivity X/5 | Viral X/5
   ```

9. **Log** to `memory/logs/${today}.md`:
   ```
   ## Hyperstitions Ideas
   - **Question:** [the market question]
   - **Reflexivity:** X/5
   - **Viral:** X/5
   - **Trigger:** [what signal inspired it]
   - **Notification sent:** yes/no
   ```
