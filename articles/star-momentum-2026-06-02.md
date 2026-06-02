# Star Momentum — 2026-06-02

**Verdict:** NO_ALERTS — 0 repos in launch window today

*Audited 2 repos · 0 alerts · projection method: linear extrapolation from 7-day rolling average*

---

## aaronjmars/aeon — 471⭐ → 500⭐ in ~7d

| Metric | Value |
|--------|-------|
| Current stars | 471 |
| Target milestone | 500 |
| Gap | 29 |
| 3-day avg / day | 4.00 |
| 7-day avg / day | 4.14 |
| Days remaining (v7) | 7 |
| Projected date (v7) | 2026-06-09 (Tuesday) |
| Days remaining (v3) | 8 |
| Projected date (v3) | 2026-06-10 (Wednesday) |
| In Show HN window | YES — Tuesday inside 7-14d |
| Verdict | ALREADY_ALERTED |

Timing gates both pass: 7d projection lands in the 7-14d window, and Tuesday is a valid Tue/Wed/Thu dispatch day. Alert suppressed — notification fired 2026-06-01 (1 day ago, within the 7-day per-milestone dedup window). Next eligible re-alert opens 2026-06-08 if the milestone hasn't crossed by then.

### Source data — aaronjmars/aeon

| Date | Stars | Δ |
|------|-------|---|
| 2026-05-19 | 387 | — |
| 2026-05-20 | 402 | +15 |
| 2026-05-21 | 417 | +15 |
| 2026-05-22 | 421 | +4 |
| 2026-05-23 | 429 | +8 |
| 2026-05-24 | 433 | +4 |
| 2026-05-25 | 442 | +9 |
| 2026-05-26 | 451 | +9 |
| 2026-05-27 | 455 | +4 |
| 2026-05-28 | 456 | +1 |
| 2026-05-29 | 459 | +3 |
| 2026-05-30 | 464 | +5 |
| 2026-05-31 | 466 | +2 |
| 2026-06-01 | 471 | +5 |

*v7 uses the 7 most recent deltas (May 25→26 through May 31→Jun 01): 9+4+1+3+5+2+5 = 29 / 7 = 4.14/day*

---

## aaronjmars/minitor — STALLED

| Metric | Value |
|--------|-------|
| Current stars | 11 |
| Target milestone | 50 |
| Gap | 39 |
| 3-day avg / day | 0.0 |
| 7-day avg / day | 0.0 |
| Days remaining (v7) | — |
| Projected date (v7) | — |
| Projected date (v3) | — |
| In Show HN window | NO — STALLED |
| Verdict | STALLED |

v7 dropped to 0.0/day today. The last positive delta — May 24→25 (+1 star) — has rolled out of the trailing-7 window, leaving all seven most-recent deltas (May 25→26 through May 31→Jun 01) at zero. Yesterday's run still showed a 0.14/day v7 (273-day OUT_OF_WINDOW projection) because that delta was just barely in range. Today it isn't. No projection is meaningful; no alert fires.

### Source data — aaronjmars/minitor

| Date | Stars | Δ |
|------|-------|---|
| 2026-05-19 | 9 | — |
| 2026-05-20 | 9 | 0 |
| 2026-05-21 | 9 | 0 |
| 2026-05-22 | 9 | 0 |
| 2026-05-23 | 9 | 0 |
| 2026-05-24 | 10 | +1 |
| 2026-05-25 | 11 | +1 |
| 2026-05-26 | 11 | 0 |
| 2026-05-27 | 11 | 0 |
| 2026-05-28 | 11 | 0 |
| 2026-05-29 | 11 | 0 |
| 2026-05-30 | 11 | 0 |
| 2026-05-31 | 11 | 0 |
| 2026-06-01 | 11 | 0 |

---

## What this means

**aaronjmars/aeon** — 471⭐ is projected to cross 500⭐ on 2026-06-09 (Tuesday), 7 days from today. Pace: 4.14/day across the last 7 days, 4.00/day across the last 3. Tuesday is inside the Show HN dispatch window. Both timing gates pass — the alert is suppressed only because an identical notification fired yesterday (2026-06-01). The situation is unchanged: the milestone is on a qualifying day, inside the qualifying window. Next re-alert is eligible on 2026-06-08 (7 days post-June-01 notification) if 500⭐ hasn't crossed by then.

**aaronjmars/minitor** — The repo crossed from OUT_OF_WINDOW to STALLED today as the last positive growth signal aged out of the 7-day trailing window. Two stars were gained across May 23–25; nothing since. 11 stars, target 50, no current momentum. No action.

---
*Reads `memory/logs/YYYY-MM-DD.md` repo-pulse blocks. Pure local file I/O. Companion to `star-milestone` (post-crossing celebration) and `show-hn-draft` (the launch artifact this signal times).*
