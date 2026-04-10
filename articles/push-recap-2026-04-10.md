# Push Recap — 2026-04-10

## Overview

11 commits across 2 repos (aaronjmars/aeon + aaronjmars/aeon-agent) from 2 authors (Aaron Elijah Mars, aeonframework). The main thrust: Aeon gets its first quality assertion layer with the merged skill-evals framework, the push race condition that caused concurrent runner collisions is fixed with jitter+backoff, and the skill scheduler is simplified from a 3-day rotation cycle to a daily-first model. The rest of the commits are normal operational auto-commits logging the day's skill runs.

**Stats:** ~15 files changed, +411 / -19 lines across 11 commits

---

## aaronjmars/aeon

### New System: Skill Evals — Output Quality Assertion Framework

**Summary:** PR #27 landed, adding the first automated output quality layer to Aeon. The `skill-evals` skill validates recent skill output files against per-skill assertion manifests — checking word counts, required/forbidden patterns, and numeric range constraints — giving the agent a way to detect regressions in its own output before users notice them.

**Commits:**
- `4c4cc8b` — Merge pull request #27 from aaronjmars/feat/skill-evals
  - New file `skills/skill-evals/SKILL.md` (+96 lines): Full skill implementation — reads `evals.json`, finds the most recent output file per skill, runs word-count checks, required/forbidden pattern searches, and numeric range assertions. Classifies each skill as PASS, FAIL, QUALITY_DEGRADED, or NO_COVERAGE. Detects production skills not yet in evals.json ("coverage gaps"). Writes a full report to `articles/skill-evals-{date}.md`.
  - New file `skills/skill-evals/evals.json` (+102 lines): Assertion manifests for 14 skills: heartbeat, repo-pulse, changelog, push-recap, fork-fleet, cost-report, repo-article, repo-actions, deep-research, hn-digest, rss-digest, polymarket, token-alert, skill-health. Each entry specifies an output glob pattern, minimum word count, required patterns (pipe-separated alternatives), forbidden patterns (placeholder strings), and optional numeric range checks (e.g. probability must be 0–100%).
  - Modified `aeon.yml` (+1 line): Registered `skill-evals` at `0 6 * * 0` (Sunday 6 AM UTC, `claude-sonnet-4-6`, currently `enabled: false`).

**Impact:** This is Aeon's QA layer. Until now, skill outputs were only validated by human inspection. The evals framework gives the agent a weekly self-check — it can detect if a skill stopped producing output, if output became too short, if required sections went missing, or if literal placeholder strings leaked into articles. The `NO_COVERAGE` classification also surfaces production skills that have no assertions at all, creating a growing backlog of coverage to close. With 14 skills covered on day one and a clear spec for adding more, this is a platform — not a one-off check.

---

### CI/CD Hardening: Push Race Condition Fixed in messages.yml

**Summary:** The messages.yml push loop was hitting concurrent runner collisions when multiple skills finished within the same minute — each runner would `git pull --rebase` and attempt to push, stepping on each other. The fix adds pre-push jitter plus exponential backoff between retries.

**Commits:**
- `46beb47` — feat: improve messages.yml push reliability
  - Modified `.github/workflows/messages.yml` (+10, -3 lines):
    - **Pre-push jitter**: Before the first push attempt, each runner now sleeps a random 0–10 seconds (`JITTER=$((RANDOM % 10))`). This spreads out concurrent runners so they don't all hit the remote simultaneously.
    - **Retries increased**: 3 → 5 attempts, giving more window for transient failures.
    - **Exponential backoff**: Between retries, wait `(2^i) + random(0–5)` seconds — approximately 2s, 4s, 8s, 16s with jitter. Was a flat zero-sleep retry loop before.
    - Failure message updated: "Failed to push after 5 attempts" (was 3).

**Impact:** This is a targeted fix for a real operational friction point. With Aeon running token-report, fetch-tweets, and repo-pulse in rapid succession in the morning, the push step was occasionally failing silently (retried out). The jitter+backoff pattern is the standard solution for concurrent writer contention on a shared branch — identical to what large CI systems use for lease-based locking. The five-attempt ceiling still allows the job to fail noisily if there's a genuine merge conflict.

---

## aaronjmars/aeon-agent

### Infrastructure: Skill Schedule Overhaul

**Summary:** The aeon-agent `aeon.yml` scheduler was restructured from a 3-day rotation cycle (Day 1: market; Day 2: content; Day 3: build) to a simpler model: daily for high-frequency market/social skills, every-2-days for content and meta skills. All times shifted earlier to front-load the day's activity. This is a human-authored commit (Aaron, with Claude assist), not an auto-commit.

**Commits:**
- `d88588d` — Update skill schedule: daily market tasks, every-2-day content/meta, shift times earlier
  - Modified `aeon.yml` (+14, -16 lines):
    - **Daily (market & social)**: `token-report` at 6 AM UTC, `fetch-tweets` at 6:30 AM, `repo-pulse` at 10 AM. Were on a Mon/Thu/Sun cycle — now run every day.
    - **Every 2 days (content & meta)**: `repo-actions` at 2 PM, `push-recap` at 3 PM, `repo-article` at 4 PM, `self-improve` at 1 PM. Were on Tue/Fri; now `*/2` gives more frequent cadence.
    - **Build (daily)**: `feature` at 11 AM, `hyperstitions-ideas` Saturdays at 10 AM.
    - **Housekeeping**: `heartbeat` moved from 9 PM to 7 PM. `memory-flush` now runs Sun+Wed (was Sundays only) — double the consolidation frequency.
    - Removed the 3-day rotation comment block entirely.

**Impact:** The 3-day rotation was designed to avoid running all skills every day (cost control), but it created irregular cadences — users checking on a Tuesday would get no market data, Friday would be content-heavy. The new schedule makes market/social data daily (predictable for token holders) while keeping content and meta on a moderate cadence. Shifting memory-flush to Sun+Wed keeps the memory index from growing stale mid-week. The earlier time slots (6–4 PM vs. 8 AM–7 PM) front-load work and reduce latency before output reaches the Telegram group.

---

### Operational Commits — Daily Skill Runs (2026-04-09/10)

**Summary:** 7 auto-commits in aeon-agent logging the outputs and state of today's scheduled skill runs. These are normal operational housekeeping — the agent commits after each skill to persist state.

**Commits:**
- `4a17209` — chore(token-report): auto-commit 2026-04-10
  - Added `articles/token-report-2026-04-10.md` (+47 lines): Full token report (AEON: $0.000001280, +59.3% 24h, new ATH, FDV $128K)
  - Updated `memory/logs/2026-04-10.md` with token-report entry

- `485e525` — chore(fetch-tweets): auto-commit 2026-04-10
  - Updated `memory/logs/2026-04-10.md` with 5 new tweets logged
  - Updated `.gitignore` (+15 lines): Added new exclusions

- `0803023` — chore(repo-pulse): log 2026-04-10 — 151 stars, 16 forks (+2/+1)
  - Updated `memory/logs/2026-04-10.md` with repo-pulse entry

- `bd89d24` — chore(feature): log mcp-skill-adaptor build 2026-04-10
  - Updated `memory/MEMORY.md`: Added mcp-skill-adaptor skill entry
  - Updated `memory/logs/2026-04-10.md` with feature/MCP entry

- `120f230` — chore(self-improve): log hacker-news-digest improvement 2026-04-10
  - Updated `memory/logs/2026-04-10.md` with self-improve entry (hn-digest dedup + aeon-agent PR #7)

- `39e31ce` — log: repo-actions run 2026-04-10
  - Updated `memory/logs/2026-04-10.md` with repo-actions entry (5 ideas: Workflow Security Audit, A2A Gateway, Dashboard Live Feed, Skill Leaderboard, Email Channel)

- `c3e3c1e` — chore(heartbeat): auto-commit 2026-04-09
  - Updated `memory/logs/2026-04-09.md` with heartbeat entry

**Impact:** These commits represent Aeon completing a full operational day — token report, tweet fetch, repo pulse, feature build (MCP adaptor), self-improvement, repo-actions ideation, and heartbeat. The agent persisted all outputs and state correctly. The .gitignore update is a minor cleanup.

---

## Developer Notes

- **New files**: `skills/skill-evals/SKILL.md`, `skills/skill-evals/evals.json`, `articles/repo-actions-2026-04-10.md`, `articles/token-report-2026-04-10.md`
- **Breaking changes**: None. Schedule changes in aeon-agent `aeon.yml` affect cron timing but not skill logic.
- **Architecture shifts**: The skill-evals framework introduces a meta-layer pattern — a skill that reads and validates other skills' outputs. This is the foundation for a self-correcting agent loop.
- **Tech debt**: `skill-evals` registered with `enabled: false` — needs to be enabled once the first manual run confirms assertion accuracy against current outputs.

## What's Next

- Enable `skill-evals` in aeon.yml after a manual validation run confirms the 14 assertion specs are correctly tuned
- The repo-actions ideas for today (Workflow Security Audit, A2A Gateway, Dashboard Live Feed, Skill Leaderboard, Email Channel) are candidates for the next `feature` skill run
- PR #28 (MCP Skill Adaptor) is open on aaronjmars/aeon — needs review and merge before the A2A Gateway idea makes sense to build on top of it
- Aeon-agent PR #7 (enable HN digest) is open — schedule now has `every 2 days` cadence available for it
