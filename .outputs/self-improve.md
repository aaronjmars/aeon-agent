*Agent Self-Improvement — 2026-05-08*

xai-prefetch truncation early-warning
Added a `::warning::` annotation to the shared `xai_search` helper that fires whenever an XAI response's `output_tokens` lands within 5% of `max_output_tokens` (currently 16384). The warning includes both the raw output count and the reasoning-token breakdown so operators can see whether reasoning or actual output is consuming the cap.

Why: On May 6, fetch-tweets silently delivered 2 tweets instead of 10+ because grok-4-1-fast spent 6,486 of 7,354 tokens on reasoning before the response was truncated. PR #32 raised the cap to 16384 to fix the symptom, but the prefetch step still prints "saved <file>" with no signal that the underlying cache was clipped — six skills share the helper (fetch-tweets, refresh-x, remix-tweets, tweet-roundup, narrative-tracker, article) and any of them is exposed to the same silent-clip failure mode.

What changed:
- scripts/prefetch-xai.sh: factor `16384` into a `local max_output_tokens` so the request body and the check share one source of truth; after each saved response, parse `.usage.output_tokens` from the XAI response and emit a GitHub Actions warning annotation when it crosses 95% of the cap.

Impact: heartbeat and `./scripts/skill-runs --failures` already surface workflow warnings, so the next time a skill brushes the ceiling — instead of finding out from a notification with 2 tweets — the regression shows up directly in workflow logs and gets escalated by the existing observability stack. Behavior on the happy path is unchanged.

PR: https://github.com/aaronjmars/aeon-agent/pull/33
