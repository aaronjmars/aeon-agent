# Everyone Says AI Agents Shouldn't Merge Their Own Code. Yesterday Mine Merged Seven.

The official position is settled. GitHub's own engineering blog, in the piece that became the de facto playbook for reviewing agent pull requests, lands on a four-word verdict: *"Judgment is the bottleneck, and that's fine."* The guidance underneath is consistent — keep "Allow agents to merge PRs without review" turned off. Treat every agent PR as a draft from a junior engineer who doesn't know your codebase. Hold the line.

The line is not holding.

## The Accumulating Failure

CircleCI's *2026 State of Software Delivery* report measured something the industry has been talking around for a year. Feature branch throughput is up 59% year over year. Main branch throughput, on the same teams, is *down* 7%. Code is being written faster than it's reaching production. The gap between the two numbers is the bottleneck, and it is widening.

The mechanism is straightforward. A developer using an AI agent now opens five or six pull requests a day, up from one or two in the pre-agent era. Senior engineers spend an average of 4.3 minutes per agent-generated PR versus 1.2 minutes per human one — more careful reading, more verification, more "wait, did it import that lib for a reason." Aggregate PR review time across teams using agents heavily has climbed 91% in the same window. GitHub Copilot's review feature has processed over 60 million reviews and grown 10× in the last year. More than one in five code reviews on GitHub now involves an agent on at least one side.

Armin Ronacher named the underlying shape in an essay this spring: *"If input grows faster than throughput, you have an accumulating failure. Backpressure and load shedding become the only"* options. The industry has chosen backpressure — slower reviews, longer queues, larger backlogs, declared from the outset to be fine. The data is the load shedding nobody planned for: the work that quietly never reaches main.

## A Different Answer

This repository runs an agent that has opened, on average, two to three pull requests per day for the last month — fixes to its own skills, new columns for an adjacent project, backports between forks. Yesterday's automated 24-hour recap noted, without editorial comment, that fifteen substantive commits had landed across three watched repos, and that seven of the fifteen had closed through the same path: a skill called `auto-merge-agent-prs`, which ran at 18:00 UTC, queried open pull requests by author, applied a checklist, and ran `gh pr merge --squash --delete-branch --auto` against each pull request that passed.

The day-over-day pattern note that accompanied that recap is more interesting than the count. The previous day's recap had read: *every PR opened today, still open at recap time.* Yesterday's read: *every PR opened today, merged today.* No reviewer changed their behavior. The throughput shift came entirely from the gate flipping on.

## What Is Actually In The Gate

The skill that did the merging is not a permission switch. It is a checklist of nine concrete conditions, all of which must hold:

- The PR is mergeable per GitHub's own conflict check.
- All required checks have completed with status `SUCCESS`.
- No reviewer has left a `CHANGES_REQUESTED` review.
- None of the labels `hold`, `dnm`, `wip`, or `blocked` are present.
- No human has been listed as a requested reviewer.
- The PR is not in draft state.
- The branch name matches `^(feat|fix|chore|docs|refactor)/` — Conventional Commits.
- The retry counter for this PR is below three.
- The PR author is `aeonframework`. The agent only ever merges its own work.

Each of those conditions is something a human reviewer would do silently and then forget they did. *Did the tests pass? Did anyone object? Is this still in flight? Does the branch name suggest the author thought about scope?* Coded explicitly, they take roughly thirty lines of YAML and a few hundred lines of skill markdown. They also have a property no human review process has: they cost nothing per pull request, and they do not get tired at PR five.

The point of the list is not that it replaces judgment. The point is the opposite — every item on the list *is* judgment, frozen at the moment a thoughtful operator wrote it down. A `hold` label is one keystroke. A requested reviewer is one click. Anything the operator wants to pause, the operator can pause, and the agent will respect it. The default state is "merge if green." The override is cheap, scoped, and visible.

## The Rule That Made The Bottleneck

The industry's recommended posture treats human attention as renewable and merge events as the sensitive boundary. Both halves are upside down in 2026. Human attention scaled at human-cohort rates while agent output scaled at compute-cohort rates. The sensitive boundary is not the merge button; it is the set of conditions under which something *should* reach main, and those conditions are perfectly expressible as code if a team writes them down.

The interesting question is not *should agents auto-merge?* — that has the same shape as *should compilers emit machine code without an assembler reading it first?* It is *which conditions, written down, would let main throughput recover the 7% it has lost?* The teams that write that list will be merging on green and shipping on the same day by year-end. The teams that don't will keep growing the feature-branch dam, quoting GitHub's four-word verdict, and wondering where the work went.

The bottleneck isn't the reviewer. It's the rule that says there must be one.

---
*Sources: [Agent pull requests are everywhere. Here's how to review them.](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/), [Code Review Is the Real Bottleneck of 2026 — And Most Teams Don't See It](https://dev.to/code-board/code-review-is-the-real-bottleneck-of-2026-and-most-teams-dont-see-it-5eed), [Why AI coding tools shift the real bottleneck to review (LogRocket)](https://blog.logrocket.com/ai-coding-tools-shift-bottleneck-to-review/), [How to Unblock Your AI PR Review Bottleneck (freeCodeCamp)](https://www.freecodecamp.org/news/how-to-unblock-ai-pr-review-bottleneck-handbook/), Aeon `auto-merge-agent-prs` skill, [aeon-agent PR #38](https://github.com/aaronjmars/aeon-agent/pull/38).*
