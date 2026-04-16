# Repo Action Ideas — 2026-04-16

**Repos:** aaronjmars/aeon (173 stars, 20 forks, 90+ skills, 0 open PRs) | aaronjmars/aeon-agent

**Context:** Record-breaking growth: +16 stars and +3 forks in 24h. Token in second breakout leg (+77% 24h, +228% 7d). Dev.to syndication merged, A2A gateway live, MCP adaptor running. With 90+ skills and distribution infrastructure in place, the next frontier is making the system more self-documenting, extending reach to crypto-native channels, and converting raw growth into observable social moments. No open PRs or issues — clean slate for new work.

---

### 1. Dashboard Live Feed
**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** Skills write json-render specs to `dashboard/outputs/` after every run, but the dashboard has no live update mechanism — operators reload manually or miss runs entirely. A real-time feed turns the dashboard from a static report viewer into an active ops center. This directly increases engagement for operators who have the dashboard open and makes Aeon feel alive rather than a batch system.
**How:**
1. Add a `/api/feed` Server-Sent Events endpoint to the Next.js dashboard that uses `fs.watch` on `dashboard/outputs/` and streams new file events as they land.
2. Wire the dashboard front page to this SSE stream: new skill outputs animate into the top of the feed without a page reload.
3. Add a pulsing "Live" indicator to the dashboard header that activates when a skill run is detected — matching the real-time feel of the token and notification panels already in place.

---

### 2. Farcaster Syndication
**Type:** Integration
**Effort:** Small (hours)
**Impact:** Dev.to reaches the developer audience; Farcaster reaches the crypto-native audience that overlaps most directly with AEON token holders and DeFi users. A post-process hook adds zero overhead to existing skill runs and extends Aeon's distribution footprint into a channel its audience already lives in. Follows the same pattern as `postprocess-devto.sh` — no sandbox changes needed.
**How:**
1. Create `scripts/postprocess-farcaster.sh`: reads article URLs from `.pending-notify/`, formats a Farcaster cast (title + canonical URL + #aeon tag), and POSTs to the Neynar API using `NEYNAR_API_KEY` and `FARCASTER_FID`. Runs after Claude finishes, same as the Dev.to postprocess.
2. Add `NEYNAR_API_KEY` and `FARCASTER_FID` to the Distribution group in `dashboard/app/api/secrets/route.ts`.
3. No changes to `./notify` or any SKILL.md needed — the postprocess hook picks up existing `.pending-notify/` files automatically.

---

### 3. Star Milestone Announcer
**Type:** Growth
**Effort:** Small (hours)
**Impact:** Aeon tracks stars daily but never does anything with milestone crossings. When the count crosses a round number (175, 200, 250, 500...), an automated notification with a milestone message and a summary of what shipped to get there turns a passive metric into a shareable social moment. Operators share their own bot announcing its growth — free word-of-mouth at exactly the right audience (people already watching the repo).
**How:**
1. Add milestone detection to `skills/repo-pulse/SKILL.md`: after fetching `stargazers_count`, check against a milestone list `[175, 200, 250, 300, 500, 1000]`. If today's count crosses a threshold not recorded in `memory/topics/milestones.md`, send a bonus celebratory notification with the milestone count and 2–3 lines on what shipped since the last milestone.
2. Write crossed milestones to `memory/topics/milestones.md` (create if absent) to prevent re-triggering on the next daily run.
3. Notification links back to the repo — a natural share moment for the operator.

---

### 4. Skill Dependency Map
**Type:** Feature / DX
**Effort:** Medium (1 day)
**Impact:** With 90+ skills, `chains:` relationships, and `consume:` dependencies in `aeon.yml`, the architecture is opaque — even to contributors. A self-updating Mermaid diagram in `docs/skill-graph.md` makes the dependency DAG visible, helps new operators understand execution order, and is a compelling visual for repo articles and social posts (the chart itself tells a story about complexity managed). Zero ongoing maintenance cost once the generator skill is live.
**How:**
1. Create `skills/skill-graph/SKILL.md` as `workflow_dispatch`. Parse `aeon.yml` `chains:` and `consume:` fields to extract step-level dependencies. Scan SKILL.md files for inline references to other skill names (e.g. "read skills/X/SKILL.md", "chains consume:") to catch implicit relationships.
2. Output a Mermaid `flowchart LR` diagram grouped by skill category to `docs/skill-graph.md`.
3. PR the file to the repo and add a "Skill Architecture" link to the README under the skills table — makes the graph discoverable without cluttering the top-level docs.

---

### 5. Public Status Page
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** 173 stars and 20 forks means there are operators running Aeon instances that new visitors can't see. A GitHub Pages status page at `aaronjmars.github.io/aeon/status` showing 30-day skill health (green/yellow/red per skill, success rates, last run time) builds credibility — "yes, this runs reliably in production" — and gives operators a URL to share when explaining their setup. All data is already in `memory/logs/`; this is a rendering layer on existing output.
**How:**
1. Extend `update-gallery` (already runs weekly) to also generate `docs/status.md` by parsing the last 30 days of heartbeat log entries. Extract per-skill status mentions, compute 30-day success rates, and format as a table with ✅/⚠️/❌ indicators.
2. Add "Status" to the GitHub Pages gallery navigation alongside the existing Articles and Skills pages.
3. Link from the README under the Instance Fleet section: "Check the live status page for uptime across all skills."
