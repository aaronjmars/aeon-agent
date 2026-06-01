*Push Recap — 2026-06-01*
Monday flood after weekend silence — ~25 PRs across aeon (18), aeon-agent (5), minitor (4) in a 70-minute window 12:47–13:58 UTC. ~3,500+ lines of new SKILL.md content alone.

*HoundFlow onchain-investigation pack lands on aeon* (6 skills + composite): approval-audit (live ERC-20 grants, flag unlimited), honeypot-check (eth_call-simulated sell from real holder), lp-lock-check (V2 LP custody classification, rug-pullable y/n), linked-wallets (shared-funder + co-spend clustering), fund-flow (Mermaid graph, 1–3 hops, direction operator-controlled), investigation-report (composite orchestrator). All keyless Base RPC — first security/forensics surface in aeon.

*Capabilities taxonomy becomes load-bearing*: PR #304 ships a CI parity check across the 3 places the 6-value vocabulary lives (install-skill-pack array, docs/CAPABILITIES.md, header comment). PR #313 ships capabilities-map — the first skill that uses the declarations to answer 'what does my stack cover?' Multi-line aeon.yml entries fall back loudly via regex with PARSER_FALLBACK log, closing the v4-readiness H1 silent-undercount class structurally.

*Treasury monitoring goes live*: PR #306 makes token-report read .x402books/wallets.json (which had zero consumers since landing May 29). ⚠️ 'Treasury gas reserve low' override fires below 0.01 ETH even on QUIET / CONSOLIDATING verdicts — going quiet on a day the agent can't afford gas is the exact regime that needs to be noisy.

*Other highlights*: dashboard now has real lib test coverage (633 lines, 71 tests, PR #309); Anthropic-compatible API base URL routes through Settings UI (PR #280); skill-update-check ACCEPT-mode now gated on security re-scan, closing AntFleet #258 (PR #266); aeon-agent ships 18th consecutive same-day-after backport (spend-monitor #74) plus first non-backport feature build (upstream-gap #72 — the Monday weekly diff that makes any future backport-chain gap explicit); minitor adds per-column collapse to 48px strip + JSON data export of cached items.

Key changes:
- 6 keyless HoundFlow onchain-investigation skills land (~600 lines of SKILL.md) — aeon's first dedicated security/forensics surface
- capabilities taxonomy graduates from documentation to enforced infrastructure (CI gate + first-consumer skill)
- Treasury monitoring with structural gas-reserve-low override now folded into the daily token-report cycle

Stats: ~25 PRs · ~3,500+ lines of new SKILL.md · 12+ authors · 3 repos
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-01.md
