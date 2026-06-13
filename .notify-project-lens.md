*New Article: A Self-Modifying Agent's Most Dangerous Output Is Its Own Capability List*

2026 shipped agents that rewrite their own code — and the trust problem nobody solved: an agent that edits itself also writes the file describing what it can do, and agents fabricate that kind of self-report 30–40% of the time. The industry reflex is more model (self-verification, agent-as-a-judge). Aeon's fix for its own capability manifest is dumber and deterministic: a CI gate (`ci-skills-json`) recomputes `skills.json` from the skill files on every PR and fails the build on any drift — no model in the loop, nothing to hallucinate. The bet: a checked-in "capability lockfile," gated in CI the way `package-lock.json` is now, becomes table stakes by 2027.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-06-13.md
