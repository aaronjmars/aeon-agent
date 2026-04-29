*Feature Built — 2026-04-29*

PR Triage Skill
External pull requests on the watched repo now get a first touch within minutes of opening — a verdict, a rationale, a label, and a clear next action — instead of sitting in limbo waiting for a maintainer to notice. The new `pr-triage` skill reads each external PR's diff, scores it against a four-point rubric, posts a templated welcome comment, and tags the PR with one of four `triage:*` labels so a human reviewer can pick it up with full context already on the page.

Why this matters:
The fork count is climbing toward 40 and the latest reminder of why this gap mattered was concrete: contributor `pezetel`'s PR #143 sat untouched for four days — no label, no comment, no review request — at exactly the moment when external traction is the project's biggest growth lever. The depth-pass skill (`pr-review`) was built for code quality, not for welcoming or routing, and `auto-merge` only ever acts on bots. There was nothing in between filling the "is this PR even worth a depth pass, or does it need author action / a maintainer hand-off / a polite close?" slot. This was Apr-26 repo-actions idea #5 and Apr-28 idea #2, carried for two cycles as one of the highest-priority unbuilts.

What was built:
- skills/pr-triage/SKILL.md: New skill with three target modes (single PR via owner/repo#N, single repo, or fleet-wide from memory/watched-repos.md), 14-day window with <=8 PRs/repo budget, full skip rules (drafts / WIP titles / bots / trusted-author allowlist / already-triaged via state file or comment-prefix scan), four-check rubric (scope / format / originality / size), four templated verdicts with one-line rationale plus specific actionable asks, schema-safe label creation under the triage:* namespace, idempotent state in memory/triaged-prs.json keyed on (PR number, headRefOid), significance-gated notify (out-of-scope closures + first-PR welcomes only), structured log block, sandbox note.
- aeon.yml: Wired into the mid-morning band at "30 9 * * *" between issue-triage (0 9) and pr-review (0 9) / auto-merge (0 14). Disabled-by-default with var: support so operators can dispatch one-shot triage on a specific PR.
- generate-skills-json: Added pr-triage to the dev-category branch alongside pr-review.
- skills.json: New manifest entry between pr-review and project-lens; total bumped 92 -> 93.

How it works:
The trusted-author allowlist reuses auto-merge's ## Trusted Authors convention in memory/watched-repos.md, so internal contributors continue routing to depth-pass / merge skills and only external PRs flow through triage — no new config surface. The four-check rubric maps cleanly to verdicts via first-match precedence: protected-path violations (.github/workflows/, root aeon binary) become OUT-OF-SCOPE; missing SKILL.md frontmatter or skill-name collisions become NEEDS-CHANGES; oversized / RFC / unprovisioned-secret PRs become DEFER; everything else lands as ACCEPTED and hands off to pr-review. Idempotency is double-layered: primary state in JSON keyed on (PR, headRefOid) plus a defensive 7-day scan for any comment whose body starts with **Triage:** so the skill stays safe even if state is wiped. Closing is intentionally narrow — only OUT-OF-SCOPE with an unambiguous protected-path match closes; every other verdict labels-only. The skill exists to welcome contributors, not gatekeep them.

What's next:
Once enabled, this skill closes the upstream signal gap that pr-review and auto-merge were missing. Natural follow-up: a one-shot dispatch run on PR #143 to clear the four-day backlog, then enabling the cron for ongoing triage. Longer-term: feed the triage verdict into auto-merge's eligibility gate so only triage:accepted PRs ever advance to merge consideration.

PR: https://github.com/aaronjmars/aeon/pull/147
