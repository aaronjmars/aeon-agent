*Push Recap — 2026-05-19*
5 substantive merges (2 aeon, 3 aeon-agent, 0 minitor) — fork-intelligence parity + cron-path hygiene week.

*Same-day-after backports continue (8th + 9th in row):* aeon-agent absorbed `fork-skill-gap` (#52, upstream PR #176) and `fork-first-run-alert` (#50, upstream PR #179) — fork-intelligence layer now at full parity with upstream (5 skills: alive? shipped? who pushed? what's missing? when activated?).

*XAI direct-curl primary path retired:* `refresh-x` (#51) rewired off `curl -H "Authorization: Bearer $XAI_API_KEY"` — last enabled-eligible XAI consumer migrated to the prefetch-cache contract. 4th explicit-marker fix after PR #37 (.error), PR #43 (.truncated), PR #48 (fetch-tweets-log fallback in token-report).

*New surveillance angle:* `competitor-launch-radar` (aeon PR #183) — 8th read-only ecosystem watcher in aeon, first one pointed at NEW entrants outside the 9-framework cohort. Weekly Mon 10:00 UTC, keyless PH RSS + HN Algolia, 9 framework keywords, count-driven notify.

*scan.sh empty-array crash squashed:* aeon PR #186 wraps highs/mediums/lows print loops in length guards (closes #182). Fixes the `[PASS]` → `✗ BLOCKED` false-positive that hit every macOS operator running `./add-skill` on Bash 3.2.

Key changes:
- aeon-agent skills.json 86 → 88 (two new fork-intelligence skills)
- aeon skills.json 119 → 120 (competitor-launch-radar)
- skills/skill-security-scan/scan.sh +17/-9 — three length guards mirror existing JSON-path pattern

Stats: 10 files changed, +1,114/-15 lines across 5 PR merges
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-19.md
