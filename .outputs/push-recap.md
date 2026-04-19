*Push Recap — 2026-04-19*
aeon + aeon-agent — 7 meaningful commits by @aaronjmars + 1 PR merge (aeonframework)

Notification & scheduler dedup: Aaron shipped two late-night fixes to both repos (~23:40 UTC Apr 18) that close duplicate-notification paths. Scheduler catch-up no longer fires if the skill already ran at the earlier tick; ./notify dedups by SHA256 hash within a run and suppresses short test/trace probes.

Skip-path notifications: aeon-agent fetch-tweets and tweet-allocator now notify on empty days instead of exiting silently — operators can distinguish "nothing to report" from "silent crash."

Feature merges (pre-window edge): star-milestone skill #39 and Farcaster syndication #40 landed on aeon main at 16:42–16:43 UTC. PR #15 (repo-pulse same-day dedup) merged to aeon-agent main at 16:47.

Key changes:
- aeon .github/workflows/aeon.yml +54/-3: notify dedup via hash file + trace-probe suppression (<120-char test/trace/ping/debug messages dropped)
- aeon/aeon-agent messages.yml +21/-7: scheduler catch-up gate — LAST_DISPATCH_EPOCH < SCHED_EPOCH required to fire
- aeon-agent skills/fetch-tweets + skills/tweet-allocator: skip-path "stop silently" replaced with one-line ./notify calls

Stats: 8 files changed across 7 commits, +358/-79 lines (excluding 43 chore auto-commits)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-19.md
