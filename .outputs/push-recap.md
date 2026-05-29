*Push Recap — 2026-05-29*
16 substantive commits across aeon / aeon-agent / minitor from 5 authors (~+5,629 / -444 lines).

*Dashboard editorial overhaul (aeon, 3 PRs):* The dashboard is now visually the same product as the marketing site — dark canvas, coral #d24b40, Dela Gothic display, Inter body, Space Mono labels. Editorial heroes with dithered red halftone, numbered sections ("01 / Departments"), and a new Animated.tsx motion file porting Scramble / Flip odometer / VelocityMarquee from aeon.fun. TopBar buttons normalized to 32px uniform height; AUTH no longer towers over PULL / PUSH.

*Skill catalog +11 in one day (aeon):* HoundFlow contributed 6 keyless Base onchain investigators (rug-scan, contract-audit, wallet-profile, deployer-trace, tx-explain, holder-concentration — Etherscan v2 chainid=8453, optional key only raises rate limit). 5 generic ops skills landed too: spend-monitor (daily $200 watchdog), follow-up-patrol, narrative-convergence, mcp-pulse, generalized fleet-scorecard (no more hardcoded repos). Plus fork-health-score — Monday-morning per-fork ACTIVE/WARM/STALE/QUIET tier with hard "≥2 enabled skills" floor so placeholder forks can't claim ACTIVE.

*Skill-pack manifest matures (aeon, AntFleet PRs #267 + #268):* Two additive fields close the trust + install-UX gap — capabilities[] with locked 6-value taxonomy (read_only / external_api / writes_external_host / onchain_writes / agent_messaging / sends_notifications) and secrets_required / secrets_optional. install-skill-pack now surfaces missing secrets as loud warnings (not gates) and `--list --no-secrets` filters discovery.

*aeon-agent backport chain → 16 consecutive days:* pr-skill-triage backport (PR #68) lands as the structured receipt for inbound skill PRs (security scan + secrets enumeration + cron slot check + quality signals → one PR comment, dedup on head SHA). push-recap also fixed itself yesterday (PR #67) — today's run no longer needs the operator to improvise the cutoff date by hand.

Key changes:
- skills/fork-health-score/SKILL.md (+366) — Monday fleet synthesis with WoW deltas on percentage points, never raw counts
- dashboard/components/ui/Animated.tsx (+271, new) — Scramble / Flip / VelocityMarquee, single shared cubic-bezier motion ease
- minitor PR #53: per-column tab groups + tab bar above the deck grid (migration 0006, +649/-44, 10 files) — untagged columns ride along with every named tab so half-grouped decks stay usable

Stats: ~64 files changed, +5,629/-444 across 16 substantive commits (~40 cron auto-commits in aeon-agent excluded as noise)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-29.md
