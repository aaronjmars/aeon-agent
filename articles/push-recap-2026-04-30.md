# Push Recap — 2026-04-30

## Overview
Two meaningful commits today, both shipped by `@aaronjmars` and both landing in the social-channel pipeline: PR #148 on `aaronjmars/aeon` adds the **thread-formatter** skill — auto-format the day's top event as a five-tweet thread ready to paste — and PR #22 on `aaronjmars/aeon-agent` adds **stock-watchlist spam quarantine** to `fetch-tweets`. One adds outbound amplification capacity for noteworthy days; the other strips inbound noise out of the daily Top Tweets notification. The remaining 31 commits on `aeon-agent` are scheduler / per-skill auto-commits and were filtered out.

**Stats:** 9 files changed, +334/-11 lines across 2 meaningful commits (203 added on `aeon`, 131/-11 on `aeon-agent`)

---

## aaronjmars/aeon

### Theme 1: New skill — Thread Formatter (outbound social layer)

**Summary:** Closes Apr-28 repo-actions idea #1, carried for three cycles (also Apr-26 #4 and Apr-24 #3) — the highest-priority unbuilt the agent can ship without external blockers. Every daily run already produces a narratable event (a feature shipping, a 15%+ price move, a star milestone, a 20-like tweet), but most of it dies in Telegram because nobody copy-pastes it onto X. `thread-formatter` reads `memory/logs/${today}.md`, scores the events that actually happened, picks the single highest-signal one, and emits a five-tweet thread ready to paste. The thread is organic content — it doesn't spend the `tweet-allocator` budget.

**Commits:**
- `f07d975` — feat: thread-formatter skill — auto-format top daily event as 5-tweet thread (#148)
  - **New file** `skills/thread-formatter/SKILL.md` (+190 lines, new) — the full skill prompt. Defines the scoring table (PR shipped +6, star milestone crossed +5, ≥15% price move +5, ≥10% price move +3, skill built +4, notable PR merge +3, ≥20-like tweet +3, recognizable new fork +2), the structure (hook → context A → context B → implication → CTA), the hard constraints (280-char/tweet limit; no `🧵` / `thread:` prefix; no hashtags / emojis; no financial-advice framing; one URL max in tweet 5), and the four-exit taxonomy: `THREAD_FORMATTER_OK` | `THREAD_FORMATTER_NO_DATA` (empty/missing log) | `THREAD_FORMATTER_NO_SIGNAL` (top score < 3) | `THREAD_FORMATTER_DEDUP` (3-day topic dedup vs prior `articles/thread-*.md`). Also bakes in a soul-aware Voice section that falls back to "clear, direct, opinionated style" when soul files are empty templates.
  - Changed `aeon.yml` (+1 line) — registers `thread-formatter: { enabled: false, schedule: "30 17 * * *", var: "" }` in the social/feed-generation block, after the 17:00 UTC content cluster (`fetch-tweets` / `write-tweet` / `tweet-roundup` / `agent-buzz`) so the thread is composed once those have logged.
  - Changed `skills.json` (+12 lines) — adds the catalog entry between `telegram-digest` and `token-alert`, category `social`, with the schedule `30 17 * * *` mirroring `aeon.yml`. Brings total skill catalog count to 94.

**Impact:** Thread-formatter doesn't post anything — the operator still chooses whether and when to paste — but it removes the friction that's been killing organic amplification on every shipped feature, every star milestone, and every meaningful price move. Threshold gate (top score < 3 → `NO_SIGNAL`) prevents forced threads on quiet days; 3-day topic dedup prevents repetition. First natural use will be the 300-star milestone, ~46 stars away (~11 days at the current ~4-stars/day momentum). Companion to `write-tweet` (size variants on operator-picked topic) and `tweet-allocator` (inbound narrative budget) — same content lane, different role.

---

## aaronjmars/aeon-agent

### Theme 2: Self-improve cleanup — fetch-tweets stock-spam quarantine

**Summary:** Trims a recurring, agent-classified-but-still-shown noise pattern out of the daily Top Tweets notification. For two consecutive days the same shape of low-engagement stock-watchlist spam tweets (Apr 29 PorterMark60200 ×2, Apr 30 VeronicaWe87856 + KellyBrady8253) was already being labelled "stock spam" / "noise" inside the log entries themselves — but still piped into the notification body and the `tweet-allocator` candidate pool. Conservative AND-of-three filter routes them to a separate `### Filtered (spam)` subsection of the log instead.

**Commits:**
- `40268db` — improve(fetch-tweets): quarantine stock-watchlist spam from notifications (#22)
  - Changed `skills/fetch-tweets/SKILL.md` (+10/-3) — the load-bearing change. Adds **step 5b** with a three-signal AND filter: (i) engagement is `0 likes AND 0 retweets AND 0 replies`, (ii) tweet body treats `$AEON` as one of 3+ unrelated stock tickers with no `aeonframework` / `github.com/aaronjmars/aeon` link and no agent / framework / token-contract mention, (iii) author handle has no prior aeon mention in `memory/fetch-tweets-seen.txt` or recent logs **and** matches a stock-spam-bot pattern (e.g. `FirstnameLastnameNNNNN`, generic-influencer template). Updates step 6 so quarantined tweets are still logged but under a separate `### Filtered (spam)` subsection. Updates step 6b so spam URLs still get appended to `memory/fetch-tweets-seen.txt` — the same accounts don't recycle. Updates step 7 so the notification only includes non-spam survivors. **Min-3-tweet floor:** if filtering leaves fewer than 3 tweets, fall back to including borderline cases ranked by engagement so the notification is never empty when real tweets exist. Conservative AND-of-three keeps legit small accounts (`DaMikey23`, `BasedCult33`, `cybercelos`) from being culled — those carry zero engagement on most days but aren't stock-watchlist spam.
  - Changed `memory/MEMORY.md` (+1) — adds the `fetch-tweets (spam quarantine)` row to the Skills Built table.
  - Changed `memory/logs/2026-04-30.md` (+11) — logs the self-improve run that produced this PR, including the trigger pattern, files changed, branch, and PR URL.
  - Changed `dashboard/outputs/self-improve-2026-04-30T13-31-17Z.json` (+101, new) — JSON spec emitted by the self-improve run for the dashboard live feed (chain-runner pattern; not load-bearing for the skill behaviour).
  - Changed `.outputs/self-improve.md` (+7/-8) — chain-runner stub refresh.
  - Changed `memory/token-usage.csv` (+1) — token-cost ledger row.

**Impact:** Tightens the inbound side of the social pipeline that thread-formatter sits on the outbound side of — same flow, two ends. The seen-file integration is the non-obvious bit: by adding spam URLs to `memory/fetch-tweets-seen.txt` *anyway*, the same accounts can't show up again under a different framing on a future day, even though they were never visible in any past Top Tweets notification. Three-signal AND filter (rather than single-signal OR) is the design choice that protects against false positives — the kind of cull that quietly drops a real small-account contributor would be a worse failure mode than seeing two stock-spam tweets per day. The `tweet-allocator` candidate pool also benefits: spam-flagged tweets won't show up there either, so the budget can't accidentally pay a stock-bot wallet (though `tweet-allocator`'s Bankr-wallet requirement made that unlikely in practice).

---

## Developer Notes

- **New dependencies:** none.
- **Breaking changes:** none. Both shipped behaviours are additive — `thread-formatter` lands `enabled: false` (operator flips on); `fetch-tweets` quarantine activates immediately on the daily run but only narrows what was visible, never widens.
- **Architecture shifts:** none structural. `thread-formatter` follows the same shape as the other content skills (read `memory/logs`, write `articles/<skill>-${today}.md`, `./notify`, log) and the same exit-taxonomy convention introduced by the autoresearch-evolution rewrites (OK / NO_DATA / NO_SIGNAL / DEDUP). `fetch-tweets` step 5b is one new conditional inside an existing seven-step skill — no fanout, no new prefetch dependency.
- **Tech debt:** `thread-formatter` ships `enabled: false`; the maintainer flip-on is the pre-condition for the first scheduled run. The skill is also subject to the standing 80-PR backport gap (aeon PRs #46–#136 not yet backported to `aeon-agent`, day 13) — but it's a content skill with no upstream prefetch, so the gap doesn't block its first run.

## What's Next

- **Enable `thread-formatter` in `aeon.yml`** — the natural first scheduled run is the 300-star milestone (~46 stars away, ~11 days). Until then it can be exercised with `${var}` overrides during quiet windows to validate the scoring table and 280-char compliance against today's logs.
- **First inbound test of fetch-tweets quarantine** lands on the next morning's `06:45 UTC` run — if the signal table is right, tomorrow's Top Tweets notification will not contain a stock-watchlist line.
- **Auto-Merge Agent PRs** (Apr-26 repo-actions idea #1) — still blocked on workflows-scope PAT (day 13). It's the last remaining human-bottleneck closer in the dev/CI cluster; thread-formatter and pr-triage both shipped first because they don't need that scope.
- **Backport the 80-PR autoresearch-evolution gap** to `aeon-agent` — pre-evolution `SKILL.md` versions still running here. Today's two ships (thread-formatter on `aeon`, fetch-tweets quarantine on `aeon-agent`) don't make the gap any wider, but the next thread-formatter use here will need the new exit-taxonomy support also present.
- **Day 13 of PAT-with-`workflows`-scope persistence** — heartbeat is in 7-day extended-persistence backoff; next escalation due ~May 1 (tomorrow).
