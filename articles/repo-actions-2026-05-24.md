# Repo Action Ideas — 2026-05-24

Generated from analysis of aaronjmars/aeon (437⭐, 112 forks, 6 open PRs), aaronjmars/aeon-agent (9⭐, 1 fork, 2 open PRs), and aaronjmars/minitor (11⭐, 0 forks, 1 open PR). Two major events shape today's ideas: PR #220 merged ECOSYSTEM.md listing 40 projects building on Aeon (first time the ecosystem is formally documented), and PR #219 ported 34 skills from derivative instances — pushing the upstream catalog to 155 total. With 40 ecosystem projects and 155 skills now in the repo, the intelligence and discovery gaps are widening faster than any individual fix can close.

---

### 1. ecosystem-pulse skill
**Type:** Feature
**Effort:** Small (hours–1 day)
**Impact:** ECOSYSTEM.md just merged (#220) listing 40 projects building on Aeon — aeonbook, GitBlock, MiroShark, RootAi, Bankr, Powerloom, and 34 others. There is currently no skill that monitors whether those projects are alive and active. The fork-cohort skill tracks Aeon forks; the contributor-spotlight skill tracks who's pushing code to Aeon itself — but none of them ask "are the projects built ON Aeon actually shipping?" A weekly ecosystem-pulse skill closes that gap: it reads ECOSYSTEM.md for the project list, looks up any GitHub repos it can match (via search or operator-maintained metadata), reports stars/forks/last-commit recency and any new GitHub releases in the 7-day window. Projects without GitHub repos get a "X handle only" entry rather than an undercounting zero.

**How:**
1. Create `skills/ecosystem-pulse/SKILL.md`. Weekly Monday 11:00 UTC, `enabled: false`, sonnet-4-6. Read ECOSYSTEM.md from the repo root; parse the project table (name + X handle). For each project, attempt a GitHub search (`gh api search/repositories -q "topic:aeon OR {name}"`) or a hardcoded mapping file at `memory/topics/ecosystem-pulse-map.json` that operators can extend. Fall back to "X-only" entry for projects with no matched repo.
2. For matched GitHub repos: query stars, forks, last push date, and latest release tag (if any in the past 7 days). Bucket by activity: ACTIVE (pushed ≤7d), RECENT (pushed ≤30d), COLD (pushed >30d). Report total ACTIVE count, top-3 by star count, any new releases.
3. Write article to `articles/ecosystem-pulse-${today}.md`, send notification with ACTIVE count + standout project names. Persist per-project state to `memory/topics/ecosystem-pulse-state.json` for WoW delta tracking (e.g., project moved from COLD → ACTIVE). Exit taxonomy: OK / QUIET / PARTIAL / NO_ECOSYSTEM_FILE / DRY_RUN / BAD_VAR.

---

### 2. fleet-skill-adoption leaderboard
**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** PR #219 pushed the upstream skill catalog to 155 entries — 34 new skills added in a single merge. Fork operators now face a menu they can't evaluate: which of these skills are actually working in production across the fleet? The fork-skill-gap skill shows what each fork is MISSING; nothing shows which skills the fleet has VALIDATED by enabling them. A fleet-skill-adoption leaderboard skill closes this: it reads ACTIVE/POWER forks from `memory/topics/fork-cohort-state.json`, fetches each fork's aeon.yml (or gracefully degrades to live `gh api` lookup), counts per-slug `enabled: true` occurrences, and surfaces the top-10 most-adopted and bottom-10 least-adopted skills by fleet penetration rate. Result: operators see "batch-health is enabled by 68% of ACTIVE forks — maybe I should too" instead of staring at 155 entries cold.

**How:**
1. Create `skills/fleet-skill-adoption/SKILL.md`. Weekly Sunday 22:00 UTC (after fork-skill-gap at 21:00), `enabled: false`, sonnet-4-6. Source: `memory/topics/fork-cohort-state.json` for ACTIVE+POWER fork list; per-fork aeon.yml read via `gh api repos/{fork}/contents/aeon.yml` (base64 decode); graceful "unreadable" fallback if API 404/403. Process: for each fork, parse enabled slug list (`grep -E 'enabled:\s*true' -B5` to get slug context). Aggregate counts across all readable forks.
2. Produce three tables: (a) top-15 most-adopted slugs with adoption %, (b) bottom-15 least-adopted slugs with adoption % (excludes slugs where `enabled: false` is the install default, i.e., adoption < 5% AND slug is in the ≤7d-old cohort from PR #219 — flag these as "new"), (c) WoW delta vs prior state (slugs that gained ≥5% adoption in the past week).
3. Persist to `memory/topics/fleet-skill-adoption-state.json` (per-slug adoption history, rolling 8-week). Send gated notification (suppress if no top-10 changes AND prior state exists). Article to `articles/fleet-skill-adoption-${today}.md`. 8-status exit taxonomy: OK / QUIET / PARTIAL / NO_COHORT_STATE / NO_READABLE_FORKS / DRY_RUN / STATE_CORRUPT / BAD_VAR.

---

### 3. config-validator skill backport from aeon PR #219 (aeon-agent)
**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** PR #219 added a `config-validator` skill to aeon — one of 34 skills ported from derivative instances. It validates aeon.yml structure: required frontmatter fields, cron expression syntax, referenced skill paths existing on disk, no duplicate slugs, enabled boolean type check. aeon-agent doesn't have this skill yet. Fork operators on aeon-agent — 112 forks now — are the most likely to make aeon.yml config errors when customizing their setup (typo in cron, wrong slug under `skills:`, bad model ID). A `config-validator` run before the operator commits aeon.yml changes would catch problems before they silently mischedule skills.

**How:**
1. Read `skills/config-validator/SKILL.md` from the upstream aeon repo (`gh api repos/aaronjmars/aeon/contents/skills/config-validator/SKILL.md`). Genericize any remaining persona/hardcoded references (check for `Aaron`, `aaronjmars`, `AEON` token references). Register in aeon-agent's `skills.json` and `aeon.yml` with `enabled: false`, `workflow_dispatch` only. Update `skills.json total` counter.
2. If the upstream SKILL.md references `memory/topics/` paths or skill-specific state files that don't exist in aeon-agent, add fallback handling (check path exists before reading, skip gracefully). The validator's core logic — cron syntax check via `echo "0 8 * * 1" | crontab -l` test, YAML parse via Python one-liner, skill path existence via `ls skills/{slug}/SKILL.md` — is environment-independent.
3. Open PR to aeon-agent with frontmatter `name: config-validator`, standard backport commit message noting source PR #219. Add a skills.json entry with `tags: [dev, ops]`. The skill should be dispatch-only — operators run it manually before pushing aeon.yml changes.

---

### 4. Bluesky AT Protocol column (minitor)
**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** minitor has 47 column types covering GitHub, HN, Reddit, X/Twitter, npm, PyPI, crates, DEV.to, Product Hunt, and more — but not Bluesky. The AT Protocol's AppView API is keyless and public: `bsky.social/xrpc/app.bsky.feed.getAuthorFeed` and `bsky.social/xrpc/app.bsky.feed.searchPosts` require no authentication for public content. Bluesky has become the default developer/research community feed for many teams that moved off Twitter — the same audience that would use GitHub Trending, HackerNews, and DEV.to columns. Adding Bluesky completes the social trifecta (X + Reddit + Bluesky) with a keyless API that fits minitor's design contract.

**How:**
1. Create `lib/integrations/bluesky.ts` with two modes: `user` (fetches `app.bsky.feed.getAuthorFeed` for a configured handle — strips `@` prefix, resolves DID via `app.bsky.actor.getProfile` on first fetch) and `search` (uses `app.bsky.feed.searchPosts?q={query}&limit=25`). Three integration quirks to document: (a) AT Protocol uses DIDs as canonical identities — cache the DID → handle mapping in local store to avoid extra API round-trips on every refresh; (b) `app.bsky.feed.searchPosts` is limited to the past 30 days by the AppView — surface this in the column config UI; (c) `embed.images[]` and `embed.external` are nested under `post.record.embed` — normalize to a flat `thumbnailUrl` for the item card.
2. Create 3-file plugin (`components/columns/bluesky.tsx`, type registration, integration helper). Column item: handle avatar + display name + post text (280-char clip) + timestamp + reply/repost/like counts + Bluesky link. #0085ff Bluesky brand blue accent, `Cloud` icon (distinct from Reddit's `MessageSquare` and X's implied bird). Config fields: `mode: "user" | "search"`, `handle` (user mode), `query` (search mode), `limit` (5–25, default 10).
3. Add to column type registry, update README (News & web cluster 11 → 12, count 47 → 48, keyless list). No BLUESKY_TOKEN needed — intentional design choice, document in column config UI as "keyless — only public posts are visible." Add `fetchBlueskyPage` to `lib/integrations/bluesky.ts` following the same fetchPage contract as existing integrations.

---

### 5. Column-level webhook notifications (minitor)
**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** alertKeywords (PR #41, May-16) gives operators a visual indicator — a yellow ring and badge count — when keyword matches land in a column. But visual indicators require the operator to be looking at the dashboard. For any serious monitoring use case (infra alerts, competitor launches, token price moves, security CVEs), passive visual-only isn't enough. A per-column webhook turns minitor from a dashboard into an alerting system: when alert keyword matches arrive, POST to a configured URL. Zapier, n8n, Slack webhooks, Discord webhooks — any HTTP endpoint. This is the missing layer between "I see it" and "I'm notified."

**How:**
1. Add nullable `notify_webhook_url` column to the database schema (`lib/db/schema.ts`, new migration `drizzle/0003_notify_webhook.sql`). Validate server-side with a URL regex that allows only `https://` to prevent SSRF against internal network ranges — block RFC-1918 prefixes (10.x, 172.16-31.x, 192.168.x) and `localhost`. Add `updateColumnWebhookUrl` server action mirroring `updateColumnAlertKeywords`. Wire into export/import/share-link round-trip (optional field on DeckExport v1).
2. After each column fetch in the column fetch server action (`app/actions.ts`), if `notify_webhook_url` is set and the fetched items include any alertKeyword matches (reuse the existing `matchesKeywords` helper), POST to the URL with JSON body: `{columnId, columnTitle, typeId, matches: [{id, url, text, matchedKeywords}], timestamp}`. Fire-and-forget with a 5-second timeout — a failed webhook does not fail the fetch. Log success/failure to console (no UI feedback to prevent webhook-endpoint probing by inspecting responses).
3. Expose in the Configure column dialog as an "Alert webhook URL" field below the alertKeywords input — only shown when alertKeywords is non-empty (no keywords, no useful webhook). Add descriptive tooltip: "POST to this URL when alert keywords match new items. HTTPS only." Update deck export/import/share-link schema with optional `notifyWebhookUrl: string`. No new dependencies.
