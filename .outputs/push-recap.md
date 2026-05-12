*Push Recap — 2026-05-12*
3 repos · 6 commits · 6 merged PRs · all by @aaronjmars · 28 files, +2,143/-13 lines

Two-wave merge sweep: wave 1 (23:30 UTC May 11) landed yesterday's open feature PRs; wave 2 (12:35 UTC May 12) landed today's. Two new PRs per repo, perfectly balanced. The May-10 repo-actions idea brief is now fully consumed — every single idea has a merged PR.

*aeon — real-time + fork-fleet event layer (#165 + #166):*
price-threshold-alert (ATH / ±20% 1h / operator targets, */30 min, 4h dedup per gate) closes the window between calm-daily token-report and event-driven signal. fork-release-tracker (Sunday 19:30 UTC) answers "did any fork ship a tagged release this week?" — pairs with fork-cohort's 19:00 UTC "is the fork alive?" scan. With today's ATH at $0.0000331, the price-alert ATH gate would have fired had it been enabled.

*aeon-agent — last manual checkpoints close (#38 + #39):*
auto-merge-agent-prs (daily 18:00 UTC, 9 eligibility gates incl. author=aeonframework + branch-name discipline + retry cap, gh pr merge --squash --auto) removes the operator click on every agent-authored PR. thread-formatter backport (9-signal scoring, threshold 3, 5-tweet 280-char structure) pre-builds the paste-block when a high-signal event lands. Same-day-after backport pattern now caught up — only v4-readiness remains.

*minitor — column count 39 → 41 (#34 + #35):*
github-actions column (CI run visibility — workflow + branch filter, status pill across 9 terminal conclusions + in-flight) closes minitor's last big repo-health gap. npm column (keyless registry search + weekly-downloads badge, 4 sort modes heavy-weighted 0.8/0.1/0.1) fills the package-discovery surface — the canonical TypeScript discovery layer for minitor's audience. Two-day plugin sprint (39 → 41) is the largest in the project's history.

Key changes:
- aeon ATH ($0.0000331, +454% 24h) lands two hours before fork-release-tracker merges — both would have fired together if the skills were on
- auto-merge-agent-prs needed the workflows-scope PAT rotated May 6 to enable gh pr merge --auto; that unblock turned into shipped code 5 days later
- minitor's github-actions plugin documents 3 integration quirks inline (workflow filter applied client-side, page-completeness uses raw length, no partial-duration on in-flight runs) — fifth PR in a row following that pattern

Stats: 28 files changed, +2,143/-13 lines · 0 open PRs from today's feature at cutoff · 299⭐ on aeon (1⭐ from 300⭐ milestone)

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-12.md
