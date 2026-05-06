# Repo Action Ideas — 2026-05-06

Generated from analysis of aaronjmars/aeon (276⭐, 43 forks), aaronjmars/aeon-agent (7⭐, 1 fork), and aaronjmars/minitor (7⭐, 1 fork).

---

### 1. star-milestone skill
**Type:** Feature
**Effort:** Small (hours)
**Impact:** star-momentum-alert (aeon PR #159, May 5) explicitly defers post-crossing celebrations to a `star-milestone` skill that doesn't exist yet. At 276⭐ growing at ~6/day, the 300-star milestone is ~4 days away — the notifier needs to exist before the moment arrives. Fires one tailored celebration notification per (repo, milestone) pair on first crossing, state in `memory/topics/star-milestone-state.json`. Pairs with show-hn-draft (already written, waiting for dispatch signal) to make the milestone a media event, not a quiet counter tick.
**How:**
1. Add `skills/star-milestone/SKILL.md` — daily cron (after repo-pulse), reads last 7 days of `memory/logs/YYYY-MM-DD.md` repo-pulse blocks for each watched repo, checks `stargazers_count` against milestone targets (300, 500, 1000, 2500, 5000), fires notify on first crossing with celebration copy + Show HN timing cue, deduplicates via state JSON keyed on `(repo, milestone)`.
2. Register in `aeon.yml` (enabled: false, daily 10:15 UTC after repo-pulse), bump `skills.json` total.
3. Enable `star-momentum-alert` alongside it — the two skills form a complete milestone pipeline: momentum-alert times the approach, star-milestone fires the crossing.

---

### 2. Reddit column (minitor)
**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** Reddit is the primary discussion forum for AI agents, crypto, and programming — the exact audience watching Aeon. minitor has social (X, Bluesky, Mastodon, Farcaster), news (HN, Lobsters, RSS), and on-chain (wallet-tx, Polymarket) but no Reddit surface. The public JSON API (`https://reddit.com/r/{subreddit}.json`) is fully keyless (no OAuth needed for read-only public feeds), returns posts with title, author, score, num_comments, and permalink. Fills the last major community-signal gap before minitor's social cluster is complete.
**How:**
1. Add `plugins/reddit/` — integration layer handles `.json` suffix fetch with four modes: `hot` / `new` / `rising` / `top` (+ optional `time_filter: hour|day|week|month|year` for top). Zod config `{ subreddit, mode: 'hot'|'new'|'rising'|'top', timeFilter?, limit? }`. Schema-drift safe: drop posts missing `id` or `title`. Respect Reddit's crawl-delay via `User-Agent: minitor/1.0` header.
2. Standard 3-file plugin + 3 registry edits (manifest, registry, server-registry). Score icon (ArrowUp), brand orange `#ff4500` distinct from HN orange `#ff6600` so the two community-news columns stay visually differentiated. Renderer matches Lobsters' serif-title-with-hover treatment with score/comments footer. `flair` shown as tag pill when present.
3. Update README: column count 35 → 36, Social/News cluster row, hero paragraph picks up "Reddit communities."

---

### 3. fork-cohort backport (aeon-agent)
**Type:** Feature (backport)
**Effort:** Small (hours)
**Impact:** fork-cohort shipped to aeon on May 2 (PR #152) but hasn't been backported to aeon-agent. With 43 forks and growing, the running agent has no weekly view of which forks are POWER / ACTIVE / STALE / COLD. Matches the operator-scorecard (May 3→4) and skill-freshness (May 4→5) same-day-after-merge backport pattern — both shipped as next-morning PRs. Week-over-week delta tagging (LEVELED_UP, REVIVED, WENT_STALE, NEW_ACTIVE, WENT_COLD, NEW_FORK, DROPPED_FROM_POWER) makes the fork cohort data actionable, not just informational.
**How:**
1. Copy `skills/fork-cohort/SKILL.md` from aeon verbatim into aeon-agent. Read the current aeon version via `gh api repos/aaronjmars/aeon/contents/skills/fork-cohort/SKILL.md` to get the exact post-PR-#152 text.
2. Add to `aeon.yml`: `fork-cohort: { enabled: false, schedule: "0 19 * * 0", model: "claude-sonnet-4-6" }` (Sunday 19:00 UTC, after heartbeat). Bump `skills.json` total 57 → 58, same category as aeon (community).
3. Enable once confirmed working — first natural Sunday run May 10 if enabled today.

---

### 4. v4-readiness backport (aeon-agent)
**Type:** Feature (backport)
**Effort:** Small (hours)
**Impact:** v4-readiness shipped to aeon today (PR #160, 11:39 UTC) as a workflow_dispatch one-shot preflight checker. V4 is ~2 weeks out per operator's social posts (x.com/Mnosh06 May 5: "v4 redesign ETA 2 weeks from early May"). Backporting same-day keeps the running agent aligned with the canonical upgrade readiness tool before v4 drops. The embedded manifest (Safe / Review / Removed tables) lives inside the SKILL.md itself and travels per-fork — backporting it now means the agent has the manifest ready to be updated as v4 change PRs land upstream.
**How:**
1. Copy `skills/v4-readiness/SKILL.md` from aeon verbatim. Read via `gh api repos/aaronjmars/aeon/contents/skills/v4-readiness/SKILL.md` for the exact post-PR-#160 text (check PR is merged first; it's open as of this run).
2. Add to `aeon.yml`: `v4-readiness: { enabled: false, schedule: "workflow_dispatch", var: "" }`. Bump `skills.json` total 57 → 58 (or 59 if fork-cohort also lands), productivity category.
3. Operator dispatches manually pre-v4-announcement to seed the readiness baseline; re-dispatches after each v4 PR is merged and manifest updated.

---

### 5. thread-formatter backport (aeon-agent)
**Type:** Feature (backport)
**Effort:** Small (hours)
**Impact:** thread-formatter was built for aeon (PR #148, Apr 30) but hasn't been backported to aeon-agent. This fork runs the daily content pipeline (fetch-tweets, repo-article, project-lens, token-report) but has no auto-format-to-thread capability. With the 300-star milestone ~4 days away and show-hn-draft (also unbackported) waiting in aeon, having a paste-ready 5-tweet thread queued for the milestone moment is the difference between a prepared launch and a reactive one. The skill is pure local file I/O — reads `memory/logs/${today}.md`, picks highest-signal event via scoring table, writes `articles/thread-${today}.md`.
**How:**
1. Copy `skills/thread-formatter/SKILL.md` from aeon. Read via `gh api repos/aaronjmars/aeon/contents/skills/thread-formatter/SKILL.md`.
2. Add to `aeon.yml`: `thread-formatter: { enabled: false, schedule: "30 17 * * *", model: "claude-sonnet-4-6" }` (after 17:00 social block). Bump `skills.json` total, productivity/content category.
3. Enable once star-momentum-alert is also enabled (the two feed the same "time the launch" workflow); first natural run same evening if both enabled.
