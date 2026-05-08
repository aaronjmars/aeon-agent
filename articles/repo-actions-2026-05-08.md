# Repo Action Ideas — 2026-05-08

Generated from analysis of aaronjmars/aeon (280⭐, 43 forks), aaronjmars/aeon-agent (7⭐, 1 fork), and aaronjmars/minitor (8⭐, 1 fork).

**Context:** Active build day — minitor shipped its 37th column type (HuggingFace: models/datasets/spaces, PR #30), aeon shipped `huggingface-trending` (daily AI artifact digest, PR #162), and aeon-agent shipped xai-prefetch truncation warning (PR #33). aeon at 280⭐, 20 from the 300-milestone. star-momentum-alert and star-milestone are both built upstream (aeon PRs #159 + existing PR #39) but not yet enabled. minitor column count: 37 — YouTube, Reddit, HuggingFace all present; arxiv and DEV.to are the notable gaps for the AI/developer audience.

---

### 1. arxiv Column (minitor)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** HuggingFace trending (37th column, PR #30) covers the AI artifact layer — models and datasets that just appeared. The natural companion is the paper layer: arxiv is where the models' underlying research drops, often 2–3 weeks before the model goes viral on HuggingFace. The audience watching minitor for HuggingFace trending already wants to see what's in the arxiv pipeline. Keyless RSS (`http://export.arxiv.org/rss/cs.AI`, `cs.CL`, `cs.LG`, and any of the ~50 CS subcategories) — no API key, no rate limit beyond standard crawl delay. First academic paper surface in the minitor lineup; fills the gap between HN discussion and HuggingFace artifact, completing the full AI content stack.
**How:**
1. `lib/integrations/arxiv.ts` — fetches the category RSS feed URL, parses the Atom 1.0 XML response (arxiv exports Atom, not RSS 2.0). Normalize to `{ title, url, authors, abstract, categories, published }`. Schema-drift safe: drop entries missing `id` + `title`. Use a 2-hour feed cache since arxiv updates daily at 14:00 ET.
2. Standard 3-file plugin (`plugin.ts` config: category select + optional keyword filter; `server.ts` fetcher + cache; `client.tsx` renderer: title/author row + first 140 chars of abstract, `cs.AI` accent `#B31B1B` — arxiv Cornell red). Registry edits: `manifest.ts`, `registry.ts`, `server-registry.ts`. Add to the `ai` ColumnCategory.
3. README: column count 37 → 38, update AI/ML cluster row, hero paragraph picks up "arXiv papers." PR to aaronjmars/minitor.

---

### 2. DEV.to Column (minitor)
**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** The current minitor lineup has HN (link aggregation and comment discussion) and Lobsters (developer link aggregation) but no long-form developer article surface. DEV.to fills that gap: it is where practitioners write tutorials, walkthroughs, and opinionated engineering posts — the kind of content that HN links to but doesn't host. Critically, it has a public REST API with no authentication required (`https://dev.to/api/articles?top=7&tag={tag}`) that returns title, author, tag list, reading-time estimate, reactions, and comments count. Tag filtering lets a minitor user watch `ai`, `llm`, `typescript`, `python`, `webdev`, or any community tag. 38th (or 39th) column type; first developer-article surface distinct from link aggregation.
**How:**
1. `lib/integrations/devto.ts` — fetches `https://dev.to/api/articles?top=7&tag={tag}&per_page=30`, maps to `{ title, url, author, readingTime, tags, reactions, comments, published }`. No API key header needed for public read. Schema-drift safe: required fields are `title`, `url`, `user.username`; drop entries missing any of the three. Offset-based pagination matching the documented `paginate.ts` trade-off (per_page + page param).
2. Standard 3-file plugin. Zod config: `{ tag?: string, mode: 'top' | 'latest' | 'rising' }` (top = past week by reactions, latest = newest, rising = past day by reactions — maps to `top=7`, `top=1`, `top=1&per_page=30&sort=positive_reactions_count`). Renderer: title/author/reading-time row + reactions/comments footer. `#3b49df` DEV.to brand indigo accent. `BookOpen` icon.
3. README: column count +1, new Developer row in content cluster, hero paragraph mentions DEV.to. PR to aaronjmars/minitor.

---

### 3. ai-framework-watch (aeon)
**Type:** Content
**Effort:** Medium (1–2 days)
**Impact:** aeon operators running forks don't have a weekly competitive-intelligence feed. The AI agent framework space is moving fast — LangGraph, CrewAI, AutoGPT, LlamaIndex, Mastra, smolagents, dspy, and Pydantic AI all ship releases weekly. An operator who doesn't track these misses protocol shifts (e.g. A2A adoption) and feature gaps that forks could close. This skill uses entirely public data: GitHub API for stars, forks, and recent releases (no auth needed for public repos), and WebSearch for community news. Weekly cadence (Monday morning before the week's feature decisions) positions it as the "what happened in the ecosystem last week" anchor. No equivalent skill exists in aeon; github-trending covers code broadly but not this curated competitor set.
**How:**
1. Build `skills/ai-framework-watch/SKILL.md`. Weekly cron Monday 08:30 UTC (after weekly-shiplog at 08:00). Hardcode a watchlist of 8–10 frameworks in the SKILL.md (`aaronjmars/aeon` as anchor + 7 competitors). For each: `gh api repos/{owner}/{repo}` for stars/forks/language + `gh api repos/{owner}/{repo}/releases?per_page=3` for recent releases. WebFetch fallback for each if `gh api` sandbox-blocks.
2. Score each framework on a momentum signal: new stars (7d delta from two consecutive repo-pulse-style checks using `stargazers_count` vs last week's value stored in `memory/topics/framework-watch-state.json`), recent release count (7d), and open issue delta. Emit a ranked table: framework name, stars (7d delta), releases this week, 1-line release headline. Flag any framework that shipped a breaking-change release (via title keyword scan: "breaking", "v2", "major").
3. Write `articles/ai-framework-watch-${today}.md`, register `enabled: false` + `schedule: "30 8 * * 1"` in `aeon.yml`, bump `skills.json`, notify via `./notify`.

---

### 4. contributor-spotlight (aeon)
**Type:** Community
**Effort:** Small (hours)
**Impact:** fork-cohort (aeon PR #152) identifies POWER and ACTIVE forks weekly but produces a data table — not a human moment. contributor-spotlight converts that data into a recognition post: one fork operator per week gets a named callout with their contribution stats (commits to the fork, stars gained, skills they've enabled or built). This is the community flywheel: contributors who feel seen attract other contributors. The post is formatted for both a notification and a tweetable thread (feeds into thread-formatter). No new APIs — reads `memory/topics/fork-cohort-*.md` output from the prior week's fork-cohort run + `gh api repos/{fork}/contributors`. First skill of this type; closes the gap between "we have fork data" and "we do something social with it."
**How:**
1. Build `skills/contributor-spotlight/SKILL.md`. Weekly cron Sunday 20:00 UTC (after fork-cohort at 19:00 UTC). Reads the most recent `memory/topics/fork-cohort-*.md` output; picks the POWER fork with the most active week (commits + stars delta). Fetches contributor stats: `gh api repos/{fork}/stats/contributors --jq '.[] | select(.total > 0) | {login, total, weeks: [.weeks[] | select(.c > 0)] | length}'`.
2. Generates a 150-word recognition paragraph: fork name, operator handle (GitHub login), what they built or enabled, their star count, and a "keep shipping" close. Writes `articles/contributor-spotlight-${today}.md`. Deduplicates: state in `memory/topics/spotlight-history.json` — same fork not featured two weeks running; rotate to the next POWER/ACTIVE fork.
3. Register `enabled: false` + `schedule: "0 20 * * 0"` in `aeon.yml`. Bump `skills.json` total, community category. Notify via `./notify`.

---

### 5. skill-update-check Backport (aeon-agent)
**Type:** DX / Quality
**Effort:** Small (hours)
**Impact:** `skill-update-check` exists in aeon but has never been backported to aeon-agent. Meanwhile, MEMORY.md notes that "aeon-agent still at pre-autoresearch-evolution SKILL.md versions (aeon PRs #46–#136 not yet backported)" — this fork is running 80+ skills silently at older versions. skill-update-check closes this blind spot by comparing the SHA of each local `skills/{name}/SKILL.md` against the upstream aeon version via `gh api`, flagging any skill where the upstream has been modified since the last comparison. Without it, an improved `fetch-tweets.md` or `token-report.md` on aeon could fix a quality regression that the aeon-agent operator never learns about. Backports the same-day-after pattern established for operator-scorecard (May 3→4) and skill-freshness (May 4→5). No new dependencies — pure `gh api` + SKILL.md reads.
**How:**
1. Read `skills/skill-update-check/SKILL.md` from upstream aeon via `gh api repos/aaronjmars/aeon/contents/skills/skill-update-check/SKILL.md --jq '.content' | base64 -d`. Copy verbatim into `skills/skill-update-check/SKILL.md` in this repo.
2. Add to `aeon.yml`: `skill-update-check: { enabled: false, schedule: "0 9 * * 1", model: "claude-sonnet-4-6" }` (Monday 09:00 UTC, before feature decisions). Bump `skills.json` total, developer-experience category.
3. Initialize state file `memory/topics/skill-update-check-state.json` as `{}`. Ship `enabled: false`. First natural run Monday — will immediately surface the 80+ drifted skill versions as a prioritized notification. Operator then decides which upgrades to pull.
