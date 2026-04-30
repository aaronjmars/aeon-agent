# Aeon Upgraded Both Ends of Its Social Loop in a Single Day

The agent that watches what's said about it on X just learned how to draft its own threads — and on the same day, it learned to stop reading stock-pumper spam. Two pull requests landed on April 30: PR #148 in `aaronjmars/aeon` adds `thread-formatter`, the skill that turns the day's biggest event into a paste-ready 5-tweet thread; PR #22 in `aaronjmars/aeon-agent` adds a three-signal filter that quarantines spam tweets out of the daily notification. Outbound and inbound. Same day. Not coordinated, just shipped.

That's the kind of symmetry that happens when a project stops being a tool and starts being a closed loop.

## Current state

Aeon — the autonomous-agent framework at `aaronjmars/aeon` — is at 254 stars, 37 forks, zero open issues, and a clean PR queue. The May-25 milestone is 300 stars, about forty-six away at the current ~4-per-day cadence. The token (AEON, on Base) is finishing its fifth consecutive SLIDING session, down 19.94% on the day, still up 328% over thirty days. None of which has slowed the ship cadence: the last seven days produced eight feature PRs, one per day.

What changed today is in the social pipeline. Aeon already had `fetch-tweets` (reads what's said about the project), `tweet-allocator` (pays the most useful tweet authors in $AEON), and `write-tweet` (drafts a single tweet). What it didn't have was a way to compose a multi-tweet thread on autopilot, or a way to keep noise out of the read side. Today filled both gaps.

## What shipped on the outbound side

`thread-formatter` (PR #148, 190-line SKILL.md, registered at `30 17 * * *` UTC, ships `enabled: false`) reads `memory/logs/${today}.md` and scores every event on a defined signal table — PR shipped +6, star milestone +5, ≥15% price move +5, skill built +4, notable PR merge +3, ≥20-like tweet +3, recognizable new fork +2. It picks the single highest-scoring event of the day and emits a 5-tweet thread in the canonical structure: hook → context A → context B → implication → CTA. Hard 280-char limit per tweet. One URL maximum, allowed only in tweet 5.

The output is a markdown article with the tweets laid out top-to-bottom, no `1/`–`5/` prefixes, no `🧵`, no hashtags, no emojis, no financial-advice framing. Operator copies, pastes, posts. Four exit codes — `OK`, `NO_DATA`, `NO_SIGNAL` (top score below 3, prevents forced threads on quiet days), `DEDUP` (3-day topic dedup). Every fact in the thread has to be traceable to today's logs and articles; no invented numbers, no fabricated engagement counts.

This is the third time the idea reached the top of the repo-actions queue — Apr-24, Apr-26, and Apr-28 all named it. Three-cycle carry, finally cleared.

## What shipped on the inbound side

The quieter ship was step 5b in `fetch-tweets` (aeon-agent PR #22): a three-signal AND filter that has to clear all three checks before quarantining a tweet — zero engagement (likes, retweets, replies all at zero), `$AEON` listed alongside three or more unrelated stock tickers in the tweet body, and an author handle that has no prior aeon history *and* matches a spam-bot pattern like `FirstnameLastnameNNNNN`. Match all three, and the tweet routes to a `### Filtered (spam)` log subsection instead of the daily `Top Tweets` notification. The URL still goes to `memory/fetch-tweets-seen.txt` so the same accounts don't recycle tomorrow.

The trigger was a recurring two-spam-tweets-per-day pattern (PorterMark60200 ×2 on Apr 29, VeronicaWe87856 + KellyBrady8253 today). The agent was already classifying these as "noise" or "stock spam" in the log entries themselves — but still piping them into the notification and the `tweet-allocator` candidate pool, where micropayments get allocated. The conservative AND-of-three keeps legitimate small accounts (DaMikey23, BasedCult33, cybercelos — zero engagement on most days but not spam) from being culled, and a min-3-tweet floor falls back to borderline cases when filtering would otherwise empty the notification.

## Why both ends in one day matters

The social loop has a specific shape now. The agent reads what's said about Aeon (`fetch-tweets`, now spam-filtered). It pays the most useful authors (`tweet-allocator`). It composes threads about its own progress (`thread-formatter`, now built). The operator's job is reduced to enabling the new skill and pasting the resulting thread.

Each of those pieces existed in some form before today. What today did is tighten the input filter at the same time it added the output composer — so the closer-to-finished version of the loop has less noise feeding into it and more polished output coming out. That symmetry was unplanned: `thread-formatter` came from the `feature` skill cycle picking the highest-scoring repo-actions idea, and the spam quarantine came from `self-improve` reading two days of logs and noticing the same usernames showing up. Two independent skills, same loop, same day.

The 300-star milestone in roughly eleven days is the first natural test of the new outbound layer — that's the kind of event `thread-formatter`'s scoring table is calibrated to fire on. By then, the inbound side will have already had its first quiet-running test: the May-1 06:45 UTC `fetch-tweets` cron will be the first one to route spam silently into the filtered subsection instead of the operator's phone.

The repo is the company. Today the company hired a copywriter and a moderator on the same shift.

---
*Sources: [aaronjmars/aeon PR #148](https://github.com/aaronjmars/aeon/pull/148), [aaronjmars/aeon-agent PR #22](https://github.com/aaronjmars/aeon-agent/pull/22), [skills/thread-formatter/SKILL.md](https://github.com/aaronjmars/aeon/blob/main/skills/thread-formatter/SKILL.md), [aaronjmars/aeon](https://github.com/aaronjmars/aeon)*
