⚠️ Heartbeat — 4 skills stuck since outage, weekly cadence delaying self-heal

🔴 STUCK (update, not new): 4 skills dispatched during the Aug 2–4 GH Actions outage never completed and were never redispatched — repo-pulse (dispatched Aug 3, 10:00 UTC), shiplog (Aug 3, 10:00 UTC), changelog (Aug 3, 08:37 UTC), memory-flush (Aug 2, 18:01 UTC). Yesterday's heartbeat expected these to "self-heal" like token-report/secured-watch/holdings did — they didn't. Root cause: all four are weekly-cadence skills, so the scheduler won't re-fire them until their next natural cron tick (memory-flush: Sun Aug 9 18:00 UTC; changelog/shiplog/repo-pulse: Mon Aug 10). Each is 9–10 days past its last real success. Manual re-trigger (workflow_dispatch) recommended if the operator doesn't want to wait until next week.

🟢 CLEAR: heartbeat self-check — last success 2026-08-04 19:36 UTC (<24h), no longer stale.

🟢 CLEAR: 0 open PRs, 0 issues, GH Actions scheduler running normally since recovery (Aug 4 14:46 UTC).

Status page: 🔴 DEGRADED (unchanged from yesterday, same root cause — 4 skills still stuck, not new breakage).