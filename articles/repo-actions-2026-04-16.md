# Repo Action Ideas — 2026-04-16

**Repos:** aaronjmars/aeon (173 stars, 20 forks, 90+ skills, 1 open PR) | aaronjmars/aeon-agent

**Context:** Best growth day on record: +16 stars and +3 forks in 24h. Second token breakout in 72h (+77%). The fork merge last week absorbed 25 community skills, pushing the catalog past 90. Reactive triggers, A2A gateway, MCP adaptor, skills.lock, and heartbeat escalation are all live or in-flight. Open PR #36 adds Dev.to syndication. With momentum at its highest, the priority shifts to converting new attention into active operators, closing the contributor loop, and building the distribution layer that compounds the growth.

---

### 1. Setup Wizard — `./aeon setup`
**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** 16 new stars in one day means first-time visitors are arriving in volume. Current onboarding: read a 500-line README, manually edit aeon.yml. A setup wizard that outputs a ready-to-paste config in under 2 minutes converts passive stargazers into active operators — and each active fork is a distribution node. Even a 10% improvement in conversion compounds.
**How:**
1. Create a `setup` bash script at the repo root. Prompt for: (a) use case (crypto/content/developer/custom), (b) notification channel (Telegram/Discord/Slack/email), (c) preferred cadence (daily/weekly/on-demand).
2. Generate a minimal aeon.yml snippet with the relevant skills pre-enabled, commented with which secrets to add.
3. Print a final checklist: secrets to configure, how to verify with `gh workflow run aeon.yml`.

---

### 2. Contributor Auto-Reward
**Type:** Integration
**Effort:** Small (hours)
**Impact:** The `distribute-tokens` skill exists but is manual. Wiring it to a reactive trigger on external PR merge creates a fully automated contributor incentive loop. An external contributor opens a PR, it merges, they receive AEON tokens automatically. This is a public viral moment — contributors announce it, which drives word-of-mouth for both the repo and the token. Directly closes the community loop that the A2A gateway and MCP adaptor opened.
**How:**
1. Add a reactive trigger to `aeon.yml`: `schedule: "reactive"` with `trigger: pr_merged` that fires when `PR author != merger` (i.e., external contribution).
2. The triggered skill reads the PR author's GitHub username, looks them up in a `contributors.yml` registry (wallet address mapping), and calls `distribute-tokens` with the resolved address and a fixed reward amount.
3. Send a notification with the contributor's name, PR title, and tokens distributed.

---

### 3. Weekly Operator Newsletter
**Type:** Content/Growth
**Effort:** Small (hours)
**Impact:** With 173+ stars and a working SendGrid integration, a weekly digest email is the highest-leverage retention play available. Most stars never return to the repo — a newsletter brings Aeon's output (token reports, repo articles, skill highlights) directly to their inbox. Converts passive audience into engaged operators. The distribution infrastructure is already built; this is a routing layer on top of it.
**How:**
1. Create `skills/weekly-newsletter/SKILL.md`. It reads the past week's articles from `articles/`, pulls the token-report summary, and synthesizes a curated digest.
2. Format as plain+HTML email with a consistent weekly structure: one lead story, token snapshot, skill spotlight, one tip for operators.
3. Schedule Sunday 10:00 UTC. Use the existing SendGrid path (`SENDGRID_API_KEY`). Add an opt-in field to the dashboard secrets panel (`NOTIFY_NEWSLETTER_TO`) for subscriber emails.

---

### 4. Memory Search Skill
**Type:** Feature
**Effort:** Small–Medium (1 day)
**Impact:** Aeon's memory corpus spans `logs/`, `topics/`, `issues/`, `MEMORY.md` — all unindexed. Skills currently read the index and recent logs but miss long-tail context. A search skill answers queries like "what happened with auto-merge?" or "find all token reports from March" by scanning the full memory tree. Surfaces relevant past context for deeper skill runs and lets operators query accumulated knowledge directly from the dashboard or CLI.
**How:**
1. Create `skills/memory-search/SKILL.md` as `schedule: workflow_dispatch` (var: search query). Skill recursively reads all `.md` files under `memory/`, scores relevance to the query using keyword + semantic matching, and returns top 5 matches with excerpts.
2. Cache results in `memory/search-cache/{query-hash}.md` with a 24h TTL to avoid re-scanning on repeated queries.
3. Expose as an MCP tool via the existing `mcp-skill-adaptor` so Claude Desktop operators can query Aeon's memory in natural language.

---

### 5. Fork Spotlight Page
**Type:** Community/Growth
**Effort:** Medium (1–2 days)
**Impact:** 20 forks exist but are invisible to each other and to new visitors. A weekly-updated GitHub Pages page showcasing active forks — their purpose, top enabled skills, and unique customizations — creates social proof, incentivizes operators to differentiate their instances, and gives new visitors concrete production examples. Builds directly on the `fork-fleet` and `skill-leaderboard` data already collected weekly. Zero additional API calls needed; this is a rendering layer on existing outputs.
**How:**
1. Extend `update-gallery` to also generate `docs/fleet.md` — a browsable page listing active forks with: operator handle, instance purpose (from their MEMORY.md), top 5 enabled skills, star count, last active date.
2. Source data from `fork-fleet`'s weekly output (already written to `articles/fork-fleet-*.md`). Schedule `update-gallery` to run after `fork-fleet` on Sundays.
3. Add a "Fleet" tab to the existing GitHub Pages gallery nav and link it from the main README under the "Instance Fleet" section.
