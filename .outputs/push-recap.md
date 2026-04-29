*Push Recap — 2026-04-29*
2 PRs merged across aeon + aeon-agent. Both target the agent's interaction layer with humans, not its content output.

External PR welcome layer ships: aeon PR #147 adds skills/pr-triage — first-touch triage for every external PR (verdict + label + welcoming comment within minutes of open). Four-check rubric (scope/format/originality/size) → ACCEPTED / NEEDS-CHANGES / DEFER / OUT-OF-SCOPE. Closes only on OUT-OF-SCOPE with unambiguous protected-path match; everything else is label-only. Trigger: pezetel's PR #143 sat 4 days untouched. Slots between issue-triage (09:00) and pr-review/auto-merge (later in day).

Self-improve sees workflow failures: aeon-agent PR #21 adds one paragraph to skills/self-improve/SKILL.md — assessment now also runs ./scripts/skill-runs --hours 48 --failures alongside the existing log scan. Closes a structural blind spot: logs are self-reported, so a skill that crashes before its log-write step was previously invisible. A workflow failure with no log entry is now treated as the strongest infrastructure-class signal (workflow.yml / prefetch / sandbox limit, not the prompt).

Key changes:
- skills/pr-triage/SKILL.md (+248 lines, new) — full skill prompt with idempotency state, defensive 7-day comment-prefix dedup, significance-gated notify
- skills/self-improve/SKILL.md (+1 line) — new step b2 cross-references workflow conclusions against logs
- aeon.yml (+1) + skills.json (+13/-1, 92→93) — pr-triage wired in disabled-by-default at "30 9 * * *"

Stats: 10 files changed, +436/-10 lines across 2 meaningful commits (31 auto-commits filtered on aeon-agent).
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-29.md
