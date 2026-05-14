*Agent Self-Improvement — 2026-05-14*

Extended `.truncated` marker handling to the three other modern XAI cache consumers (narrative-tracker, remix-tweets, tweet-roundup). The prefetch script writes the marker for every XAI skill, but only fetch-tweets read it — the other three silently shipped truncated caches as if they were full results, making budget-exhaustion days look like quiet days.

Why: scripts/prefetch-xai.sh lines 130-134 explicitly name six target consumers as marker readers, but `grep -l truncated skills/` showed only fetch-tweets implementing it. PR #40 (merged yesterday) only closed one of those six. Same silent-clip bug as May-12 fetch-tweets could hit any of the others.

What changed:
- skills/narrative-tracker/SKILL.md: read narratives.json.truncated, status NARRATIVE_TRACKER_OK_TRUNCATED
- skills/remix-tweets/SKILL.md: read remix-tweets.json.truncated, status REMIX_TWEETS_OK_TRUNCATED, don't pad to 10 from fewer source tweets
- skills/tweet-roundup/SKILL.md: read each topic cache's .truncated companion, status TWEET_ROUNDUP_OK_TRUNCATED, list affected topics

Impact: operator sees "⚠️ XAI cache truncated (output_tokens=N/max=M)" inline on any future budget-exhaustion day across these three skills, instead of mistaking a short notification for low activity. Older consumers (refresh-x, article) still need the same plus the .error pattern — left for separate cleanup.

PR: https://github.com/aaronjmars/aeon-agent/pull/43
