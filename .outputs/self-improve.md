*Agent Self-Improvement — 2026-05-04*

Heartbeat-only fallback for the operator-scorecard agent-health verdict. The weekly scorecard backport that merged earlier today (PR #28) would have permanently reported WATCH on every Monday in this fork, because it depends on a skill that isn't enabled here. This patches the verdict logic before the first natural run on May 11.

Why: operator-scorecard reads `articles/skill-analytics-*.md` for paragraph 1, but skill-analytics is not enabled in aeon-agent (0 such articles on disk). Under the original spec, `agent_health_source=missing` fired every run, paragraph 1 emitted INSUFFICIENT_DATA, and the worst-of-three rollup demoted the overall weekly verdict to WATCH — even on weeks where every heartbeat ran clean (the steady state on this fork). That defeats the "was this week worth it?" answer the skill is supposed to deliver.

What changed:
- skills/operator-scorecard/SKILL.md (+31/-10): step 2d split into three branches — A (skill-analytics present → original logic), B (skill-analytics missing, heartbeat present → verdict from heartbeat counts alone), C (both missing → preserved INSUFFICIENT_DATA). Article paragraph, notification line, and log line all resolve per-branch placeholders so paragraph 1 doesn't print null/null/null. Constraints adds an explicit "heartbeat-only is first-class, not a degraded mode" note so future maintainers don't revert it.

Impact: when operator-scorecard is enabled (still shipped enabled: false, first natural run May 11 if turned on), the weekly scorecard reports a real OK/WATCH/DEGRADED verdict computed from heartbeat history instead of permanent WATCH. Heartbeat itself audits every scheduled skill against logs + Actions runs each evening, so a week of clean HEARTBEAT_OK reports is a real OK signal — not insufficient data.

PR: https://github.com/aaronjmars/aeon-agent/pull/29
