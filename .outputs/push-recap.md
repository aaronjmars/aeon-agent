*Push Recap — 2026-05-11*
3 repos — 4 commits / 4 PRs by @aaronjmars (all four queued in yesterday's recap landed at ~22:39 UTC, four minutes apart)

*Weekly-cadence framework layer joins the watch triple* (aeon #164 ai-framework-watch): aeon's competitive-intel stack now spans code (github-trending), artifacts (huggingface-trending), and frameworks themselves — a 9-framework hardcoded watchlist (aeon anchor + langgraph/crewai/autogen/llamaindex/mastra/smolagents/dspy/pydantic-ai) with 7d/30d star deltas, release listings, breaking-change flags, and a verdict priority order that never stacks signals.

*Fork-cohort backport lands on the agent fleet* (aeon-agent #36): same-day-after backport pattern caught up to four most-leveraged skills (operator-scorecard, skill-freshness, skill-update-check, fork-cohort). Buckets every fork by activation stage using GitHub Actions run history — not pushed_at — so the distinction is "actually executing skills" vs. "had an auto-commit yesterday."

*Error-marker contract made explicit* (aeon-agent #37): yesterday's BANKR auth failure exposed an implicit contract — Claude inferred to read the .error marker file. Step 4 now reads the marker first and surfaces its content verbatim across all three failure codes (BANKR_API_KEY_MISSING / _INVALID / BANKR_LOOKUPS_FAILED).

*DEV.to column closes long-form-developer surface* (minitor #33): 39th column type, news-and-web cluster 6 → 7. Keyless REST API, three modes (top week / latest / rising 24h), 1–5 tag AND-filter, dual-shape parsing for both tag_list (array) and tags (CSV).

Key changes:
- skills/ai-framework-watch/SKILL.md — new 307-line weekly competitive-intel skill on aeon with 9-framework anchor-vs-peers digest, precise-over-permissive breaking-change detection
- skills/fork-cohort/SKILL.md — verbatim backport from aeon May-2 PR #152, run-history-driven activation bucketing, 7-day delta tagging
- skills/tweet-allocator/SKILL.md — two-branch step 4 (marker first, cache second), three deterministic failure-mode routings
- minitor lib/integrations/devto.ts + 3-file plugin + 3 registry edits — keyless DEV.to integration with three modes and 5-tag AND-filter

Stats: 15 files changed, +1131/-13 lines.
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-11.md
