---
name: Status
description: At-a-glance operational overview of the agent
var: ""
---
> **${var}** — Section to focus on. If empty, shows full status.

If `${var}` is set, show only that section (e.g. "skills", "actions", "config").


Today is ${today}. Generate an operational status report for Aeon.

Steps:
1. Read `memory/MEMORY.md` for context.
2. **Skill inventory** — Parse `aeon.yml` and list all skills grouped by status:
   - Enabled skills with their schedule (cron → human-readable)
   - Count of disabled skills by time slot
   - Flag any skills that are enabled but have no matching `skills/<name>/SKILL.md`
3. **Recent activity** — Read the last 3 days of `memory/logs/` and summarize:
   - Number of skill runs per day
   - Which skills ran
   - Any errors or warnings logged
4. **GitHub Actions health** — Run:
   ```
   gh run list --limit 10 --json status,conclusion,name,createdAt,headBranch
   ```
   Summarize: total runs, pass/fail ratio, any currently running/queued.
5. **Open PRs** — Run `gh pr list --json number,title,state,createdAt,author` and list any open PRs.
6. **Configuration summary** — From `aeon.yml`, report:
   - Model in use
   - Notification channels configured (check which env vars are set)
   - Messaging integrations enabled
7. Format the report:
   ```
   *Aeon Status — ${today}*

   SKILLS: X enabled / Y total
   Enabled: skill1 (daily 7am), skill2 (daily 12pm)

   ACTIVITY (last 3 days):
   - YYYY-MM-DD: N runs (skill1, skill2, ...)
   - ...

   ACTIONS: X/Y passed | Z running
   OPEN PRs: N (list if any)

   CONFIG: model | channels
   ```
8. Send the report via `./notify`.
9. Log to `memory/logs/${today}.md`.
