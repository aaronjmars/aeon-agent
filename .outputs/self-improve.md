*Agent Self-Improvement — 2026-04-26*

Tweet-allocator now dedups its `TWEET_ALLOCATOR_ERROR` notification on a 48h window. When `.bankr-cache/verified-handles.json` is missing or empty (`{}`), the skill scans the two prior daily logs for a matching prior alert. First occurrence in 48h still pings; repeats log silently. A successful run resets the window automatically — next failure pings again.

Why: The same error fired Apr-25 and Apr-26 — `.bankr-cache/verified-handles.json` empty (`{}`), root cause `BANKR_API_KEY` unset/invalid or every Bankr lookup failing. Operator-dependent and won't fix itself between runs, so a daily duplicate alert is noise, not signal. Same shape as the PAT-with-`workflows`-scope issue heartbeat just got an extended-persistence backoff for in PR #18.

What changed:
- `skills/tweet-allocator/SKILL.md`: Step 4 hard-stop branch gains a 48h dedup gate before calling `./notify`; Status-flags section documents the new behavior and reset condition.

Impact: Operator-dependent error stops generating daily noise — first occurrence is still loud, follow-ups are silent until either the operator fixes the secret or the skill succeeds again. Same dedup shape now applies in two places (heartbeat persistent issues + tweet-allocator Bankr cache), making it a reusable pattern future skills can adopt.

PR: https://github.com/aaronjmars/aeon-agent/pull/19
