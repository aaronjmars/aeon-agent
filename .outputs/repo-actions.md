*Repo Action Ideas — 2026-06-04*
Generated from analysis of aaronjmars/aeon (482⭐, 161 forks), aaronjmars/aeon-agent, and aaronjmars/minitor.

1. ecosystem-links skill (Feature, Medium)
   Weekly ECOSYSTEM.md URL health auditor — checks GitHub repos for archive/disable status and project URLs for HTTP 404s; completes the ecosystem monitoring trio alongside ecosystem-entrants + ecosystem-pulse.

2. Atrium catalog watcher (Integration, Small)
   Diffs the Atrium skill catalog weekly and notifies on new or updated packs — closes the feedback loop on the install-from-atrium path so new upstream skills surface automatically.

3. mcp-pulse backport (DX, Small)
   The natural 22nd consecutive same-day-after backport from upstream PR #272 — monitors the MCP server ecosystem (npm + GitHub) for new releases and adoption signals; last clean backport before fleet-scorecard which requires memory/instances.json.

4. $(date) batch self-fix — 3 remaining sites (DX, Small)
   Eliminates the shell-substitution anti-pattern from repo-article, repo-actions, and star-momentum-alert — the 4 prior fixes (PRs #63/#67/#71/#77) explicitly left these for future runs.

5. Column color labels (Feature, Small)
   DB-backed per-column hex color label shown as a dot in the expanded header and as the accent line on collapsed strips — the last missing at-a-glance layer on multi-column decks.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-06-04.md
