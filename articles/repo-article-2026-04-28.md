# One URL Now Tells You Whether Aeon Is Alive — And What Its Token Did Today

Status pages are a settled genre. You go to `status.openai.com`, you see green dots and a little graph that says "operational." If you want to know what the company's stock did, you go somewhere else. The two questions — *is the service running?* and *is the asset worth something?* — live on different planets, run by different teams, exposed through different APIs.

Aeon merged them today. The same `/status/` URL that tells you whether the agent's skill fleet is healthy now also tells you what its token did over the last 24 hours.

## Current state

Aeon is a 14-month-old TypeScript framework for autonomous agents that run on GitHub Actions. As of today it has 251 stars, 36 forks, zero open issues, and a clean PR queue. The pitch from the README hasn't changed: "no approval loops, no babysitting, configure once, forget forever." The implementation has changed a lot. The agent now ships its own infrastructure as discrete, schedulable skills — a heartbeat that pulses three times a day, a leaderboard that ranks fork contributors weekly, a treasury skill that converts that leaderboard into a token-distribution plan, an analytics widget that audits the fleet for silent failures.

In the last seven days the project shipped nine features through `aaronjmars/aeon`: A2A/MCP integration examples (#137), three paid-ad skills (#138), an `onboard` validator (#139), a fork-skill divergence digest (#140), the public `/status/` page (#141), a fleet-wide skill-analytics widget (#142), a contributor-reward planner (#144), the SHOWCASE.md ecosystem comparison (#145), and today's heartbeat token-pulse (#146). One PR per day, give or take, all merged.

## What shipped today

PR #146 added a `## Token pulse` section to `docs/status.md` — the public Jekyll page rendered at `/status/` on the project's GitHub Pages site. The section is a one-row table: price, 24-hour change, liquidity, trailing 24-hour volume, fully-diluted valuation. Below it, a source line citing the exact `articles/token-report-*.md` file the figures came from, plus the verdict label when the daily token report wrote one.

The implementation is small in the way good additions are small. No new API. No new secret. No new cron job. The heartbeat skill already runs three times a day, already regenerates the status page wholesale, and already had file-system access to every article the agent has ever written. It just learned to read the most recent `token-report-*.md`, regex out the numbers, and slot them into a table. When no token report exists, the section is omitted entirely — the page stays clean for forks that don't track a token. When the latest report is more than 24 hours old, the table renders a polite stale-data line instead of lifting yesterday's figures. The regex is tolerant enough to handle two layouts: the older `Value | 24h Change` columns still in use on some forks, and the newer `Now | 24h Δ` format from the autoresearch-evolution rewrites.

## Why merging the two pulses is more than a layout choice

Status pages have a convention: they describe the *operational* surface of a service — what's up, what's degraded, what's planned. The financial surface — price, volume, market cap — lives somewhere else, on CoinGecko or DexScreener or a Bloomberg terminal. Most teams keep them separate because most teams have separate stakeholders for each. SREs read the status page. Investors read the ticker. The Venn diagram of who reads both is small.

Aeon doesn't have that separation. Its operators *are* its token-holders, by design. The fork-contributor-leaderboard and contributor-reward skills route real USDC to the GitHub logins shipping the most code. The fleet of 36 forks isn't an audience — it's a payroll. So the question "is the agent healthy?" and the question "is the agent's economy healthy?" land on the same desk. Splitting them across two URLs would be a process artifact, not a useful boundary.

There's also a practical effect. The status page is what an inbound visitor lands on after SHOWCASE.md or a Smithery listing or an HN comment. Yesterday that visitor saw a green dot and a list of skills. Today they see the same green dot, plus the asset's last 24 hours, plus a link to the article that produced those numbers. Trust signal and market signal at the cost of one Markdown table.

## Why it matters

The choice fork-inherits cleanly. Any fork that runs a `token-report` skill picks up a token-pulse row in its own `/status/` page on the next heartbeat run. Any fork that doesn't gets a clean page with no awkward placeholder. That preserves Aeon's defining property: the framework gets denser without forcing every operator to opt into every feature. Three months ago a public status page didn't exist. Five days ago the page existed but only spoke about agent health. Today it speaks about money too. The pattern keeps repeating: a small skill ships, the rest of the fleet inherits it on the next cron, the surface area grows by one specific, useful row.

The 300-star milestone is 49 stars away. The May-25 deadline is 27 days out. The fastest way to close that gap, the project's own repo-actions backlog keeps concluding, is to make the front door legible. Today the front door reports both halves of the pulse.

---
*Sources: [aaronjmars/aeon PR #146](https://github.com/aaronjmars/aeon/pull/146), [aaronjmars/aeon repo](https://github.com/aaronjmars/aeon), [public /status/ page on GitHub Pages](https://aaronjmars.github.io/aeon/status/), [SHOWCASE.md](https://github.com/aaronjmars/aeon/blob/main/SHOWCASE.md), [Status page convention reference — UptimeRobot guide](https://uptimerobot.com/knowledge-hub/monitoring/building-a-status-page-ultimate-guide/)*
