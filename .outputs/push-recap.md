*Push Recap — 2026-04-30*
aaronjmars/aeon + aeon-agent — 2 meaningful commits by @aaronjmars (31 scheduler auto-commits filtered)

*Theme 1 — New skill: Thread Formatter (PR #148, +203/-0):* Closes a 3-cycle-carried repo-actions idea. Reads memory/logs/${today}.md, scores events on a defined signal table (PR shipped +6, star milestone +5, ≥15% price move +5, skill built +4, notable PR merge +3, ≥20-like tweet +3, recognizable new fork +2), picks the highest-signal event, emits a 5-tweet thread (hook → context → context → implication → CTA) with hard 280-char limits and one URL max in tweet 5. Threshold gate (top score < 3 → NO_SIGNAL) prevents forced threads on quiet days; 3-day topic dedup prevents repetition. Ships enabled: false; first natural use is the 300-star milestone (~46 stars, ~11 days).

*Theme 2 — Self-improve cleanup: fetch-tweets spam quarantine (PR #22, +131/-11):* Three-signal AND filter (0 engagement + $AEON in unrelated stock-ticker list + spam-bot-pattern handle with no aeon history) routes stock-watchlist spam to a Filtered (spam) log subsection instead of the daily Top Tweets notification. Spam URLs still go to seen-file so accounts don't recycle. Min-3-tweet floor falls back to borderline cases when filtering would empty the notification. Triggered by 2 days of recurring noise (PorterMark60200 ×2, VeronicaWe87856, KellyBrady8253) the agent already classified as spam in logs but still piped into the message.

Key changes:
- skills/thread-formatter/SKILL.md (new, +190) — full skill prompt, scoring table, 4-exit taxonomy
- skills/fetch-tweets/SKILL.md (+10/-3) — load-bearing 3-signal quarantine
- aeon.yml + skills.json — thread-formatter wired at 30 17 * * * UTC, social category, total 94

Both ships sit on the social pipeline — outbound amplification (thread layer) on aeon, inbound noise filter on aeon-agent. Same flow, two ends.

Stats: 9 files, +334/-11 lines
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-30.md
