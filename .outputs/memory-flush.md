Done. Here's a summary of what was flushed:

## Summary

**Promoted to MEMORY.md:**
- 3 missing project-lens articles added to Recent Articles table:
  - 06-19: *The EU AI Act's Audit Trail Is Just a Commit History*
  - 06-20: *Every Agent Platform Promises Faster Restarts. One Framework Made Them Mandatory.*
  - 06-21: *The Part of a Cron-Native Agent That Has to Be a Server*

**Removed stale entries:**
- PRs #513 (Dependabot cfg), #512 (MCP README), #511 (Charon pack) — all merged per 06-21 push-recap; stripped from Next Priorities
- Removed aeon-agent #109 reference (CLAUDE.md sandbox PR — merged per 06-20 log)

**Updated:**
- Next Priorities: reflects current state — only #510 (LENS pack) and #418 (BEAMR, stalled) remain open; Dependabot now active with first-run context; ideas #2/#3/#5 re-eligible date set to 2026-07-02
- Last consolidated date: 2026-06-17 → 2026-06-21

**New lesson added:**
- `apps/**` npm changes in aaronjmars/aeon are NOT gated by any CI — only post-merge Vercel build catches app dep errors (surfaced by Dependabot batch, 2026-06-21)
