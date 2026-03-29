# Repo Action Ideas — 2026-03-29 (Run 2)

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 132 (aeon) / 4 (aeon-agent) | **Forks:** 15 / 0 | **Language:** TypeScript | **Open Issues:** 4 / 4
**Contributors:** aaronjmars (132 commits), github-actions[bot] (43), Aeon (11)

Aeon is at 132 stars with 57 skills, 4 open PRs on each repo. The aeon repo has shipped major infrastructure this week: skill forking (PR #3), RSS feed generator (PR #4), agentic workflow templates (PR #2), and analytics dashboard (PR #1). On aeon-agent, self-improvement PRs are stacking up (heartbeat timing, per-skill models, tweet dedup, PR awareness guard). The repo-actions skill has now generated 30 ideas across 6 runs; several have been built (skill forking, per-skill models, RSS feed, PR guard). This run focuses on distribution and ecosystem integration — packaging Aeon for the exploding Claude Code plugin ecosystem, listing on emerging skill registries, and migrating to GitHub's native agentic workflows.

## Ecosystem Context (March 29, 2026)

- **Claude Code plugin ecosystem at 9,000+ plugins** — ClaudeMarketplaces.com lists 2,300+ skills and 770+ MCP servers. Anthropic now has an official plugin directory with verified badges. Aeon's 57 skills are the right format but aren't listed anywhere — invisible to the 5.2M Claude Code VS Code users. ([source](https://claudemarketplaces.com/))
- **Vercel launched Skills.sh — "npm for AI agents"** — An open ecosystem for sharing agent commands, prioritizing composability over protocol complexity. While MCP solved how agents talk to tools, Skills.sh solves how devs share and discover agent capabilities. Aeon skills are already SKILL.md files — the native format. ([source](https://www.infoq.com/news/2026/02/vercel-agent-skills/))
- **SkillsMP hit 145,964 skills; Skills4Agents launching paid tiers** — The skills marketplace is exploding. Skills4Agents offers monetization at $10–$500 per skill, creating a creator economy for agent capabilities. Aeon's specialized skills (token-report, polymarket, code-health) have no equivalents at this quality level. ([source](https://calmops.com/ai/ai-agent-skills-complete-guide-2026/))
- **GitHub Agentic Workflows in technical preview** — Markdown-authored workflows that run coding agents (Copilot CLI, Claude Code, Codex) in sandboxed GitHub Actions. Native triggers for issues, PRs, schedules, and comments. This is exactly what Aeon does manually — but with GitHub's security model (read-only by default, safe outputs for writes, tool allowlisting). ([source](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/))
- **Only 130 of thousands of "AI agent" vendors are genuinely agentic** — Analysts estimate massive overcount in agent claims. Aeon's daily autonomous operation with self-improvement PRs, memory management, and multi-skill orchestration puts it in the genuine tier. Credentialing matters as the market matures. ([source](https://joget.com/ai-agent-adoption-in-2026-what-the-analysts-data-shows/))

Previous runs (Mar 25–29) generated 30 ideas covering: plugin registration, skill DAG, community validation, state snapshots, Telegram control plane, skill evals, awesome-list, agentic workflow templates, SkillsMP publish, A/B testing, cost tracker, security audit, live feed, dependency chains, memory search, A2A gateway, OTEL tracing, Agent SDK runner, autonomy levels, context budgets, multi-model routing, skill forking, webhook triggers, reputation dashboard, Telegram skill store, MCP adaptor, skill smoke tests, onboarding wizard, RSS feed, and skill metrics. The following 5 ideas are entirely new.

---

### 1. Claude Code Plugin Package — Ship Aeon as a First-Class Plugin

**Type:** Integration / Growth
**Effort:** Medium (1-2 days)
**Impact:** The Claude Code plugin ecosystem has 9,000+ extensions across multiple directories — but Aeon isn't one of them. A proper plugin package would bundle Aeon's top skills as slash commands (e.g., `/aeon-digest`, `/aeon-token-report`), register its MCP server for json-render, and include hooks for automatic skill execution on file changes or git events. This is different from the MCP adaptor idea (run 6) — that exposed skills as MCP tools for programmatic invocation. A plugin is user-facing: it shows up in Claude Code's plugin list, gets an entry on ClaudeMarketplaces.com and Anthropic's official directory, and can earn an "Anthropic Verified" badge. With 5.2M VS Code installs, even 0.1% adoption is 5,200 users — 40x Aeon's current star count. The plugin format also bundles agents, hooks, and templates alongside skills, enabling richer integration than raw SKILL.md files.

**How:**
1. Create a `plugin/` directory following the [Claude Code plugin spec](https://code.claude.com/docs/en/plugins): `plugin.json` manifest with name, version, description, and entry points. Map 10 high-value skills to slash commands: `/aeon-digest`, `/aeon-token-report`, `/aeon-push-recap`, `/aeon-code-health`, `/aeon-pr-review`, `/aeon-changelog`, `/aeon-hn-digest`, `/aeon-polymarket`, `/aeon-write-tweet`, `/aeon-morning-brief`.
2. Include a pre-configured MCP server entry for json-render and an agent definition for "Aeon background tasks" that runs skills on a schedule when Claude Code is open. Add hooks that trigger `pr-review` on git push and `code-health` on file saves.
3. Submit to Anthropic's plugin directory and ClaudeMarketplaces.com. Add install instructions to the README: `claude plugin install aaronjmars/aeon`. Target the "Anthropic Verified" badge by following their quality guidelines.

---

### 2. Skills.sh Registry Listing — Tap Into Vercel's Distribution Layer

**Type:** Growth / Community
**Effort:** Small (hours)
**Impact:** Vercel's Skills.sh is positioning as "npm for AI agents" — the canonical registry for discovering and installing agent skills. It prioritizes composability: skills are versioned, tagged, and installable via a single command. Aeon has 57 skills that are already in the SKILL.md format Skills.sh expects, but none are registered. Listing even the top 15 skills would make Aeon the largest single contributor to the registry, establishing it as a foundational skill library in the ecosystem. Skills.sh also supports dependency declarations — Aeon's composable skills (morning-brief depends on rss-digest + hn-digest) would showcase the platform's composition model. This is the lowest-effort, highest-visibility growth play: the registry is new, early movers get prime placement, and the format is already native.

**How:**
1. Create a `scripts/publish-skills-sh.sh` that reads `skills.json` (already generated by the skill-forking PR) and registers each skill on Skills.sh using their CLI: `skills publish --name aeon-token-report --description "..." --file skills/token-report/SKILL.md --tags crypto,monitoring,daily`.
2. Add dependency metadata for composed skills: `morning-brief` depends on `rss-digest` + `hn-digest`; `daily-routine` depends on `token-movers` + `fetch-tweets` + `paper-pick` + `github-issues` + `hn-digest`. This demonstrates the composition model.
3. Add a "Available on Skills.sh" badge to the README with install commands for the top 5 most useful standalone skills. Run the publish script weekly via a `skills-publish` skill to keep the registry in sync as new skills are added.

---

### 3. GitHub Agentic Workflows Native Mode — Run on GitHub's Agent Infrastructure

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** GitHub's Agentic Workflows (technical preview, Feb 2026) let you write workflow instructions in plain Markdown inside `.github/workflows/`, triggered by issues, PRs, schedules, or comments. The runtime handles agent execution with sandboxing, safe outputs, and tool allowlisting — exactly the security model Aeon manually implements. Migrating Aeon's dispatch to native agentic workflows would: eliminate the custom workflow dispatcher (aeon.yml is 200+ lines of bash plumbing), inherit GitHub's security model (read-only by default, explicit write approvals), support any coding agent as the backend (not just Claude Code — users could swap in Copilot CLI or Codex), and enable comment-triggered skill invocation (`/aeon run token-report` in any issue or PR). This positions Aeon as a showcase project for GitHub's newest feature — likely to get visibility from GitHub's own promotion of the platform.

**How:**
1. Create `.github/workflows/aeon-agent.md` — a markdown-format agentic workflow that reads `aeon.yml` config, determines which skills are due based on schedule, and executes them. Use the `gh aw` CLI format with explicit tool permissions per skill category (read-only for data skills, write for content skills, full for feature skills).
2. Add issue-comment triggers: when someone comments `/aeon <skill-name> [var]` on any issue or PR, the workflow dispatches that skill with the comment context as input. This enables interactive agent invocation without leaving GitHub.
3. Keep the existing `aeon.yml` cron dispatch as a fallback for users not in the technical preview. Add a `runtime: agentic-workflows | classic` config option so users can opt in when ready.

---

### 4. Skill Monetization Pipeline — Publish Premium Skills on Skills4Agents

**Type:** Growth / Content
**Effort:** Small (hours)
**Impact:** Skills4Agents is launching with paid tiers at $10–$500 per skill, creating a creator economy for agent capabilities. Aeon has several skills with genuine alpha — `polymarket` (Gamma API integration, volume-sorted market analysis), `token-report` (on-chain + CoinGecko data synthesis), `code-health` (TODO/dead code/coverage analysis), and `self-improve` (autonomous PR generation with safety guards). These are non-trivial to build from scratch and have been battle-tested across 80+ daily runs. Packaging them as premium skills with documentation, example outputs, and configuration guides would generate revenue while marketing Aeon to a paying audience. Even at $10/skill, the listing itself drives discovery — paid marketplaces attract serious users, not tire-kickers. This also validates the skill-as-product model: if Aeon's skills sell, it proves the architecture creates real economic value.

**How:**
1. Select 5 premium-tier skills: `polymarket` (crypto market intelligence), `token-report` (on-chain analytics), `code-health` (codebase quality audit), `self-improve` (autonomous agent improvement), and `morning-brief` (aggregated daily intelligence). Package each with: SKILL.md, example output, required secrets list, setup guide, and a 1-paragraph value proposition.
2. Create a `skills/export/` script that generates a standalone skill package with all dependencies resolved — helper scripts, referenced memory files, notification setup. Use the existing `export-skill` from the skill-forking PR as the base.
3. List on Skills4Agents with appropriate pricing ($10 for single-purpose skills like `polymarket`, $25 for composed skills like `morning-brief`, $50 for meta-skills like `self-improve`). Add "Premium on Skills4Agents" badges to the README alongside the free open-source versions.

---

### 5. Skill Versioning and Upstream Sync — Keep Forkers in Lockstep

**Type:** DX Improvement / Community
**Effort:** Medium (1-2 days)
**Impact:** Aeon has 15 forks but zero external contributions. One reason: forkers can't tell when upstream skills have changed or whether their local modifications conflict with improvements. There's no versioning — a skill is just a markdown file that changes without notice. Adding semantic versioning to skills (major.minor.patch in frontmatter) with an automated changelog and sync checker would let forkers: see which skills have upstream updates, diff their local modifications against the latest version, and pull updates for skills they haven't customized. This is the missing piece that turns passive forkers into active ecosystem participants — they can confidently take upstream improvements without losing their customizations. The `skills.json` manifest already has the metadata infrastructure; versioning extends it with a time dimension.

**How:**
1. Add a `version` field to each SKILL.md frontmatter (start at `1.0.0`). Create a pre-commit hook or CI check that requires version bumps when a skill's Steps section changes (patch for fixes, minor for new features, major for breaking changes to var format or output structure).
2. Create a `skills/sync-check/SKILL.md` that compares a fork's `skills.json` versions against upstream's, generates a diff report showing which skills are behind, and posts a summary. Run it weekly or on-demand.
3. Add a `scripts/sync-upstream.sh` that fetches upstream skill versions and offers a three-way merge for each outdated skill: take upstream (overwrite), keep local (skip), or merge (show diff for manual resolution). Document the sync workflow in CONTRIBUTING.md to encourage forkers to stay current and submit improvements back.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-29 (run 2). This is run 7 overall, bringing the total to 35 ideas. Ecosystem data from web searches performed same day.*

Sources:
- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [ClaudeMarketplaces.com — Plugin & Skill Directory](https://claudemarketplaces.com/)
- [Vercel Skills.sh — InfoQ Coverage](https://www.infoq.com/news/2026/02/vercel-agent-skills/)
- [AI Agent Skills Complete Guide 2026 — Calmops](https://calmops.com/ai/ai-agent-skills-complete-guide-2026/)
- [GitHub Agentic Workflows Technical Preview](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)
- [Automate Repository Tasks with GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)
- [AI Agent Adoption 2026 — Analyst Data](https://joget.com/ai-agent-adoption-in-2026-what-the-analysts-data-shows/)
- [7 Agentic AI Trends to Watch in 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/)
- [Awesome Claude Plugins — ComposioHQ](https://github.com/ComposioHQ/awesome-claude-plugins)
