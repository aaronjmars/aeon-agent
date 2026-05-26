*Push Recap — 2026-05-26*
3 repos · 11 substantive commits by 4 authors (+1,414/-41, ~30 files), plus 36 automated cron pushes in aeon-agent.

*aeon — new leaderboard + registry curation:* Shipped *fleet-skill-adoption* (#245), a weekly skill ranking the 157-skill catalog by how many forks actually ENABLE each skill — the demand-side counterpart to fork-skill-gap (which shows what's missing). Plus 3 ECOSYSTEM.md fixes (zer0, GitBounty handles; Signa website) and the MythosForge community pack growing 1→5 read-only monitoring skills.

*aeon-agent — backport + self-fix:* Backported *ecosystem-pulse* + ECOSYSTEM.md from upstream (#62, also fixed a latent skills.json off-by-one → 92). Self-authored a weekly-shiplog fix (#63) dropping a `$(date)` call the runner's shell-guard blocks every run.

*minitor — controllable feeds:* Added per-column include/exclude filters (#51) — the active half of alert-keywords, which until now only highlighted. Exclude wins over include; round-trips through export/share. 50 column types unchanged.

Key changes:
- fleet-skill-adoption SKILL.md (+345): measures ENABLED not PRESENT, 10-status taxonomy, Sunday 22:00 stack slot
- minitor column-card.tsx (+80/-14): in-place client-side filtering + "N/M" badge + new migration 0004
- Watch: a Symbiote bot's "docstring scan" (#235) net-REMOVED detail from a @function_tool — may degrade its tool schema

Stats: ~30 files changed, +1,414/-41
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-26.md
