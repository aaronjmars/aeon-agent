*Agent Self-Improvement — 2026-05-26*

Fixed weekly-shiplog so it stops fighting the runner's shell-expansion guard. Its step-1 commits query used a `since="$(date -u -d '7 days ago' ...)"` shell substitution, which the runner hook blocks every run — forcing the agent to hand-improvise the query each time. The cutoff is now a literal ISO date computed from today minus 7 days, matching the jq-internal pattern the PR/release queries in the same step already use.

Why: The 2026-05-25 weekly-shiplog run logged it plainly — "repo hook blocks shell variable expansion ('Contains simple_expansion') — gathered per-PR stats via literal gh api calls instead." Recurring weekly friction on an otherwise-healthy skill (all 21 skills at 100% success rate, zero failures this scan).

What changed:
- skills/weekly-shiplog/SKILL.md: commits cutoff `$(date ...)` → literal `since=YYYY-MM-DDT00:00:00Z` from ${today}; added a note on the hook constraint; also parenthesized `(.commit.message | split("\n")[0])` to fix a latent jq precedence bug on the same line.

Impact: weekly-shiplog runs its prescribed query directly instead of improvising around a blocked command — fewer wasted turns, more reproducible weekly digests.

PR: https://github.com/aaronjmars/aeon-agent/pull/63
