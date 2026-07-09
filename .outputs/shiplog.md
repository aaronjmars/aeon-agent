aeon + miroshark shiplog ⭐ jul 6 → jul 9

shipped ~95 PRs across repos + 30 commits. the bytes:

- secretcurl: ./secretcurl replaces the entire prefetch/postprocess pattern — skills now do auth'd API calls in-run. XAI, coingecko, alchemy, etherscan, github reads. prefetch-xai.sh retired. the sandbox "blocks env var expansion" myth is dead, and the docs say so now.
- attestation: every skill execution now signs a Sigstore manifest. "your agent ran this" is cryptographically verifiable against the Rekor log. public traces + proof.
- headless CLI: `aeon` CLI ships, non-interactive mode. scripts and CI can drive it without the browser.
- langfuse: optional per-run tracing — every claude code tool call grouped in one Langfuse session. first-class observability with no per-skill work.
- website wallet: buy $aeon directly from the site. privy auth (github/X/google/wallet), swap widget in the hero, 0x affiliate fee (1%), ERC-8021 attribution. first miroshark buyback done — 100% of x402 revenue.
- dashboard copy pass: Team→Skills, Hire→Add, Assignment brief→Skill settings. the dashboard speaks english now.
- security: chain-input injection (GHSA-h9v2/GHSA-cqvj) + Discord/Slack author allowlist nudge (GHSA-252cF5) — both fixed, both fork-safety relevant.
- scheduler: missed-skill catch-up (exact-slot debt model), decoupled from messages, Issues-as-state backend live.
- pack restructure: 59 skills, 6 packs. category == pack.

traction:
- aeon 571 ⭐ (+3 this window)
- miroshark 1357 ⭐
- @Base_Insights (22k): aeon in "Leading" tier of July Base Ecosystem Tier List
- tx-explain skill: 52 likes, 2590 views on @aeonframework
- sparkleware using aeon skill packs as holographic registry — now tradeable on Robinhood
- miroshark farcaster mini-app dropped

the harness is the model. ⭐🦈

https://github.com/aaronjmars/aeon-agent/blob/main/articles/shiplog-2026-07-09.md
