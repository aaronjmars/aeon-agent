*Repo Action Ideas — 2026-05-18*
Generated from analysis of aeon (370⭐, 78 forks), aeon-agent, and minitor. Fresh pipeline — May-16 ideas fully consumed.

1. Backport fork-skill-gap to aeon-agent (Feature, Small)
   Verbatim backport of aeon PR #176 — per-fork upstream-skill-adoption gap report; continues daily same-day-after cadence.

2. Fix scan.sh empty-array crash on macOS Bash 3.2 (Bug, Small)
   Issue #182: add ${#warnings[@]} length guard so clean scans don't false-block skill installs; unblocks macOS add-skill for 78+ fork operators.

3. Extend gateway.provider for custom API base URLs (Feature, Medium)
   Issue #181: add optional baseUrl + authHeader fields to gateway.provider — unlocks MiniMax (APAC), Together.ai, and other Anthropic-compatible providers blocked by local model-name validation.

4. CoinGecko trending + price column for minitor (Integration, Small)
   46th column type; keyless /search/trending + /coins/markets; crypto-native operator base has no price signal today — fills the obvious gap.

5. IndieHackers RSS column for minitor (Integration, Small)
   47th column type; keyless RSS feed; completes the startup-launch trifecta (ProductHunt + HN + IH) for operators monitoring product launches.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-18.md
