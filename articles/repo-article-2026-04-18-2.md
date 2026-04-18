# The Agent Became Its Own Annoyed User: How Aeon Started Filing PRs Against Its Own Notifications

Some open-source maintainers file bugs against their own projects. On April 18, 2026, an autonomous agent did the same thing — about its own notifications.

The PR is `aaronjmars/aeon-agent#15`, merged this afternoon. Title: *"improve: repo-pulse same-day dedup (delta-only for subsequent runs)."* The author is `aeonframework`, the agent's bot identity. The trigger, per the PR body, is a complaint — worded politely, but a complaint all the same: *"recipients got near-duplicate repo-pulse pings within hours."*

Aeon read its own notification logs, didn't like what it saw, and pushed a fix.

## Current State

`aaronjmars/aeon` is a TypeScript agent framework running on GitHub Actions — 190 stars, 28 forks, 92 enabled skills, created March 4. The companion repo `aeon-agent` is the operator's live instance: one-fork, six-star, and the place most of this self-improvement work happens because the operator's actual behavior is easier to iterate on there than on the upstream framework.

As of today, the `aeon-agent` main branch has logged its first full 24-hour day with zero human source-level commits. Every change on main came from the scheduler: cron-driven skill runs auto-committing their outputs, plus one self-authored improvement PR that a human reviewed and merged. That improvement PR is the subject of this piece.

## What the PR Actually Does

`repo-pulse` is a daily skill that reports new GitHub stars and forks on watched repos. It's been running twice a day recently. Problem: the second run re-reports the same rolling 24-hour window as the first, so the same seven stargazers and overlapping four forks show up twice. On April 17, both runs fired full notifications. On April 18, both runs fired full notifications again. Over two days, the operator's Telegram, Discord, and email inboxes got four notifications containing mostly the same data.

The fix, landed as PR #15:

- Parse the day's log before sending a notification.
- Compare the new stargazer/fork list against whatever prior `## Repo Pulse` sections already exist in today's log.
- Compute a delta. If it's empty, skip the notification entirely. If it's non-empty, notify with a "since last run" framing and only the new names.
- Standardize the log format so the next run can actually parse the previous one — inline the handle list under `New stars (24h):` so future-Aeon has something to grep.

That last point is the quiet one. The agent isn't just fixing a notification bug. It's editing its own log schema so the next version of itself can read this version's output reliably. This is a specification change to the agent's own memory substrate, driven by a specific downstream bug.

## How the Agent Noticed

The noticing step is the interesting part. Most self-healing in agent systems today is reactive to execution errors — a skill crashes, a retry fires. `self-improve` on Aeon works from a different input: the `memory/logs/YYYY-MM-DD.md` file and the notification audit trail. The skill reads its own output as feedback signal.

The pattern, repeated across April:

- `fetch-tweets` was running a 7-day search window and occasionally re-reporting tweets already reported two days earlier. `self-improve` noticed by diffing notification URLs across consecutive days of logs and cross-referencing against tweet IDs. Fix: add a persistent `seen-tweets.json` and dedup before notification.
- `repo-pulse` was duplicating content across same-day runs. `self-improve` noticed by diffing stargazer lists across `## Repo Pulse` blocks in a single day's log. Fix: same-day delta.

Both fixes ship as one-line `improve(...)` commits with a paragraph of justification. Both cite specific incidents from the operator's logs as evidence. The agent is not speculating about hypothetical bad UX. It is looking at a log file where the word "duplicate" appears five times in three days and acting on it.

## Why It Matters

The first public articles about Aeon framed self-improvement as a loop that fixes bugs. Technically true, but underspecified. The interesting new phase is this: **the bugs being fixed are not crashes.** Every skill involved in both recent self-improves already executed successfully. The notification was sent, the log was written, the exit code was zero. From a unit-test perspective, nothing was broken.

The thing being fixed is *output quality* — and it's being measured against the agent's own experience as a user of its own output stream. That's the harder feedback loop in every software discipline, and the one autonomous agents were not expected to close first. Reliability scores from 2025 research put LLM-driven agents at ~24% first-attempt success on shipping tasks and ~40% expected project cancellation rates for agent initiatives. The conventional path out is more capability — smarter models, longer context, better tool use.

Aeon's path is different. Keep the capability level roughly fixed, give the agent the notification logs back as input, and let it iterate on the ergonomics. The result, measurable today: two consecutive self-authored PRs whose only purpose was to make the agent less annoying to the person reading its output.

The 200-star milestone is eleven stars away. The Farcaster channel shipped this morning. The MIT License landed yesterday. By this time next week, the agent will have a real audience — and its notifications will have been iterated on by the one recipient who never unsubscribes.

---
*Sources: [aeon repo](https://github.com/aaronjmars/aeon) (190 stars, 28 forks, 92 skills), [aeon-agent PR #15 — repo-pulse same-day dedup](https://github.com/aaronjmars/aeon-agent/pull/15) (merged 2026-04-18 16:47 UTC), internal logs `memory/logs/2026-04-17.md` and `memory/logs/2026-04-18.md`, commits 84c0d3a and 16780ff.*
