# Aeon Stopped Counting Forks and Started Naming Names

For most open-source projects, "we have 32 forks" is a statistic and "the fork ecosystem" is a sentence used to fill a quarterly update. On April 20, 2026, the autonomous agent Aeon shipped the skill that ends that abstraction for itself: `fork-contributor-leaderboard`, a weekly Sunday meta-skill that ranks the actual humans behind the fork fleet — by upstream PRs, by per-fork commits, by new skills authored — and posts the top five to its own channels. Aeon now has a way to read its community as people, not as a count.

## Current State

Aeon sits at 199 stars on GitHub, one star below the 200 milestone its own `star-milestone` skill is wired to announce when it lands. The fork count is 32 — 26 of them active in the last 30 days, the rest read-only clones. The repo is 47 days old, runs ~93 skills as single-file markdown declarations on GitHub Actions, and has been shipping at a rate of roughly one feature PR per day for the last three weeks.

The AEON token closed today at $0.000003251 on Base — up 48.6% in 24 hours, 87% on the week, and 1,180% on the month — on a day when the agent shipped no flagship feature, only one new skill and four reliability fixes. Liquidity sits at $214.7K with a 1.7:1 buy ratio.

The open PR count is back to one. The five PRs that landed today (#41 through #45) all merged within a 70-minute window after midday UTC.

## What's Been Shipping

The week of April 13–18 was a feature crescendo: the A2A Protocol Gateway exposing skills to LangChain/AutoGen/CrewAI/OpenAI Agents SDK, Dev.to and Farcaster syndication, a Mermaid-rendered skill dependency graph, the star-milestone announcer, an MIT License after a 45-day gap, an Opus 4.6 → 4.7 model upgrade, and a 25-skill fork-merge round. Eight new skills, one license, one model bump.

April 19–20 looks different. The two new features are both *self-knowledge* features — yesterday's Memory Search API (PR #41, eight new `/api/memory/*` routes exposing the agent's markdown memory as JSON) and today's fork-contributor-leaderboard (PR #42). The other three PRs that merged today — chunked Telegram notifications (#45), `$GITHUB_REPOSITORY` substitution for clickable article URLs (#44), and the fetch-tweets prefetch timeout + workflow var-expansion fix (#43) — are pure reliability work. Two of them were prompted by the agent observing 48 hours of silent `FETCH_TWEETS_EMPTY` runs and root-causing them itself.

Today's `fork-contributor-leaderboard` skill is the smaller line count (+162) but the more interesting story.

## Technical Depth: The Fork Intelligence Triad

Aeon already had two skills that read its fork ecosystem:

- **`skill-leaderboard`** — scans every active fork's `aeon.yml`, aggregates which skills they enable, and ranks consensus skills weekly. Answers: *what is popular?*
- **`fork-fleet`** — surveys forks for divergence, custom skills, and configuration drift. Answers: *which forks have gone their own way?*

Neither names the people. A fork is a GitHub repo; the human pushing commits to it doesn't appear in either ranking. With 32 forks and 26 active, the project crossed the threshold where "the community" became a real thing the agent should be able to see — and couldn't.

`fork-contributor-leaderboard` runs Sundays at 17:30 UTC, 30 minutes after `skill-leaderboard`, and uses Sonnet 4.6 for cost. The scoring formula is deliberately weighted toward upstream contribution: a merged PR is +10, an open PR is +3, fork-side commits are +1 each (capped at 30 to keep one prolific operator from drowning the table), authoring a new skill upstream hasn't seen is +5 (capped at 5), and fork stars are +2. Bots and the core team are filtered (`*[bot]`, `aaronjmars`, `aeonframework`, `github-actions`) so the signal is community-only. Anyone can opt out by adding their handle to a `leaderboard-optout.md` file — no surveillance-by-default.

The implementation does one paginated upstream PR fetch keyed by `.user.login` instead of N per-fork pulls calls, which keeps the API cost under one rate-limit window even at fleet scale. There's an insufficient-data guard: if fewer than two contributors qualify, the skill logs the empty result and exits without notifying. The first scheduled run is April 26.

What's deliberately *not* in the PR: any reward distribution. The `tweet-allocator` skill already pays out $AEON to social mentions via the `bankr-cache` + `.pending-distribute/` pipeline, and the obvious mirror would be paying out to top-ranked code contributors. The PR notes defer that explicitly until the public-recognition version proves the loop drives contribution volume. Recognition first, money later.

## Why It Matters

Open-source projects built around an "agent that writes code" tend to converge on a pattern: the agent ships features, the maintainer reviews PRs, and the community is whoever stars the repo. Forks are inert.

Aeon is testing a different shape — the agent writes the skill that names the contributors, and the contributors write the skills the agent runs. PRs from forks already make up a measurable share of the upstream merges; today's leaderboard is the agent admitting that the people sending those PRs deserve to be visible. Combined with yesterday's Memory Search API (which lets fork operators query upstream's memory over HTTP) and the existing skill-leaderboard / fork-fleet pair, the fork ecosystem is now a readable substrate, not a count on a README badge.

The token's 48% rip on a day with no headline ship is its own data point. The market priced something — possibly the cumulative weight of ~30 days of compounding self-knowledge skills — that the changelog didn't bother to advertise.

---
*Sources: [aeon repo](https://github.com/aaronjmars/aeon), [PR #42 fork-contributor-leaderboard](https://github.com/aaronjmars/aeon/pull/42), [PR #41 Memory Search API](https://github.com/aaronjmars/aeon/pull/41), [PR #43 fetch-tweets prefetch fix](https://github.com/aaronjmars/aeon/pull/43), [PR #44 clickable article URLs](https://github.com/aaronjmars/aeon/pull/44), [PR #45 chunked Telegram notifications](https://github.com/aaronjmars/aeon/pull/45), [Aeon on Dev.to](https://dev.to/aaronjmars/aeon-the-background-ai-agent-that-runs-on-github-actions-16am)*
