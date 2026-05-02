# Repo Action Ideas — 2026-05-02

**Repos analyzed:** aaronjmars/aeon (260★, 39 forks, 3 open PRs), aaronjmars/aeon-agent (7★, 3 open PRs), aaronjmars/minitor (5★, 3 open PRs)

**Context:** Three repos with a combined 9 open unreviewed PRs and no auto-merge path (workflows-scope PAT still pending, day 15). v4 redesign announced as ~2 weeks out. Star count at 260, ~40 from the 300-star milestone at ~4/day pace (~10 days). show-hn-draft ready but not dispatched. Carried unbuilts: Operator Value Scorecard (#5, 2 cycles), Skill Dependency Freshness Validator (#4, 2 cycles). Minitor just shipped its 31st column type (Bluesky). fork-cohort shipped today — "X of 39 forks running in production" number now trackable for the first time.

---

### 1. Operator Value Scorecard
**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Closes the "was this worth it?" question operators ask after a week of autonomous runs. Right now the answer requires reading skill-analytics + heartbeat + tweet-allocator + token-report + repo-pulse separately. A weekly plain-language synthesis removes that friction and surfaces the ROI signal directly. Carried two cycles (Apr-30 idea #5).
**How:**
1. Monday 10:30 UTC skill reads last 7 days of skill-analytics articles (success rates, anomaly flags), heartbeat verdicts (P0–P3 signals), tweet-allocator totals ($AEON distributed), token-report 7d price delta, and repo-pulse weekly star/fork deltas.
2. Produces a 3-paragraph summary: **Agent health** (skills fired, pass rate, any anomalies), **Community growth** (stars gained, forks added, notable new contributors), **Economic activity** ($AEON distributed, recipients, token 7d performance). Appends a one-line verdict: OK / WATCH / DEGRADED mirroring heartbeat's language.
3. Writes `articles/operator-scorecard-${today}.md`, notifies via `./notify`, logs to memory/logs.

---

### 2. Skill Dependency Freshness Validator
**Type:** Feature
**Effort:** Small (hours)
**Impact:** Prevents chained skills from silently acting on stale data. Currently there is no check that a skill consuming `articles/token-report-*.md` or `.outputs/skill-a.md` is reading today's version rather than yesterday's (or last week's, if the upstream skill failed). Carried two cycles (Apr-30 idea #4).
**How:**
1. Parse every `SKILL.md` for `articles/`, `.outputs/`, and `memory/topics/` file references. Parse `aeon.yml` `chains: consume:` edges. Build a flat dependency map: `{consumer_skill: [upstream_paths]}`.
2. For each dependency, check disk mtime and compare to the consumer skill's expected freshness threshold (articles 28h, outputs 4h, topics 7d). Flag any dependency older than its threshold.
3. Exit `FRESHNESS_OK` / `FRESHNESS_WARN {list}` / `FRESHNESS_STALE {list}`. Wire to skill-health as a new P2 signal. Pure local file I/O, no new APIs.

---

### 3. Star Momentum Alert
**Type:** Growth
**Effort:** Small (hours)
**Impact:** Bridges the gap between "show-hn-draft is ready" and "it's time to dispatch it." Currently there is no signal telling the operator when the 300-star milestone is close enough to time a Show HN launch. With 260 stars and ~4/day momentum the window is ~10 days — but the rate varies, and the optimal launch window (Tuesday–Thursday morning per show-hn-draft checklist) needs to be anticipated, not reactive.
**How:**
1. Reads the last 14 days of `articles/repo-pulse-*.md` articles, extracts daily star deltas, computes 3-day and 7-day rolling averages.
2. When projected milestone date lands within the next 7–14 days AND falls on a Tue–Thu: fires a targeted notification with the projected date, current rate, and a "consider dispatching show-hn-draft on [date]" prompt. Deduplicates: one alert per milestone approach (state in `memory/state/star-momentum-state.json`).
3. Runs daily alongside repo-pulse (`10 10 * * *`), exits silently outside the target window. Zero new APIs — reads files already written by repo-pulse.

---

### 4. Mastodon Column for minitor
**Type:** Integration
**Effort:** Small (2–3 hours)
**Impact:** Completes the decentralized social trifecta in minitor — Bluesky (shipped May 2) + Farcaster + Mastodon. Mastodon's public API requires no API key for search on federated instances (`mastodon.social/api/v2/search`, `accounts/lookup`). The Bluesky column shipped today is the direct template: same 3-file plugin structure + 3 registry edits, same cursor-based pagination pattern, same avatar-led card renderer. Adds the 32nd column type.
**How:**
1. `lib/integrations/mastodon.ts` — fetches from `https://${instance}/api/v2/search` (keyword mode) or `https://${instance}/api/v1/accounts/lookup` + `/statuses` (author mode); no auth header required for public instances. Handle reblog filtering (same as Bluesky repost filter). Status `url` field is the permalink.
2. Standard 3-file plugin (`plugin.ts` / `server.ts` / `client.tsx`): Zod `{ instance, mode: "search"|"author", query, handle }` with `instance` defaulting to `mastodon.social`. Elephant icon (or Globe), Mastodon brand purple `#6364ff`. Renderer matches Bluesky card layout (avatar + text + engagement footer: favourites/reblogs/replies).
3. Three registry edits (manifest, registry, server-registry parity check). README Social row 6 → 7. PR to aaronjmars/minitor.

---

### 5. v4 Readiness Checker
**Type:** DX / Community
**Effort:** Small (hours)
**Impact:** v4 full redesign is ~2 weeks out per operator tweets (Apr 30). There are 39 forks running on current architecture. Without a structured readiness guide, fork operators will hit breaking changes blind. A one-shot `workflow_dispatch` skill that reads their current aeon.yml + skills.json + memory/MEMORY.md and generates a personalized upgrade checklist gives them lead time to prepare — and gives aaronjmars a structured surface for "what's changing in v4."
**How:**
1. Reads `aeon.yml` (enabled skill list, model overrides, chain definitions, custom schedules), `skills.json` (catalog fingerprint), and `memory/MEMORY.md` (Skills Built list for custom skills). Cross-references against a known list of patterns likely to change in v4 (skill frontmatter schema, chain runner interface, memory directory layout, MCP server tool naming).
2. Produces a personal checklist: **Safe** (patterns confirmed stable), **Review** (patterns known to change), **Unknown** (custom skills with no upstream equivalent), **Action items** (concrete steps before upgrading). Appends estimated complexity score per item.
3. Writes `articles/v4-readiness-${today}.md`, notifies via `./notify`, logs. Ships `enabled: false` / `workflow_dispatch` — operator runs it manually as v4 release approaches. Useful now for building the checklist template; the per-fork content fills in as v4 details are announced.
