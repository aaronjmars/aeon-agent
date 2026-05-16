# Repo Action Ideas — 2026-05-16

**Repos analyzed:** aaronjmars/aeon (344⭐, 56 forks, 119 skills), aaronjmars/aeon-agent (9⭐, 86 skills), aaronjmars/minitor (9⭐, 43 column types)

**Pipeline state:** May-14 ideas fully consumed (all 5 built May-15/16). This run seeds the May-17+ feature pipeline with a fresh batch.

---

### 1. Product Hunt Column (minitor)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** Minitor is "a dashboard for the internet" but has no visibility into the world's #1 product launch platform. The operator is actively preparing a PH launch (PR #175). A PH column means watching your own launch day rank in real time inside the dashboard — and monitoring competitor/ecosystem launches every day. PH RSS (`producthunt.com/feed`) is keyless, same pattern as the existing `substack` and `rss` plugins.
**How:**
1. Create `lib/integrations/producthunt.ts` — fetches `producthunt.com/feed` (RSS), parses items for title/link/description/pubDate, extracts vote counts and tagline from description text
2. 3-file plugin (`plugin.ts`, `server.ts`, `client.tsx`) with modes: `today` (24h window), `trending` (past 7d ranked), `tech` (today filtered to tech/dev tools). Accent: `#DA552F` PH orange, `Rocket` icon
3. Wire 3 registry edits + README (News & web cluster 9 → 10, total count 43 → 44)

---

### 2. GitHub Discussions Column (minitor)
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Completes the GitHub monitoring cluster — stars, forks, PRs, issues, releases, search, actions, backlinks, and trending all have dedicated columns, but Discussions (the async Q&A/community layer GitHub is actively pushing as the default) is missing. Repos transitioning from Issues-only to Discussions-first lose visibility in minitor. GitHub Discussions API is GraphQL-only; GITHUB_TOKEN covers both public and private repos at 5,000 req/hr.
**How:**
1. Create `lib/integrations/github-discussions.ts` — queries GitHub GraphQL endpoint with `repository { discussions(first: N, orderBy: {field: CREATED_AT}) { ... } }`, returns `number`, `title`, `url`, `author.login`, `createdAt`, `upvoteCount`, `category.name`, `isAnswered`, `comments.totalCount`
2. 3-file plugin with modes: `recent` (newest by date), `unanswered` (open without accepted answer), `top` (most upvoted in 7d). Map `isAnswered` to a "resolved" badge. Accent: `#7C3AED` purple (distinct from all existing GitHub column colors), `MessageSquare` icon
3. Wire 3 registry edits + README (GitHub cluster 9 → 10, count 44 → 45)

---

### 3. Skill Health Triad Backport (aeon-agent)
**Type:** DX improvement
**Effort:** Medium (1-2 days)
**Impact:** aeon-agent runs 86 skills with zero autonomous self-monitoring. Upstream aeon has `skill-health`, `skill-evals`, and `skill-repair` — the complete self-healing loop: health skill files structured issues to `memory/issues/` → repair skill reads them and applies fixes → evals skill runs regression tests. Without this triad, the operator depends on heartbeat to notice degradation manually. With it, the agent detects, classifies, and patches its own skill failures overnight. Continues the same-day-after backport pattern (operator-scorecard, skill-freshness, fork-cohort, thread-formatter, v4-readiness all already backported).
**How:**
1. Copy `skills/skill-health/SKILL.md`, `skills/skill-evals/SKILL.md`, `skills/skill-repair/SKILL.md` verbatim from upstream aeon — same pattern as all prior backports
2. Register all three in `aeon.yml`: skill-health (daily 20:00 UTC), skill-evals (weekly Sunday 22:00 UTC), skill-repair (daily 21:00 UTC, after skill-health). Note: skill-repair requires workflows-scope PAT — already active since May-6 rotation
3. Update `skills.json` 86 → 89 (+3 entries). Verify `memory/issues/INDEX.md` exists (CLAUDE.md memory structure already defines it — just needs the file seeded with empty tables)

---

### 4. Fork First-Run Alert (aeon)
**Type:** Community
**Effort:** Small (hours)
**Impact:** Fork-cohort tracks LEVELED_UP and NEW_ACTIVE week-over-week deltas but only fires weekly. A new fork completing its very first skill run is the highest-signal community event — someone deployed, configured secrets, and actually ran Aeon. This skill reads fork-cohort's cached state daily, detects new ACTIVE forks not yet in its seen-list, and sends a named real-time alert ("Fork `speend/aeon` just ran its first skill"). Two-sided value: operator knows who just activated, new operator feels seen. Closes the gap between fork-cohort's weekly cadence and the actual moment of activation.
**How:**
1. New `skills/fork-first-run-alert/SKILL.md` — reads `memory/topics/fork-cohort-state.json`, diffs ACTIVE forks vs `memory/topics/fork-first-run-state.json` (persistent seen-list); for each new entry fetches fork's most recent run metadata via `gh api repos/{fork}/actions/runs?per_page=1`
2. Sends named per-fork alert (fork slug, first skill name if detectable, link to fork); deduplicates via seen-list; batch-notify if >3 new activators in 24h to avoid notification spam. 5-status exit taxonomy: OK / QUIET / NO_STATE / DRY_RUN / API_FAIL
3. Register in `aeon.yml`: daily 20:30 UTC (slots after fork-cohort 19:00 on Sundays, runs mid-week to catch intra-week activations). skills.json 119 → 120

---

### 5. Competitor Launch Radar (aeon)
**Type:** Intelligence
**Effort:** Small (hours)
**Impact:** `ai-framework-watch` tracks star momentum for 8 known peer frameworks — but misses *new entrants*. In the current AI agent sprint, a new framework can post to Product Hunt, get 400 upvotes, and appear in the HN front page before accumulating a single GitHub star. This weekly skill scans PH RSS and HN Algolia API for "agent framework / autonomous agent / MCP server / agentic" keyword matches and sends a digest of new launches the operator doesn't know about yet. Fills the blind spot between known competitors (ai-framework-watch) and unknown challengers launching this week.
**How:**
1. New `skills/competitor-launch-radar/SKILL.md` — fetches PH RSS (`producthunt.com/feed`, keyless) + HN Algolia `search?tags=show_hn` (keyless) with keyword filter list: [agent framework, autonomous, agentic, claude, MCP, multi-agent]. Noise floor: PH ≥10 upvotes OR HN ≥10 points
2. Classify each match: (a) AI agent framework — direct competitor, (b) MCP server/tool — ecosystem adjacent, (c) agent-powered product — downstream use case. Dedup via state file (announced set). Digest article with links, upvote counts, classification labels
3. Register in `aeon.yml`: weekly Monday 10:00 UTC (after weekly-shiplog 09:00 and ai-framework-watch 08:30, completing the Monday morning intelligence cluster). skills.json 120 → 121

---

## Summary

| # | Idea | Repo | Type | Effort |
|---|------|------|------|--------|
| 1 | Product Hunt column | minitor | Integration | Small |
| 2 | GitHub Discussions column | minitor | Feature | Medium |
| 3 | Skill Health Triad backport | aeon-agent | DX | Medium |
| 4 | Fork First-Run Alert | aeon | Community | Small |
| 5 | Competitor Launch Radar | aeon | Intelligence | Small |

**Cross-cutting theme:** The agent fleet has crossed a density threshold — 56 forks, 86 local skills, 43 dashboard columns — where the next layer isn't more features but smarter sensing: knowing the moment a fork goes live (#4), watching for new challengers before they're on the radar (#5), and giving the running agent the ability to heal itself (#3). Ideas #1 and #2 complete Minitor's dashboard-for-the-internet promise on the two surfaces it doesn't yet see (launch discovery, community Q&A).
