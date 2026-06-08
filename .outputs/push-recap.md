*Push Recap — 2026-06-08*
14 substantive merges across aeon, aeon-agent, minitor (plus ~30 cron auto-commits). Centre of gravity: a 98-minute window on aeon between 11:11 and 12:49 UTC.

*Three new framework skills on aeon*: `ecosystem-links` (PR #351) — weekly Monday URL-health audit of ECOSYSTEM.md with two-strike INCONCLUSIVE rule so sandbox-blocked outbounds can't false-flag DEAD; closes the three-skill ecosystem loop (pulse + entrants + links). `vigil-revoke` (PR #354) — Bankr-gated approval revoker with `wallet:spender:token` triplet allowlist, pre-flight wallet check, NOOP short-circuit on already-zero, chain-confirmed success; closes the detection→revoke loop wallet-risk-weekly opened Jun-04. `star-milestone auto-dispatch` (PR #358) — first cross-skill routing wire on the framework, seeded `aeon:500 → show-hn-draft` so the launch draft fires on its own when aeon crosses 500★ (~Jun-11 at v7=3.6/day; currently 492).

*Three external ecosystem entries on aeon*: Mneme (agent-native database with pgvector + graph + Base streams + async LLM reflection, 8-skill pack), Careful Finance pack, SIGNA pack update from 10→20 skills now shipping bounded spend mandates + x402 receipts.

*aeon-agent*: shell-substitution anti-pattern chain finally closed across last 2 sites (PR #83 — chain ran 6 PRs over 13 days); self-improve now reads cron-state.json instead of sandbox-blocked skill-runs (PR #84); 23rd consecutive same-day-after backport — skill-of-the-day from upstream PR #341 (PR #85, first backport in chain where notify wiring needed no translation); repo-pulse now enriches new stargazers/forkers with `gh api users/$LOGIN` profile data + low-signal fake-star flag (PR #88, lands first run tomorrow).

*minitor*: 8th rung on per-column UX axis — width control narrow/normal/wide as view-state (PR #63); per-deck color labels (DB-backed, round-trips through export/import, deck-axis analog of column color PR #61) (PR #62); DeFiLlama gainers gets a default $1M TVL floor so $500 microcaps doubling overnight don't outrank $1B protocols (PR #64).

Key changes:
- aeon PR #358 introduces cross-skill routing for the first time — `memory/topics/milestone-dispatch.json` rule map (+9 lines) + new step 8 in star-milestone (+46/-5) wires arbitrary (repo, threshold) → skill pairings via `gh workflow run`
- aeon PR #354 vigil-revoke (+290 lines) is the security stack's first write-side skill — detection (wallet-risk-weekly + approval-audit) finally has an autonomous remedy path
- minitor PR #62 per-deck color labels (+708 lines, 11 files, drizzle migration 0009) reuses normalizeColumnColor verbatim from PR #61 so column-level + deck-level surfaces stay coherent

Stats: ~51 files changed, +2144/-35 across 14 substantive PRs (plus ~30 cron auto-commits)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-08.md
