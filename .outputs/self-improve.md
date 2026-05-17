*Agent Self-Improvement — 2026-05-16*

token-report's Social Pulse step has been emitting "XAI_API_KEY not set — no social data" for five consecutive days (May 13–16) even though the key IS set and is being consumed by fetch-tweets / tweet-allocator prefetch every morning. Root cause: the sandbox blocks `$XAI_API_KEY` expansion inside curl `-H` headers, so the direct-curl path in step 5 silently auth-fails and the skill misreads that as a missing key. Replaced the broken curl with a sandbox-safe read of the most recent `## fetch-tweets` section in `memory/logs/` — today's first, yesterday's as fallback (token-report at 06:00 UTC, fetch-tweets at 06:30 UTC, so yesterday's is the typical source).

Why: five-day-streak misleading log line, traced to a known sandbox limitation already worked around for fetch-tweets / tweet-allocator / narrative-tracker — token-report was the last consumer still on the legacy direct-curl pattern.

What changed:
- skills/token-report/SKILL.md: step 5 rewritten to read fetch-tweets log instead of curl-ing XAI; step 6 Social Pulse template updated; section is now omitted entirely if no fetch-tweets log exists within 2 days (instead of lying about XAI_API_KEY)
- memory/logs/2026-05-16.md + memory/MEMORY.md Open Improvement PRs: index updated

Impact: stops the daily false "key not set" line in the most-read skill output. Adds a real social signal (2-3 themes from logged tweets) on every run where fetch-tweets has produced output in the last 48h — which is every day under the current schedule.

PR: https://github.com/aaronjmars/aeon-agent/pull/48
