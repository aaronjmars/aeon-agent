*Agent Self-Improvement — 2026-04-30*

Stock-watchlist spam quarantine in fetch-tweets
The fetch-tweets skill now routes obvious stock-spam tweets (where $AEON appears in a list of unrelated stock tickers, posted by zero-engagement throwaway-looking handles) into a separate "Filtered (spam)" subsection of the daily log instead of including them in the Top Tweets Telegram notification. The spam URLs still get tracked in the persistent seen-file so the same accounts don't recycle into future runs.

Why: a recurring 2-spam-tweets-per-day pattern was visibly polluting the daily message. Apr 29 had two PorterMark60200 stock-picker spam tweets; Apr 30 had VeronicaWe87856 and KellyBrady8253 stock spam. The agent was already labeling them "noise" / "stock spam" in the log entries themselves but still piping them into the notification and the tweet-allocator candidate pool.

What changed:
- skills/fetch-tweets/SKILL.md: adds step 5b — a tight AND-of-three filter (0 engagement + ticker-list body with no aeon-framework context + spam-bot-pattern handle with no prior aeon history). Updates step 6 to log spam under "### Filtered (spam)" subsection. Updates step 6b so spam URLs still go to the seen-file. Updates step 7 to exclude spam from the notification. Min-3-tweet floor falls back to including borderline cases so the notification is never empty when real tweets exist.

Impact: cleaner daily Top Tweets notifications (estimated ~20% noise reduction based on Apr 29-30 pattern), cleaner tweet-allocator candidate pool, no false positives on legit small accounts (DaMikey23, BasedCult33, cybercelos all pass the conservative AND filter).

PR: https://github.com/aaronjmars/aeon-agent/pull/22
