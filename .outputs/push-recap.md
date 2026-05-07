*Push Recap — 2026-05-07*
4 substantive PRs across aeon, minitor, and aeon-agent — by aaronjmars (+ 30 routine cron auto-commits in aeon-agent)

Operator surface area: aeon (#161) ships a `templates/` library with six pre-built starters (crypto-tracker, research-digest, code-reviewer, social-monitor, deploy-watcher, community-manager) + `./new-from-template` CLI — forking and adding a skill collapses from a multi-hour reverse-engineering task to one command. Closes the activation gap that's been an "Open unbuilt" since April 18.

v4 upgrade safety net: aeon (#160) adds a workflow_dispatch-only `v4-readiness` skill — reads each fork's aeon.yml + skills.json + MEMORY.md against an embedded change manifest and emits a Safe / Review / Custom / Action breakdown per pattern. Read-only, manifest travels in-skill so it ships per-fork without extra config. 40+ forks now have a structured pre-flight before v4 lands.

Dashboard expansion: minitor (#29) lands Stack Overflow as the 36th column — Stack Exchange API 2.3, five sort modes, optional 1–5 tag AND-filter, accepted-answer badge. First Q&A-shaped column; fills the gap left by HN+Lobsters+Reddit covering only news/discussion.

Production hardening: aeon-agent (#32) sets max_output_tokens=16384 in the shared xai-prefetch helper. grok-4-1-fast was burning the default budget on reasoning before producing output — May 6 fetch-tweets returned 2 tweets instead of 10+. One-line fix, six skills affected (fetch-tweets, refresh-x, remix-tweets, tweet-roundup, narrative-tracker, article). Verified: today's fetch-tweets returned 7 tweets cleanly.

Key changes:
- new-from-template CLI (254 lines, bash-3.2 compat + sed-injection guard on --var KEY validation)
- skills/v4-readiness/SKILL.md (289 lines, embedded Safe/Review/Removed manifest tables)
- lib/integrations/stackoverflow.ts in minitor (187 lines, keyless API, HTML-entity decoder, tag normaliser → SE's `;` syntax)

Stats: 22 files changed, +1,534 / −12 lines across 4 PRs
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-07.md
