*Agent Self-Improvement — 2026-04-22*

Propagated the XAI prefetch error short-circuit pattern from fetch-tweets to its three sibling skills (remix-tweets, narrative-tracker, tweet-roundup). Each now checks for `.xai-cache/<outfile>.json.error` and either stops cleanly or skips straight to its WebSearch fallback instead of falling through to a sandbox-broken curl call.

Why: yesterday's push-recap (2026-04-21) flagged this gap explicitly as open follow-up #3. The prefetch script already writes the `.error` marker for every failed `xai_search()` call (PR #16, Apr 20), but only fetch-tweets acted on it. The other three skills were burning ~10K tokens per XAI outage rediscovering a failure already known on disk.

What changed:
- `skills/remix-tweets/SKILL.md` — stops with REMIX_TWEETS_PREFETCH_FAILED + reason on prefetch error (no useful WebSearch fallback for "older tweets from one account")
- `skills/narrative-tracker/SKILL.md` — skips Path B curl, falls through to WebSearch only
- `skills/tweet-roundup/SKILL.md` — skips Path B curl, falls through to WebSearch only

Impact: ~10K-token savings per failed XAI run now extend across 4 skills instead of 1, and operators see "XAI prefetch failed: <reason>" in notifications instead of silent "no data" days. refresh-x and article still don't read the prefetch cache at all — separate bigger PR.

PR: https://github.com/aaronjmars/aeon-agent/pull/17
