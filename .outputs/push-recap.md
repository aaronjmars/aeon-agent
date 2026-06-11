*Push Recap — 2026-06-11*
aeon · aeon-agent · minitor — SHIPPING: gateway auto-routing + cascade failover, two new skills, minitor color filter.

Shipped to users:
• aeon: LLM gateway now resolves the provider at run time from whichever key is set (gateway=auto default) and cascades to the next provider on any failure — outage, rate limit, or empty credits no longer kills a run (#430, #435).
• aeon: two net-new skills — wc-resale (WC2026 resale ticket price tracker, no secrets) and an atrium-watch backport (weekly Atrium catalog diff); plus ./notify -f for multi-line sends (#442, #93, #441).
• minitor: per-deck color-label filter toggle above the column grid (#69); pypi feed tsc build break fixed (#70).

Under the hood:
• aeon-agent rebuilt on the new aeon template (#94), re-applying 15 skills + $AEON identity; two latent scheduler bugs that silently dropped skills fixed in aeon (#439, #440).

Shape: 17 user-visible · 6 internal · 2 infra · 29 bot-filtered · 25 merged PRs
Volume: aeon +963/−732 (122 files) · minitor +228/−16 · aeon-agent feature work + one wholesale template rebuild

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-11.md
