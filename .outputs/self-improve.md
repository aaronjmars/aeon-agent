*Agent Self-Improvement — 2026-04-28*

self-improve now cross-checks workflow failures via scripts/skill-runs
The self-improve skill's assessment phase used to scan only memory/logs/ for the last 2 days. From this PR onward it also runs `./scripts/skill-runs --hours 48 --failures` and cross-references any workflow-level failures against the logs.

Why: Logs are self-reported. A skill that crashes, times out, or fails in a pre-skill workflow step (prefetch script, sandbox limit, runner setup) never reaches the log-write step — so today's self-improve assessment was blind to that whole class of failures. GitHub Actions' workflow conclusion is the ground truth, and skill-analytics + heartbeat already use scripts/skill-runs the same way.

What changed:
- skills/self-improve/SKILL.md: new step 2b2 — run scripts/skill-runs --hours 48 --failures, cross-reference against the existing log scan, and treat a workflow failure with no corresponding log entry as the strongest infrastructure-class signal (points to workflow yml / prefetch script / sandbox limit, not the skill prompt).
- memory/MEMORY.md + memory/logs/2026-04-28.md: skills-built table + today's log.

Impact: Self-improve gains visibility into the failure class it most needs to fix — silent infrastructure errors. Same data source already powers two other meta-skills, so no new dependencies and no new secrets.

PR: https://github.com/aaronjmars/aeon-agent/pull/21
