*Repo Action Ideas — 2026-05-24*
Generated from analysis of aaronjmars/aeon (437⭐, 112 forks), aaronjmars/aeon-agent, and aaronjmars/minitor. Two big events shaped today: ECOSYSTEM.md merged listing 40 projects building on Aeon, and PR #219 pushed the skill catalog to 155 total.

1. ecosystem-pulse skill (Feature, Small)
   Weekly skill that monitors the 40 projects in ECOSYSTEM.md for activity — the first skill to ask "are the things built on Aeon actually shipping?"

2. fleet-skill-adoption leaderboard (Feature, Medium)
   Reads ACTIVE/POWER forks, counts per-slug enabled:true occurrences, surfaces top/bottom-15 by fleet adoption % — operators can see which of the 155 skills the community has actually validated

3. config-validator backport from PR #219 (DX, Small)
   Ports the config-validator skill from the 34-skill batch to aeon-agent — validates aeon.yml structure (cron syntax, slug paths, required frontmatter) before operators commit bad configs

4. Bluesky AT Protocol column (Integration, Medium)
   48th column type for minitor — keyless bsky.social AppView API, user + search modes, completes the social trifecta (X + Reddit + Bluesky)

5. Column-level webhook notifications (Feature, Medium)
   When alertKeywords match incoming items, POST to a per-column HTTPS webhook — turns minitor from a passive dashboard into an active alerting system

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-24.md
