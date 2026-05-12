# Repo Action Ideas — 2026-05-12

*Generated from analysis of aaronjmars/aeon (299⭐, 48 forks), aaronjmars/aeon-agent (7⭐, 61 skills), aaronjmars/minitor (8⭐, 41 column types). AEON token ATH day: $0.0000331 (+454% 24h, $1.37M volume). 300⭐ imminent on aeon.*

---

### 1. v4-readiness Backport
**Type:** DX Improvement
**Effort:** Small (hours)
**Repo:** aaronjmars/aeon-agent

**Impact:** Closes the aeon-agent backport queue before Claude v4 ships. The v4-readiness skill (aeon PR #160, May 6) runs a per-fork checklist — model references, deprecated APIs, aeon.yml schema drift — and notifies operators of breaking changes they need to handle before the upgrade. With 48 forks active and AEON at ATH, operators are engaged and v4 timing is closing in. This is the last backport in the May-6 batch (operator-scorecard, skill-freshness, skill-update-check, fork-cohort, thread-formatter — all done as of today). After this PR, aeon-agent's skill set is at full parity with aeon's pre-v4 stack.

**How:**
1. Fetch raw content of `skills/v4-readiness/SKILL.md` from `aaronjmars/aeon` via GitHub API (raw `Accept` header to avoid base64 corruption — same pattern as skill-update-check backport, PR #34)
2. Create `skills/v4-readiness/SKILL.md` in aeon-agent with verbatim content; add `v4-readiness: { enabled: false, schedule: "workflow_dispatch", model: "claude-sonnet-4-6" }` to aeon.yml; bump skills.json count 61 → 62
3. Open PR; note in description that dispatch timing should be coordinated with the v4-announcement — this skill runs on operator demand, not cron

---

### 2. Reddit Column
**Type:** Integration
**Effort:** Small (hours)
**Repo:** aaronjmars/minitor

**Impact:** Fills the community discussion layer that is entirely absent from minitor's 41 column types. HN and Lobsters cover curated link aggregation; DEV.to covers tutorials; Stack Overflow covers Q&A — but community threads are missing. Reddit is where AI researchers post early experiment reactions, r/LocalLLaMA debates fine-tune results before they reach papers, and r/webdev surfaces tooling opinions before they reach blog posts. It's a different signal type from every existing column. Keyless for public subreddits (returns JSON without auth — only a User-Agent header needed), consistent with minitor's no-secrets-required design philosophy.

**How:**
1. Fetch `reddit.com/r/{subreddit}/{sort}.json?limit=25&t={timeframe}` with a `User-Agent` header (Reddit's public JSON API; no OAuth for public subreddits); 4 sort modes: `hot`, `top` (timeframe: `week`/`month`/`all`), `new`, `rising`; optional flair filter applied client-side on `link_flair_text`
2. Standard 3-file plugin (`plugin.ts`, `server.ts`, `client.tsx`) with `#FF4500` Reddit orange accent, `MessageSquare` icon; row shows: score badge (upvotes), comment count, optional flair chip, subreddit header; `fetchRedditPosts` in `lib/integrations/reddit.ts`; integration quirks: (1) `score` field can be `null` on brand-new posts — fallback to 0; (2) filter `over_18: true` posts by default; (3) skip `[deleted]`/`[removed]` titles
3. 3 registry edits (manifest, server-registry, registry) + README cluster row News & web 8 → 9, count 41 → 42

---

### 3. Fleet-State Digest
**Type:** Community
**Effort:** Medium (1-2 days)
**Repo:** aaronjmars/aeon

**Impact:** Three per-signal skills now produce fork intelligence independently: fork-cohort (activation stage), contributor-spotlight (individual recognition), fork-release-tracker (versioned artifacts). But there is no synthesis — no single weekly "state of the fleet" narrative. The operator reads three separate notifications to understand fleet health. Fleet-State Digest closes this gap: one Monday read that answers "how many POWER forks, who leveled up, who shipped a release, who is the spotlight pick" — with week-over-week deltas. Especially timely now that the fleet has grown to 48 forks and fork-release-tracker only shipped today (May 12, PR #166), making the synthesis layer the next natural step.

**How:**
1. Read state from the three constituent skills (`memory/topics/fork-cohort-state.json`, `memory/topics/contributor-spotlight-history.json`, `memory/topics/fork-release-state.json`); supplement with `gh api repos/{parent}/forks --paginate` for current snapshot; compute POWER/ACTIVE/STALE/COLD counts + week-over-week delta by comparing to prior week's state in `memory/topics/fleet-state.json`
2. Generate a ranked fleet table with stage counts, transition highlights (LEVELED_UP/WENT_STALE/REVIVED), any releases from the 7-day window, and the current spotlight pick; 6-status exit taxonomy (OK/QUIET/PARTIAL/NO_FORKS/STATE_MISSING/ERROR); QUIET suppresses notify when no transitions, no releases, and prior state exists
3. Register `fleet-state: { enabled: false, schedule: "0 8 * * 1", model: "claude-sonnet-4-6" }` — Monday 08:00 UTC, slots 30 min before ai-framework-watch (08:30) and 1h before weekly-shiplog (09:00); state persists to `memory/topics/fleet-state.json` for longitudinal tracking

---

### 4. Webhook-to-Skill Bridge
**Type:** Feature
**Effort:** Medium (1-2 days)
**Repo:** aaronjmars/aeon-agent

**Impact:** All skills currently trigger on cron or manual `workflow_dispatch`. No external event can fire a skill without operator access to the GitHub Actions UI. The webhook bridge enables event-driven composition: a DexScreener price alert fires → token-report runs; a GitHub release on a fork → push-recap runs; a Telegram message → any skill runs. The `reactive:` section of aeon.yml already anticipates this pattern — `skill-repair` and `autoresearch` are commented out but structurally defined. This is the implementation that gives that section a real consumer.

**How:**
1. Create `.github/workflows/webhook-runner.yml` that listens to `repository_dispatch` events with `event_type: aeon-skill`; reads `github.event.client_payload.skill` and `client_payload.var`; validates the skill name against skills.json (reject unknowns); dispatches the target skill via `gh workflow run` with optional `var` passthrough
2. Create `skills/webhook-bridge/SKILL.md` documenting the calling convention for operators: `gh api repos/{owner}/{repo}/dispatches -f event_type=aeon-skill -f client_payload[skill]=token-report -f client_payload[var]="optional"` — plus worked examples for Zapier (webhook step), n8n (HTTP Request node), and GitHub Actions (`repository_dispatch` cross-repo trigger)
3. Register `webhook-bridge: { enabled: false, schedule: "workflow_dispatch" }` in aeon.yml; bump skills.json; document HMAC secret validation pattern for callers that support it

---

### 5. Bluesky Column
**Type:** Integration
**Effort:** Small (hours)
**Repo:** aaronjmars/minitor

**Impact:** Bluesky/AT Protocol has become the primary developer-adjacent social network as X's API costs pushed researchers and builders to migrate. The `api.bsky.app` public REST API is fully keyless for reading public feeds — unlike X which now requires a paid developer account. AI researchers post paper reactions, tool announcements, and ecosystem hot takes on Bluesky hours before the same content appears on HN. Adding Bluesky gives minitor a live developer social signal no existing column type covers.

**How:**
1. Fetch from AT Protocol REST API: `api.bsky.app/xrpc/app.bsky.feed.searchPosts?q={keyword}&limit={n}` for search mode (no auth, public); `app.bsky.feed.getAuthorFeed?actor={handle}` for profile mode; `app.bsky.feed.getFeed?feed=at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot` for trending mode
2. 3-file plugin with `#0085FF` Bluesky blue accent, `CloudSun` icon; row shows: handle, text snippet (140 chars), like + repost counts, timestamp; 3 modes: `search` (keyword/hashtag), `profile` (specific handle's feed), `trending` (what's-hot curator feed); `fetchBlueskyPosts` in `lib/integrations/bluesky.ts`
3. 3 registry edits + README News & web cluster 9 → 10, count 42 → 43; integration quirks: (1) AT Protocol `uri` uses `at://` scheme — reconstruct `bsky.app` permalink from DID + rkey; (2) image embeds in `embed.images[]` — show count badge only, no inline render; (3) quote posts include a nested `record` — display the outer text only, mark as "↩ quote" in UI
