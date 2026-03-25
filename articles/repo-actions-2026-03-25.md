# Repo Action Ideas — 2026-03-25 (Run 3)

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon)
**Stars:** 118 | **Forks:** 15 | **Language:** TypeScript | **Open Issues:** 1 (PR: skill analytics dashboard)

Aeon is an autonomous background agent on GitHub Actions powered by Claude Code — 50 skills across research, dev tooling, crypto, and productivity. The last 14 days saw 65+ commits shipping a local dashboard, per-skill model overrides, token usage tracking, json-render feed, Telegram bidirectional messaging, and the first community PR (skill analytics dashboard). The aeon-agent instance has run 25+ skill executions in a single day across polymarket, push-recap, fetch-tweets, repo-actions, token-report, repo-article, write-tweet, and feature skills.

## Ecosystem Context (Late March 2026)

Key developments since last analysis:

- **Claude Code Plugin Marketplace** surfaced in settings.json in March 2026 — Claude Code is transitioning from a tool to a platform. This is a new distribution channel Aeon hasn't tapped.
- **Agent Skills Open Standard** adopted by 16+ tools (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, JetBrains Junie, etc.). SKILL.md format is now the lingua franca. Aeon's format is already compatible.
- **NIST AI Agent Standards Initiative** (Feb 2026) — government standardization of agent interoperability and security. Signals that agent trust/verification will become a compliance requirement.
- **Letta .af Agent File Format** — open format for packaging AI agents with memory and behavior, enabling checkpointing, version control, and portability across frameworks.
- **Claude Code v2.1.80** — Voice mode, /teleport (terminal-to-browser handoff), Opus 4.6 default with 1M context. Aeon could leverage these for richer interactions.
- **SkillsMP** now at 66,500+ skills. The "skill economy" is real — agencies charge for skill access rather than hours.

Previous runs already covered Skills.sh publishing, skill integrity verification, GitHub Agent HQ bridge, analytics dashboard (now built as PR #1), and awesome-list submissions. The following 5 ideas are new opportunities.

---

### 1. Claude Code Plugin Registration — Become a First-Class Plugin

**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** Claude Code's settings.json now includes a plugin marketplace, signaling a shift from tool to platform. Aeon's skills are already SKILL.md-compatible, but registering as a Claude Code plugin would make Aeon discoverable directly from Claude Code's interface — no GitHub visit needed. With Claude Code's 17 releases in 30 days and rapid adoption, early plugins get disproportionate visibility. This is the equivalent of being in the App Store at launch.

**How:**
1. Create a `claude-plugin.json` manifest at the repo root following the Claude Code plugin spec — listing Aeon's name, description, install command, and skill categories.
2. Add a `claude code install aaronjmars/aeon` one-liner to the README and submit to the Claude Code plugin directory.
3. Ensure the `./aeon` launcher script works as a plugin entry point, auto-launching the dashboard when installed via Claude Code.

---

### 2. Skill Composition DAG — Formalize Multi-Skill Pipelines

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Aeon already supports ad-hoc skill composition (e.g., `morning-brief` reads `rss-digest` and `hacker-news-digest` inline). But this is implicit — there's no dependency graph, no caching of intermediate results, no parallel execution of independent sub-skills. Formalizing this into a `depends_on` field in aeon.yml would unlock pipelines: `daily-routine` could declare it depends on `token-movers`, `hn-digest`, and `github-issues`, and the scheduler would run dependencies first (in parallel where possible), cache their outputs, and pass them to the parent skill. This turns Aeon from a skill runner into a workflow engine.

**How:**
1. Add an optional `depends_on: [skill1, skill2]` field to the skill config in `aeon.yml`. The scheduler resolves the DAG and runs dependencies before the parent skill.
2. Store sub-skill outputs in a `runs/outputs/` directory keyed by skill name and date. The parent skill reads these instead of re-running the sub-skill.
3. Add a "Pipeline View" to the dashboard showing the dependency graph for composite skills, with status indicators for each stage.

---

### 3. Community Skill Contributions — Auto-Validate Incoming PRs

**Type:** Community / DX Improvement
**Effort:** Small (hours)
**Impact:** Aeon has 50 skills but only 1 contributor. The skill format is trivially simple (a SKILL.md file), making community contributions low-friction — but there's no contribution guide, no validation CI, and no template. Adding a `CONTRIBUTING.md`, a skill template generator, and a GitHub Action that validates incoming skill PRs (checks SKILL.md frontmatter, lints for security anti-patterns, runs a dry-run test) would open the door to community skills without requiring manual review of every submission. With 15 forks already, the contributor base exists — they just need a runway.

**How:**
1. Create `CONTRIBUTING.md` with a "Add a Skill" guide: fork, create `skills/<name>/SKILL.md`, add frontmatter (name, description, var), write instructions, open PR.
2. Add a `validate-skill` GitHub Action triggered on PRs touching `skills/*/SKILL.md` — checks frontmatter schema, scans for security patterns (no hardcoded URLs, no env exfiltration), verifies the skill directory structure.
3. Create a `build-skill` template: `gh repo create-from-template aaronjmars/aeon-skill-template` that scaffolds a new skill with example SKILL.md, README, and test instructions.

---

### 4. Agent State Snapshots — Export & Restore Memory + Config

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Aeon accumulates state over time — memory files, watched repos, log history, skill configs, articles. There's no way to snapshot this state, share it, or restore it. Inspired by Letta's .af agent file format, an export/import system would let users checkpoint their agent ("save before I experiment"), share configurations ("here's my crypto-monitoring Aeon setup"), or migrate between repos. This is especially valuable for the 15 forks — they could import the original's memory topics without replicating the discovery process.

**How:**
1. Add an `export-state` skill that bundles `memory/`, `aeon.yml`, and `memory/watched-repos.md` into a single `.aeon-snapshot.json` file with metadata (export date, skill count, memory size).
2. Add an `import-state` skill that reads a snapshot file and merges it into the current repo — with conflict resolution (skip existing memories, merge watched repos, prompt on config differences).
3. Store snapshots in `snapshots/` directory and add a "Snapshots" section to the dashboard for visual export/import.

---

### 5. Telegram as Full Control Plane — Manage Skills from Chat

**Type:** Feature / DX Improvement
**Effort:** Medium (1-2 days)
**Impact:** Aeon already supports bidirectional Telegram messaging — users can trigger skills by chatting. But the control surface is limited to "run this skill." Expanding Telegram into a full control plane — enable/disable skills, view run status, adjust schedules, see recent notifications — would let users manage Aeon entirely from mobile without opening the dashboard or GitHub. This is the "butler" UX: tell Aeon what to do from your phone, check in later for results. Key commands: `/skills` (list enabled), `/enable <skill>`, `/disable <skill>`, `/status` (last 5 runs), `/schedule <skill> <cron>`.

**How:**
1. Extend the Telegram message handler to parse command-style messages (`/skills`, `/enable`, `/disable`, `/status`, `/schedule`) and dispatch them to appropriate handlers.
2. For `/enable` and `/disable`, modify `aeon.yml` in-place, commit, and push — mirroring what the dashboard does. For `/status`, query the GitHub Actions API and format a concise run summary.
3. Add a `/help` command that lists all available Telegram commands with examples, and a confirmation step for destructive actions (disable, schedule changes).

---

*Generated by Aeon's `repo-actions` skill on 2026-03-25 (run 3). Ecosystem data from web search performed same day.*
