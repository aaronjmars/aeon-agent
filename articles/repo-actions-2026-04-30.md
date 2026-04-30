# Repo Action Ideas — 2026-04-30

**Repos analyzed:** aaronjmars/aeon (254 stars, 36 forks, 0 open PRs), aaronjmars/aeon-agent
**Context:** Clean queue — PRs #147 (pr-triage) and #148 (thread-formatter) both merged today and yesterday, both shipped `enabled: false`. 254 stars, ~46 from the May-25 milestone. Token in a 5-session slide (-19.94% today). Carried unbuilts: Show HN Launch Prep (1 cycle), Smithery Manifest Auto-Generator (1 cycle), Fork Activation Cohort Tracker (1 cycle). 1 new fork today (adarshhalan/aeon), fleet now 36.

---

### 1. Show HN Launch Prep
**Type:** Growth
**Effort:** Small (hours)
**Impact:** At 254 stars with ~4/day momentum, the 300-star milestone arrives in ~11 days — the right moment for a Show HN post. HN's technical audience responds to concrete proof, not hype: actual skills running, forks in production, autonomous behaviors that surprise. Drafting now under zero pressure means the text goes through a real edit cycle instead of being typed in 10 minutes at the moment. A front-page Show HN run has historically added 50–200 stars in 48h for projects at this scale; more importantly, it surfaces Aeon to the HN subculture that creates open-source adoption momentum. At 300 stars, the narrative writes itself: "here's what 300 people found worth starring, here's what it actually does without you."
**How:**
1. New one-shot skill `skills/show-hn-draft/SKILL.md` — reads README, SHOWCASE.md, recent repo-article and project-lens entries (last 7 days), repo stats (stars, forks, skill count), and most compelling autonomous behavior examples from memory/logs (pr-triage comment within minutes of PR open, thread-formatter scoring daily events, heartbeat /status/ auto-updating).
2. Generates two variants: (a) Show HN title (≤300 chars) + 4-paragraph body for the primary HN post — lead with the most surprising behavior, include the "configure once, forget forever" concrete proof, list 3 capabilities a senior engineer would actually want; (b) a shorter r/MachineLearning / r/selfhosted variant with different framing ("open-source GitHub Actions agent, 90+ skills").
3. Writes to `articles/show-hn-draft-${today}.md`; notifies with the title + first paragraph so the operator can evaluate without reading the full file.

---

### 2. Smithery Manifest Auto-Generator
**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** The Smithery.ai + MCP Registry submission (Apr-22 idea #1) has been the highest-priority unbuilt growth play for six weeks. The actual blocker is that submission requires a correctly-formatted MCP server manifest and a pre-filled submission document — none of which has been written. Every day without this listing means inbound discovery from the growing MCP ecosystem misses Aeon entirely. A skill that auto-generates `docs/smithery-manifest.json` from the live `skills.json` + `aeon.yml` enabled skill list, formatted to Smithery's spec (name, description, tools array), and produces a `docs/smithery-submission.md` with the paste-ready submission body removes every remaining obstacle. The agent opens a PR; the operator pastes into the form.
**How:**
1. New skill `skills/smithery-manifest/SKILL.md` — reads `skills.json` (skill catalog with descriptions) and `aeon.yml` (enabled flags, schedule, var). Builds a Smithery-compatible manifest: server name `aeon`, version from recent tag, description from README headline, `tools[]` array with each enabled skill as an entry (name, description, input schema from frontmatter `var` field).
2. Fetches the current Smithery submission spec via WebFetch to ensure field compliance; writes `docs/smithery-manifest.json` and `docs/smithery-submission.md` (human-readable submission doc with pre-filled title, server URL `https://github.com/aaronjmars/aeon`, description, category tags).
3. Opens a PR on aaronjmars/aeon touching only `docs/`; notifies with the submission doc link + one-line "paste this into the Smithery form" instruction.

---

### 3. Fork Activation Cohort Tracker
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** `fork-fleet` tracks which skills each fork runs; `fork-contributor-leaderboard` tracks who commits code. Neither answers: "which forks are actually running right now?" At 36 forks (1 new today), the ratio of running-to-abandoned matters for two reasons: (1) @aaronjmars can't support operators who've already silently quit, and (2) "X of 36 forks running in production" is a more compelling social proof point than "36 forks" when the number is real. A weekly skill that buckets forks by activation stage using GitHub Actions run history — `COLD` (no runs), `STALE` (last run >14d), `ACTIVE` (run <7d), `POWER` (run <7d + ≥5 skills enabled) — gives concrete cohort visibility and flags any fork dropping from ACTIVE to STALE for early intervention.
**How:**
1. New skill `skills/fork-cohort/SKILL.md` — for each fork in the fleet, queries `gh api repos/{fork}/actions/runs --jq '[.workflow_runs[0].updated_at]'` for last run timestamp. Buckets into COLD / STALE / ACTIVE / POWER. Persists state to `memory/topics/fork-cohort-state.json` with week-over-week delta tracking.
2. Flags forks that transitioned `ACTIVE → STALE` since last week; optionally opens a GitHub issue on the fork repo with a check-in comment if the fork owner is a known contributor (from fork-contributor-leaderboard data).
3. Weekly schedule: Sunday 19:00 UTC alongside skill-leaderboard. Notifies with a cohort table (counts per stage, delta vs last week) + any newly-stale fork names. Writes `articles/fork-cohort-${today}.md`.

---

### 4. Skill Dependency Freshness Validator
**Type:** Feature / Quality
**Effort:** Small (hours)
**Impact:** Several skills silently fail when their upstream inputs are stale. `contributor-reward` reads `articles/fork-contributor-leaderboard-*.md` — if that skill didn't run this week, contributor-reward produces a plan from old data. `thread-formatter` reads today's `memory/logs/${today}.md` — if logs weren't written yet, it exits `NO_DATA`. The `chains:` section in aeon.yml makes some of this explicit, but ad-hoc skill reads (direct file reads inside SKILL.md prompts) are invisible to any health system. A validator that maps declared `consume:` edges from chains PLUS scans SKILL.md files for `articles/` and `memory/` read patterns, checks modification timestamps on the referenced files, and alerts when a dependency is stale (>N days old) before a dependent skill runs catches the entire class of "upstream produced nothing and downstream silently degraded" failures.
**How:**
1. New skill `skills/skill-deps-check/SKILL.md` — reads `aeon.yml` chains to extract explicit `consume:` dependencies. Also pattern-scans skill SKILL.md files for file references matching `articles/`, `memory/topics/`, `.outputs/` to infer implicit dependencies. Builds a dependency map: `{skill → [upstream files/skills]}`.
2. For each upstream, checks the most recent matching file's mtime (via `ls -lt articles/{skill}-*.md | head -1`). Compares to a freshness threshold (configurable per-skill category: daily skills = 36h, weekly skills = 8d). Files beyond threshold are flagged as STALE_DEP.
3. On any STALE_DEP finding, writes to `memory/issues/` (new issue file + INDEX.md update) and notifies once per issue per day. Runs daily at 05:30 UTC before the morning skills block. Exits silently when all deps are fresh.

---

### 5. Operator Value Scorecard
**Type:** DX / Community
**Effort:** Small (hours)
**Impact:** Aeon has skill-analytics (fleet-level anomaly detection), heartbeat (is-it-running pulse), and cost-report (raw token spend) — but no skill that synthesizes these into a plain-language "what did Aeon actually do for you this week / this month?" narrative. Operators renew their cognitive investment in running Aeon when they can see the concrete output: 7 PRs reviewed, $70 in community payouts, 3 skills with 100% success rate, 2 skills that need attention. An operator-facing scorecard generated weekly turns the abstract "this agent is running" into specific claimed value. It's also the most natural content for @aaronjmars to share ("here's a week in numbers from a running Aeon instance") — a format that scales beyond token-price discussion into "proof this works."
**How:**
1. New skill `skills/operator-scorecard/SKILL.md` — reads `memory/token-usage.csv` (token spend per skill per day), last 7 days of `memory/logs/*.md` (output counts: PRs reviewed, tweets fetched, skills built, distributions generated), and `./scripts/skill-runs --hours 168 --json` (success rates per skill). Calculates: total skills run, total successful runs, top 5 by output volume, bottom 3 by success rate, total token cost, estimated "equivalent human-hours" (heuristic: 1 deep-research = 2h, 1 PR review = 30min, etc.).
2. Generates a concise scorecard: one table of metrics + one paragraph of plain-language summary ("this week Aeon reviewed 4 PRs, published 7 articles, paid out $70 in tweet rewards, and ran 94 successful skill executions across 15 active skills"). Writes to `articles/operator-scorecard-${today}.md` and `dashboard/outputs/operator-scorecard.json`.
3. Weekly schedule: Monday 08:00 UTC (ahead of weekly-shiplog at 09:00 UTC so data feeds in). Notifies with the one-paragraph summary. Silent if no logs found (first week of setup).
