*Agent Self-Improvement — 2026-04-16*

fetch-tweets now reads from the pre-fetched XAI cache before attempting the direct API call. The skill has returned FETCH_TWEETS_EMPTY on every run for 4+ consecutive days because it never read from .xai-cache/fetch-tweets.json — even though the prefetch script already cached X.AI results there before Claude starts.

Why: The X.AI API requires auth headers with env vars, which are blocked inside the Claude sandbox. The prefetch infrastructure existed and worked, but the skill prompt never referenced it. Other skills (tweet-roundup, narrative-tracker, remix-tweets) already used this pattern correctly.

What changed:
- skills/fetch-tweets/SKILL.md: Restructured step 3 to check .xai-cache/fetch-tweets.json first, fall back to direct API, then WebSearch. Added Sandbox note section.

Impact: fetch-tweets should now return actual tweet data instead of empty results on every run. Saves wasted compute from daily Sonnet runs that produced nothing.

PR: https://github.com/aaronjmars/aeon-agent/pull/13
