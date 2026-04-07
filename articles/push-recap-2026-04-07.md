# Push Recap — 2026-04-07

## Overview
A massive build day on 2026-04-06 across both `aaronjmars/aeon` and `aaronjmars/aeon-agent`. The main repo got a full dashboard redesign (Hyperstitions/Evangelion aesthetic), three new skills (monitor-polymarket, remix-tweets, technical-explainer), a standalone scheduler workflow, upstream skill-sync tooling, and four merged PRs. The agent repo picked up critical reliability fixes — unpushed-commit detection, expanded tweet search, and model-cost optimization.

**Stats:** ~85 files changed, +3,200 / −2,600 lines across 12 meaningful commits (plus automated chores)

---

## aaronjmars/aeon

### Dashboard Overhaul: Hyperstitions Design System
**Summary:** The dashboard received a complete aesthetic redesign porting the Evangelion-inspired "Hyperstitions" design system — sharp corners everywhere, a LoadingHUD spinner, a TargetCursor effect, and a 1.4x-scaled grid/stripe/scrollbar system. Alongside the visual changes, the scheduling logic was extracted from `messages.yml` into a dedicated `scheduler.yml` workflow, and the broken `test-skills.yml` was removed.

**Commits:**
- `2372300` — feat: redesign dashboard with Hyperstitions design system
  - Changed `dashboard/app/page.tsx`: Rewrote from ~1531 lines down to ~612 — removed dead state, added skills search bar, feed-to-runs fallback (+612, −1531)
  - Changed `dashboard/app/globals.css`: Full theme overhaul — sharp corners, updated scrollbar, grid pattern at 1.4x scale (+199, −10)
  - Added `dashboard/components/ui/TargetCursor.tsx` + `TargetCursor.css`: Interactive cursor that tracks mouse position with a crosshair ring effect (+344 lines)
  - Added `dashboard/lib/config.ts`: Centralized dashboard configuration (+180 lines)
  - Changed `dashboard/app/layout.tsx`: Applied new font and metadata (+19, −6)
  - Changed `dashboard/package.json` + `package-lock.json`: Added new dependency for cursor component

- `2372300` (same commit) — Workflow restructure:
  - Added `.github/workflows/scheduler.yml`: New dedicated 5-minute cron scheduler — moved scheduling logic out of `messages.yml` entirely (+280 lines)
  - Changed `.github/workflows/messages.yml`: Removed the now-redundant schedule job (−157 lines)
  - Changed `.github/workflows/aeon.yml`: Switched skill dropdown from `type: choice` to free-text input (removes need to maintain dropdown list, +117/−66)
  - Changed `aeon.yml`: Minor config cleanup (+6/−9)
  - Removed `.github/workflows/test-skills.yml`: Broken workflow (missing smoke.sh) removed to keep CI clean

**Impact:** The dashboard now has a distinctive visual identity matching the project's aesthetic. The scheduler refactor makes the cron system easier to extend — adding a new scheduled skill no longer requires touching the workflow dropdown list.

---

### New Skills: Polymarket Monitor, Remix Tweets, Technical Explainer
**Summary:** Three new skills ported from `aeon-aaron` (a sister fork): a targeted Polymarket market watcher, a tweet-remixing content engine, and a visual technical explainer that generates hero images via Replicate.

**Commits:**
- `0f57a24` — feat: add monitor-polymarket, remix-tweets, technical-explainer skills
  - Added `skills/monitor-polymarket/SKILL.md` (+141 lines): Monitors specific prediction markets by event slug for 24h price moves, volume changes, and fresh comments. Reads a watchlist from `skills/monitor-polymarket/watchlist.md`
  - Added `skills/monitor-polymarket/watchlist.md` (+3 lines): Stub watchlist (one slug per line)
  - Added `skills/remix-tweets/SKILL.md` (+125 lines): Fetches 10 random past tweets from the account, generates 10 new rephrased versions in the same voice — content recycling engine
  - Added `skills/technical-explainer/SKILL.md` (+132 lines): Auto-selects a recent article topic, generates a visual explanation using Replicate for a hero image
  - Changed `aeon.yml`: Added model override comment, added per-skill model config documentation
  - Changed `.github/workflows/aeon.yml`: Added `deep-research`, `monitor-polymarket` to dispatch dropdown (+7 lines)
  - Removed `.github/workflows/test-skills.yml`: Same broken workflow (duplicate removal across two commits)

**Impact:** Polymarket monitoring is now specific rather than broad — the watchlist-based approach lets the agent track a curated set of markets rather than the generic top-20. The remix-tweets skill closes a gap in content velocity: existing material gets repurposed automatically.

---

### Miroshark Port: Workflow Hardening + Repo Intelligence Suite
**Summary:** Battle-tested improvements from a production fork (`miroshark-aeon`) were merged in: Telegram 4000-char truncation with Markdown fallback, explicit Claude CLI error capture, a SKILL_MODEL sed parsing fix, unpushed-commit detection, and schedule dedup window widening. This commit also introduced four new "repo intelligence" skills.

**Commits:**
- `21201d3` — feat: port battle-tested improvements from miroshark-aeon
  - Changed `.github/workflows/aeon.yml`: 
    - Telegram notify: truncates messages to 4000 chars (API limit), falls back from Markdown to plain text on failure
    - Claude CLI: wraps call in `if !` to capture stderr and fail explicitly
    - SKILL_MODEL sed: strips trailing `}` and `"` from YAML parse (was silently passing bad model names)
    - Unpushed-commit detection: after Claude's run, checks `git rev-list origin/main..HEAD` — if commits were made but never pushed, pushes them
    - Schedule dedup window: 90 → 150 min (handles edge case where two runs start ~2 hours apart)
    - SKILL_VAR env export: cleaner export pattern (+43, −8)
  - Changed `.github/workflows/messages.yml`: Added stderr capture, explicit Claude CLI failure (+9, −5)
  - Added `skills/push-recap/SKILL.md` (+126 lines): Deep git diff analysis skill with themed article generation
  - Added `skills/repo-article/SKILL.md` (+84 lines): Writes narrative articles about current repo state and vision
  - Added `skills/repo-actions/SKILL.md` (+97 lines): Generates 5 actionable improvement ideas per run
  - Added `skills/repo-pulse/SKILL.md` (+90 lines): Daily star/fork tracking with O(1) stargazer API optimization
  - Changed `aeon.yml`: Added "Repo intelligence" block scheduling all 4 new skills at 3 PM UTC (+6)

**Impact:** The SKILL_MODEL sed bug fix is high-priority — it was silently passing malformed model names to Claude, potentially causing failures or using the wrong model. Unpushed-commit detection closes the gap where Claude commits during a run but the workflow exits before pushing those commits (the bug this repo's `aeon-agent` also had until today).

---

### Skill Versioning & Upstream Sync Tools
**Summary:** Skills now track their own version via SHA hash and date in `skills.json`. A new `scripts/sync-upstream.sh` script and `sync-check` skill let any Aeon fork compare its installed skills against upstream and pull updates.

**Commits:**
- `2d77e5a` — feat: skill versioning and upstream sync tools (PR #11)
  - Changed `generate-skills-json`: Added `get_skill_sha()` (7-char git SHA of last commit touching `SKILL.md`) and `get_skill_updated()` (YYYY-MM-DD date) — both fields now included in `skills.json` output (+15, −1)
  - Added `scripts/sync-upstream.sh` (+153 lines): Interactive/auto/dry-run bash script to compare fork's skills against `aaronjmars/aeon`. Modes: `--auto` (update all outdated), `--dry-run` (preview), `--missing` (also install absent skills)
  - Added `skills/sync-check/SKILL.md` (+71 lines): Aeon-native skill that fetches upstream `skills.json`, compares SHAs, reports outdated/missing skills, and optionally triggers sync

- `26e2d64` — Merge PR #11 feat/skill-versioning-sync

**Impact:** Forks can now self-maintain by running `sync-check` periodically. This is the foundation for a "skill update" notification system — forks get told when upstream has a newer version of a skill they're running.

---

### PR Merges: Deep Research & Skill Smoke Tests
**Summary:** Two pending PRs were merged: deep-research (comprehensive multi-source synthesis skill) and skill-smoke-tests (CI validation for SKILL.md files), with a quick fix to `actions/checkout@v4` (v5 doesn't exist).

**Commits:**
- `9f94e27` — Merge PR #9 feat/deep-research-skill: 30–50 source synthesis, 3K–5K words, shallow/deep modes via `--depth` flag
- `e7a0384` — Merge PR #10 feat/skill-smoke-tests: Static SKILL.md validator + CI workflow
- `7e6e235` — fix: use actions/checkout@v4 (v5 does not exist) — CI fix that unblocked smoke tests merge

**Impact:** Deep research and skill smoke tests are now live on main. Every PR touching `skills/` will now run static validation before merging.

---

## aaronjmars/aeon-agent

### Reliability: Push Unpushed Commits Fix
**Summary:** Fixed a silent failure mode where commits made by Claude during a skill run were never pushed because the commit step exited early when it found no staged changes.

**Commits:**
- `e19a47c` — fix: push unpushed commits from Claude's session
  - Changed `.github/workflows/aeon.yml`: Replaced `git diff --staged --quiet && exit 0` with a two-step check — if staged is clean, then check `git rev-list origin/main..HEAD --count`. If any unpushed commits exist, push them before exiting (+11, −2)

**Impact:** Skills that write files and commit internally (like heartbeat, memory-flush) were previously leaving commits in the local state, never synced to remote. This fix ensures every run's work actually persists.

---

### Fetch Tweets: GitHub Repo Mentions Added
**Summary:** Extended the tweet search scope to include mentions of the GitHub repo URL, not just the AEON token ticker.

**Commits:**
- `327345c` — fetch-tweets: also search for GitHub repo mentions
  - Changed `aeon.yml`: Updated `fetch-tweets` var from `"AEON crypto token on Base chain"` to `"AEON crypto token on Base chain AND https://github.com/aaronjmars/aeon"` (+1, −1)

**Impact:** The daily tweet search will now surface developer/builder mentions of the repo alongside the token community — a broader signal for both market activity and organic developer interest.

---

### Cost Optimization: Sonnet for repo-actions
**Commits:**
- `363fb71` — config: add sonnet model override for repo-actions
  - Changed `aeon.yml`: Added `model: "claude-sonnet-4-6"` to the `repo-actions` skill — aligns with pattern of using sonnet for data-collection skills and saving opus for creative/synthesis work (+1, −1)

---

## Developer Notes
- **New dependencies:** One dashboard package added (cursor effect library) — see `dashboard/package.json`
- **Breaking changes:** `aeon.yml` skill dropdown switched from `type: choice` to free-text in `aeon.yml` — dispatch now accepts any skill name, no more dropdown maintenance
- **Architecture shifts:** Scheduler extracted into its own `scheduler.yml` workflow — cleaner separation from the messaging/command-handling logic in `messages.yml`
- **Removed skills:** `hacker-news-digest`, `polymarket-comments`, `search-papers`, `sync-check` removed from aeon main (sync-check temporarily, then re-added via PR #11)
- **Tech debt:** `sync-check` skill was added then removed in the same day's commits — appears to have been an ordering issue between the dashboard commit (which removed it) and the versioning PR (which re-added it)

## What's Next
- Polymarket monitor `watchlist.md` is empty — needs event slugs populated to be useful
- `sync-check` skill can now run automatically to keep forks current; likely to be scheduled
- Deep research skill is live — candidate for scheduling on high-signal topics (new papers, breaking events)
- Skill smoke tests are merged and active — next PR touching skills/ will validate the CI works end-to-end
- Unpushed commit fix in aeon-agent mirrors the same fix already in aeon; both forks now have it
