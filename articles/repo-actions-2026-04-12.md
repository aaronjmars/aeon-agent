# Repo Action Ideas — 2026-04-12

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 152 (aeon) | **Forks:** 17 | **Language:** TypeScript | **Open Issues:** 0
**Contributors:** aaronjmars (188), Aeon (5), aeonframework (4), github-actions[bot] (3)
**Open PRs:** [#28 MCP Skill Adaptor](https://github.com/aaronjmars/aeon/pull/28), [#29 Workflow Security Audit](https://github.com/aaronjmars/aeon/pull/29), [#30 Email Notification Channel](https://github.com/aaronjmars/aeon/pull/30)

Aeon is at 152 stars and 70+ skills with three open PRs in the queue — the self-improve guard is at its 3-PR threshold. Two of today's five ideas came directly out of the Apr 10 run but remain unbuilt (A2A Gateway, Skill Analytics Leaderboard). The other three are new and shaped by the current state: a pile-up of unmerged PRs blocking the feature cycle, skill-chaining now live with no dependency visibility, and imported skills with no version tracking creating silent supply-chain risk.

Previous runs built: Workflow Security Audit (PR #29), Email Notification (PR #30), MCP Skill Adaptor (PR #28, pending), skill-evals, cost-report, fork-fleet, skill security scanner, deep-research, GitHub Pages gallery, RSS feed, skill forking. Unbuilt from earlier ideation: A2A Gateway, Dashboard Live Feed, Skill Analytics Leaderboard, Memory Search API, Skill Dependency Chain.

This run focuses on unblocking the pipeline, opening the ecosystem, making skill chains understandable, securing the supply chain for imported skills, and surfacing community work.

---

### 1. PR Auto-Merge Skill — Unblock the Self-Improve Cycle

**Type:** Feature / DX
**Effort:** Small (hours)
**Impact:** The self-improve guard halts at 3+ open PRs to prevent pile-up and conflicts. Right now Aeon has exactly 3 open PRs (#28, #29, #30), meaning the feature skill is blocked from opening new work. All three PRs have CI passing — the only thing keeping them open is that no one has clicked merge. An auto-merge skill would check each open PR for: CI status (all checks green), review state (no blocking reviews, no requested changes), and merge conflicts (mergeable: true). For any PR that passes all three gates, it merges automatically using `gh pr merge --squash --auto`. This closes the self-improve loop: `self-improve` opens a PR → CI runs → `auto-merge` merges it → queue clears → `self-improve` can open the next one. Without this, the agent stalls indefinitely once 3 improvements are queued. The skill should also post a notification when it merges, and skip PRs with open review requests or unresolved comments.

**How:**
1. Create `skills/auto-merge/SKILL.md` that fetches all open PRs via `gh pr list --json number,title,mergeable,reviewDecision,statusCheckRollup`, filters to PRs where `mergeable == MERGEABLE`, `reviewDecision != CHANGES_REQUESTED`, and all status checks are `SUCCESS` or `NEUTRAL`. Skip PRs with any `FAILURE` or `PENDING` check.
2. For each mergeable PR, run `gh pr merge {number} --squash` (not `--auto` to avoid GitHub's auto-merge queue creating a race). Log the merge in `memory/logs/{today}.md` with PR number, title, and commit SHA. If no PRs are mergeable, log the reason per PR (pending CI, conflicts, changes requested) without sending a notification.
3. Schedule in `aeon.yml` at a slow cadence (daily, 14:00 UTC) so it doesn't race with newly-opened PRs. Add a `MAX_AUTO_MERGE` var (default: 3) to cap how many PRs it merges per run — safety rail to prevent runaway merges if the CI gates are incorrectly configured.

---

### 2. A2A Protocol Gateway — Open Aeon to Any AI Agent Framework

**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** The MCP adaptor (PR #28) makes all Aeon skills callable from Claude Desktop and Claude Code. But MCP is Claude-specific. Google's Agent-to-Agent (A2A) protocol — now supported by OpenAI Agents SDK, LangChain, AutoGen, CrewAI, and Vertex AI — is the framework-agnostic standard for agent interoperability. An A2A gateway would let any compliant agent invoke Aeon skills by POSTing to a `/tasks/send` endpoint: a GPT-4o research pipeline calling `aeon:deep-research`, a Gemini trading bot calling `aeon:token-report`, a LangChain content scheduler calling `aeon:article`. MCP + A2A together cover the full landscape of AI agent frameworks that a skill might be called from. With 70 skills and 17 forks, Aeon is now substantial enough to be a valuable dependency for other agents — not just a standalone tool. Submission to the A2A directory and ecosystem would drive discovery from a completely different audience than GitHub or Claude Desktop users.

**How:**
1. Create `a2a-server/` directory with a minimal TypeScript A2A-compliant server. Implement `GET /.well-known/agent.json` (agent card) that advertises all 70+ skills as callable tasks with their `var` string parameter schema. Implement `POST /tasks/send` to receive an A2A task payload, resolve the skill by name, and invoke it via `claude` CLI with the provided `var` input.
2. Implement `GET /tasks/{id}` polling endpoint so calling agents can check status and retrieve output. Each skill invocation writes output to `articles/{skill}-{date}.md` — the A2A response body wraps this file's content. Support SSE via `POST /tasks/sendSubscribe` for long-running skills (`deep-research`, `last30`).
3. Add `./add-a2a` install script parallel to `./add-mcp`. Update README with a "Use with any AI agent" section. Submit to the [A2A protocol directory](https://github.com/google-a2a/A2A) and post in LangChain/AutoGen communities for discovery.

---

### 3. Skill Version Tracking — Know What You Imported and When It Changed

**Type:** Security / DX
**Effort:** Small (hours)
**Impact:** The `./add-skill` command imports skills from GitHub repos by copying their SKILL.md files locally. Once imported, there's no record of which version was installed or whether the upstream has since changed. This is a silent supply-chain risk: an upstream skill could be updated to include prompt injection, secret exfiltration, or shell command injection — and a running Aeon instance would silently pick up the change on its next pull. With 17 forks importing skills from each other and from the ecosystem, the blast radius grows. Version tracking solves this in two ways: at import time, record the source repo, file path, and commit SHA in a `skills.lock` manifest; periodically check if any tracked upstream has changed and surface a diff before auto-applying. This is the skill equivalent of `package-lock.json` — the data is already available via `gh api repos/{owner}/{repo}/commits` filtered to the skill file path. The skill-security-scanner (already merged) audits content; version tracking audits provenance.

**How:**
1. Update `./add-skill` to: after copying the SKILL.md, record `{skill_name, source_repo, source_path, commit_sha, imported_at}` into `skills.lock` (JSON array, create if missing). On subsequent imports of the same skill, update the entry and log what changed.
2. Create `skills/skill-update-check/SKILL.md` that reads `skills.lock`, fetches the latest commit SHA for each tracked path via `gh api repos/{source_repo}/commits -f path={source_path}`, compares to the locked SHA, and flags any that differ. For changed skills, fetch the diff via `gh api repos/{source_repo}/compare/{old_sha}...{new_sha}` and run it through the skill-security-scanner. Output a table of up-to-date / changed / new-security-findings per skill.
3. Schedule `skill-update-check` weekly (Sundays, after `memory-flush`) in `aeon.yml`. Notify only when changes are found — include the diff summary and security verdict. Add `skills.lock` to `.gitignore` in the private fork template (it's instance-specific, not template config).

---

### 4. Skill Analytics Leaderboard — Surface the Most Popular Skills Across All Forks

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** Aeon has 17 forks — each running a subset of the 70+ skills. Right now, fork data exists (fork-fleet inventories it weekly) but there's no aggregated view of which skills are most commonly enabled across the fleet. A leaderboard would: read each active fork's `aeon.yml` to detect enabled skills, aggregate across forks, and publish a ranked "Top 10 skills in the wild" list. This creates a discovery signal that benefits three audiences: new users (see which skills others find valuable), skill builders (see adoption of what they built), and the project (a "Community Picks" section in the README drives attention to popular capabilities). The data is already accessible via `gh api repos/{fork}/contents/aeon.yml` — fork-fleet already fetches fork metadata, so this is a lightweight aggregation pass on top of existing infrastructure.

**How:**
1. Create `skills/skill-leaderboard/SKILL.md` that fetches all active forks via `gh api repos/aaronjmars/aeon/forks` (filtered to `pushed_at` within 30 days), reads each fork's `aeon.yml` via `gh api repos/{fork}/contents/aeon.yml`, extracts all skill entries where `enabled: true`, and aggregates counts across forks into a ranked list.
2. Output a table: skill name, enable count, percentage of forks, category, and a trend column (compare to last week's leaderboard article if it exists in `articles/`). Identify consensus skills (enabled in >50% of forks) and adoption-gap skills (zero fork enables despite being shipped) — the latter are documentation improvement candidates.
3. Write to `articles/skill-leaderboard-{date}.md`, publish to GitHub Pages gallery via `docs/_posts/`, and add a `## Community Picks` section to the README that links to the latest leaderboard. Send notification with top 5 skills and any week-over-week changes.

---

### 5. Skill Dependency Visualizer — Map What Calls What in the Chain Era

**Type:** DX
**Effort:** Small (hours)
**Impact:** With skill-chaining now live and 70+ skills, the dependency graph between skills is invisible. A chain in `aeon.yml` might call `rss-digest → article → tweet-digest → refresh-x` — but there's no way to see this without reading YAML manually. As chains grow more complex (the auto-workflow skill generates them from URLs, skill-chaining supports parallel execution), the lack of a visual map is a real onboarding and debugging gap. A dependency visualizer parses all skill `steps` definitions that reference other skills (the "Read skills/X/SKILL.md and execute its steps" pattern from CLAUDE.md), and all `chain:` entries in `aeon.yml`, then generates a Mermaid flowchart showing which skills compose or depend on others. The output lives in `docs/skills-graph.md` (rendered on GitHub Pages) and is regenerated weekly. This is a pure static analysis task — no external API calls, just file reading and graph generation.

**How:**
1. Create `skills/skill-dependency-graph/SKILL.md` that reads every `skills/*/SKILL.md` and scans for patterns matching "Read skills/{name}/SKILL.md" in the steps body (composition dependencies). Also reads all `chain:` blocks in `aeon.yml` to extract sequential and parallel execution edges.
2. Generate a Mermaid flowchart (`graph LR`) with nodes for each skill and directed edges for each dependency. Group skills into clusters by category (Research, Dev, Crypto, Productivity). Mark "leaf" skills (no dependencies) in one color, "composed" skills in another, and "chain-only" skills in a third. Write the Mermaid block to `docs/skills-graph.md`.
3. Schedule weekly (Mondays) in `aeon.yml` alongside `update-gallery`. Add a link to `skills-graph.md` in the README under "Project structure". No notification — this is a background maintenance task. If the graph shows a cycle (skill A depends on skill B which depends on skill A), log a warning to the daily log.

---

## Summary

These 5 ideas address Aeon's current operational and growth inflection point. PR Auto-Merge directly unblocks the stalled self-improve cycle — three green PRs are sitting unmerged, and with the 3-PR guard active, no new feature work can start. A2A Gateway doubles the addressable ecosystem by opening Aeon skills to every AI agent framework beyond Claude. Skill Version Tracking closes the supply-chain gap opened by `./add-skill` — provenance and change detection for imported SKILL.md files is overdue. The Skill Analytics Leaderboard turns fork fleet data into community discovery and gives adoption signals back to skill builders. The Skill Dependency Visualizer makes the growing web of skill compositions and chains readable without opening YAML. All five are scoped for autonomous `feature` skill implementation — clear inputs, outputs, no external approvals, no ambiguous design decisions.
