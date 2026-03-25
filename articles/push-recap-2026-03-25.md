# Push Recap — 2026-03-25

## Overview
35 commits by 4 authors (Aaron Elijah Mars, @aaronjmars, github-actions[bot], Aeon) landed across both watched repos today. The biggest story: the **aeon-agent repo was born** — a full fork/spinoff of the agent codebase with its own dashboard, skills, workflows, and memory system, seeded with 11,000+ lines in its initial commit. On the aeon side, a massive commit delivered the json-render feed pipeline, Tailwind v4 migration, scheduler hardening, and three new skills. Both repos saw heavy automated skill activity throughout the day.

**Stats:** ~130 files changed, +15,400/-1,470 lines across 35 commits

---

## aaronjmars/aeon

### json-render Feed System + Dashboard Overhaul
**Summary:** A full end-to-end pipeline that converts skill notification output into structured json-render specs and renders them in the dashboard's new Feed tab. Combined with a Tailwind v3-to-v4 migration and a redesigned 2-column tabbed layout.

**Commits:**
- `f938ecf` — feat: json-render feed, Tailwind v4, operational hardening, 3 new skills
  - New file `notify-jsonrender` (+75 lines): Bash script that pipes skill markdown through Claude Haiku with a system prompt defining 15 component types (Card, Stack, Grid, Table, Stat, TweetCard, StoryLink, etc.). Validates JSON before writing to `dashboard/outputs/`. Works with both API key and OAuth token.
  - New file `dashboard/lib/catalog.ts` (+23 lines): Registers 12 json-render component types using `@json-render/core` and `@json-render/shadcn`.
  - New file `dashboard/app/api/outputs/route.ts` (+61 lines): API route serving stored json-render specs with git-pull refresh capability.
  - Changed `dashboard/app/page.tsx` (+372/-78 lines): Major UI rewrite — 2-column tabbed layout (Skills/Secrets | Feed/Runs), SpecNode renderer for all 15 component types, inline YAML editing, Pull/Push buttons with status indicators.
  - Changed `dashboard/app/api/skills/route.ts` (+125/-65 lines): Extended to support inline `{ }` YAML format parsing.
  - Removed `dashboard/tailwind.config.ts`, updated CSS config for Tailwind v4.

**Impact:** Every skill notification now automatically gets a rich visual dashboard card. The dashboard becomes a real-time feed viewer, not just a config panel.

---

### Operational Hardening
**Summary:** Significant resilience improvements across the scheduler, launcher, and nine existing skills.

**Commits:**
- `f938ecf` — (same commit, operations portion)
  - Changed `.github/workflows/messages.yml` (+74/-25 lines): Batch-fetches all dispatched runs in 1 API call (was N), 90-minute smart dedup window, catch-up logic for missed cron windows, day/month/weekday filtering.
  - Changed `aeon` launcher (+16/-4 lines): Lockfile-based stale server cleanup, loop-based port finding — prevents zombie dashboard processes.
  - Changed 9 skill files: `polymarket-comments` (actual API instead of scraping), `token-movers` (trending endpoint), `action-converter` (flexible categories, anti-repetition), `paper-pick` (arXiv primary, 429 handling), `reply-maker` (memory-log fallback), `polymarket` (removed unreliable endpoint), `startup-idea` (domain variation), `heartbeat` (2h grace, batch alerts), `github-issues` (skip empty notifications).

**Impact:** The scheduler is more resilient, the launcher handles stale processes, and nine skills got real-world edge case fixes.

---

### Three New Skills
**Summary:** GitHub trending repos, token momentum tracking, and daily pick recommendations.

**Commits:**
- `f938ecf` — (same commit, new skills)
  - New file `skills/github-trending/SKILL.md` (+44 lines): Scrapes GitHub trending page, extracts top 10 repos with metadata.
  - New file `skills/monitor-runners/SKILL.md` (+136 lines): Token momentum tracker across 6 GeckoTerminal networks with quality filters.
  - New file `skills/token-pick/SKILL.md` (+79 lines): Daily curated pick combining CoinGecko trending + Polymarket volume data.

**Impact:** Three high-value intelligence skills for ecosystem awareness, token momentum, and daily recommendations.

---

### Housekeeping
**Commits:**
- `f938ecf` — Renamed 5 images from root to `assets/` directory, updated README paths.
- `de2071d` — Add support address to README
  - Changed `README.md` (+4 lines): Added support/donation section with the project's Base address (0xbf8e...aba3).

---

## aaronjmars/aeon-agent

### New Repo: aeon-agent Born
**Summary:** The aeon-agent repository was created today as a standalone agent deployment. The initial commit seeds the entire codebase — workflows, dashboard, 45+ skills, memory system, articles, and configuration — in a single 11,234-line commit.

**Commits:**
- `96abb8a` — Initial commit
  - New `.github/workflows/aeon.yml` (+342 lines): Full skill dispatcher workflow with cron triggers, model selection, and json-render support.
  - New `.github/workflows/messages.yml` (+500 lines): Message polling and scheduler workflow with batch run fetching and smart dedup.
  - New `dashboard/` (full Next.js app, ~5,000+ lines): Complete dashboard with skills management, secrets UI, feed viewer, run logs, import/upload endpoints.
  - New `skills/` (45+ skill files): All skills from the parent repo — from `morning-brief` to `write-tweet`, covering digests, monitoring, social, DeFi, code health, and more.
  - New `memory/` system: MEMORY.md index, watched-repos.md (tracking both aaronjmars/aeon and aaronjmars/aeon-agent), logs directory.
  - New `aeon.yml` (+87 lines): Full skill configuration with schedules, all skills disabled by default except heartbeat.
  - New `CLAUDE.md` (+73 lines): Agent instructions, tool docs, security rules.

**Impact:** A fully operational second agent deployment. Self-contained — can run independently from the parent aeon repo with its own schedule, config, and memory.

---

### Three New Self-Referential Skills
**Summary:** Added skills that make the agent self-aware: tracking its own repos' growth, generating reflexive prediction market ideas, and improving itself from its own logs.

**Commits:**
- `d782ea2` — feat: add repo-pulse, hyperstitions-ideas, self-improve skills + disable TG polling
  - New file `skills/repo-pulse/SKILL.md` (+77 lines): Daily stars/forks/traffic tracker for watched repos using GitHub API. Fetches stargazers with timestamps, recent forks, traffic views/clones, and top referrers. Calculates deltas against previous logged values. Skips notification if no new activity.
  - New file `skills/hyperstitions-ideas/SKILL.md` (+81 lines): Generates prediction market ideas from live signals — repo activity, tweet data, token movements. Scores ideas on reflexivity (does the market's existence change the outcome?) and viral potential. Only notifies if both scores are 3+/5.
  - New file `skills/self-improve/SKILL.md` (+85 lines): Reads the last 24h of logs, identifies failing or low-quality skills, picks one improvement, implements it, creates a branch, opens a PR. The agent improving itself autonomously.
  - Changed `.github/workflows/messages.yml` (+20/-23 lines): **Disabled Telegram polling** — commented out the entire TG getUpdates block. Outbound notifications still work; only inbound message polling is off.
  - Changed `aeon.yml` (+6/-1 lines): Scheduled all three new skills — repo-pulse at 10 AM, hyperstitions-ideas at 3:30 PM, self-improve at 5 PM UTC.
  - Changed `memory/watched-repos.md` (+1 line): Added `aaronjmars/aeon-agent` — the agent now watches itself.

**Impact:** The agent gains self-monitoring (repo-pulse), creative ideation (hyperstitions-ideas), and autonomous self-improvement (self-improve). Disabling TG polling removes a source of accidental triggers while keeping outbound notifications functional.

---

### Richer Notifications + Social Fixes
**Summary:** Major upgrade to notification quality across the feature skill and fetch-tweets, plus a README overhaul documenting what Aeon actually does.

**Commits:**
- `3863a2d` — feat: richer notifications, fetch-tweets fix, README overhaul
  - Changed `skills/feature/SKILL.md` (+91/-25 lines): Complete rewrite. Feature skill now targets the **watched repo** (not the agent itself), clones it to `/tmp/build-target`, implements features, pushes branches, and opens PRs on the watched repo. Notification format expanded from 3-4 lines to a detailed template with sections for what was built, why it matters, what changed, how it works, and what's next. Includes a "BAD example" and "GOOD example" to enforce quality. Picks ideas from repo-actions output first.
  - Changed `skills/fetch-tweets/SKILL.md` (+34/-16 lines): Replaced `@handle` with `x.com/handle` format (avoids tagging users on Telegram). Added clickable `[View tweet](URL)` links. Search prompt now includes chain name and contract address to eliminate false matches. Removed the cashtag-specific section in favor of a more general "build the search prompt" approach.
  - Changed `README.md` (+20/-1 lines): Added "What Aeon does" section explaining all capabilities in plain language — push recaps, repo articles, token tracking, social monitoring, action ideas, auto-building features, and the memory system. Added repo-actions, repo-article, and token-report to the skills table.
  - Changed `aeon.yml` (+1/-1 lines): Updated fetch-tweets var from `"cashtag aeon OR $aeon token"` to `"AEON crypto token on Base chain"` for more precise search.

**Impact:** Feature skill now properly targets watched repos instead of the agent itself. Notifications are dramatically richer — enforced with examples. Tweet search is more precise with chain/contract context.

---

### Automated Skill Runs
**Summary:** 20+ auto-commits from github-actions[bot] show the agent running at full capacity throughout the day — skills firing on schedule and committing their outputs.

**Commits (sample):**
- `6eccb2b`, `08269b7`, `21d021d`, `e5c2189` — push-recap (4 runs)
- `bc5fb54`, `161fd24`, `b73e52e` — fetch-tweets (3 runs)
- `3222400`, `2623ba0`, `0c09be1` — feature (3 runs)
- `c19c543`, `f803300` — token-report (2 runs)
- `23e7b01`, `19f531a`, `5cf3257` — repo-actions (3 runs)
- `8ca90ec`, `de76b9e` — repo-article (2 runs)
- `ffe97ea`, `45a2909` — hyperstitions-ideas (2 runs)
- `6450898` — polymarket (1 run)
- `ba916a8` — repo-pulse (1 run)
- `2af4fac` — memory-flush (1 run)
- `741caea` — log: skill run analytics dashboard built for aaronjmars/aeon
- `4d48b1c` — chore(feature): log status skill build to memory and logs

**Impact:** The agent is fully operational — 12 different skills ran autonomously, producing articles, reports, and analysis. The feature skill successfully built an analytics dashboard for the watched repo.

---

### Dashboard Config Updates
**Commits:**
- `9aae629`, `6cbcffd`, `0373143`, `2115ed0`, `74039d2`, `eac6496` — 6 config updates from dashboard
  - These are incremental aeon.yml changes made through the dashboard UI (enabling/disabling skills, adjusting schedules).

---

## Developer Notes
- **New dependencies:** `@json-render/core`, `@json-render/react`, `@json-render/shadcn` (aeon dashboard); Tailwind CSS v4
- **Breaking changes:** Tailwind config moved from JS to CSS; `aeon.yml` switched to inline `{ }` format; Telegram inbound polling disabled on aeon-agent
- **Architecture shifts:** json-render pipeline is a new output channel — markdown in, structured dashboard cards out. The aeon-agent repo creates a second independent agent deployment watching the same repos.
- **Tech debt:** `notify-jsonrender` shells out to `claude` CLI per notification (adds latency). The feature skill clones watched repos to `/tmp` — no caching between runs.

## What's Next
- The three new self-referential skills (repo-pulse, hyperstitions-ideas, self-improve) are now scheduled — first real runs will test whether the agent can meaningfully track its own growth, generate reflexive ideas, and improve itself
- 20+ auto-commits show the agent is running hot — next step is likely analyzing skill output quality and tuning underperforming skills
- The json-render feed on aeon needs real output to populate — first `JSONRENDER_ENABLED=true` run will prove the pipeline end-to-end
- Telegram polling is disabled — if inbound messaging is needed, Discord or Slack channels are the fallback
- The aeon-agent repo is watching itself (`aaronjmars/aeon-agent` in watched-repos.md), creating a self-referential monitoring loop
