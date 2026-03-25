# Push Recap — 2026-03-25

## Overview
2 commits by 2 authors (Aaron Elijah Mars, @aaronjmars) landed on main today. The main thrust was a major infrastructure upgrade: a json-render pipeline for converting skill output into rich dashboard cards, a Tailwind v4 migration, operational hardening across the scheduler and launcher, and three brand-new skills (github-trending, monitor-runners, token-pick).

**Stats:** 36 files changed, +3,730/-1,403 lines across 2 commits

---

## aaronjmars/aeon

### json-render Feed System
**Summary:** A full end-to-end pipeline that converts skill notification output into structured json-render specs, stores them as JSON files, and renders them in the dashboard's new Feed tab. This gives every skill a rich visual card in the dashboard without any per-skill UI work.

**Commits:**
- `f938ecf` — feat: json-render feed, Tailwind v4, operational hardening, 3 new skills
  - New file `notify-jsonrender` (+75 lines): Bash script that pipes skill markdown output through Claude Haiku with a detailed system prompt defining 15 component types (Card, Stack, Grid, Table, Stat, TweetCard, StoryLink, etc.). Validates output as JSON before writing to `dashboard/outputs/`. Works with both API key and OAuth token auth.
  - New file `dashboard/lib/catalog.ts` (+23 lines): Defines the json-render catalog using `@json-render/core` and `@json-render/shadcn` — registers 12 component types (Card, Stack, Heading, Text, Badge, Grid, Table, Button, Link, Alert, Progress, Separator) for rendering specs.
  - New file `dashboard/app/api/outputs/route.ts` (+61 lines): Next.js API route that serves stored json-render specs from the outputs directory (GET) and pulls latest from git (POST with stash/rebase logic). Returns newest-first with skill name and timestamp parsed from filenames.
  - New file `dashboard/outputs/.gitkeep`: Empty directory placeholder for json-render output files.
  - Changed `.github/workflows/aeon.yml` (+28/-4 lines): Added `JSONRENDER_ENABLED` env var from repo vars, exports `SKILL_NAME`, and added a post-run step that saves pending notification content for json-render conversion. Added `actions: read` permission. Registered 3 new skills in the workflow dispatch list.
  - Changed `aeon.yml` (+55/-141 lines): Added `channels.jsonrender.enabled: true` config section. Converted entire skills config from multi-line YAML to compact inline `{ }` format (pure formatting, no semantic changes to existing skills). Added `github-trending`, `monitor-runners`, and `token-pick` to their respective time slots.

**Impact:** Every skill that sends a notification now automatically gets a rich, structured dashboard card. The json-render pipeline is opt-in via `JSONRENDER_ENABLED` and requires zero changes to existing skills — it intercepts the notification text and converts it.

---

### Dashboard Overhaul (Tailwind v4 + UX)
**Summary:** Migrated the dashboard from Tailwind v3 to v4 (CSS-based config), redesigned the layout with a 2-column tabbed interface, and added the Feed/Runs tab for viewing json-render output.

**Commits:**
- `f938ecf` — (same commit, dashboard portion)
  - Changed `dashboard/app/page.tsx` (+372/-78 lines): Major UI rewrite — added 2-column tabbed layout (Skills/Secrets | Feed/Runs), SkillFeed component with SpecNode renderer for all 15 json-render component types, stacked skill rows, dynamic model select width, inline YAML editing for PATCH/DELETE (supports `{ }` format), Pull button with behind-count indicator, Push button with changes indicator.
  - Changed `dashboard/app/api/skills/route.ts` (+125/-65 lines): Extended the skills API to support inline YAML format parsing and editing, matching the new `{ }` config style.
  - Changed `dashboard/app/api/sync/route.ts` (+7/-1 lines): Sync API now returns a `behind` count so the UI can show how many commits behind the local copy is.
  - Changed `dashboard/app/globals.css` (+9/-3 lines): Tailwind v4 CSS-based config (replaces JS config).
  - Changed `dashboard/package.json` (+8/-6 lines): Updated Tailwind and PostCSS dependencies for v4.
  - Changed `dashboard/package-lock.json` (+2,412/-933 lines): Lockfile update for dependency changes.
  - Changed `dashboard/postcss.config.mjs` (+1/-2 lines): Simplified PostCSS config for Tailwind v4.
  - Removed `dashboard/tailwind.config.ts` (-16 lines): No longer needed — Tailwind v4 uses CSS-based config.

**Impact:** The dashboard now has a live feed of skill outputs rendered as rich cards, plus a cleaner 2-column layout for managing skills and secrets. The Tailwind v4 migration modernizes the styling infrastructure.

---

### Operational Hardening
**Summary:** Significant improvements to the scheduler, launcher, and multiple skills to handle edge cases — missed cron windows, rate limits, stale processes, and data validation.

**Commits:**
- `f938ecf` — (same commit, operations portion)
  - Changed `.github/workflows/messages.yml` (+74/-25 lines): **Scheduler rewrite** — batch-fetches all dispatched runs in a single API call (was N calls), adds `recently_dispatched()` function with 90-minute smart dedup window (was simple daily dedup), checks previous hour for catch-up when GitHub Actions misses a cron window, filters by day/month/weekday first for efficiency, supports new inline `{ }` YAML format, removes per-skill model override from scheduler (simplification), eliminates `eval` for dispatch commands.
  - Changed `aeon` launcher (+16/-4 lines): Lockfile-based stale server cleanup and loop-based port finding — prevents zombie dashboard processes from blocking new launches.
  - Changed `CLAUDE.md` (+8/-1 lines): Documents the json-render integration and `notify-jsonrender` script.
  - Changed `skills/polymarket-comments/SKILL.md` (+98/-51 lines): Rewrote to use the actual Polymarket comments API instead of scraping.
  - Changed `skills/token-movers/SKILL.md` (+23/-7 lines): Added trending endpoint as a data source.
  - Changed `skills/action-converter/SKILL.md` (+19/-12 lines): More flexible category handling and anti-repetition logic.
  - Changed `skills/paper-pick/SKILL.md` (+16/-15 lines): Switched to arXiv as primary source, gracefully skips 429 rate-limit responses.
  - Changed `skills/reply-maker/SKILL.md` (+9/-5 lines): Added memory-log fallback when primary context is unavailable.
  - Changed `skills/polymarket/SKILL.md` (+8/-5 lines): Removed unreliable liquidity endpoint, added data validation.
  - Changed `skills/startup-idea/SKILL.md` (+8/-17 lines): Added domain variation to avoid repetitive outputs.
  - Changed `skills/heartbeat/SKILL.md` (+6/-2 lines): 2-hour grace period, alias mapping, batch alerts.
  - Changed `skills/github-issues/SKILL.md` (+1/-5 lines): Skip sending notification when there are no issues (avoids empty messages).

**Impact:** The scheduler is now more resilient (catches missed windows, smarter dedup, fewer API calls), the launcher handles stale processes, and nine existing skills got reliability improvements for real-world edge cases.

---

### Three New Skills
**Summary:** Three new skills added to expand coverage into GitHub trending repos, token momentum tracking, and daily pick recommendations.

**Commits:**
- `f938ecf` — (same commit, new skills)
  - New file `skills/github-trending/SKILL.md` (+44 lines): Scrapes GitHub's trending page via WebFetch, extracts top 10 repos with stars/language/description, supports language filtering via var parameter. Scheduled at 9 AM UTC.
  - New file `skills/monitor-runners/SKILL.md` (+136 lines): Comprehensive token momentum tracker using GeckoTerminal API. Scans trending pools across 6 networks (global, Solana, ETH, Base, BSC, Arbitrum), applies quality filters (min $50k volume, buy/sell ratio, pool age), ranks by 24h price change, and provides momentum analysis for top 5 runners. Includes rate-limit handling with retry logic. Scheduled at 12 PM UTC.
  - New file `skills/token-pick/SKILL.md` (+79 lines): Daily recommendation skill that picks one token and one prediction market. Combines CoinGecko trending/market data with Polymarket volume data, cross-references against recent logs for multi-day momentum, and uses WebSearch for fresh catalysts. Scheduled at 12 PM UTC.

**Impact:** Adds three high-value daily intelligence skills — GitHub ecosystem awareness, real-time token momentum detection, and a curated daily pick combining crypto and prediction market signals.

---

### Housekeeping
**Summary:** Asset reorganization and README update.

**Commits:**
- `f938ecf` — (same commit)
  - Renamed 5 image files from root to `assets/` directory (aeon.gif, aeon.jpg, openclaw.jpg, skills.jpg, tg.png)
  - Changed `README.md` (+5/-5 lines): Updated image paths to reference `assets/` directory

- `de2071d` — Add support address to README
  - Changed `README.md` (+4/-0 lines): Added a support/donation section at the bottom with the project's Base address (0xbf8e8f0e8866a7052f948c16508644347c57aba3)

**Impact:** Cleaner repo structure with images in a dedicated directory, and a way for supporters to contribute.

---

## Developer Notes
- **New dependencies:** `@json-render/core`, `@json-render/react`, `@json-render/shadcn` (dashboard); Tailwind CSS v4 + updated PostCSS
- **Breaking changes:** Tailwind config moved from `tailwind.config.ts` to CSS-based (`globals.css`); `aeon.yml` switched to inline `{ }` format (backwards-compatible in the scheduler)
- **Architecture shifts:** json-render pipeline introduces a new output channel — skills produce markdown, Haiku converts to specs, dashboard renders them. This is a foundational piece for the dashboard becoming the primary skill output viewer.
- **Tech debt:** The `notify-jsonrender` script shells out to `claude` CLI for conversion — this works but adds latency per notification. Could be optimized with a batch approach or direct API call.

## What's Next
- All three new skills (github-trending, monitor-runners, token-pick) are registered but disabled — likely next step is enabling them and running initial tests
- The json-render feed is wired up end-to-end but needs real skill output to populate — first enabled skill run with `JSONRENDER_ENABLED=true` will be the proof point
- The scheduler's catch-up logic and 90-minute dedup window suggest preparation for more aggressive cron schedules
- Nine skills got hardening patches, suggesting they've been running in production and hitting real edge cases
