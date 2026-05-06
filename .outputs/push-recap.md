*Push Recap — 2026-05-06*
6 substantive commits across 3 watched repos by aaronjmars (yesterday's three feature PRs cleared review at 01:02–01:23 UTC; three early-morning forward-fixes on aeon-agent followed at 01:02–03:35 UTC).

Show HN dispatch loop on aeon: star-momentum-alert (PR #159) projects each repo's next milestone-crossing date by linear extrapolation off the 7-day rolling star delta and fires only when the projection lands 7–14 days out on a Tue/Wed/Thu — the same launch window already baked into show-hn-draft's checklist. Closes the lead-time gap between "the launch post is pre-written" (PR #151, May 1) and "it's time to dispatch it." Plus PR #158 hardens dashboard/app/api/skills/[name]/run/route.ts by swapping execSync for execFileSync (defense-in-depth, mirrors PR #150).

Reliability stack on aeon-agent: skill-freshness backport (PR #30) lands the silent-staleness watchdog from yesterday's aeon PR #157 verbatim — daily audit of explicit chains: consume: edges + implicit articles/.outputs/topics/state references against per-class freshness thresholds, fingerprint-deduped over 7d. Plus PR #29 forward-fixes the operator-scorecard backport from May 4: paragraph 1 reads articles/skill-analytics-*.md, but skill-analytics isn't enabled on this fork — every weekly run would have demoted the verdict to WATCH. PR #29 carves out a heartbeat-only fallback branch (Branch B) that computes the verdict from heartbeat counts alone, since heartbeat is itself a fleet-health audit. Plus PR #31 extends token-report with daily-volume trend (24h/7d/30d), surfaced in both article + notification.

Polymarket column on minitor (PR #28): 35th column type. Keyless Gamma API, four modes (trending/newest/ending-soon/tag); 24h-volume sort canonical because newest markets are mostly zero-volume crypto bets. Five Polymarket-specific quirks handled in the integration layer (JSON-string outcome arrays, leading-outcome-first binary sort, price clamping, past-dated drop-defense, event-vs-market permalink fallback) plus a smoke-test fix in the same PR (volume24hr field replaces always-null volume24hrNum). Closes the prediction-market gap in the on-chain cluster.

Key changes:
- skills/star-momentum-alert/SKILL.md (+280) — daily 10:10 UTC sonnet skill, dual-gate alert, per-(repo,milestone) 7-day re-emit dedup
- skills/skill-freshness/SKILL.md (+286) — daily 08:00 UTC fork-portable, per-class thresholds derived from producer cron, fingerprint-deduped
- lib/integrations/polymarket.ts (+256) — five quirks of the Polymarket Gamma API neutralized in a single integration

Stats: 17 files changed, +1,202/-27 across 6 commits + ~37 routine cron auto-commits on aeon-agent main.
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-06.md
