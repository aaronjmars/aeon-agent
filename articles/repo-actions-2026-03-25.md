# Repo Action Ideas — 2026-03-25 (Run 2)

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon)
**Stars:** 118 | **Forks:** 15 | **Language:** TypeScript | **Open Issues:** 0

Aeon is an autonomous agent running on GitHub Actions powered by Claude Code, with 50 skills across research, dev tooling, crypto monitoring, and productivity. The project has seen explosive development — 65+ commits in the last 14 days, shipping a local dashboard (Next.js), per-skill model overrides, token usage tracking, json-render feed system, and Telegram bidirectional messaging.

## Ecosystem Context (March 2026)

The AI agent skills ecosystem has matured dramatically:

- **Vercel Skills.sh** launched in Feb 2026 as an open standard for agent commands — already adopted by Claude Code, Codex, Gemini CLI, Cursor, and 12+ other agents. Skills.sh uses the same SKILL.md format Aeon already uses.
- **SkillsMP** hosts 145,000+ open-source skills. ClawHub has 5,700+. The skill economy is real.
- **ClawHavoc** (Feb 2026) exposed 341 malicious skills on ClawHub distributing macOS malware — security is now top-of-mind for every skill platform.
- **GitHub Agent HQ** (Feb 2026) lets users assign issues to Claude, Codex, or Copilot directly from GitHub — agents now compete on the same platform Aeon already runs on.
- **awesome-claude-code** hit 27k+ stars. The toolkit variant by rohitg00 trended #1 on GitHub in Feb 2026. Composio's awesome-claude-skills has 44k+ stars. These are the directories that matter.

Aeon's unique angle — zero-infra background agent on GitHub Actions, 50 built-in skills, markdown-only skill format — positions it perfectly in this landscape. The following ideas exploit that position.

---

### 1. Skills.sh Compatibility — Make Aeon Skills Installable Everywhere

**Type:** Integration / Growth
**Effort:** Medium (1-2 days)
**Impact:** Vercel's Skills.sh is becoming the npm of agent skills, already supporting 17+ agents including Claude Code and Codex. Aeon's 50 skills use the same SKILL.md format but aren't discoverable through Skills.sh. Publishing them there would instantly expose Aeon's entire library to hundreds of thousands of developers across every major coding agent. This is the single highest-leverage growth move available — turning Aeon from a standalone tool into a skills publisher for the entire ecosystem.

**How:**
1. Add a `skills.json` manifest at the repo root listing all 50 skills with metadata (name, description, tags, var schema) in the Skills.sh registry format.
2. Create a `publish-skills` GitHub Action that syncs the manifest to Skills.sh whenever skills are added or updated.
3. Add `skills install aaronjmars/aeon/<skill-name>` badges to each skill's README section, enabling one-command installation on any supported agent.

---

### 2. Skill Integrity Verification — Signed Skills & Import Audit

**Type:** Security
**Effort:** Small (hours)
**Impact:** ClawHavoc proved that the skill ecosystem has a trust problem — 341 malicious skills on ClawHub, 7.1% of registry skills leak API keys. Aeon's `search-skill` and `add-skill` commands import skills from external repos with no verification. Adding a lightweight integrity layer — SHA-256 checksums for installed skills, a warning when skills contain shell commands or URL fetches, and an audit log of all imported skills — would make Aeon the security-conscious choice. This matters especially for users running Aeon with API keys and wallet credentials.

**How:**
1. When `add-skill` imports a skill, compute and store its SHA-256 hash in `skills/.integrity.json`. On each run, verify the hash matches — alert if a skill was tampered with.
2. Add a static analysis pass that scans SKILL.md files for suspicious patterns: `curl | bash`, hardcoded URLs to unknown domains, instructions to exfiltrate env vars.
3. Surface an "Imported Skills Audit" section in the dashboard showing each external skill's source, install date, and integrity status.

---

### 3. GitHub Agent HQ Bridge — Accept Issue Assignments

**Type:** Feature / Integration
**Effort:** Medium (1-2 days)
**Impact:** GitHub Agent HQ now lets users assign issues directly to AI agents. Aeon already runs on GitHub Actions and has a `feature` skill that can implement code changes. Bridging the two — letting users assign a GitHub issue to Aeon and have it automatically pick it up, run the `feature` skill, and open a PR — would put Aeon on equal footing with Copilot and Codex in the Agent HQ paradigm. This is the natural evolution: Aeon already monitors repos, now it can act on direct assignments.

**How:**
1. Add an `issue_assigned` trigger to the Aeon workflow that fires when an issue is assigned to the Aeon bot account (or labeled `aeon`).
2. Route assigned issues to the `feature` skill with the issue body as the `var` input, including the issue number for PR cross-referencing.
3. Post a comment on the issue when work starts ("Aeon is working on this") and link the resulting PR when done.

---

### 4. Skill Run Analytics & Cost Dashboard

**Type:** DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Token usage tracking was just shipped (`feat: track token usage after each skill run`), and per-skill model overrides landed too. But there's no way to see the data — which skills cost the most, which fail often, how total spend trends over time. A `/analytics` page in the dashboard would close the observe-optimize loop: users could see that `repo-article` on Opus costs 10x more than `push-recap` on Sonnet, then make informed model-selection decisions. With Claude Opus 4.6 at ~$15/MTok output vs Haiku at ~$1.25/MTok, this visibility directly saves money.

**How:**
1. Parse `memory/logs/*.md` files and GitHub Actions API run data to extract per-skill metrics: run count, success/failure, duration, token usage, model used.
2. Add a `/analytics` route to the Next.js dashboard with summary cards (total runs, total tokens, total cost estimate) and time-series charts (daily spend by skill, success rate trend).
3. Add a "Cost Optimizer" recommendation: flag skills running on Opus that could use Sonnet based on their complexity profile (data-fetch skills vs creative-writing skills).

---

### 5. Awesome-Claude-Code & Ecosystem Directory Listings

**Type:** Growth
**Effort:** Small (hours)
**Impact:** awesome-claude-code has 27k+ stars and is the primary discovery channel for Claude Code extensions. awesome-claude-code-toolkit trended #1 on GitHub in Feb 2026. Composio's awesome-claude-skills has 44k+ stars. Aeon isn't listed on any of them. Given Aeon's unique positioning (50 skills, GitHub Actions-native, zero-infra, dashboard UI, bidirectional Telegram), it would immediately stand out in the "Autonomous Agents" or "Agent Orchestrators" sections. This is the lowest-effort, highest-visibility growth action available.

**How:**
1. Open PRs to [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code), [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit), and [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) adding Aeon with a compelling one-liner and link.
2. Submit to [AI Agents Directory](https://aiagentsdirectory.com/landscape) interactive map under "Autonomous Agents" category.
3. Add listing badges to the Aeon README for social proof and cross-discovery.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-25 (run 2). Ecosystem data from web search performed same day.*
