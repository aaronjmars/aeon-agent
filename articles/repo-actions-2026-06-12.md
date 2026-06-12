# Repo Actions — aaronjmars/aeon — 2026-06-12

**Top pick for tomorrow:** #1 — Rebase PR #418 to unblock BEAMR gateway integration (Integration, Medium)
**Verdict:** Five PRs landed on `aeon` today and left one community contribution conflicting and four structural files absent — a 509-star repo with active external contributors has no CONTRIBUTING.md, dependabot, issue templates, or security policy.

## Actions

### 1. Rebase PR #418 to clear BEAMR gateway merge conflicts after today's five merges
**Priority:** HIGH
**Type:** Integration
**Effort:** Medium (1–2 days)
**Anchor:** PR:#418 "feat(gateway): add BEAMR as an LLM gateway"
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** BEAMR becomes Aeon's 6th gateway option — users with BEAMR credits can route all Claude Code calls through it — but only once the branch is unstuck; every day it sits conflicted is a discouraging signal to the contributor.
**How:**
1. Check out `feat/beamr-gateway` and rebase on current `main`; the conflicts are in `scripts/llm-gateway.sh` (new BEAMR case added by PR #419's merges changing the file's shape) and `apps/dashboard/lib/types.ts` + `apps/dashboard/app/api/secrets/route.ts` (dashboard type changes from recent PRs)
2. Resolve by following the 5-file gateway pattern documented in `README.md#adding-a-gateway` (lines 386–394): add BEAMR to `GatewayProvider` union and `GATEWAY_PROVIDERS` array in `types.ts`, list secret `BEAMR_LLM_KEY` in `BUILTIN_SECRETS` and map it in `GATEWAY_SECRETS` in `secrets/route.ts`, add native-tier `case` branch in `scripts/llm-gateway.sh`, and add a gateway table row to the README
3. Run the CI checks (`ci-skills-json`, `ci-capabilities-parity`) locally via `gh workflow run`, push the rebased branch, and leave a comment on the PR flagging it's ready for re-review
**Definition of done:** `gh pr view 418 --repo aaronjmars/aeon --json mergeable -q .mergeable` returns `MERGEABLE` and CI is green; the workflow log on a test run prints `::notice:: gateway=auto resolved to beamr`.

---

### 2. Add CONTRIBUTING.md anchored to the gateway and skill submission patterns already in README
**Priority:** MED
**Type:** Community
**Effort:** Small (hours)
**Anchor:** MISSING:CONTRIBUTING.md
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** External contributor SahilParikh03 is actively submitting PRs (PR #418 open) with no formal guide to follow; 166 forks with no onboarding doc means every contributor figures out branch naming, CI gates, and skill-submission conventions independently.
**How:**
1. Create `CONTRIBUTING.md` that surfaces the patterns already documented inline in `README.md`: (a) how to add a skill — copy the template directory, register in `aeon.yml`, run `./generate-skills-json`; (b) how to add a gateway — the 5-file checklist at `README.md#adding-a-gateway`; (c) CI gates that must pass (`ci-skills-json`, `ci-capabilities-parity`); (d) PR checklist (branch from main, squash-merge expected, `skills.json` must be regenerated if SKILL.md touched)
2. Add a "Contributing" badge or link to the file in the README header shields block
3. Open as a PR targeting main
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/CONTRIBUTING.md --jq .size` returns a non-null size; the README links to it; the PR description includes a "closes no issue — adding missing community health file" note.

---

### 3. Add .github/dependabot.yml covering npm packages in apps/dashboard and GitHub Actions versions
**Priority:** MED
**Type:** Security
**Effort:** Small (hours)
**Anchor:** MISSING:.github/dependabot.yml
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** The `apps/dashboard` Next.js frontend has no automated dep bump PRs — outdated packages accumulate silently until a CVE forces a manual emergency update; GitHub Actions in `.github/workflows/*.yml` are also pinned to unpinned major versions with no automated refresh.
**How:**
1. Create `.github/dependabot.yml` with three `package-ecosystem` entries: `npm` for `directory: "/apps/dashboard"` (weekly, Monday, max-open-prs: 5), `npm` for `directory: "/"` if a root `package.json` exists (check via `gh api repos/aaronjmars/aeon/contents/package.json`), and `github-actions` for `directory: "/"` (weekly, Monday)
2. Set `target-branch: main` and `commit-message.prefix: "chore(deps)"` on each block for clean PR titles
3. Open as a PR; no code changes required beyond the single config file
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/.github/dependabot.yml --jq .size` returns non-null; within one weekly cycle a Dependabot PR appears for at least one stale dep in `apps/dashboard`.

---

### 4. Add GitHub issue templates (bug report + feature request) for a repo with zero open issues and no templates
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** MISSING:.github/ISSUE_TEMPLATE
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** Zero open issues on a 509-star repo almost certainly means friction rather than perfection — users hitting bugs lack a clear filing format, especially given Aeon's skill+secret+cron complexity where "it failed" is useless without the skill name, `cron-state.json` entry, and whether the failure was API or sandbox.
**How:**
1. Create `.github/ISSUE_TEMPLATE/bug_report.yml` (YAML form) with fields: skill name (dropdown of common ones or free text), describe the bug, steps to reproduce, expected vs actual behavior, relevant `memory/logs/` entry (redacted), and whether notifications were received
2. Create `.github/ISSUE_TEMPLATE/feature_request.yml` with: feature type (new skill / gateway / dashboard / core), description, proposed `var:` if a skill, whether the requester can open a PR
3. Create `.github/ISSUE_TEMPLATE/config.yml` with `blank_issues_enabled: false` so contributors are funneled through templates
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/.github/ISSUE_TEMPLATE --jq '[.[] | .name]'` returns an array with at least `bug_report.yml` and `feature_request.yml`; opening a new issue on the repo presents the template chooser.

---

### 5. Fix stale skill count "197" in README.md after beamr-route and CTRL merged today
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md
**Score:** L=3 C=3 N=4 (total 10/15)
**Impact:** First-time visitors read "197 skills" in the hero section and the full catalog, but two skills landed today — `beamr-route` (x402 micropayment inference, tags: crypto + dev) and `ctrl` (Base on-chain automation, tags: crypto + automation + base + defi) — making the count at least 199 and leaving both absent from the per-category rows.
**How:**
1. In `README.md`, update the bold heading `**197 skills across 8 categories**` → `**199 skills across 8 categories**`
2. Update the `<details>` summary `Full catalog (all 197 skills)` → `Full catalog (all 199 skills)`
3. Verify the exact category for each skill by checking `skills.json` (the CI gate just healed it in PR #458) — `beamr-route` with tags `[crypto, dev]` and `ctrl` with tags `[crypto, automation, base, defi]` both likely land in Crypto & Markets; update that row's count from `(29)` to `(31)` and append `beamr-route` and `ctrl` to its skill name list
4. Note: `assets/skills-aeon-197.jpg` image filename stays as-is (can't regenerate assets autonomously); a follow-up image update is a human task
**Definition of done:** `grep "197" README.md` returns no hits in the skills count context; both `beamr-route` and `ctrl` appear in the full catalog table under their correct category; PR CI is green.

---

## Fleet follow-ons
<!-- aaronjmars/minitor has 1 repo in the watched list beyond the primary target -->

- aaronjmars/minitor: Ship the Dexscreener column plugin (tsc+lint clean, built as a fast follow to #71) as a new PR once PR #71 (build fix — `"use server"` export extraction) merges and `main` compiles — plugin contract follows `lib/columns/plugins/_template/` with registration in manifest.ts + registry.ts + server-registry.ts and integration in `lib/integrations/`.

---

**Source status:** gh=ok code_search=rate_limited memory_topics=missing articles_dir=missing watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** — (first repo-actions run)
