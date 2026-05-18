*Push Recap — 2026-05-18*
aeon + aeon-agent + minitor — 8 substantive PRs + ~50 cron auto-commits

Fork-intelligence layer (aeon): two new skills shipped — `fork-skill-gap` (weekly per-fork upstream-skill-adoption report) and `fork-first-run-alert` (daily named alert the day a fork runs its first workflow). Together with fork-cohort + fork-release-tracker + contributor-spotlight that's a 5-skill cluster with composable state-file chaining; both new skills include live `gh api` fallback so they work before the cohort cache is populated.

Sandbox-fix completion (aeon-agent): PR #48 rewrote `token-report` step 5 to read the most recent fetch-tweets log instead of curling XAI directly — closes the four-patch "explicit-marker contract" sequence that started May-10 with PR #37. `token-report` was the last enabled-eligible XAI consumer still on direct-curl. Today's self-improve run opened PR #51 to apply the same fix to `refresh-x` (latent — still enabled:false).

Minitor 43 → 44 columns + first cross-plugin retrofit: Product Hunt added as the 44th column (keyless RSS, `Rocket` icon, #DA552F brand orange) and column-level `alertKeywords` retrofitted across all 43 existing plugins (yellow inset ring + Bell badge with live match count). The alert-keywords migration is additive nullable — existing decks export-import cleanly.

Key changes:
- aeon: dashboard API routes now pass `-R {repo}` to `gh run list/view` — multi-remote operators no longer silently see wrong runs (PR #178 — also closes a latent shell-interpolation surface on `${id}`).
- aeon-agent: full autonomous cron loop ran end-to-end (7 articles produced, repo-actions seeded next-day pipeline, self-improve opened PR #51) with zero human intervention outside the two 21:58 UTC PR merges.
- minitor: alert-keywords is the first feature in the project that touches every plugin without per-plugin work — a true column-axis primitive (sibling to `title`, never sent to server fetchers, sidesteps every plugin's strict Zod schema).

Stats: 33 files changed, +2,917 / −47 lines across 8 substantive commits
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-18.md
