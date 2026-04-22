*Feature Built — 2026-04-22*

Onboard Validator (./onboard CLI + onboard skill)
A guided setup checker for fresh Aeon forks. Drops two new things into the repo: a `./onboard` command operators run after they fork, and a matching `onboard` skill that does the same checks inside GitHub Actions and posts the result to their notification channel. Whichever path they take, they get a checklist that says exactly what is missing and the exact command to fix it.

Why this matters:
Aeon has 33 forks but the path from "I forked the repo" to "first skill is running" was undocumented. Operators set some secrets, missed others, and went silent. This was idea #2 in the 2026-04-20 repo-actions digest — flagged as recoverable growth: even 20% setup-stage abandonment at the current fork rate is a meaningful loss of community. The onboard skill closes that gap by turning "fork and hope" into a guided 10-minute setup with a confirmation message that says "you're done."

What was built:
- onboard (executable, 315 lines): Local bash CLI. Runs 8 read-only checks — workflow files present, aeon.yml has skills enabled, memory/ writable, ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN set, at least one notification channel configured (Telegram / Discord / Slack / Email), GitHub Actions has run, memory/logs/ has entries, optional GH_GLOBAL PAT for cross-repo skills. Each gap prints the exact `gh secret set ...` or `chmod ...` or `git checkout ...` command. Modes: --remote (dispatch the skill), --quiet, --json, --help. Exits 1 on any failure for CI use.
- skills/onboard/SKILL.md (93 lines): workflow_dispatch one-shot skill. Runs `./onboard --json`, formats the result as a verdict + grouped checklist with embedded fixes, sends via ./notify. Optional `var: --silent-on-pass` for nightly self-audits that only notify on regression. Logs every run to memory/logs/ and a one-line trend to memory/topics/onboard-history.md.
- aeon.yml: registers `onboard` as workflow_dispatch (disabled by default since it is operator-triggered).
- generate-skills-json + README.md: onboard categorized as productivity/meta; Quick start gains step 5 "Verify"; project-structure listing for ./onboard; Meta/Agent skill count bumped 12 → 13.

How it works:
The CLI is the single source of truth — every check, fix string, and exit-code rule lives there. The SKILL.md is a thin wrapper that runs the CLI in --json mode, transforms output, and routes through ./notify. That keeps the contract testable: you run ./onboard locally, see the checklist, fix gaps, and rerun. The local-vs-remote split is the design point — local gives instant terminal feedback while operators are still in the setup loop, and `./onboard --remote` confirms the full GH Actions + secrets + ./notify pipeline actually works end-to-end (catches the "I set the secret but it is not visible to Actions" failures local-only checks would miss). gh secret list calls go through gh's built-in auth, which bypasses the env-var-in-curl sandbox restriction documented in CLAUDE.md.

What is next:
Could surface onboard status in the dashboard as a top-level health card (currently the dashboard shows skill runs but not setup completeness). Could also wire onboard into add-skill so each new skill installation prompts a re-validation if it depends on a secret the operator has not configured yet.

PR: https://github.com/aaronjmars/aeon/pull/139
