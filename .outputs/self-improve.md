*Agent Self-Improvement — 2026-04-16*

Heartbeat now escalates persistent issues instead of silently suppressing them.

The 48h dedup rule had a bug: it checked whether an issue was logged recently, but since heartbeat logs every finding every run, the dedup window never expired. Persistent problems (like project-lens and weekly-shiplog not dispatching for 4+ days) got one notification on day 1, then silence forever.

Why: Logs from Apr 13–16 show project-lens and weekly-shiplog flagged as non-dispatching across 5+ heartbeat runs, but every run after the first said "within 48h dedup — no new notification." The operator never got a follow-up.

What changed:
- skills/heartbeat/SKILL.md: Replaced flat 48h dedup with a tiered system — transient issues still dedup normally, but issues persisting 3+ consecutive days trigger an ESCALATION re-notification that overrides the dedup. Also fixed the dedup check to look for notification-sent markers rather than log entries.

Impact: Persistent unfixed issues will now re-surface with escalation context (how many days, what has been tried, suggested action) instead of going silent. Heartbeat becomes a proper watchdog, not just a one-shot alert.

PR: https://github.com/aaronjmars/aeon-agent/pull/12
