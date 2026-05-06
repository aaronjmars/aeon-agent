*Feature Built — 2026-05-06 — aaronjmars/aeon*

v4 Readiness Checker
Aeon now has a one-shot pre-flight check for the upcoming v4 release. When v4 lands, every fork operator can run this skill on their own fork and get a personalized list of what's safe to keep, what's about to change, and what custom skills they added that won't have an upstream answer — without having to read the v4 release notes line by line and cross-reference their own config.

Why this matters:
The operator has been signposting a v4 redesign on social — roughly two-week lead time. There are 40+ forks running on the current architecture today. Without a structured per-fork pre-flight, operators hit breaking changes blind: their custom aeon.yml contains a now-removed key, a chain consumer references a renamed skill, a model override points to a retired model. Every one of those is recoverable in five minutes if surfaced ahead of time and unrecoverable in five hours when a cron fires on it. This skill closes that gap. It was the highest-impact unbuilt in yesterday's repo-actions article (May-4 idea #5, also carried from May-2 idea #5 and Apr-30 idea #5).

What was built:
- skills/v4-readiness/SKILL.md — new sonnet skill with the v4 change manifest embedded directly in the SKILL.md itself (Safe / Review / Removed tables). Operators update the Manifest tables in place as v4 PRs land — no separate config file. Skill prose stays stable so the article can be regenerated without merging upstream changes to skill behavior.
- aeon.yml — registered after show-hn-draft as workflow_dispatch only (no cron — the article only matters in the pre-v4 / during-v4 window). Ships enabled: false.
- skills.json — bumped total 110 → 111, productivity category, alphabetical insertion before vercel-projects.

How it works:
The skill walks the fork's aeon.yml, skills.json, and memory/MEMORY.md, then scans them against the embedded manifest. Each manifest row is one of three categories: Safe (patterns confirmed stable into v4), Review (patterns flagged for v4 redesign — chains: runner interface, reactive: triggers, schedule syntax, model selectors, gateway block, MCP tool naming, add-skill/add-mcp/add-a2a CLIs, skills.json schema, dashboard catalog), or Removed (empty until v4 lands; populated row by row as v4 PRs merge). Custom-skill detection is heuristic — anything under skills/ whose slug isn't in skills.json with an upstream install: line is treated as custom and tagged manual for the operator's review. Each Review item gets an effort tag (trivial / minor / moderate / manual). Local mode is pure file I/O over the working tree; remote mode (var=owner/repo) uses single gh api contents calls per input — about 5 calls per fork, well under the 5,000/h GITHUB_TOKEN budget for ad-hoc fleet surveys. Read-only contract: never auto-mutates aeon.yml, never opens a PR, never pulls upstream — the upgrade decision belongs to the operator.

What's next:
The Manifest's Removed table is intentionally empty today. When v4 PRs start landing upstream, the maintainer (or the agent via a follow-up self-improve PR) edits the Removed rows in skills/v4-readiness/SKILL.md with one-line migration recipes per row. Once Removed is populated, the skill's verdict can escalate to ACTION rather than just READY/REVIEW. Companion to skill-update-check (drift in imported skills) and onboard (first-touch setup validator) — different scopes that don't overlap.

PR: https://github.com/aaronjmars/aeon/pull/160
