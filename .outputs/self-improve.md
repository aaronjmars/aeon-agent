*Agent Self-Improvement — 2026-05-20*

project-lens — made the rotation rule mathematically feasible. The skill said "Never repeat an angle used in the last 14 days" but listed only 8 angle categories. With daily runs, by pigeonhole at least one category must repeat within 14 days — the rule was unachievable as written.

Why: Reviewing recent project-lens logs. May 18 entry literally noted "Cathedral vs Bazaar sub-angle, distinct from May-15 antifragility — only Philosophy use in last 14 days was antifragility" — the agent was already working around the impossible rule by tracking sub-angles informally. May 19 confirmed it: Current Events used May 6/10/19, Contrarian used May 7/8/12/14/16. Stated rule and actual practice had drifted apart.

What changed:
- skills/project-lens/SKILL.md (Angle Selection): no-repeat window reduced from 14d to 7d (feasible: 7 < 8 categories); pigeonhole note added so a future edit doesn't slide back to 14
- skills/project-lens/SKILL.md (Angle Selection): formalized sub-angle hygiene with two worked examples (Philosophy can rotate cathedral-vs-bazaar → antifragility; Historical parallel can rotate printing press → railway gauge wars)
- skills/project-lens/SKILL.md (step 2): updated check to read ## Project Lens log entries too, with explicit fallback for the all-8-used edge case
- skills/project-lens/SKILL.md (step 7 log block): added a Sub-angle field so the next run can dedup on the finer-grained signal

Impact: instructions now describe what the agent has already been doing for at least two weeks — future runs no longer have to silently re-derive the sub-angle workaround. Same shape as the explicit-marker family (PRs #37 / #43 / #48 / #51): convert an undocumented latent workaround into a written contract.

PR: https://github.com/aaronjmars/aeon-agent/pull/54
