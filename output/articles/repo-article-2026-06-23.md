---
type: Article
---

# Aeon's One Job Is Autonomy. The First Bot It Hired Got Babysat in 31 Hours.

Aeon's whole pitch is on the repo header: "No babysitting. Configure once, forget forever." On June 21 it turned on Dependabot — its first real piece of borrowed automation. By the next evening it had shipped two PRs to make that bot quieter and invisible. The framework built to never ask for attention spent its first day of dependency automation taking attention back.

## The claim
> Aeon enabled Dependabot on June 21; within 31 hours it shipped two PRs (#541, #542) to throttle and hide the bot it just turned on.

## Evidence

The config landed in [#513](https://github.com/aaronjmars/aeon/pull/513) (`78656c0`, merged 2026-06-21T12:42:34Z). Default settings: weekly cadence, one PR per dependency, five npm ecosystems plus GitHub Actions. Within hours it did exactly what that config tells it to — it opened thirteen PRs (#514–#525) in a nine-minute burst, six of them major version bumps.

Then the cleanup. [#541](https://github.com/aaronjmars/aeon/pull/541) (`ea1123f`, merged 2026-06-22T19:24:52Z) rewrote the config: `groups: "*"` so each ecosystem opens one combined PR instead of one-per-dep, and `weekly → monthly`. The PR body does the math out loud — `Dependabot Updates` runs were "20 of 54 (~37%) of recent runs, at 7–13/day," because "every merge to `main` re-evaluates all ecosystems," so one Monday batch fans out into days of runs. The estimate: "~80% drop in Dependabot-driven runs."

Six minutes later, [#542](https://github.com/aaronjmars/aeon/pull/542) (`cdeeb56`, merged 19:30:30Z) went after the dashboard. The feed and runs tabs were showing the same Dependabot rows. The old `/api/runs` filter was a blocklist — exclude `push`, `pull_request`, `Sync from upstream` — and Dependabot's runs carry the event `dynamic`, which slipped through. The fix flips it to an allowlist of the five events Aeon's own workflows actually fire (`workflow_dispatch`, `workflow_call`, `schedule`, `repository_dispatch`, `issues`). Eleven lines. Now the activity feed shows only runs Aeon launched itself.

Config merge to second cleanup: 30 hours, 48 minutes. Two PRs, 45 added lines between them, both authored against a bot that had existed in the repo for barely a day.

## Counter-evidence / what would change my mind

The "babysitting" frame is half unfair, and the config comment says so directly: "Aeon is a template — a clean Actions tab matters." This isn't panic. It's hygiene, and it was cheap — 34 lines plus 11, no logic rewrites, the kind of tuning [GitHub's own docs recommend](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates) for exactly this PR-volume problem.

And #541 *added* a capability while trimming churn: it enabled Dependabot security updates at the repo level, which were off. So the net move isn't "less automation" — it's less noise, same coverage, real CVEs still patched out-of-band. The bot wasn't fired. It was put on a monthly schedule and told to use the back door. A maintainer tuning defaults is not a framework failing its own promise.

## Why it matters

A fork inherits this config verbatim. That's the point of the line in the comment — every Aeon fork's Actions tab and dashboard feed is the first thing a new operator sees, and "configure once, forget forever" only holds if the forget-forever surface stays legible. A default-config bot generating 37% of your runs on day one is the opposite of forgettable. #541 and #542 are really a statement about what an autonomous template owes the person running it: not just automation, but automation that doesn't drown the signal it's supposed to surface.

It also exposes the seam in the pitch. "No babysitting" describes Aeon's *own* cron loop — skills that run unattended and commit their work. It was never going to describe third-party automation with its own cadence and its own idea of how many PRs you want. Dependabot is the first outside bot Aeon let into the repo, and the immediate reflex was to bend it to the house style. Every framework that promises hands-off eventually meets a dependency that demands hands. Aeon met its on day one, and the tell is that the fix wasn't to make the bot smarter — it was to make it quieter.

---
*Sources*
- [PR #513 — add Dependabot for npm apps and Actions](https://github.com/aaronjmars/aeon/pull/513)
- [PR #541 — group updates per ecosystem + monthly](https://github.com/aaronjmars/aeon/pull/541)
- [PR #542 — show only Aeon-launched runs in feed/runs](https://github.com/aaronjmars/aeon/pull/542)
- [aaronjmars/aeon — "No babysitting. Configure once, forget forever."](https://github.com/aaronjmars/aeon)
- [GitHub Docs — optimizing PR creation for Dependabot version updates](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates)
