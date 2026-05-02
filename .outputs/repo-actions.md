*Repo Action Ideas — 2026-05-02*
Generated from analysis of aaronjmars/aeon (260★, 39 forks), aeon-agent (3 open PRs), and minitor (5★, 31 column types). v4 redesign ~2 weeks out, 300-star milestone ~10 days away, 9 open unreviewed PRs across all repos.

1. Operator Value Scorecard (DX, Small)
   Weekly Monday skill synthesizing skill-analytics + heartbeat + tweet-allocator + token-report + repo-pulse into a 3-paragraph plain-language answer to 'was this worth it?' — carried 2 cycles

2. Skill Dependency Freshness Validator (Feature, Small)
   Scans every SKILL.md and aeon.yml consume: edges, checks mtime of each upstream file, and alerts when a chained skill is reading stale data — carried 2 cycles

3. Star Momentum Alert (Growth, Small)
   Reads 14 days of repo-pulse deltas, projects 300-star milestone date, fires a one-time notification when the launch window aligns with Tue–Thu morning — coordinates show-hn-draft dispatch timing

4. Mastodon Column for minitor (Integration, Small)
   Public API, no key required; completes decentralized social trifecta alongside Bluesky (shipped today) + Farcaster — standard 3-file plugin, same pattern as Bluesky column

5. v4 Readiness Checker (DX, Small)
   workflow_dispatch skill that reads current aeon.yml + skills.json and generates a personalized upgrade checklist for 39 forks before v4 ships in ~2 weeks

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-02.md
