---
name: Heartbeat
description: Proactive ambient check — surface anything worth attention
var: ""
tags: [meta]
---
> **${var}** — Area to focus on. If empty, runs all checks.

If `${var}` is set, focus checks on that specific area.


Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.

Check the following:
- [ ] Any open PRs stalled > 24h? (use `gh pr list` to check)
- [ ] Anything flagged in memory that needs follow-up?
- [ ] Check recent GitHub issues for anything labeled urgent (use `gh issue list`)
- [ ] Scan aeon.yml for scheduled skills — cross-reference with **both** today's logs AND today's GitHub Actions runs to find any that haven't run when expected.
  **Detection method (use ALL three signals before flagging a skill as missing):**
  1. Check `memory/logs/${today}.md` for a `## ` header containing the skill name (case-insensitive, partial match — e.g. "Token Report" matches `token-report`)
  2. Run `gh run list --workflow=aeon.yml --created=$(date -u +%Y-%m-%d) --json displayTitle,status` — if the skill appears in a completed/in-progress/queued run, it's NOT missing
  3. Only flag as missing if the skill was expected to run **more than 2 hours ago** AND neither logs nor Actions runs show it
  **Log header aliases:** Skills often log under a human-readable header, not their aeon.yml name. Match flexibly:
  - `token-report` → `## Token Report`
  - `fetch-tweets` → `## Fetch Tweets`
  - `push-recap` → `## Push Recap`
  - `repo-article` → `## Repo Article`
  - `repo-actions` → `## Repo Actions`
  - `hyperstitions-ideas` → `## Hyperstitions` or `## Ideas`
  - `hacker-news-digest` / `hn-digest` → `## HN Digest` or `## Hacker News`
  - `polymarket` / `polymarket-comments` → `## Polymarket`
  - `repo-pulse` → `## Repo Pulse`
  When in doubt, also check the Actions run list — the `displayTitle` always contains the exact skill name from aeon.yml.

## Dedup & Escalation Rules

Before sending any notification, apply these rules in order:

1. **48h dedup (transient issues):** Grep memory/logs/ for the same item. If a **notification was sent** for this exact issue in the last 48h (look for "Notification sent" or "notification sent" near the item), skip it. Log it as "within 48h dedup → no new notification."

2. **Escalation (persistent issues):** If the same issue has been **logged but NOT resolved** for 3+ consecutive days (i.e., it appears in logs from 3 different dates without a corresponding resolution or fix), **re-notify** with an `ESCALATION:` prefix even if it was logged recently. This overrides the 48h dedup. A persistent unfixed problem is worse than a duplicate notification.
   - To check: count how many distinct dates in `memory/logs/` contain the same finding (e.g., "project-lens — STILL MISSING"). If >= 3 dates, escalate.
   - Escalation notifications should include: how many days the issue has persisted, what has been tried, and a concrete suggested action.

3. **Extended-persistence backoff (7+ days):** Once an issue has been escalated and is still unresolved after 7 consecutive days, **switch the re-notify cadence from every 48h to every 7 days**. Keep the `ESCALATION:` prefix and include the persistence count, but stop nagging every other day — operator-dependent issues (missing secrets, external setup, third-party outages) often can't be resolved quickly, and fifth+ ping is noise, not signal.
   - To check: find the most recent `Notification sent: yes (ESCALATION...)` log entry for this issue. If it was within the last 7 days AND the issue is already 7+ days old, **suppress** this run's notification and log `Notification sent: no (7d extended-persistence backoff — last ESCALATION <N> days ago)`.
   - The first escalation after crossing the 7-day threshold still fires on the normal 48h cadence; backoff kicks in only on the *next* escalation after that.
   - Resolution resets everything: once the issue is fixed (or the log entry disappears from recent days), all counters restart.

4. **Batch:** Group all findings (both new and escalated) into a single notification — don't send one per issue.

**Key distinction:** The dedup check looks for whether a *notification* was sent, not whether the issue was *logged*. Heartbeat logs findings every run for record-keeping, but that should not reset the dedup timer.

If nothing needs attention, log "HEARTBEAT_OK" and end your response.

If something needs attention:
1. Send a concise notification via `./notify`
2. Log the finding and action taken to `memory/logs/${today}.md`
   - For each finding, clearly mark: **"Notification sent: yes"**, **"Notification sent: no (48h dedup)"**, **"Notification sent: yes (ESCALATION — N days persistent)"**, or **"Notification sent: no (7d extended-persistence backoff — last ESCALATION N days ago)"**
   - This distinction is critical — future heartbeats use it to decide whether to dedup, escalate, or apply extended backoff
