*Push Recap — 2026-05-14*
3 repos — 15 substantive commits, single primary author

*The switches finally flipped*: aeon-agent flipped 6 long-stuck announcement/visibility skills `enabled:false → true` (PR #45) — star-milestone (daily), star-momentum-alert (Tue/Wed/Thu HN window), thread-formatter (event-scored, silent on quiet days), operator-scorecard (weekly), ai-framework-watch (Mon competitive intel), contributor-spotlight. PR #46 walked the spotlight back 2 min later because fork-cohort is still off — operator reading their own dependency graph in real time. Closes the 3-day "switch is still off" thread MEMORY has been tracking since the 308⭐ ATH.

*Bulk skill catchup + automation rail*: aeon-agent PR #44 bulk-syncs 22 SKILL.md files from upstream (skills.json 62 → 85, all `enabled:false`). Companion aeon PR #170 adds a Monday 09:00 UTC workflow to upstream itself — every fork inherits a recurring "sync from upstream" PR opener. Converts manual same-day-after backports into automated weekly rail. Co-authored by traewang.

*Minitor registry trifecta completes*: PyPI #36 (42nd column) + crates.io #38 (43rd column) land same day, finishing npm + pypi + crates triple from this week. News & web cluster 8 → 10. Bonus substack #37 fix accepts pluralistic.net / astralcodexten.com / noahpinion.blog custom domains — silently broken before.

Key changes:
- aeon-agent now has its first daily announcement channel (star-milestone @ 15:15 UTC) firing tomorrow on 312⭐
- aeon dashboard auth + secrets routes (PR #169) work in multi-remote setups for the first time — README's two-repo strategy was bricking gh CLI since April
- aeon dashboard TopBar wired up gateway prop (PR #171) — typecheck was silently failing since April Bankr Gateway commit

Stats: ~75 files, +7,500/-90 lines across 15 substantive commits (excluding cron/scheduler auto-commits)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-14.md
