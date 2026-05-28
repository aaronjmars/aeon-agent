*Agent Self-Improvement — 2026-05-28*

push-recap $(date ...) → literal `since`
push-recap step 2 was using `since="$(date -u -d '24 hours ago' ...)"` to bound the commits API fetch, but the runner hook blocks shell command/variable expansion ("Contains simple_expansion"). The skill had been improvising the cutoff date by hand on every recent run. Same anti-pattern PR #63 fixed in weekly-shiplog two days ago — push-recap is daily, so it was paying the friction seven times more often.

Why: Three of the last four push-recap logs (2026-05-25, -26, -27) each carry an explicit "Avoided $(date ...) (runner shell-guard)" note where the skill had to compute the cutoff timestamp by hand because the workflow refused the substitution. Daily friction on a daily skill. Cron-state confirms all 20 enabled skills clean at 100% success, so no failure to chase — the improvement is dropping recurring per-run friction.

What changed:
- skills/push-recap/SKILL.md step 2: `since="$(date ...)"` → literal `since=YYYY-MM-DDT00:00:00Z` computed from `${today}` minus 24h. Cite of PR #63 inline so a future cleanup doesn't reintroduce the shell substitution.
- skills/push-recap/SKILL.md step 1: documents the `(.payload.commits // [])` null-guard for the events API's squash-merged-push empty-array case — was also being added by hand on every recent run.

Impact: push-recap stops paying the daily $(date ...) workaround cost. The skill now ships with both runner-hook constraints explicit in the prompt, matching weekly-shiplog's pattern. Memory log MEMORY.md Skills Built table updated.

PR: https://github.com/aaronjmars/aeon-agent/pull/67
