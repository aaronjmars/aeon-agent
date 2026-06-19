*Push Recap — 2026-06-19*
aaronjmars/aeon + aeon-agent + minitor — MIXED: A2A gateway documented, catalog scrubbed, heartbeat reliability fixed

Shipped to users:
• `ab15246` A2A gateway finally has a README — 116-line quickstart in `apps/a2a-server/README.md` covering `./add-a2a`, all three endpoints, a copy-paste Python submit+poll client, and framework example table (LangChain/AutoGen/CrewAI/OpenAI Agents SDK)
• `2a4c441` heartbeat: `docs/status.md` stops flashing 🔴 DEGRADED on a single recovered failure — now requires `consecutive_failures ≥ 3` or a non-recovered `last_status: failed` to reach DEGRADED; transient blips drop to 🟡 WATCH
• `90e8b5f` skill gallery (`docs/index.md`) updated from stale "50 skills" to 180+ with live slugs; skill-graph pruned from 196 to 176 mapped nodes, 17 dead entries removed
• `d1e07e8` Polymarket Trader by Simmer added to pack registry — 3 skills (intel/markets/trade), simulate-by-default, registry's first onchain position-taking pack (by adlai88)
• `7bd1b8d` clawhunter-skills added — bounty discovery + x402-paid content studio (by Claw Hunter)

Under the hood:
• #503/#504/#505/#506: four-pass dangling-ref sweep clears all 17 skills deleted 2026-06-15 from docs, evals, manifests, and SKILL.md cross-refs; `smoke.sh` canary repointed from deleted `token-report` to live `token-movers`
• minitor ships its first CI build gate — `next build` on every push/PR, catching the exact failure class behind recent regressions (#76/#77)

Shape: 6 user-visible · 3 internal · 2 infra · ~35 bot-filtered · 11 merged PRs
Volume: ~50 files, +393/−208 lines

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-19.md
