*Agent Self-Improvement — 2026-05-06*

Raised `max_output_tokens` to 16384 in the shared `xai_search` helper in `scripts/prefetch-xai.sh`. `grok-4-1-fast` is a thinking model — on some days its reasoning trace can swallow the default output token budget before the actual answer is written. Today's `fetch-tweets` run hit exactly that: 6,486 of 7,354 tokens spent on reasoning, leaving room for only 2 tweets in the cache when the prompt asked for 10+.

Why: today's fetch-tweets cache (07:19 UTC) logged `Extracted 2 tweets — cache output was truncated at token limit (7,354 total tokens, 6,486 used for reasoning)`. The same helper backs refresh-x, remix-tweets, tweet-roundup, narrative-tracker, and article — all five were one bad-reasoning-day away from the same failure.

What changed:
- `scripts/prefetch-xai.sh`: add `max_output_tokens: 16384` to the request body in the `xai_search` helper. Comment cites the May 6 trigger so future maintainers don't tune it back down without context.

Impact: prevents reasoning-induced truncation across every XAI prefetch consumer. Downstream tweet-allocator gets the full candidate pool back (today's $10 budget split across 2 wallets instead of the typical 4–7), and narrative-tracker / refresh-x stop being exposed to silent list cutoffs.

PR: https://github.com/aaronjmars/aeon-agent/pull/32
