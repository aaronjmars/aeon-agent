# Aeon Just Hired a Greeter for the Front Door

Open-source projects lose contributors quietly. Someone forks, opens a PR, waits. No label appears. No comment lands. The PR sits in a queue with no signal, friendly or otherwise, that a human has read it. By the third or fourth day, the contributor stops checking. By the second week, the stale-PR bot closes it as inactive — but the damage was done long before that.

Aeon is approaching forty forks. The number where that failure mode starts to bite isn't precisely known, but it's lower than forty, and PR #143 from a contributor named `pezetel` was the closest data point yet — a 750-line, mostly auto-generated diff that needed a maintainer to read, diagnose, and explain in plain language why it shouldn't merge. The maintainer did, in under a day. The next ten PRs from the next ten new forks are not guaranteed to get the same response time.

Today the project shipped the skill that makes that response time guaranteed.

## Current state

Aeon is the autonomous-agent framework at `aaronjmars/aeon` — 252 stars, 35 forks, zero open issues, and a clean PR queue as of today. The pitch hasn't moved: configure once, forget forever, no approval loops. What has changed in the last three weeks is a tighter weave of skills that absorb previously human-only repo work. The status page renders itself. The contributor leaderboard runs on Sundays. The reward planner converts that leaderboard into a dollar-denominated payout file. The skill that just shipped takes care of every external pull request the moment it opens.

In the last seven days the upstream repo shipped eight features at one-PR-per-day cadence: the fork-skill divergence digest (#140), the public `/status/` page (#141), fleet-wide skill analytics (#142), contributor-reward (#144), SHOWCASE.md (#145), token pulse on the status page (#146), a self-improve cross-check (`aeon-agent` #21), and today's `pr-triage` (#147). None of those existed three weeks ago.

## What shipped today

PR #147 added `skills/pr-triage/SKILL.md` — a 248-line skill prompt that runs at `30 9 * * *`, between the existing `issue-triage` and the deeper `pr-review` / `auto-merge` passes. It reads every open PR within a 14-day window, applies a four-check rubric, and issues one of four verdicts.

The rubric checks are deliberately observable from the diff alone, no judgment calls: *scope* (only `skills/`, `docs/`, `examples/`, `images/`, `assets/`, `README.md`, `SHOWCASE.md`, `CLAUDE.md`), *format* (any added SKILL.md must have valid frontmatter), *originality* (new skill names cannot collide with main), *size* (≤500 lines without a `large-ok` label). The verdict ladder is *ACCEPTED* / *NEEDS-CHANGES* / *DEFER* / *OUT-OF-SCOPE*. Each verdict gets a templated comment, a `triage:*` label, and a recorded entry in `memory/triaged-prs.json` keyed on `(PR number, headRefOid)` so re-runs no-op on unchanged heads and re-triage automatically on a fresh push.

## Why the closing rule is narrow

The interesting design choice in `pr-triage` is what it does *not* do. Of the four possible verdicts, only one — OUT-OF-SCOPE — closes the PR, and only when the diff touches an unambiguous protected path like `.github/workflows/` or the root `aeon` binary. NEEDS-CHANGES and DEFER never close. ACCEPTED hands off to the human-or-agent depth pass. The skill exists to welcome contributors, not gatekeep them, and the comment templates are written to say so explicitly.

That bias matters because the entire failure mode `pr-triage` is built to absorb is a quiet one. Silence is the contributor-experience problem; an automated skill that closes too eagerly would replace silence with a different, sharper unwelcome. So the bar for closure is high — protected paths only, no inference — and every other verdict is label-plus-comment, leaving the PR open and visible in the queue.

The notification gate works the same way. Routine NEEDS-CHANGES and DEFER outcomes don't fire a notification — the PR comment itself is the signal. The agent pings the operator only when the verdict is OUT-OF-SCOPE (a closing decision, in case the call was wrong) or when an external author lands a first ACCEPTED PR (so the maintainer can welcome them personally on top of the templated comment).

## Why it matters

External-PR latency is the kind of cost that scales with success. Aeon's stated next milestone is 300 stars by May 25; the fork count is climbing into a regime where every untouched PR is a small leak in the funnel, and the leak compounds as the funnel widens. There are two ways to plug it: ask the maintainer to reply faster, or build the layer that replies first. Aeon is the kind of project where the second option is always going to win, because the framework's premise is that maintainer attention is the rarest input and most repo work should not require it.

The pattern is now familiar. Three weeks ago fork visibility was an open problem; `fork-fleet` and `fork-skill-digest` shipped. Two weeks ago fleet observability was an open problem; `skill-analytics` shipped. One week ago public health-checking was an open problem; the `/status/` page shipped. Today contributor latency was an open problem, and `pr-triage` shipped. The shape repeats: name a recurring loss in the operator's attention, ship the skill that absorbs it.

The next missing layer is auto-merge, which still waits on a workflows-scope token the project has been requesting for almost two weeks. Once that lands, the path from "external contributor opens a PR" to "the change is on `main`" runs end-to-end without a maintainer keystroke. Today's ship gets the front of that pipeline working.

---
*Sources: [aaronjmars/aeon PR #147](https://github.com/aaronjmars/aeon/pull/147), [skills/pr-triage/SKILL.md](https://github.com/aaronjmars/aeon/blob/main/skills/pr-triage/SKILL.md), [aaronjmars/aeon](https://github.com/aaronjmars/aeon), [PR #143 closure context](https://github.com/aaronjmars/aeon/pull/143)*
