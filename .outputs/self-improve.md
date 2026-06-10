*Agent Self-Improvement — 2026-06-10*

repo-pulse — `### owner/repo` subheader per repo in log
Multi-repo runs with profile enrichment were interleaving the second repo's stats into the first repo's `**New account profiles (24h):**` bullet list, because step 7's template only depicted one repo and no separator existed.

Why: Jun-09 and Jun-10 logs both show `**aaronjmars/minitor**: stargazers_count=11, forks_count=1` appearing as the last bullet of aeon's profile enrichment list instead of its own repo block. Profile enrichment shipped Jun-07 (PR #88); the formatting gap surfaced the moment aeon had enriched profiles and minitor had zero stars.

What changed:
- skills/repo-pulse/SKILL.md (+8/-2): step 7 now mandates `### owner/repo` subheader per repo + revised template + parser-safety note (downstream parsers match the literal `**owner/repo**: stargazers_count=N` bullet, not surrounding markdown).

Impact: cleaner per-repo log blocks for operator + agent scanning; no change to `star-momentum-alert`, `operator-scorecard`, `heartbeat` which all parse the same literal bullet.

PR: https://github.com/aaronjmars/aeon-agent/pull/92
