# Repo Action Ideas — 2026-04-07

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 147 (aeon) / 6 (aeon-agent) | **Forks:** 15 / 0 | **Language:** TypeScript | **Open Issues:** 1 / 0
**Contributors:** aaronjmars (152), Aeon (5), github-actions[bot] (3), aeonframework (2)

Aeon is at 147 stars and 59 skills as of today. The past week was platform-defining: skill versioning (SHA+date in skills.json, sync-upstream.sh), smoke-test CI (static SKILL.md validator on every PR), deep research mode (30–50 sources, 3K–5K words, 1M context), dashboard redesign with Hyperstitions/Evangelion aesthetic, and cost reporting now headed to main via PR #12. This run focuses on the next tier of platform maturity: quality assurance, distribution, fleet coordination, and live infrastructure.

Previous runs (Mar 25–Apr 4) generated 40+ ideas. Built: skill forking, RSS feed, skill security scanner, autonomous skill discovery, GitHub Pages gallery, deep research, skill smoke tests, cost-report. Unbuilt from earlier ideation: Fork Fleet Coordination, Workflow Security Audit, Dashboard Live Feed, Skill Dependency Chain, Memory Search API, MCP Skill Adaptor, A2A Gateway, Skill Evals.

---

### 1. Skill Evals — Automated Quality Testing for Skill Outputs

**Type:** Feature / Quality
**Effort:** Medium (1-2 days)
**Impact:** The smoke-test CI (merged in PR #10) validates SKILL.md *structure* — frontmatter, cron syntax, secrets references, no placeholders. But it says nothing about whether a skill actually produces good output. A skill can pass every structural check and still return a blank article, a hallucinated token price, or a truncated digest. Skill Evals would close this gap by running each skill against a controlled test harness and asserting on output quality: non-empty, within expected length range, containing required fields (headline, sources, price), and free of obvious errors. With 59 skills and 15 forks now depending on them, a regression in `token-report` or `hacker-news-digest` may go unnoticed for days. Evals make regressions visible immediately. This is the logical next step in Aeon's CI maturity — structural validation is stage one, output validation is stage two.

**How:**
1. Create `skills/skill-evals/SKILL.md` that, for each skill in a configurable test list, invokes the skill via `workflow_dispatch` in a sandbox branch, captures the output artifact (the generated article file), and runs assertions: minimum word count, presence of required keywords, valid markdown structure, no placeholder strings like `[TODO]` or `${var}`, and for data skills (token-report, repo-pulse) — numeric values within plausible ranges.
2. Create `skills/skill-evals/evals.json` — a per-skill assertion manifest. Each entry specifies: `min_words`, `required_patterns` (regex list), `forbidden_patterns`, and `output_file` (e.g. `articles/token-report-{date}.md`). Skills without an eval entry are flagged as "eval coverage gap" in the output.
3. Add to `test-skills.yml` CI: run evals on any PR that modifies a skill's SKILL.md. Output a pass/fail table in the PR comment. Schedule a weekly full-suite eval run (Sundays 6 AM UTC) and notify via `./notify` with a coverage summary: X/Y skills passing evals, Z new coverage gaps.

---

### 2. MCP Skill Adaptor — Expose Aeon Skills as Claude Desktop Tools

**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** Claude Desktop's MCP (Model Context Protocol) ecosystem now has hundreds of thousands of tools, and MCP is how Claude Code users extend their local agent. Aeon has 59 production-quality skills running in CI — but they're only accessible via GitHub Actions cron or manual `workflow_dispatch`. An MCP adaptor would wrap Aeon's skills as MCP tools so any Claude Desktop user could invoke `aeon:token-report`, `aeon:deep-research`, or `aeon:hacker-news-digest` directly from their Claude interface. This unlocks a completely new distribution channel: instead of "fork this repo and configure Actions", the install is `./add-mcp aaronjmars/aeon`. With 75% developer Claude Code adoption (per Q1 2026 data), this is the highest-leverage distribution play available. The skills already have structured inputs (`var`) and outputs (markdown files) — the adaptor is a thin translation layer, not a rewrite.

**How:**
1. Create `mcp-server/` directory with a minimal MCP server implementation in TypeScript. For each skill in `skills.json`, generate an MCP tool definition: name (`aeon:{slug}`), description (from skills.json), and `inputSchema` mapping `var` to a string parameter. The server reads `skills.json` at startup, so new skills auto-appear as tools.
2. Each tool invocation triggers the corresponding skill locally by spawning `claude` CLI with the SKILL.md instructions and the provided `var`. Output is returned as the tool result. Skills that require secrets (API keys, tokens) read from `.env` or the local Claude secrets store — no GitHub Actions needed.
3. Add `./add-mcp` install script to the repo root that: clones the MCP server, runs `npm install`, and appends the MCP server config to `~/.claude/mcp.json`. Update README with a "Use with Claude Desktop" section. Add `mcp-server` as a topic to the repo and list it on `mcp.so` (the MCP directory).

---

### 3. Fork Fleet Coordinator — Track, Update, and Sync Aeon Forks

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** Aeon has 15 forks — a real fleet. Each fork is likely a customized agent running somewhere with modified skills, different schedules, and potentially valuable improvements that haven't flowed back upstream. Currently there's zero visibility into what forks are doing or whether they're diverged from main in ways that matter (breaking changes in the scheduler, new skill categories, different notification formats). A fleet coordinator skill would: inventory active forks, detect which ones are ahead of main (commits not in upstream), surface the most impactful fork improvements for potential upstream merge, and optionally send fork owners a notification when a major Aeon release ships with changes that affect their configuration. This turns forks from a vanity metric into a community signal.

**How:**
1. Create `skills/fork-fleet/SKILL.md` that: queries `gh api repos/aaronjmars/aeon/forks --jq '[.[] | {owner: .owner.login, pushed_at, stargazers_count, open_issues_count}]'`, filters for forks that have had activity in the past 30 days (pushed_at check), and for each active fork fetches its commit list to detect commits not in upstream (diverged work).
2. For each active fork, check for: new files in `skills/`, modifications to `aeon.yml` (different schedules or new skills), changes to `dashboard/` or `notify`. Summarize divergence as: "N new skills", "custom schedule", "modified dashboard". Flag forks with 5+ unique commits as "high-divergence — potential upstream contribution".
3. Output to `articles/fork-fleet-{date}.md`: a ranked list of active forks by divergence score, the top 3 "most innovative" forks (most unique content not in main), and a suggested upstream PR for the single best improvement found. Send notification with the summary and a link to the article.

---

### 4. Workflow Security Audit — Scan GitHub Actions for Injection and Permission Issues

**Type:** Security
**Effort:** Small (hours)
**Impact:** Aeon's skill security scanner (PR #5, merged) audits external SKILL.md files before import. But the `.github/workflows/` directory itself is unaudited — and GitHub Actions workflows are a rich attack surface. Common issues: `run:` blocks that interpolate `${{ github.event.issue.title }}` without sanitization (script injection), jobs with `permissions: write-all` when read-only suffices, using unverified third-party actions (e.g., `uses: random-user/action@main` instead of a pinned SHA), and environment variables that expose secrets to logs. With Aeon's aeon-agent repo running 50+ automated workflow runs per week, a single injection vulnerability could compromise the agent's GitHub token, exfiltrate Telegram/Discord secrets, or push malicious commits. This is especially important given the upcoming MCP adaptor (idea #2) which would add a new execution surface. A one-time audit skill run would surface and fix these before they become incidents.

**How:**
1. Create `skills/workflow-security-audit/SKILL.md` that reads every `.yml` file in `.github/workflows/` and checks for: (a) script injection — `${{ github.event.* }}` or `${{ inputs.* }}` used directly in `run:` blocks, (b) overly broad permissions — `permissions: write-all` or `contents: write` on jobs that only need read, (c) unverified third-party actions — `uses: owner/action@branch` instead of `@sha`, (d) secret exposure — `echo ${{ secrets.* }}` in `run:` blocks, (e) self-hosted runner risk — `runs-on: self-hosted` without isolation labels.
2. For each finding, generate a fix: replace direct interpolation with an env var assignment (`env: TITLE: ${{ github.event.issue.title }}`), scope permissions to minimum required, pin actions to their current SHAs (fetched via `gh api repos/owner/action/git/ref/heads/main --jq '.object.sha'`).
3. Output a report to `articles/workflow-security-audit-{date}.md` with severity (critical/high/medium) and exact line references. For critical findings, open a PR with the fixes applied automatically. Send notification with the finding count and highest-severity issue.

---

### 5. Dashboard Live Feed — Real-Time Skill Run Activity Stream

**Type:** Feature / DX
**Effort:** Medium (1-2 days)
**Impact:** The dashboard has a beautiful Hyperstitions/Evangelion redesign and an analytics tab with per-skill metrics — but it's all historical. When Aeon is running a skill right now (deep research, fetch-tweets, token-report), the dashboard shows nothing until the run completes and an article is written. A live feed would show: which skill is currently executing, how long it's been running, the last log line written (via tail of the log file), and recent completions with their outputs. This closes the "is it working?" gap for new users — currently you have to check GitHub Actions directly to see if a run is in progress. A live feed also turns the dashboard into a monitoring panel, which is the missing piece between "skill gallery" and "operational control plane". The json-render infrastructure is already in place (`dashboard/outputs/`); this extends it to streaming state.

**How:**
1. Create a `dashboard/components/live-feed/` component that polls `dashboard/outputs/` for new `.json` files every 30 seconds. Each skill run writes a `{skill}-running.json` stub at start (via a `./notify-running` hook in the scheduler) and replaces it with `{skill}-{date}.json` on completion. The feed component distinguishes "running" stubs (yellow dot, elapsed time) from "completed" entries (green dot, output preview).
2. Add a `./notify-running "skill-name"` script that writes a minimal running-state JSON to `dashboard/outputs/{skill}-running.json`: `{status: "running", skill, started_at, pid}`. The scheduler calls this at the start of each skill invocation. On completion, `./notify` overwrites the running stub with the final output.
3. Wire the live feed into the dashboard layout as a sidebar panel: last 10 events (running or completed), each with skill name, status indicator, elapsed/duration, and a link to the full output. Add a "Skills running now: N" badge to the dashboard header. This requires no backend — the file-watching approach works within the static-site model already in use.

---

## Summary

These 5 ideas reflect Aeon's current maturity stage: past the "does it work?" phase (smoke tests, cost reporting), now entering the "does it work *well*?" and "how do others use it?" phase. Skill Evals closes the output-quality gap that structural validation leaves open. The MCP adaptor opens a distribution channel that could 10x installs. Fork Fleet Coordination turns the 15-fork vanity metric into community intelligence. The Workflow Security Audit clears the technical debt before the MCP surface area expands. Dashboard Live Feed makes the operational state visible without requiring a GitHub Actions tab. All five are scoped for autonomous `feature` skill implementation with clear inputs, outputs, and no external approvals required.
