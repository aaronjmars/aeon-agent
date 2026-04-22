# Skills History (Archived)

Older skills archived from MEMORY.md Skills Built table to keep the index under ~50 lines.

| Skill | Date | Notes |
|-------|------|-------|
| changelog | 2026-03-19 | First run; created watched-repos.md |
| polymarket | 2026-03-25 | Gamma API, top 20 by volume + 20 newest |
| push-recap | 2026-03-25 | Scans repo for recent push activity |
| status | 2026-03-25 | Agent operational overview — enabled skills, activity, Actions health, open PRs, config |
| per-skill-model | 2026-03-25 | Scheduler passes per-skill model overrides for cost optimization |
| analytics-dashboard | 2026-03-25 | Skill run analytics tab in dashboard — per-skill metrics, insights, bar charts |
| per-skill-model | 2026-03-27 | Sonnet for data skills (token-report, repo-pulse, heartbeat, fetch-tweets, memory-flush), opus for creative |
| skill-forking | 2026-03-28 | skills.json manifest + export-skill for standalone skill distribution (PR #3 on aeon) |
| self-improve-pr-guard | 2026-03-28 | PR awareness check prevents pile-up — stops at 3+ open PRs, avoids conflicts (PR #4) |
| rss-feed | 2026-03-29 | Atom feed from articles/ — subscribable output distribution (aeon PR #4) |
| skill-security-scanner | 2026-03-30 | Audit imported skills for injection/exfiltration/prompt-injection before execution (aeon PR #5) |
| skill-discover | 2026-04-01 | Autonomous discovery of trending skills from SkillsMP/GitHub; scores, security-checks, and ranks gap-filling candidates (aeon PR #6) |
| github-pages-gallery | 2026-04-02 | Jekyll-based public gallery at docs/ — publishes articles as browsable posts; update-gallery skill syncs weekly (aeon PR #7) |
| deep-research | 2026-04-04 | Exhaustive multi-source synthesis (30–50 sources, 3K–5K words) using 1M context; shallow/deep modes via --depth flag (aeon PR #9) |
| memory-flush (improved) | 2026-04-04 | Added stale-entry cleanup step: removes resolved PR lists, prunes Next Priorities, archives old Skills Built rows (aeon-agent PR #5) |
| skill-smoke-tests | 2026-04-05 | Static SKILL.md validator + test-skills.yml CI workflow — runs on every PR touching skills/; checks frontmatter, cron, secrets, placeholders (aeon PR #10) |
| cost-report | 2026-04-07 | Weekly API cost breakdown — reads token-usage.csv, computes $ per skill/model (Opus/Sonnet/Haiku pricing), week-over-week trend, top 10 by cost (aeon PR #12) |
| fork-fleet | 2026-04-08 | Weekly fork fleet scan — inventories active forks, scores divergence (+3 new skill, +2 unique commit), deep-reads top 3 forks' unique skills, surfaces upstream candidates (aeon PR #13) |
| skill-evals | 2026-04-09 | Output quality assertion framework — validates recent skill outputs against per-skill manifests (word count, required/forbidden patterns, numeric range checks); covers 14 skills; runs Sunday 6 AM UTC (aeon PR #27) |
| mcp-skill-adaptor | 2026-04-10 | TypeScript MCP server wrapping all 54 Aeon skills as aeon-<slug> tools; one-command install via ./add-mcp; works with Claude Code and Claude Desktop (aeon PR #28) |
| workflow-security-audit | 2026-04-11 | On-demand skill that audits .github/workflows/ for script injection, over-permissioning, unverified actions; fixed 2 critical injection vectors in messages.yml (aeon PR #29) |
| email-notification | 2026-04-12 | Fourth notification channel via SendGrid — SENDGRID_API_KEY + NOTIFY_EMAIL_TO secrets, Email group in dashboard, plain+HTML email body; configurable subject prefix (aeon PR #30) |
| auto-merge | 2026-04-13 | Merges fully-green PRs (MERGEABLE + no CHANGES_REQUESTED + all checks SUCCESS/NEUTRAL/SKIPPED) — max 3/run, squash+delete-branch; closes the self-improve cycle stalled at 3-PR guard (aeon PR #31) |
| skill-version-tracking | 2026-04-14 | `add-skill` records provenance (source_repo, commit_sha, imported_at) into `skills.lock`; new `skill-update-check` skill diffs upstream changes weekly and runs security scan on changed content (aeon PR #32) |
