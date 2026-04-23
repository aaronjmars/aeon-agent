*Push Recap — 2026-04-23*
aeon — 1 meaningful commit by @aaronjmars (squash-merged from aeonframework autonomous PR). aeon-agent — 0 meaningful commits (27 autonomous cron/scheduler auto-commits excluded).

Fork-intelligence triangle complete: PR #140 lands fork-skill-digest — a Sunday 18:30 UTC skill that reads every active fork's aeon.yml, compares vs upstream, and bins divergence into 5 buckets (flip-enable / flip-disable / model-consensus / var-hotspot / emerging-watchlist). Closes Apr-22 repo-actions idea #2 — second of two highest-priority unbuilts.

Peer-learning layer now exists. skill-leaderboard ranks what's popular; fork-fleet surfaces per-fork work; fork-skill-digest is the first skill that answers "where does the fleet consistently disagree with upstream defaults" — converts 33 forks' implicit ballot on each default into a weekly actionable signal.

Significance-gate pattern shipped greenfield. Constraint block codifies "silent runs are correct, not failures" — notification fires only on N_CONFIGURED ≥ 2 AND ≥ 1 signal bucket non-empty. First skill to land this pattern without retrofit; pre-evolution push-recap (still running here) and weekly-shiplog are next candidates.

Key changes:
- New skills/fork-skill-digest/SKILL.md (+357) — 14-step spec with 5-bucket divergence taxonomy, week-over-week state persisted to memory/topics/fork-skill-digest-state.json, template-fork exclusion, six-priority verdict line picker, 5-state exit taxonomy.
- aeon.yml (+1) — slot after skill-leaderboard (17:00) and fork-contributor-leaderboard (17:30) to cluster all three fork-intelligence skills in one Sunday window.
- State-file-as-contract pattern extended: fork-skill-digest-state.json is authoritative (article text is derivative), mirrors .admanage-state/campaigns.json from Apr-22's paid-ads PR.

Stats: 3 files changed, +359/-1 lines.
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-23.md
