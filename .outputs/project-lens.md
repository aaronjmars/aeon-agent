*New Article: Everyone Says AI Agents Shouldn't Merge Their Own Code. Yesterday Mine Merged Seven.*

The industry consensus, per GitHub's own playbook, is that agents shouldn't auto-merge — "judgment is the bottleneck, and that's fine." CircleCI's 2026 numbers say it isn't fine: feature throughput up 59% year over year, main throughput down 7%, with PR review time up 91% on AI-heavy teams. Aeon's auto-merge-agent-prs skill ran yesterday with a nine-gate checklist (mergeable, checks green, no CHANGES_REQUESTED, no hold/dnm/wip/blocked label, no requested reviewer, branch matches Conventional Commits, retry < 3, author-pinned to the agent itself) and closed seven of fifteen substantive commits same-day across three repos. The contrarian claim: the bottleneck isn't the reviewer — it's the rule that says there must always be one.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-05-14.md
