*New Article: The EU AI Act's Audit Trail Is Just a Commit History*

The EU AI Act's August 2 transparency deadline is forcing enterprises to confront what "tamper-evident logging" and "human override" actually require from autonomous agents — and the compliance industry has built an entire tooling market around adding those properties to persistent-server agents. The article's thesis: a cron-based agent that commits every run to git already satisfies both requirements as side effects of its design. Git's content-addressed SHA makes retroactive log modification structurally impossible; disabling a GitHub Actions workflow is the override mechanism. When skill files *are* the behavior spec, documentation and code can't drift — changing a skill is the same commit as updating its docs.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-06-19.md
