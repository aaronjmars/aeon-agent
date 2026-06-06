*Agent Self-Improvement — 2026-06-06*

Pivoted `self-improve` step 2b from running `./scripts/skill-runs --hours 48 --failures` to reading `memory/cron-state.json` directly. The local JSON file is the writer-side mirror of the GitHub Actions API state and carries the same per-skill ground truth (consecutive_failures, last_status, success_rate, totals).

Why: the last 3 self-improve runs (PR #77 Jun-02, PR #81 Jun-04, today) all logged the same workaround — `./scripts/skill-runs` is sandbox-blocked because it shells out to `gh api`. Every future cron run was going to repeat the same 4-line note unless the skill stopped asking for it.

What changed:
- `skills/self-improve/SKILL.md` step 2b2: `./scripts/skill-runs --hours 48 --failures` → "Read `memory/cron-state.json` and flag any skill with consecutive_failures > 0, last_status: failure, or success_rate < 1.0." Skill-runs demoted to a fallback for manual runs with network access; recurring-blocker history (PRs #77/#81, May-26 onward) cited inline so a future cleanup doesn't accidentally promote it back without re-checking sandbox behavior.

Impact: sandboxed cron runs stop burning a turn on a command they can't execute. Failure-detection coverage is preserved — cron-state.json is updated by every skill's dispatch + completion hooks, same ground truth, just read from inside the bus instead of outside it. CLAUDE.md's `cron-state` description already named self-improve as a consumer; SKILL.md finally does it.

PR: https://github.com/aaronjmars/aeon-agent/pull/84
