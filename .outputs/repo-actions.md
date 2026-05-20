*Repo Action Ideas — 2026-05-20*
Generated from analysis of aeon (404⭐, 88 forks), aeon-agent, and minitor. Today closes two more AntFleet H-level findings and opens the community skill packs protocol.

1. Fix AntFleet H3: FORK_DEFAULT_BRANCH undefined in contributor-spotlight (Bug, Small)
   FORK_DEFAULT_BRANCH is fetched into /tmp/contrib-repo.json but never extracted — every contributor-spotlight run silently uses an empty ref, breaking enabled-skill counts for all 88 forks.

2. Community Skill Pack Install CLI — ./install-skill-pack (Feature, Medium)
   Closes the gap between baseddevoloper's Issue #185/PR #187 README mention and an actual one-command install protocol for community-built skill packs.

3. Honor Branch Constraint in skill-update-check — AntFleet H7 (Bug, Small)
   skills.lock branch field is ignored during the upstream SHA fetch — operators with branch-pinned skills see perpetual false update alerts.

4. Deck Share Link — URL-Fragment-Encoded Config (Growth, Small-Medium)
   "Share Deck" button encodes deck config as a base64 URL fragment; recipient opens link → one-click import. Purely client-side. Turns every operator's dashboard into a minitor distribution channel.

5. Starter Deck Templates Gallery (DX, Medium)
   On first launch, show 4 pre-built deck templates (AI Research / Base Ecosystem / Crypto DeFi / Startup Tracker) using the existing DeckExport v1 shape — eliminates the blank-slate barrier for new operators.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-20.md
