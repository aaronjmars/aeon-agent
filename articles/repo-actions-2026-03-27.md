# Repo Action Ideas — 2026-03-27

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon)
**Stars:** 125 | **Forks:** 15 | **Language:** TypeScript | **Open Issues:** 1 (PR #1: skill analytics dashboard)

Aeon is an autonomous background agent on GitHub Actions powered by Claude Code — 47 skills across research, dev tooling, crypto, and productivity. Since the last repo-actions run (Mar 25), the repo gained 7 stars (118→125), shipped the json-render feed pipeline, Tailwind v4 dashboard overhaul, per-skill model overrides, and token usage tracking. The aeon-agent instance runs 6+ skills daily across token-report, push-recap, fetch-tweets, repo-article, repo-pulse, and repo-actions.

## Ecosystem Context (Late March 2026)

Key developments informing today's ideas:

- **Anthropic Skill-Creator 2.0** (Mar 3, 2026) — skills can now be tested with evals, benchmarked across model versions, and iteratively improved in an automated loop. Four modes: Create, Eval, Improve, Benchmark. An audit of 25 skills produced a 78/100 health score — proving most skills have room to improve. ([source](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills))
- **githubnext/awesome-continuous-ai** — GitHub's official curated list of Continuous AI tools and frameworks. Lists Copilot Coding Agent, Claude Code GitHub Actions, Amazon Q Developer, Continue, and GitHub Agentic Workflows. Aeon is not listed yet. ([source](https://github.com/githubnext/awesome-continuous-ai))
- **GitHub Agentic Workflows** (Feb 13, 2026) — write workflows in plain Markdown in `.github/workflows/`, supports multiple agent engines (Copilot CLI, Claude Code, Codex). Open source under MIT. ([source](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/))
- **SkillsMP at 66,500+ skills** — the dominant marketplace for agent skills. Aeon's 47 skills are SKILL.md-compatible but not published there. ([source](https://skillsmp.com/))
- **Claude Code Auto Mode** (research preview) — allows Claude Code to run with greater autonomy. Combined with /loop for background scheduling, this opens new patterns for always-on skill execution. ([source](https://techcrunch.com/2026/03/24/anthropic-hands-claude-code-more-control-but-keeps-it-on-a-leash/))

Previous runs (Mar 25, runs 1-3) covered: skill marketplace, multi-agent orchestration, awesome-claude-code listing, analytics dashboard (now PR #1), interactive skill builder, Skills.sh compatibility, skill integrity verification, GitHub Agent HQ bridge, Claude Code plugin registration, skill composition DAG, community contributions guide, agent state snapshots, and Telegram control plane. The following 5 ideas are entirely new.

---

### 1. Skill Evals Suite — Test All 47 Skills with Anthropic's New Eval Framework

**Type:** DX Improvement / Security
**Effort:** Medium (1-2 days)
**Impact:** Anthropic's skill-creator 2.0 introduced eval and benchmark modes specifically designed to test whether skills work correctly. Aeon has 47 skills with zero test coverage — no way to know which ones break when models update, which produce degraded output, or which have become redundant as Claude's baseline improves. Running a full eval suite would produce a health score for each skill, identify weak/broken skills before users hit them, and create a regression baseline for future model upgrades. The reference audit of 25 skills scored 78/100 — Aeon's 47 skills likely have similar gaps.

**How:**
1. Create `skills/eval-suite/SKILL.md` — a meta-skill that iterates over all enabled skills, generates test prompts from each skill's description and `var` field, runs eval mode, and collects pass/fail/score results.
2. Output a `skill-health-report.md` with per-skill scores, failure reasons, and recommendations (remove, improve, or keep). Add a "Health" column to the dashboard skills tab.
3. Schedule weekly via cron so skill health is tracked over time and regressions are caught early — especially after Claude model updates.

---

### 2. Awesome Continuous AI Listing — Get on GitHub's Official Agent Directory

**Type:** Growth
**Effort:** Small (hours)
**Impact:** `githubnext/awesome-continuous-ai` is GitHub's official curated list of tools that use AI to automate software collaboration — the exact category Aeon belongs to. The list currently features Copilot Coding Agent, Claude Code GitHub Actions, Amazon Q Developer, and GitHub Agentic Workflows. Aeon is a production example of continuous AI: it runs on GitHub Actions, executes skills on cron schedules, monitors repos, writes articles, and commits its own changes. Getting listed here puts Aeon in front of every developer exploring the continuous AI space — alongside GitHub's own tools, not buried in a community awesome-list. This is a higher-signal listing than awesome-claude-code because it's maintained by GitHub Next (the R&D team).

**How:**
1. Open a PR to `githubnext/awesome-continuous-ai` adding Aeon under the "Frameworks" or "Actions" section with a one-line description: "Autonomous background agent on GitHub Actions — 47 skills for research, monitoring, crypto, and dev tooling, powered by Claude Code."
2. Ensure the Aeon README has a clear "Continuous AI" framing — emphasize cron-scheduled skills, self-committing outputs, and GitHub Actions-native execution.
3. Cross-submit to `caramaschiHG/awesome-ai-agents-2026` (25k+ stars, trending #1 in Feb) and `e2b-dev/awesome-ai-agents` for broader coverage.

---

### 3. GitHub Agentic Workflows Templates — Ship .md Workflows for Common Tasks

**Type:** Integration / Community
**Effort:** Medium (1-2 days)
**Impact:** GitHub Agentic Workflows let anyone write automation in plain Markdown — `.github/workflows/issue-triage.md` instead of complex YAML. The system supports multiple agent engines including Claude Code. Aeon already has 47 skill definitions in Markdown. Shipping a set of `.md` workflow templates that wrap Aeon's best skills (issue triage, PR review, changelog generation, security digest) as GitHub Agentic Workflows would let any repo use Aeon's logic without forking the entire project. This positions Aeon as a skill library for the emerging `.md workflow` ecosystem — a distribution channel that didn't exist two months ago.

**How:**
1. Create a `workflows/` directory with 5 `.md` workflow templates: `issue-triage.md`, `pr-review.md`, `changelog.md`, `security-digest.md`, and `code-health.md`. Each references the corresponding Aeon skill and includes the natural-language workflow description GitHub Agentic Workflows expects.
2. Add a "Use as GitHub Agentic Workflow" section to the README showing how to copy a single `.md` file into any repo's `.github/workflows/` directory.
3. Submit the templates to the `gh-aw` community examples directory for upstream visibility.

---

### 4. SkillsMP Bulk Publish — List All 47 Skills on the Dominant Marketplace

**Type:** Growth / Community
**Effort:** Small (hours)
**Impact:** SkillsMP has 66,500+ skills and is the dominant discovery platform for agent skills across Claude Code, Codex, and ChatGPT. Aeon's skills are already in SKILL.md format — fully compatible — but none are published there. Bulk-publishing all 47 skills would make them individually discoverable by the tens of thousands of developers browsing SkillsMP. Each skill listing links back to the Aeon repo, creating 47 inbound discovery paths instead of relying solely on the repo's README. This is especially valuable for niche skills (polymarket, token-alert, defi-monitor) that developers search for by keyword rather than by agent name.

**How:**
1. Create a `publish-skills` script that reads each `skills/*/SKILL.md`, extracts frontmatter (name, description), and generates the SkillsMP submission format (or uses their API/CLI if available).
2. Submit all 47 skills with proper categorization: Research & Content, Dev & Code, Crypto / On-chain, Social & Writing, Productivity, and Meta/Ops.
3. Add "Available on SkillsMP" badges to the README skills table, linking each skill to its marketplace listing for easy installation by non-Aeon users.

---

### 5. Skill A/B Testing in Dashboard — Compare Skill Versions Before Deploying

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Anthropic's skill-creator 2.0 introduced an "Improve" mode that does blind A/B comparisons between skill versions. Aeon's dashboard already manages skills (enable/disable, configure vars, trigger runs) but has no way to compare outputs between skill versions. Adding A/B testing would let users edit a skill, run both versions on the same input, and see a side-by-side comparison before committing the change. This is especially valuable for tuning high-stakes skills like `write-tweet` (tone matters), `token-report` (accuracy matters), and `repo-article` (quality matters). It turns the dashboard from a control panel into a skill development environment.

**How:**
1. Add a "Test" button next to each skill in the dashboard that opens a split-pane view. The left pane shows the current skill output; the right pane lets the user edit the SKILL.md and see the output of the modified version on the same `var` input.
2. Implement a lightweight eval: after both versions run, prompt Claude to do a blind comparison (skill outputs are anonymized as Version A and Version B) and produce a preference rating with reasoning.
3. If the user accepts the new version, the dashboard commits the updated SKILL.md and pushes — same flow as existing config changes.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-27. Ecosystem data from web searches performed same day.*

Sources:
- [Anthropic Skill-Creator 2.0](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
- [githubnext/awesome-continuous-ai](https://github.com/githubnext/awesome-continuous-ai)
- [GitHub Agentic Workflows Technical Preview](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)
- [SkillsMP Marketplace](https://skillsmp.com/)
- [Claude Code Auto Mode (TechCrunch)](https://techcrunch.com/2026/03/24/anthropic-hands-claude-code-more-control-but-keeps-it-on-a-leash/)
- [awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026)
- [GitHub Agentic Workflows Blog](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)
