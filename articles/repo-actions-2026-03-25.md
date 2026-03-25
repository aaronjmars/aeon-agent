# Repo Action Ideas — 2026-03-25

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon)
**Stars:** 118 | **Forks:** 15 | **Language:** TypeScript | **Open Issues:** 0

Aeon is an autonomous agent running on GitHub Actions powered by Claude Code, with 47 skills across research, dev tooling, crypto monitoring, and productivity. The project has seen rapid development — 60+ commits in the last 14 days, adding a local dashboard, model selection, inline run viewer, skill upload, and Telegram messaging.

The AI agent ecosystem is exploding in 2026. OpenClaw passed 210k stars with its local-first plugin architecture. GitHub shipped Agentic Workflows in technical preview. Ruflo, Auto-Claude, and others are building multi-agent orchestration on Claude Code's Agent SDK. Meanwhile, visual workflow builders (n8n, Dify) are crossing 130k+ stars by making agents accessible to non-developers.

Aeon occupies a unique niche: zero-infra background intelligence on GitHub Actions. The following ideas aim to amplify that advantage.

---

### 1. Skill Marketplace — Publish and Install Community Skills

**Type:** Community / Growth
**Effort:** Medium (1-2 days)
**Impact:** Aeon already has `search-skill` and `build-skill`, but there's no central registry where users can discover and share skills. A lightweight marketplace (a curated JSON index on GitHub + a `./aeon install <skill-url>` CLI command) would turn Aeon from a solo tool into a platform. OpenClaw's plugin ecosystem is a major driver of its growth — Aeon can do the same with less infrastructure since skills are just markdown files.

**How:**
1. Create a `skills-registry` repo (or a `registry.json` in the main repo) with metadata: name, description, author, tags, install URL.
2. Extend the `search-skill` skill to query this registry and display results with install commands.
3. Add a "Publish Skill" button to the dashboard that generates a PR to the registry with the skill's metadata.

---

### 2. Multi-Agent Skill Orchestration with Subagents

**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Claude Code's Agent SDK now supports spawning subagents that work in parallel. Currently Aeon runs skills sequentially within a single agent context. Adding subagent orchestration would let composite skills like `morning-brief` and `daily-routine` run their constituent skills in parallel, cutting execution time by 3-5x and reducing Actions minutes. This is the architectural pattern that Ruflo and Auto-Claude are built around — Aeon should adopt it natively.

**How:**
1. Update the skill runner to detect composite skills (those that reference other skills via "Read skills/X/SKILL.md").
2. Use Claude Code's `Agent` tool to spawn each sub-skill as a parallel subagent with `run_in_background`.
3. Collect results and merge them in the parent skill context. Add a `parallel: true` flag in `aeon.yml` for skills that opt into this.

---

### 3. Awesome-Claude-Code Listing and Ecosystem Presence

**Type:** Growth
**Effort:** Small (hours)
**Impact:** The [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) list is becoming the go-to directory for Claude Code extensions, skills, and agent orchestrators. Aeon isn't listed yet. Getting listed alongside Ruflo, Auto-Claude, and others would expose Aeon to the exact audience that would use it — developers already working with Claude Code who want background automation. Given Aeon's 47 skills and unique GitHub Actions approach, it would stand out immediately.

**How:**
1. Open a PR to `hesreallyhim/awesome-claude-code` adding Aeon under the "Agent Orchestrators" or "Autonomous Agents" section.
2. Also submit to `caramaschiHG/awesome-ai-agents-2026` (300+ resources, updated monthly) in the "Autonomous Agents" category.
3. Add an "awesome-claude-code" badge to the Aeon README for cross-discovery.

---

### 4. Skill Run Analytics Dashboard

**Type:** DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Aeon has a dashboard for triggering and viewing runs, but no analytics on skill performance over time — which skills run most, which fail, average execution time, token usage trends. With `feat: track token usage after each skill run` already shipped, the data exists in logs. Surfacing it as charts in the dashboard would help users optimize their skill portfolio and catch regressions. This is the "observe" step in the plan-act-observe-reflect loop that's becoming the 2026 standard for agent architectures.

**How:**
1. Parse `memory/logs/*.md` and GitHub Actions run metadata to extract per-skill metrics: run count, success rate, duration, token usage.
2. Add a `/analytics` page to the Next.js dashboard with time-series charts (use a lightweight library like Chart.js or Recharts).
3. Surface actionable insights: "digest hasn't run in 3 days", "article skill uses 4x more tokens than average", "polymarket has 100% success rate".

---

### 5. Interactive Skill Builder in Dashboard

**Type:** DX Improvement / Community
**Effort:** Large (3+ days)
**Impact:** Aeon's skill format is simple (markdown + frontmatter), but creating a new skill still requires understanding the SKILL.md format, knowing which tools are available, and writing the steps manually. An interactive skill builder in the dashboard — with a form for name/description/schedule, a step editor with tool autocomplete, and a "test run" button — would dramatically lower the barrier to creating custom skills. This is how n8n and Dify grew to 130k+ stars: visual builders that let non-developers create sophisticated workflows.

**How:**
1. Add a `/build-skill` page to the dashboard with form fields for skill metadata (name, description, var placeholder, schedule).
2. Include a structured step editor where users can add steps with tool suggestions (web search, GitHub API, file operations) and preview the generated SKILL.md.
3. Wire the "Test Run" button to trigger a workflow_dispatch with the generated skill, showing results inline.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-25.*
