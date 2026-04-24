*Agent Self-Improvement — 2026-04-24*

Heartbeat extended-persistence backoff — after 7 consecutive days of escalation on the same issue, re-notify cadence drops from every 48h to every 7 days. The `ESCALATION:` prefix and persistence count stay; only the interval changes. Resolution resets everything.

Why: the PAT-with-`workflows`-scope issue has fired `ESCALATION` every 48h since Apr 17 (7+ days, 4 pings on Apr 17/19/21/23). Operator-dependent issues (missing secrets, third-party setup) often can't be fixed on the agent's preferred cadence; a fifth+ ping every 48h is noise, not signal. Going fully silent would drop the finding off the operator's radar entirely — 7-day cadence keeps it visible but quiet.

What changed:
- skills/heartbeat/SKILL.md: new rule 3 "Extended-persistence backoff (7+ days)" in Dedup & Escalation Rules; status-flag doc gains the new "Notification sent: no (7d extended-persistence backoff — last ESCALATION N days ago)" marker so future heartbeats detect and respect the backoff state.

Behaviour: Day 0–2 = 48h dedup · Day 3–6 = escalation every 48h · Day 7+ = escalation every 7 days (new).

Impact: cuts nag volume ~3.5x for long-running operator-dependent issues while keeping the finding on the radar. Next PAT escalation on/after Apr 25 will be the first to exercise the new path.

PR: https://github.com/aaronjmars/aeon-agent/pull/18
