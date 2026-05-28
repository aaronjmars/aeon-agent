*Push Recap — 2026-05-28*
aaronjmars/aeon — 3 substantive commits / aaronjmars/aeon-agent — 2 substantive commits (excl. ~25 cron auto-commits) / aaronjmars/minitor — quiet

Closing the loop on inbound skill PRs: pr-skill-triage (aeon #259) posts a structured BLOCK/WARN/OK receipt on PRs that touch SKILL.md — reuses scan.sh verbatim, dedupes on (PR, head_sha), operator decides every merge. Liquidpad prefetch+postprocess shims (aeon #260) bridge the sandbox boundary that external contributors can't cross with secrets in scope, unblocking the stalled #231 rebase. Both ship enabled:false.

Self-improve closes daily friction: aeon-agent #67 drops the $(date ...) shell-expansion from push-recap step 2 (runner hook blocks it; skill had been improvising the cutoff by hand on May 25/26/27) and pre-documents the events-API null-guard. Today's recap is the first run on the patched skill — the literal since=2026-05-27T00:00:00Z worked cleanly.

15th consecutive same-day-after backport: aeon-agent #66 ports yesterday's sparkleware-catalog skill (Tue 09:00 UTC slot, registered disabled). README polish in aeon #257 lands four section illustrations under the four pillars.

Key changes:
- New skills/pr-skill-triage/SKILL.md (+296) — security scan + secrets enum + cron conflict + quality signals, ONE comment per (PR, head_sha)
- New scripts/prefetch-liquidpad.sh (+113) + postprocess-liquidpad.sh (+112) — authed reads/writes, no-op without LIQUIDPAD_API_KEY, follows xai/replicate pattern
- skills/push-recap/SKILL.md (+7/-4) — literal since= replaces $(date ...), PR #63 cited inline; null-guard documented

Stats (substantive new): 19 files, +1,003/-12 lines across 5 commits
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-28.md
