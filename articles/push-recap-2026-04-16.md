# Push Recap — 2026-04-16

## Overview
34 meaningful commits by 2 authors (Aaron @aaronjmars + Aeon aeonframework) across both repos, plus ~30 operational chores. Today's main thrust: a new Dev.to syndication pipeline, a complete README overhaul with autonomy positioning, Kalshi prediction market monitoring, notification reliability hardening, and a massive architecture sync bringing aeon-agent to full feature parity with upstream. The heaviest day of the week by lines changed.

**Stats:** ~200 files changed, +10,500/-2,100 lines across 34 meaningful commits (65 total including chores)

---

## aaronjmars/aeon

### New Feature: Dev.to Article Syndication
**Summary:** A complete content distribution pipeline that auto-cross-posts Aeon articles to Dev.to for organic developer discovery. Includes the skill definition, a sandbox-safe postprocess script, dashboard secret management, and aeon.yml registration — production-ready from day one.

**Commits:**
- `fbf2219` — feat: add syndicate-article skill
  - New file `skills/syndicate-article/SKILL.md`: Full 101-line skill definition. Parses articles from `articles/`, deduplicates against 7-day log history, maps filename patterns to Dev.to tags (crypto, opensource, research, etc.), builds canonical URLs back to GitHub Pages, posts via WebFetch with DEVTO_API_KEY. Falls back to postprocess pattern if WebFetch can't handle auth headers. (+101 lines)

- `78184d7` — feat: add postprocess-devto.sh for sandbox fallback
  - New file `scripts/postprocess-devto.sh`: Processes `.pending-devto/*.json` payloads after Claude finishes. Handles 201 (success), 422 (duplicate), and error responses. Self-cleaning — removes payloads on success and empty directories on completion. (+45 lines)

- `5270ad3` — feat: add DEVTO_API_KEY to dashboard secrets panel
  - Changed `dashboard/app/api/secrets/route.ts`: Added DEVTO_API_KEY under new "Distribution" group with description pointing to dev.to/settings/extensions. (+1 line)

- `19230c2` — feat: register syndicate-article skill in aeon.yml
  - Changed `aeon.yml`: Added syndicate-article at 3:30 PM UTC daily (Sonnet model), positioned under new "Content distribution" section after gallery update. (+3 lines)

**Impact:** Articles now reach Dev.to's 1M+ developer audience automatically. The canonical URL pattern preserves SEO attribution back to the GitHub Pages gallery. The postprocess fallback ensures delivery even when the sandbox blocks authenticated requests.

### Notification Reliability Hardening
**Summary:** Fixed a double-notification bug that caused messages to be sent twice — once immediately and once by the post-run retry step. The fix tracks actual delivery success and removes pending files when immediate delivery succeeds.

**Commits:**
- `02c38f3` — fix: prevent duplicate notifications by tracking delivery success
  - Changed `.github/workflows/aeon.yml`: Added `DELIVERED=false` tracking flag. Each channel (Telegram, Discord, Slack) now sets `DELIVERED=true` on successful HTTP response instead of silently continuing. When `DELIVERED=true`, the pending notification file is deleted before the post-run step can re-send it. Also fixed the Telegram success check logic — was checking for failure and retrying, now properly checks for success first. (+12/-4 lines)

**Impact:** Eliminates duplicate notifications that were cluttering channels. The root cause was that `.pending-notify/` files persisted even after successful immediate delivery, so the post-run step would re-send them.

### New Skill: Monitor Kalshi
**Summary:** A complete prediction market monitoring skill for Kalshi, the US-regulated prediction market exchange. Supports a watchlist-based approach with autodiscovery of trending events.

**Commits:**
- `7be3634` — feat: add monitor-kalshi skill
  - New file `skills/monitor-kalshi/SKILL.md`: 146-line skill covering the full Kalshi public API (events, markets, candlesticks). Calculates 24h price changes in percentage points, classifies direction (surging/rising/stable/falling/crashing), flags markets moving >5pp, and discovers trending untracked events. Includes WebFetch fallback for sandbox. (+146 lines)
  - New file `skills/monitor-kalshi/watchlist.md`: Empty starter watchlist with example tickers (KXGDP, KXFED, KXINFLATION). (+4 lines)
  - Changed `aeon.yml`: Registered at 1:00 PM UTC daily, Sonnet model, disabled by default. (+1 line)

**Impact:** Adds prediction market intelligence alongside the existing Polymarket monitoring. Kalshi's US-regulated status gives access to economic, political, and climate markets that complement Polymarket's crypto-heavy focus.

### README Overhaul & Repositioning
**Summary:** 14 commits completely restructuring the README — compacting from 768 to 496 lines, adding visual assets, an autonomy comparison table, and category-based skill listings. The new positioning leads with "the most autonomous agent framework" and backs it up with a feature comparison against Claude Code Background Tasks, Hermes, and OpenClaw.

**Commits:**
- `39476cf` — docs: reposition — "The most autonomous agent framework"
  - Changed `README.md`: New opening tagline and positioning statement (+8/-4 lines)

- `175c5e9` — docs: add autonomy comparison table
  - Changed `README.md`: Feature matrix comparing Aeon vs Claude Code Background Tasks, Hermes, OpenClaw across 8 dimensions (persistent memory, self-improvement, multi-channel, skill marketplace, etc.) (+18/-6 lines)

- `d87b1e9` — docs: add Hermes and OpenClaw to comparison
  - Changed `README.md`: Extended table with competitive detail

- `0c6fc00` — docs: list all skills per category, merge MCP+A2A, remove Telegram screenshot
  - Changed `README.md`: Replaced vague skill descriptions with full per-category listings (Content, DeFi/Crypto, Research, DevOps, Meta/System). Consolidated MCP and A2A into single "Integrations" section.

- `f08a013` — docs: compact README from 768 to 496 lines
  - Changed `README.md`: Major compaction pass — removed Troubleshooting, GitHub Agentic Workflow section, trimmed comparison table to top 3. Added `docs/telegram-instant.md` for moved content. (+43/-314 lines)

- `db0a965` — docs: update README for 91 skills, fix phantom references, add quality scoring
  - Changed `README.md`: Updated skill count, fixed references to renamed/removed skills (+120/-37 lines)
  - Changed `generate-skills-json`: Improved categorization logic (+44/-82 lines)
  - Changed `skills.json`: Regenerated with updated metadata (+1107/-555 lines)

- `2955dca` — docs: add autonomy, skills, architecture, stack images
  - Changed `README.md`: Added 4 visual diagrams/screenshots

- `bbdc131`, `c14502f`, `79c725a`, `921bb4c` — docs: section reordering
  - Moved sections for better narrative flow: soul+fleet after skills, integrations at bottom, authentication after skills, publishing above two-repo

- `a96d705`, `e3b4737` — assets: rename and replace skill.jpg

**Impact:** The README now tells a much tighter story: what Aeon is, why it's different (with a competitive comparison table), what it can do (91 skills listed by category), and how to get started — all in 496 lines instead of 768. The visual assets make it more scannable for GitHub browsers.

### Cross-Platform & Bug Fixes
**Summary:** Fixed platform-specific issues in the `add-skill` script and the reactive trigger parser.

**Commits:**
- `a10c52a` — fix: cross-platform add-skill aeon.yml insertion
  - Changed `add-skill`: Replaced macOS-only `sed -i ''` with cross-platform `awk` for inserting new skills into aeon.yml. The old approach used macOS-specific sed syntax that failed silently on Linux (where GitHub Actions runs). (+4/-6 lines)

- `57f127c` — fix: bash syntax error in reactive trigger parser
  - Changed `.github/workflows/messages.yml`: Fixed regex pattern `! [[ "$line" =~ ^\ ]]` which used a literal backslash-space that broke on some bash versions. Replaced with POSIX character class `^[[:space:]]`. (+1/-1 line)

**Impact:** The add-skill script now works on both macOS (local dev) and Linux (CI), and the reactive message trigger parser no longer throws syntax errors when parsing aeon.yml reactive blocks.

### A2A Gateway Hardening
**Summary:** Security and reliability improvements to the A2A Protocol Gateway that was merged in PR #35.

**Commits:**
- `edbff0d` — fix: harden A2A gateway — subprocess cleanup, memory limits, body cap
  - Changed `a2a-server/src/index.ts`: Added memory limits for spawned Claude processes, request body size caps, and proper subprocess cleanup on task cancellation. (+45/-3 lines)
  - Changed `add-a2a`: Improved install script error handling and platform detection. (+27/-15 lines)

**Impact:** The A2A gateway is now production-hardened against resource exhaustion — runaway skills can't consume unbounded memory, and cancelled tasks properly clean up their child processes.

### Fork Merge: 25 New Skills + Infrastructure
**Summary:** Merged upstream fork contributions bringing 25 new skills, workflow consolidation (removed separate scheduler.yml), and infrastructure additions.

**Commits:**
- `ba0143d` — feat: merge fork features — 25 new skills, 2-workflow simplification, quality fixes
  - Removed `.github/workflows/scheduler.yml` — consolidated into aeon.yml
  - Changed `.github/workflows/aeon.yml`: +91 lines of improvements
  - Changed `.github/workflows/messages.yml`: +419/-17 lines (major reactive trigger overhaul)
  - 25 new skills added: channel-recap, deal-flow, deploy-prototype, evening-recap, external-feature, farcaster-digest, github-releases, market-context-refresh, narrative-tracker, polymarket-comments, project-lens, reg-monitor, repo-scanner, self-improve, skill-leaderboard, skill-repair, telegram-digest, tool-builder, tweet-roundup, unlock-monitor, vercel-projects, vibecoding-digest, vuln-scanner, weekly-shiplog, token-report
  - Removed 7 outdated skills: build-skill, feature, hn-digest, memory-flush, polymarket, self-review, trending-coins, tweet-digest, wallet-digest
  - Added `soul/SOUL.md` and `soul/STYLE.md` templates
  - Added utility scripts: postprocess-replicate.sh, prefetch-xai.sh, skill-runs

**Impact:** The skill catalog jumps past 90 with this merge. The workflow consolidation from 3 files to 2 simplifies CI maintenance. New skills cover DeFi monitoring (unlock-monitor, market-context-refresh), content channels (farcaster, telegram), security (vuln-scanner, reg-monitor), and operations (skill-repair, fleet-control).

---

## aaronjmars/aeon-agent

### Architecture Sync: Full Feature Parity
**Summary:** A massive sync commit bringing aeon-agent up to feature parity with the upstream aeon repo. This is the single largest commit of the day, touching 110+ files across every layer of the system.

**Commits:**
- `def708b` — feat: sync boilerplate features — full architecture upgrade
  - New: A2A server (`a2a-server/src/index.ts`, 578 lines), MCP server (`mcp-server/src/index.ts`, 224 lines), chain runner workflow (`chain-runner.yml`, 338 lines)
  - New: Dashboard components overhaul — decomposed monolithic `page.tsx` (1531 lines removed) into 11 focused components (AuthModal, HQOverview, LeftSidebar, RightPanel, ScheduleEditor, SecretsPanel, SkillDetail, SpecNode, TopBar, TargetCursor) totaling ~1,100 lines
  - New: GitHub Pages docs site (`docs/` — Jekyll config, layouts, initial posts, data files)
  - New: 30+ skill definitions synced from upstream
  - New: Utility scripts (generate-feed.sh, sync-site-data.sh, sync-upstream.sh, skill-runs)
  - New: Install scripts (add-a2a, add-mcp, export-skill, generate-skills-json)
  - Changed: `CLAUDE.md` updated with skill chaining docs (+58/-9 lines)
  - Changed: `aeon.yml` expanded with new skill registrations (+69/-6 lines)
  - Changed: Dashboard CSS overhaul (+199/-10 lines)

- `9f77807` — docs: sync README and assets from upstream aeon
  - Synced the overhauled README and visual assets downstream

**Impact:** aeon-agent is now a fully-featured Aeon instance — same A2A/MCP integrations, same dashboard, same skill catalog, same docs site. This eliminates the feature gap between the upstream template repo and the operator instance.

### Heartbeat Escalation System
**Summary:** Replaced the flat 48h dedup logic in heartbeat with a tiered system that escalates persistent unfixed issues instead of silently suppressing them.

**Commits:**
- `d335bdb` — improve: add escalation logic to heartbeat for persistent issues
  - Changed `skills/heartbeat/SKILL.md`: New "Dedup & Escalation Rules" section with 3-tier logic: (1) 48h dedup for transient issues, (2) escalation override for issues persisting 3+ consecutive days, (3) batch grouping. Key fix: dedup now checks whether a *notification* was sent (not just whether the issue was *logged*), which was the root cause of persistent issues being silently suppressed. (+16/-2 lines)

**Impact:** The heartbeat skill was logging project-lens and weekly-shiplog failures for 3+ days but never re-notifying because the dedup check looked at log entries (which heartbeat writes every run) instead of notification records. Now persistent issues get escalated with an `ESCALATION:` prefix after 3 days.

### Notification Fix + Cleanup
**Summary:** Same duplicate notification fix as the aeon repo, plus cleanup of stale files.

**Commits:**
- `cd43f48` — fix: prevent duplicate notifications, clean up stale files
  - Changed `.github/workflows/aeon.yml`: Same DELIVERED tracking logic as the aeon fix (+12/-4 lines)
  - Removed `build-target`: Stale subproject commit reference
  - Removed `test-model.yml`: Leftover test file

### Schedule Changes
**Summary:** Both repo-article and project-lens upgraded from intermittent schedules to daily runs.

**Commits:**
- `64cb37f` — feat: make repo-article and project-lens daily
  - Changed `aeon.yml`: project-lens from Mon/Wed/Fri to daily. repo-article from every-2-days on even weekdays to daily. (+2/-2 lines)

**Impact:** project-lens was missing scheduled runs (flagged by heartbeat for 3+ consecutive days as non-dispatching). Making it daily eliminates the complex alternating schedule that was causing dispatch failures. repo-article benefits from the same simplification.

### Other Fixes
- `0f701e9` — fix: bash syntax error in reactive trigger parser (same `[[:space:]]` fix as aeon)
- `198a7f4` + `03197e7` — heartbeat dispatch test and revert (temporarily scheduled heartbeat at 19:20 UTC to verify dispatch was working, then restored)

---

## Developer Notes
- **New dependencies:** None (syndicate-article uses WebFetch + postprocess pattern, monitor-kalshi uses public API)
- **Breaking changes:** `scheduler.yml` removed from aeon (consolidated into aeon.yml) — forks using the old 3-workflow setup need to update
- **Architecture shifts:** aeon-agent dashboard decomposed from monolithic 1531-line page.tsx into 11 focused components — significant maintainability improvement
- **Tech debt:** Soul files (SOUL.md, STYLE.md) are still template-only — voice customization not yet configured

## What's Next
- syndicate-article skill is registered but disabled by default — needs DEVTO_API_KEY secret configured to activate
- monitor-kalshi watchlist is empty — needs event tickers added to start monitoring
- The 25 newly merged skills are registered in aeon.yml but most are disabled — selective enablement based on operator priorities
- project-lens and repo-article are now daily — first daily runs will validate the schedule fix flagged by heartbeat
- A2A gateway is merged and hardened — ready for external agent integrations
