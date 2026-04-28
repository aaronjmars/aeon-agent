# Repo Action Ideas — 2026-04-28

**Repos analyzed:** aaronjmars/aeon (251 stars, 36 forks, 0 open PRs), aaronjmars/aeon-agent
**Context:** Clean queue — PRs #145 (SHOWCASE.md) and #146 (heartbeat token pulse) both merged. 251 stars, 49 from the May-25 deadline. Carried unbuilts: Twitter Thread Auto-Formatter (2 cycles), External PR Triage (1 cycle). MCP Registry submission (Apr-22 idea #1) still blocked on external PRs. Fork count at 36 — fork activation visibility gap identified. Smithery manifest auto-generation emerges as a concrete unblocking move.

---

### 1. Twitter Thread Auto-Formatter
**Type:** Content
**Effort:** Small (hours)
**Impact:** Every daily run produces something interesting — a new skill, a price move, a star milestone, a PR merge — but organic social reach depends on manual copy-paste from Telegram. A skill that reads today's memory log, scores events by engagement proxy (new skill shipped > price move >10% > star milestone > notable tweet engagement), picks the top event, and formats a ready-to-post 5-tweet thread multiplies tweet-allocator ROI without touching the budget. The thread itself is organic content that amplifies whatever already ran.
**How:**
1. New skill `skills/thread-formatter/SKILL.md` — reads `memory/logs/${today}.md`, scores events by engagement signal weight (new PR merged +3, price move >10% +2, star milestone +2, notable fetch-tweet engagement >10 likes +1), picks the single top event, formats 5 tweets: hook → context × 2 → implication → CTA with repo link.
2. Writes to `articles/thread-${today}.md`; notifies with the full formatted thread text ready to paste.
3. Schedule: `0 18 * * *` in `aeon.yml` (after most daily skills complete); disabled-by-default so operators opt in.

---

### 2. External PR Triage
**Type:** Community
**Effort:** Small (hours)
**Impact:** `pezetel`'s PR #143 arrived April 25 with no response — no label, no comment, no review request. As the fork count climbs toward 40, external PRs will increase. A skill that reads the diff, applies a structured rubric (paths touched, SKILL.md format compliance, overlap with existing skills, size), and posts a comment (accept / needs-changes / defer / out-of-scope + rationale) within minutes of opening makes Aeon a welcoming project and prevents PRs from going stale. Automating triage signals to contributors that their work is seen even when @aaronjmars is offline.
**How:**
1. New skill `skills/pr-triage/SKILL.md` — triggered by `workflow_dispatch` with `PR_NUMBER` input; reads `gh pr view $PR_NUMBER --json title,body,additions,deletions,files,author` and `gh pr diff $PR_NUMBER`. Skips PRs authored by `github-actions[bot]`, `aeonframework`, `dependabot[bot]` (auto-merge handles those).
2. Rubric: touches only `skills/`, `docs/`, `examples/`, `README.md`? Follows SKILL.md frontmatter format? Duplicates an existing skill name? ≤500 lines changed? Assigns one verdict: `accepted` / `needs-changes` / `defer` / `out-of-scope`. Posts `gh pr comment` with verdict + bullet-point rationale. Adds label via `gh pr edit --add-label`.
3. Notify with one-liner if `accepted` or `out-of-scope`; silent for `needs-changes` / `defer` (comment on the PR is the signal).

---

### 3. Show HN Launch Prep
**Type:** Growth
**Effort:** Small (hours)
**Impact:** At 251 stars with ~4/day momentum, the 300-star milestone arrives in ~12 days — prime timing for a Show HN post (HN audience responds well to "here's what 300 people already found useful"). Drafting it now ensures the text is ready to drop at exactly the right moment, reviewed and edited rather than typed under pressure. A Show HN that lands on the front page could add 50–200 stars in 48h, which itself becomes the story for the next week's content cycle.
**How:**
1. New one-shot skill `skills/show-hn-draft/SKILL.md` — reads README, SHOWCASE.md, recent repo-article and project-lens entries, repo stats, and the last 7 days of memory/logs to assemble key proof points: total skills, forks, star trajectory, most impressive autonomous behaviors (SHOWCASE Ecosystem Comparison column wins), community contributors.
2. Generates two variants: a 300-character Show HN title + 3-paragraph body optimized for HN's "technical founder" audience (no hype words, concrete capabilities, honest tradeoffs section); plus a second variant as a community-post for r/MachineLearning or Hacker News "Ask HN" format.
3. Writes to `articles/show-hn-draft-${today}.md`; notifies with the title + first paragraph so the operator can evaluate without reading the full file.

---

### 4. Smithery Manifest Auto-Generator
**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** Smithery.ai + MCP Registry submission (Apr-22 idea #1) has been the highest-priority unbuilt for six weeks, blocked on "external PRs needed." The actual blocker is that the submission requires a correctly-formatted MCP manifest JSON and server metadata that hasn't been written. A skill that auto-generates `docs/smithery-manifest.json` from the live `skills.json` + `aeon.yml` enabled-skill list, formats it to Smithery's spec (name, description, tools array with schema, auth requirements), and produces a copy-paste PR body for submission removes the only real obstacle. The agent opens a PR on the aeon repo with the manifest; the operator pastes the body into Smithery's submission form.
**How:**
1. New skill `skills/smithery-manifest/SKILL.md` — reads `skills.json` (full skill list with descriptions) and `aeon.yml` (enabled flags) to build a Smithery-compatible manifest: server name/version/description, `tools[]` array with each skill as a tool entry (name, description, input schema from the SKILL.md frontmatter `var` + common params).
2. Fetches current Smithery spec format via WebFetch to ensure compliance; writes `docs/smithery-manifest.json` and `docs/smithery-submission.md` (the human-readable PR body template with pre-filled title, description, and server URL).
3. Opens a PR on aaronjmars/aeon touching only `docs/`; notify with the submission doc link and a one-line note that the form is ready to paste.

---

### 5. Fork Activation Cohort Tracker
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** fork-fleet tracks which skills are enabled per fork; fork-contributor-leaderboard tracks who contributes code. Neither answers: "which forks are actually running?" As the count grows toward 40, the ratio of active-to-abandoned forks matters — both for @aaronjmars knowing where to focus support and for the community narrative ("X of 36 forks are running in production"). A weekly skill that buckets forks by activation stage using GitHub Actions run history gives concrete cohort visibility. Early detection of a fork going dark enables a lightweight nudge before the operator disappears entirely.
**How:**
1. New skill `skills/fork-cohort/SKILL.md` — for each fork in the fleet, queries `gh api repos/{fork}/actions/runs --jq '[.[].updated_at] | .[0]'` to get the most recent workflow run timestamp. Buckets each fork into: `COLD` (no runs ever), `STALE` (last run >14d ago), `ACTIVE` (run in last 7d), `POWER` (run in last 7d + ≥3 skills enabled, sourced from fork-fleet state).
2. Tracks stage transitions week-over-week in `memory/topics/fork-cohort-state.json`; flags any fork that dropped from `ACTIVE → STALE` since last week. Weekly schedule: Sunday 19:00 UTC alongside skill-leaderboard.
3. Notifies with a cohort breakdown table (counts per stage, delta vs prior week) + names of any newly-stale forks. Writes article to `articles/fork-cohort-${today}.md`.
