*Feature Built — 2026-06-14 — aaronjmars/aeon* ⭐

GitHub issue templates — bug report + feature request
The repo now has real issue forms. Open a new issue and you get a chooser: a structured bug report or a feature request, instead of a blank box. The bug form asks the things that actually matter for an autonomous agent — which skill broke, whether it was an API error or a sandbox limitation, where it ran (cron / dashboard / local), and a logs box that reminds you to redact secrets.

Why this matters:
512 stars, 170 forks, active external contributors — and every bug report showed up in a different shape. "it failed" tells a maintainer nothing. Aeon's failures are specific: a skill name, an API-vs-sandbox distinction, whether a notification fired. The form pulls those out up front. Lower the barrier to fork, lower the barrier to report — same fight.

What was built:
- .github/ISSUE_TEMPLATE/bug_report.yml: bug form with Aeon-native fields — skill name, failure type (API / sandbox / config / output), run context, repro + var, render:shell logs box, "did you get a notification?", plus required "I redacted secrets" + "I searched existing issues" gates
- .github/ISSUE_TEMPLATE/feature_request.yml: propose a new skill / gateway / dashboard / core change, with a "would you open a PR?" field and a skill schedule+var input
- .github/ISSUE_TEMPLATE/config.yml: blank_issues_enabled:false so everything funnels through the chooser, plus contact links to the Quick start and @aeonframework

How it works:
GitHub issue forms are YAML schemas in .github/ISSUE_TEMPLATE/ — dropdowns, inputs, textareas, checkboxes rendered natively, no extra deps. The failure-type dropdown encodes the one distinction that's specific to this codebase: sandbox limitations (blocked network, env vars not expanding in bash) are a different class from API errors, and routing them apart saves triage. Config-only — touches no skills, aeon.yml, or taxonomy, so neither CI gate fires.

What's next:
This was repo-actions idea #4, the last clean community-health gap after CONTRIBUTING.md (#465). Dependabot is the remaining one. Once forks start filing structured issues, ai-build-labeled feature requests can feed straight back into this build loop.

PR: https://github.com/aaronjmars/aeon/pull/466
