## 🔴 Fleet incident 08-31 — all skills failed 06:00–12:00 UTC, fixed at 12:13

**Root cause found and already fixed.** Every skill dispatched today (7 skills, 17 runs, 0 successes) died with the same signature — `0 input tokens, 0 output tokens, $0.00 cost` — the LLM gateway never answered. That's the exhausted Claude subscription you pinned around with [`b054cb0`](https://github.com/aaronjmars/aeon-agent/commit/b054cb0) (gateway → GLM, 12:13 UTC). **This heartbeat is the first run through GLM and it's executing normally — the fix works.** CI on that commit is green.

**🔴 FAILED today** (all zero-token gateway errors, not per-skill bugs):
- `token-report` (3×), `repo-pulse` (3×), `shiplog` (3×), `changelog` (3×), `holdings` (3×), `aeon-update` (2×), `secured-watch` (1×)

**Action needed — re-dispatch the 5 weekly skills.** They're Monday-cadence, so their next cron is **7 days out**; without a manual run they stay red until 09-07. This is the same trap as the 08-02 spending-limit stall. `token-report` (daily 06:00) and `secured-watch` (daily 12:00) self-recover tomorrow.

Status page → **🔴 DEGRADED** until the weekly five report a success. Everything else is clean: no stalled PRs (#997 on aeonfun/aeon is 1h old), no urgent issues, no open health issues.
