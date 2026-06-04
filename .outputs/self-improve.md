*Agent Self-Improvement — 2026-06-04*

repo-article `$(date)` self-fix

`skills/repo-article/SKILL.md` step 1 was using `$(date -u -d '7 days ago' ...)` to compute the commit-history cutoff. The runner hook blocks all `$(...)` shell substitution, so every daily 16:00 UTC run had to improvise around it. Swapped for a literal `SINCE=YYYY-MM-DDT00:00:00Z` that the agent computes from `${today}` minus 7 days at write time.

Why: continuation of the runner-shell-guard cleanup wave. The Jun-02 self-improve run (PR #77, repo-pulse) explicitly listed three skills with this anti-pattern as "left for future runs." repo-article picked because daily cadence is the highest-leverage of the three and the substitution is a single line — smallest-effort next item. Same fix class as PRs #63 (weekly-shiplog), #67 (push-recap), #71 (heartbeat), #77 (repo-pulse).

What changed:
- `skills/repo-article/SKILL.md` step 1: inline `since="$(date ...)"` → `SINCE=YYYY-MM-DDT00:00:00Z` literal + paragraph citing the prior PRs so a future cleanup can't drop the constraint.
- `memory/MEMORY.md`: new Skills Built row; the two remaining unfixed sites (`repo-actions:29` and `star-momentum-alert:69`) surfaced again for future rounds.

Impact: removes daily improvisation friction on repo-article — the cutoff is now declarative and reproducible across runs instead of fighting the hook. Article remains a 7-day retrospective; the slightly wider window (7d–7d+16h) is absorbed by the prose framing.

PR: https://github.com/aaronjmars/aeon-agent/pull/81
