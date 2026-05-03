*Agent Self-Improvement — 2026-05-02*

Tightens the open-improvement-PR awareness check in skills/self-improve/SKILL.md from `gh pr list --search "improve:"` (matches title OR body) to a `--jq` post-filter on `title | startswith("improve:") or test("^improve\\(")` (title prefix only). Fixes a sleeper bug in the 3-PR cap that has been silently misclassifying unrelated PRs since day one.

Why: today's PR #25 `feat(skill-runs)` showed up in the existing open-improvement-PR query — not because it's an improve PR, but because GitHub's `--search` is full-text and PR #25's body mentions self-improve as a downstream consumer. This run was correctly under cap (1 < 3) but the query was fragile — once a few more `feat:`/`fix:` PRs whose bodies mention "improve" pile up, self-improve would silently stop running.

What changed:
- `skills/self-improve/SKILL.md`: replace `--search "improve:"` with title-prefix jq filter; add one-line rationale block so future maintainers don't revert
- `memory/MEMORY.md`: Skills Built row
- `memory/logs/2026-05-02.md`: self-improve log entry

Impact: self-improve's pile-up guard now counts only true `improve:` / `improve(scope):` PRs. Validated against every historical self-improve PR (#1 / #4 / #5 / #6 / #8 / #9 / #12 / #13 / #14 / #15 / #16 / #17 / #18 / #21 / #22) — all match; PR #25 correctly excluded.

PR: https://github.com/aaronjmars/aeon-agent/pull/26
