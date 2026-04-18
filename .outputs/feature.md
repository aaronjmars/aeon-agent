*Feature Built — 2026-04-18*

Star Milestone Announcer
Aeon now celebrates its own growth. A new skill watches every repo in memory/watched-repos.md and fires a bonus notification whenever the star count crosses a milestone threshold — 25, 50, 100, 150, 200, 250, 500, 1000, and so on up to 100K. Each announcement comes with a short highlight reel of what shipped since the previous milestone, so the message tells a story instead of just flashing a number.

Why this matters:
Aeon tracks stars daily through repo-pulse but never does anything with the round-number crossings. The repo sat at ~189 stars today, so the 200 milestone is imminent and would have slipped past silently. This was idea #3 in repo-actions 2026-04-16 — turn a passive metric into a shareable social moment at the exact audience already watching the repo. Operators get a natural reason to share their own bot announcing its growth.

What was built:
- skills/star-milestone/SKILL.md: New skill. Reads watched-repos, loads state from memory/topics/milestones.md, fetches current stargazers_count via gh api, finds the highest threshold crossed, builds a 3–5 item highlight reel from the last 14 days of memory/logs/, and sends a detailed celebratory notification. Includes bootstrap logic — on the first run against an established repo it records the already-passed milestone silently to avoid retroactive spam.
- aeon.yml: Scheduled daily at 15:15 UTC, 15 minutes after repo-pulse so the star count is already fresh.
- generate-skills-json: Added star-milestone to the dev category so the manifest regenerator classifies it correctly on its next run.
- README.md + skills.json: Added to the Dev & Code row, bumped category count 28 → 29 and total skills 91 → 92 so marketplace discovery picks it up immediately.

How it works:
The skill compares the current stargazers_count against an ordered threshold list and finds the highest M where M <= count. If M is already recorded in memory/topics/milestones.md, nothing happens. If this is the first run for the repo, it bootstraps silently. Otherwise it is a fresh crossing: the skill walks the last 14 days of log files, pulls 3–5 concrete highlights from Push Recap, Feature Built, and Repo Article sections (falling back to recent commit subjects if logs are empty), and fires a formatted notification through ./notify so it fans out to Telegram, Discord, Slack, and email. Multi-milestone jumps (180 → 260 in one run after the skill was disabled) announce only the highest and silently record the intermediates as historical anchors.

What's next:
The 200-star crossing will be the first live test in a few days. Natural follow-ups: a matching fork-milestone skill for fork thresholds, or tying milestone notifications into write-tweet so each crossing auto-generates a draft announcement post.

PR: https://github.com/aaronjmars/aeon/pull/39
