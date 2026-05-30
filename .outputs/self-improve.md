*Agent Self-Improvement — 2026-05-30*

Heartbeat $(date -u +%Y-%m-%d) → ${today} drop-in
Replaced a shell command substitution in `skills/heartbeat/SKILL.md` step 4 detection-method #2 with the `${today}` template variable that the workflow already injects. Same string, no behavioral change — just removes one more `$(...)` site the runner shell-guard would block.

Why: The runner hook blocks shell command/variable expansion with "Contains simple_expansion" — identical constraint PR #63 fixed in weekly-shiplog (May 26) and PR #67 fixed in push-recap (May 28). heartbeat runs daily at 19:00 UTC; on every run the agent had to improvise the cutoff. Picked over the four other enabled skills with the same anti-pattern (repo-pulse:27, repo-article:26, repo-actions:29, star-momentum-alert:69) because heartbeat's site is the smallest possible — a token-for-token substitution, not a 24h/7d/14d offset recomputation.

What changed:
- skills/heartbeat/SKILL.md line 21: `$(date -u +%Y-%m-%d)` → `${today}`, with a parenthetical citing PR #63/#67 so a future cleanup doesn't drop the constraint.

Impact: Daily skill no longer hits the shell-guard on its scheduled-run check. Four sibling sites remain, queued for future self-improve runs.

PR: https://github.com/aaronjmars/aeon-agent/pull/71
