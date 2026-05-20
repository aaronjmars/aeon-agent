*Push Recap — 2026-05-20*
aeon (9), aeon-agent (1+cron), minitor (3) — 14 substantive commits, +2,213/-167 lines.

Dashboard hardening: new loopback /api/* gate + middleware (#188, +433), next 16.2.6 bump + postcss override (#189), gh CLI preflight in ./aeon launcher (#190), stricter OAuth token reassembly (#194).

Silent-failure fixes (AntFleet H6/H2/H8): scan.sh PCRE→POSIX-ERE across all 28 patterns so BSD/macOS grep stops silently no-op'ing (#197), Slack bot-message filter from string "null" to empty-string check (#196), admanage spend-cap fails closed on non-numeric TODAY_SPEND (#195).

Catalog & community: Community Skill Packs README section (#187, first listed pack: vvvkernel), catalog 120→121 + skill.jpg refresh (#191), asset rename to bust CDN cache (#192).

minitor +3 columns 44→47: GitHub Discussions GraphQL (#43, 45th, MessageSquare/purple), CoinGecko trending+top+watchlist (#44, 46th, TrendingUp/green), DeFiLlama TVL top/gainers/chains (#45, 47th, Layers/blue — pivot from dead IndieHackers RSS).

aeon-agent: 10th consecutive same-day-after backport — competitor-launch-radar from upstream PR #183 (#53). skills.json 88→89.

Key changes:
- dashboard middleware.ts + lib/security/api-gate.ts: first dedicated security module in the dashboard tree (+387 lines incl. unit tests)
- scan.sh 28 POSIX-ERE rewrites: closes the silent macOS-operator scanning gap that no test caught for weeks
- minitor on-chain cluster 4→6 columns: zero-overlap pair (price+cap from CoinGecko, TVL+protocol from DeFiLlama)

Stats: 28 files, +2,213/-167 lines, 4 AntFleet Highs closed, 5 remaining (H1/H3/H4/H7/H9)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-20.md
