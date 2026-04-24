# Push Recap — 2026-04-24

## Overview
Two meaningful merges, both touching `skills/heartbeat/SKILL.md` from opposite directions on the same day. `aeon` PR #141 turns heartbeat into a public broadcaster — every run now regenerates a Jekyll-rendered `docs/status.md` so anyone can see fleet health at `aaronjmars.github.io/aeon/status/`. `aeon-agent` PR #18 goes the other way on the same skill: once an operator-dependent issue has been escalated for seven consecutive days, the 48h re-notify cadence backs off to every 7 days so the fifth+ ping stops being noise. Heartbeat got louder externally and quieter internally in the same push window.

**Stats:** 5 files changed, +110/-4 lines across 2 meaningful commits · 24 autonomous scheduler/cron/skill auto-commits excluded (token-report, fetch-tweets, tweet-allocator, repo-pulse, feature, self-improve, repo-actions + yesterday's heartbeat/project-lens/repo-article tail).

**Authors:** @aaronjmars (squash-merging both PRs authored autonomously by the aeonframework bot + Claude Opus 4.7).

---

## aaronjmars/aeon

### Theme 1: Public Agent Status Page — fork-inheritable health broadcaster

**Summary:** Heartbeat has been the agent's *internal* self-check for months (P0-P3 priority tiers, 48h dedup, escalation on 3+ day persistence). PR #141 extends the same signals outward: after the existing priority checks run, heartbeat now wholesale-rewrites `docs/status.md` with an overall verdict badge (🟢 OK / 🟡 WATCH / 🔴 DEGRADED), a per-skill table, and the open-issues feed. The workflow's auto-commit step lands the file on `main` and GitHub Pages picks it up on the next build. Zero net-new data sources, zero net-new secrets, zero net-new cron — everything the page renders is already on disk from the heartbeat's own P0-P3 checks.

**Commits:**
- `8242d84` — feat(heartbeat): public status page at /status/ (#141)
  - New file `docs/status.md` (+31 lines): Jekyll frontmatter (`layout: default`, `permalink: /status/`), a placeholder verdict block (🟢 OK · Updated: awaiting first heartbeat run · Open issues: 0), and a "Skill health" table stub with the "Fork the repo and your copy inherits this page automatically" footer. The placeholder is what ships before the first heartbeat run overwrites it.
  - Modified `skills/heartbeat/SKILL.md` (+69/-1): new "Public status page" section inserted between the priority-tier notification block and the Output rules. Codifies the three overall states (`DEGRADED` = any P0 flag, `WATCH` = any P1/P2/P3 flag or critical/high open issue, `OK` = no flags); the exact markdown template heartbeat must emit; formatting rules (sort skills by last-run desc, timestamps as `YYYY-MM-DD HH:MM UTC` with no seconds/Z, success rate as `total_successes / total_runs × 100`, status icons for ✅ / ❌ / ⏳ / 🕸 / —); and a security constraint explicitly forbidding values from `.env` or secrets because the file is public. Output verdict line extends to `HEARTBEAT_OK · STATUS_PAGE=OK`.
  - Modified `docs/_config.yml` (+1): adds `status.md` to the `header_pages` array so `/status/` shows up in the Jekyll gallery nav alongside activity / memory / skills.
  - Modified `README.md` (+1): adds a shields.io "agent-status" badge to the header row pointing at the public page.

**Impact:** Three groups get served. External observers can now check fleet health without a GitHub account or a workflow-runs permission — the badge in the README is a one-click probe. Forks that enable Pages inherit the page for free at their own URL: closes the fork-visibility gap that `fork-fleet` + `fork-skill-digest` could *observe* but not *broadcast*. Operators get an always-fresh dashboard that's 3x stale at worst (heartbeat runs 08:00 / 14:00 / 20:00 UTC); if the Updated timestamp drifts past ~8h, the agent has stopped running entirely and that's visible from the badge color alone.

---

## aaronjmars/aeon-agent

### Theme 2: Heartbeat extended-persistence backoff — 48h → 7d after a week of persistence

**Summary:** The existing escalation rule re-notifies every 48h once an issue has persisted 3+ days. That rule was correct for the first week of the PAT-with-`workflows`-scope issue (surfaced Apr 17, re-notified Apr 19 / 21 / 23). By day 7+ the cadence stops producing signal — operator-dependent issues (missing secrets, third-party outages, external setup) can't be resolved on heartbeat's preferred schedule. PR #18 inserts a third tier: after 7 consecutive escalation days, drop to a 7-day cadence until resolution resets the counters.

**Commits:**
- `96e04a6` — improve(heartbeat): extended-persistence backoff for 7+ day issues (#18)
  - Modified `skills/heartbeat/SKILL.md` (+8/-3): new rule 3 "Extended-persistence backoff (7+ days)" inserted between the existing 48h escalation rule and the Batch rule (which renumbers 3 → 4). The rule specifies a log-pattern check ("find the most recent `Notification sent: yes (ESCALATION...)` log entry; if within the last 7 days AND issue is 7+ days old, suppress this run's notification") and two edge-case clarifications: the first escalation past the 7-day threshold still fires on 48h cadence (backoff kicks in only on the *next* escalation after that), and resolution resets all counters. The output-rules block at the bottom gains a fourth marker: `Notification sent: no (7d extended-persistence backoff — last ESCALATION N days ago)` so future heartbeats can detect and respect the backoff state via the same log-scan mechanism.

**Impact:** The PAT-workflows-scope issue has fired `ESCALATION` every 48h since Apr 17 — that's four pings already (Apr 17 / 19 / 21 / 23), and yesterday's heartbeat confirmed it would fire again today on the 48h clock. Under the new rule, today's ping is the last one on the 48h cadence; the next re-notify won't fire until ~May 1. Operator gets signal on the day it matters (issue surfaces + day-3 escalation + day-5/7 reminders) but stops getting paged every-other-day indefinitely for a known-waiting-on-operator issue. The pattern also applies to any future persistent-but-operator-dependent issues: missing secrets, third-party outages, external PRs.

---

## Developer Notes

- **New dependencies:** None. Both PRs are pure documentation/skill-spec edits — no new packages, no new env vars, no new cron entries. The public status page re-uses `memory/cron-state.json` + `memory/issues/INDEX.md` + `aeon.yml` that heartbeat already reads.
- **Breaking changes:** None. Heartbeat's existing P0-P3 taxonomy, 48h dedup rule, and 3-day escalation rule all stay identical. The status page is an additive step at the end of the skill; the extended backoff adds a third tier to the dedup rules without changing the existing two.
- **Architecture shifts:**
  - **Private health signal → public fixture.** Heartbeat was the canonical observer of fleet state; now it's also the canonical *publisher*. Status page contents come from the same three files heartbeat already reads — but the consumer pool just expanded from "Aeon itself" to "every GitHub Pages visitor."
  - **Workflow auto-commit as publication mechanism.** The status page lands on `main` via the existing auto-commit step, not via a new workflow or deploy hook. Same pattern as other skill outputs (articles, memory logs, cron state) — reuses the proven "skill writes file, workflow commits, GitHub Actions rebuilds Pages" pipeline. The status page's git history is its audit trail.
  - **Three-tier escalation as a general pattern.** Day 0-2 = 48h dedup, day 3-6 = 48h escalation, day 7+ = 7d extended backoff. This codifies "known-unresolvable" as a distinct state from "new issue" — future notification patterns elsewhere in the agent (tweet-roundup, narrative-tracker, skill-health) could adopt the same shape for operator-dependent persistence.
- **Tech debt:** The status page's first Pages render ships the placeholder from `docs/status.md` — real data arrives on the first post-merge heartbeat run (~20:00 UTC today). That's a ~6.5h window where visitors would see "awaiting first heartbeat run." Acceptable for a launch day; worth watching that heartbeat's write lands cleanly.

## What's Next

- **First live status page refresh.** Heartbeat's 20:00 UTC run today is the inaugural render. Expected verdict: 🟢 OK (no P0/P1/P2/P3 flags currently active except the PAT-workflows-scope escalation, which is exempted from the status-page verdict by the `any open issue with severity critical or high` clause — the PAT issue is medium severity). Watch that the per-skill table populates correctly and timestamps are formatted as specified.
- **First 7-day backoff trigger.** Today's heartbeat should fire ESCALATION #5 on the PAT issue at 20:00 UTC (still on 48h cadence — backoff kicks in on the *next* escalation after crossing day 7). Next re-notify due ~May 1 under the new rule. If the backoff marker doesn't land in the log correctly, the rule's log-scan mechanism won't detect it and we'll get the May-1 ping as another 48h-cadence escalation by mistake.
- **Repo-actions pipeline post-merge.** Apr-22 ideas #2 + #4 both built (fork-skill-digest Apr-23 + public-status-page Apr-24). Remaining unbuilts: #1 Smithery/MCP Registry submission (external PRs, growth), #3 Webhook-to-Skill Bridge (medium), #5 Skill Run Analytics Widget (small — flagged by today's repo-actions run as the next autonomous candidate). Plus three fresh ideas from today's run: Contributor Auto-Reward, Twitter Thread Auto-Formatter, Repo Discovery Refresh.
- **Backport 80 autoresearch-evolution rewrites (aeon PRs #46-#136) to aeon-agent still outstanding.** Today's push-recap is still the pre-evolution format — no verdict line, no user-visible/internal split, no significance gate. Seven days since this was first flagged.
- **PAT with `workflows` scope.** Day 7 of persistence (unresolved since Apr 17). Today's escalation is the last 48h-cadence ping under the new rule — next one on ~May 1. Generate fine-grained PAT with `workflows` write permission, set as `GH_GLOBAL` secret.
