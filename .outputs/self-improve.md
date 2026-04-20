*Agent Self-Improvement — 2026-04-20*

Prefetch error marker + skill short-circuit on XAI failures

When the XAI prefetch curl fails (timeout or HTTP error), `scripts/prefetch-xai.sh` now writes a one-line reason to `.xai-cache/<outfile>.error`. The fetch-tweets skill checks this marker and skips Path B (sandbox blocks `$XAI_API_KEY` env-var expansion) and Path C (WebSearch returns 0 fresh tweets when XAI is the source of truth) — both fall-back paths that consistently fail anyway. The prefetch script also gets a third retry, an explicit `--connect-timeout 30`, and `-sS` so curl errors surface to stderr.

Why: Apr 19 and Apr 20 morning fetch-tweets runs both logged FETCH_TWEETS_EMPTY because the XAI prefetch curl exited at exactly 60s with no visible retry, after which the skill burned ~10K tokens probing dead-end fallbacks before giving up. Two failures in two days; same shape.

What changed:
- scripts/prefetch-xai.sh: write `.xai-cache/<outfile>.error` on terminal failure (curl exit or HTTP non-200), retry budget 2→3 attempts, --connect-timeout 30, -sS, retry-iteration logging
- skills/fetch-tweets/SKILL.md: Path A short-circuit step — if cache JSON missing AND error marker present, jump to FETCH_TWEETS_PREFETCH_FAILED with the reason in the notification
- memory/MEMORY.md, memory/logs/2026-04-20.md: log entry + Skills Built row

Impact: ~10K tokens saved per prefetch-failure run, faster failure detection (3 attempts × 30s connect ≈ 90s worst case vs. burning multi-step Claude exploration), and persistent XAI outages now surface a specific reason in notifications instead of a generic "no tweets found." Fix is generic across all xai_search() callers (refresh-x, remix-tweets, narrative-tracker, article, tweet-roundup).

PR: https://github.com/aaronjmars/aeon-agent/pull/16
