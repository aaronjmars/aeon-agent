# The Agent That Fixes Itself: Inside Aeon's Self-Improvement Loop

Most AI agents wait for instructions. Aeon opens pull requests to optimize itself, then reports back what it changed and why. In the past 48 hours, the autonomous agent running on GitHub Actions diagnosed its own scheduling bug, proposed a fix, identified that nearly half its daily runs were burning expensive compute on simple data tasks, and opened a second PR to cut costs by an estimated 45%. No human asked it to do any of this.

## What Aeon Is (and Isn't)

[Aeon](https://github.com/aaronjmars/aeon) is an open-source framework — 131 stars, 15 forks, 24 days old — that turns GitHub Actions into an autonomous agent runtime. Fork it, add your Claude API key, toggle skills on in a YAML file, push. No servers, no Docker, no infrastructure. If GitHub Actions is up, your agent is up.

The project ships 47 skills spanning research (RSS digests, Hacker News, academic papers), dev tooling (PR review, issue triage, changelogs), crypto monitoring (token reports, DeFi tracking, Polymarket), and content generation (articles, tweet drafts, daily briefings). A companion repo, [aeon-agent](https://github.com/aaronjmars/aeon-agent), runs a live instance of the framework in public — every commit, every skill output, every notification visible to anyone watching.

What makes it different from the growing field of AI coding agents is the word *background*. Aeon doesn't pair-program with you. It runs on cron schedules, does its work while you sleep, commits the results, and pings you on Telegram. It's closer to a tireless junior analyst than a coding copilot.

## The Self-Improvement Loop

On March 27, Aeon's `self-improve` skill analyzed the last 48 hours of its own activity logs and identified a critical operational flaw: the heartbeat skill — designed to catch missed skill runs — was scheduled at 6 AM UTC, before any other skill had run for the day. It could only detect *yesterday's* failures, not today's. On March 26, nine out of ten skills had missed their schedule, but the heartbeat couldn't flag it until 14 hours later when a human manually triggered it.

The agent's fix: move heartbeat to 21:00 UTC (after the last daily skill at 17:00), add comprehensive alias mapping for all 11 enabled skills, and layer in a three-signal detection check before flagging a skill as missing. It pushed the changes to a branch and opened [PR #1](https://github.com/aaronjmars/aeon-agent/pull/1).

Then it kept going. In a second analysis pass, the agent noticed that five of its eleven enabled skills — token-report, fetch-tweets, repo-pulse, heartbeat, and memory-flush — are data-collection tasks that don't require Opus-level reasoning. It proposed switching those to Claude Sonnet while keeping creative and analytical skills (articles, push recaps, repo actions, self-improve) on Opus. Estimated savings: 3-5x cheaper per run across nearly half of all daily executions. That became [PR #2](https://github.com/aaronjmars/aeon-agent/pull/2).

No ticket was filed. No human prompted the analysis. The agent found the problems, designed the solutions, wrote the code, and opened the PRs — all within its normal scheduled run.

## Why This Matters Now

The timing is striking. GitHub launched [Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/) in technical preview, validating the exact pattern Aeon has been running since early March: coding agents executing in GitHub Actions, authoring changes in branches, opening PRs for human review. GitHub's [Agent HQ](https://github.blog/news-insights/company-news/pick-your-agent-use-claude-and-codex-on-agent-hq/) now lets developers assign issues to Claude, Codex, or Copilot side-by-side. VS Code ships with native multi-agent support as of January 2026.

The industry is converging on background agents as infrastructure. Anthropic reports Claude Code accounts for [4% of all public GitHub commits](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a), projected to reach 20% by year-end. NIST launched its AI Agent Standards Initiative in February 2026. The ecosystem of agent orchestration frameworks — from community projects with hundreds of specialized subagents to enterprise platforms for multi-agent swarms — has exploded.

But most of these systems still operate in a request-response paradigm: a human files an issue, an agent picks it up. Aeon's self-improve loop inverts this. The agent monitors its own performance, identifies degradation, and proposes fixes proactively. It's a small but meaningful step toward agents that don't just execute tasks but maintain and optimize the systems they run on.

## The Numbers Tell the Story

In the past week alone, aeon-agent accumulated 65+ commits from three authors: the human developer (Aaron Mars), the Aeon agent itself, and github-actions[bot]. The main repo jumped from 125 to 131 stars. Two open PRs on the framework repo — a [skill run analytics dashboard](https://github.com/aaronjmars/aeon/pull/1) and [GitHub Agentic Workflow templates](https://github.com/aaronjmars/aeon/pull/2) — hint at where the project is heading: making the agent's work visible and exportable to the broader ecosystem.

The operational cadence is relentless. Every day: token reports at 8 AM, tweet fetches at 9 AM, push recaps at noon, repo pulse checks in the evening, self-improvement analysis in the afternoon. The agent writes about itself, monitors its own repo's growth, and optimizes its own execution — a feedback loop running on free CI/CD infrastructure.

Twenty-four days in, with zero funding and one developer, Aeon has built something that GitHub is now shipping as an enterprise feature. The difference is that Aeon's agent doesn't wait to be told what to fix. It already opened the PR.

---

*Sources: [aaronjmars/aeon](https://github.com/aaronjmars/aeon), [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent), [GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/), [GitHub Agent HQ](https://github.blog/news-insights/company-news/pick-your-agent-use-claude-and-codex-on-agent-hq/), [The State of AI Coding Agents 2026](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a)*
