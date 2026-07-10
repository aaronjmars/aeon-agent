---
type: Article
---

# Repo Actions — aaronjmars/aeon — 2026-06-20

**Top pick for tomorrow:** #1 — Validate and merge PR #511 (Charon AEON skill pack) (Community/Growth, Small)
**Verdict:** No open issues for the first time in weeks — every backlog item is closed — so this cycle is entirely PR-driven: two external packs waiting for review, a maintainer's own docs PR ready to merge, an automated dependency file that's been missing the whole time, and a 40-day stale gateway contribution that only needs a rebase prompt to unblock.

## Actions

### 1. Validate and merge PR #511 (Charon AEON skill pack)
**Priority:** MED
**Type:** Community / Growth
**Effort:** Small (hours)
**Anchor:** PR:#511 "Add Charon AEON skill pack" by CharonAI-code (created 2026-06-20T02:36:56Z)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** Every merged external pack PR is a counted ecosystem metric (STRATEGY: "merged external PRs"). Charon arrives the same week as LENS (#510) — two community contributors opening PRs on the same day is a velocity signal; letting them sit past 24h undercuts that signal. Merging within the day tells the 186-fork cohort that external packs get reviewed and shipped fast.
**How:**
1. Fetch the Charon pack repo from the PR: `gh pr view 511 --repo aaronjmars/aeon --json headRepository,headRefName,body` to get the pack source. Confirm the pack has a `skills-pack.json` with `name`, `skills[]`, `category` fields; check the license (`gh api repos/<CharonAI-code>/<repo> --jq .license.spdx_id` should return MIT or Apache-2.0); spot-check one skill: `gh api "repos/<CharonAI-code>/<repo>/contents/skills/<slug>/SKILL.md"` returns non-null.
2. Run `scripts/validate-pack.sh` logic against the pack's structure (the script exists at `scripts/validate-pack.sh` — pass the pack directory from the PR branch, or manually run the key checks if the branch isn't locally available). Confirm no write-action skills have `default_enabled: true`.
3. If validation passes: `gh pr review 511 --repo aaronjmars/aeon --approve --body "Pack structure verified — license OK, SKILL.md per skill, validate-pack.sh checks pass. Merging."` then `gh pr merge 511 --repo aaronjmars/aeon --merge`.
**Definition of done:** `gh pr view 511 --repo aaronjmars/aeon --json state -q .state` returns `"MERGED"`; the community packs table in README includes the Charon entry.

---

### 2. Validate and merge PR #510 (LENS skill pack)
**Priority:** MED
**Type:** Community / Growth
**Effort:** Small (hours)
**Anchor:** PR:#510 "Add LENS skill pack" by Tholynceus (created 2026-06-19T23:39:48Z, updated 2026-06-20T00:35:31Z)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** Same ecosystem metric as #1 — each accepted pack widens the community catalog and gives future evaluators more reason to fork. LENS is 20 hours old; at 538 stars the repo has eyes on it; shipping both community packs in the same cycle (Charon + LENS) is a stronger signal than shipping one and queuing the other.
**How:**
1. Fetch the LENS pack source from PR: `gh pr view 510 --repo aaronjmars/aeon --json headRepository,headRefName,body`. Validate the same checklist as #1: `skills-pack.json` structure, MIT/Apache license, `SKILL.md` per skill, write-action skills default-disabled.
2. Check that the PR adds a matching entry to `skill-packs.json` (the machine-readable registry); if the PR only updates `README.md`, confirm the `skill-packs.json` row is there too.
3. If validation passes: `gh pr review 510 --repo aaronjmars/aeon --approve --body "Pack structure verified — license OK, SKILL.md per skill, validate-pack.sh checks pass. Merging."` then `gh pr merge 510 --repo aaronjmars/aeon --merge`.
**Definition of done:** `gh pr view 510 --repo aaronjmars/aeon --json state -q .state` returns `"MERGED"`; the README community packs table includes the LENS entry.

---

### 3. Add `.github/dependabot.yml` for automated npm and GitHub Actions dependency tracking
**Priority:** MED
**Type:** Security / DX
**Effort:** Small (hours)
**Anchor:** MISSING:.github/dependabot.yml (confirmed absent in GraphQL response; repo has npm workspaces in `apps/dashboard/`, `apps/mcp-server/`, `apps/a2a-server/`, `apps/webhook/` and 8 GitHub Actions workflows with floating `@v4`/`@v5` tags)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** Aeon runs autonomous code with access to operator secrets and executes community pack skills on a cron. Without Dependabot, npm vulns in the dashboard's Next.js stack and mutable-tag action hijacks accumulate silently — no PRs, no audit trail. Adding `dependabot.yml` turns dep hygiene from a manual chore into a zero-cost automated signal: one weekly PR per ecosystem keeps the security posture visible to forks evaluating whether Aeon is maintained.
**How:**
1. Create `.github/dependabot.yml` with three package-ecosystems: `github-actions` (directory `/`, weekly Monday), `npm` for the dashboard (directory `/apps/dashboard`, weekly Monday), and `npm` for the MCP server (directory `/apps/mcp-server`, weekly Monday). Set `open-pull-requests-limit: 5` per ecosystem to avoid noise.
2. Open a PR with the single new file; no other changes needed — GitHub activates Dependabot automatically on merge.
3. Add `assignees: [aaronjmars]` to each ecosystem block so PRs route to the maintainer rather than landing un-assigned.
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/.github/dependabot.yml --jq .size` returns non-null > 0; within 24h of merge, GitHub's Dependency Graph tab shows "Dependabot alerts" as enabled and at least one version check has run.

---

### 4. Merge PR #512 (MCP server README by aaronjmars)
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** PR:#512 "docs: add apps/mcp-server/README.md with quickstart and Claude Desktop config" by aaronjmars (created 2026-06-20T11:05:27Z, docs-only, no conflicts, no draft flag)
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** The main README already links to `apps/mcp-server/README.md` ("Use any Aeon skill as an MCP tool in Claude Desktop or Claude Code — see `apps/mcp-server/README.md`") but the file doesn't exist in `HEAD` yet — `gh api repos/aaronjmars/aeon/contents/apps/mcp-server/README.md` 404s. Every developer who clicks through from the README hits a 404. PR #512 closes that gap; it was opened today by the maintainer and is ready to merge with zero review friction.
**How:**
1. Confirm the PR passes CI: `gh pr checks 512 --repo aaronjmars/aeon` — look for green on `ci-skills-json` and `ci-packs-json` (the two JSON-lint gates that would catch any structural issue).
2. Merge: `gh pr merge 512 --repo aaronjmars/aeon --merge`.
3. Verify: `gh api repos/aaronjmars/aeon/contents/apps/mcp-server/README.md --jq .size` returns a non-null positive integer.
**Definition of done:** `gh pr view 512 --repo aaronjmars/aeon --json state -q .state` returns `"MERGED"`; `apps/mcp-server/README.md` exists on `HEAD` and the MCP entry-point documentation gap is closed.

---

### 5. Post rebase guide comment on PR #418 to unstick BEAMR gateway
**Priority:** MED
**Type:** Community
**Effort:** Small (hours)
**Anchor:** PR:#418 "feat(gateway): add BEAMR as an LLM gateway" by SahilParikh03 (created 2026-06-10, last activity 2026-06-16, 40 days open, conflicts on `scripts/llm-gateway.sh` and `apps/dashboard/lib/types.ts` from the 2026-06-10→2026-06-20 merge train)
**Score:** L=3 C=4 N=4 (total 11/15)
**Impact:** BEAMR is one of Aeon's few non-Claude LLM gateway contributions — it expands the `gateway.provider` cascade for operators on discounted Opus access. The PR has the code; the only blocker is a rebase. SahilParikh03 may not know the exact steps for a rebase against `upstream/main` given the 10-day merge train since 2026-06-10. A clear comment with the exact commands breaks the stalemate at zero cost.
**How:**
1. Post: `gh pr comment 418 --repo aaronjmars/aeon --body "Hey @SahilParikh03 — this PR is one rebase away from merging. The conflicts are in \`scripts/llm-gateway.sh\` and \`apps/dashboard/lib/types.ts\` from the 2026-06-10→now merge train. Here's the exact sequence:\n\n\`\`\`bash\ngit fetch upstream\ngit rebase upstream/main\n# resolve any conflicts in scripts/llm-gateway.sh and apps/dashboard/lib/types.ts\ngit push --force-with-lease origin feat/beamr-gateway\n\`\`\`\n\nIf you'd like a hand with the conflict resolution, drop the conflicted output here and I can walk through it. The PR is otherwise solid — happy to merge once the rebase lands."`
2. No other files need changing.
**Definition of done:** `gh pr view 418 --repo aaronjmars/aeon --json comments --jq '.comments[-1].body'` contains the rebase instructions; SahilParikh03 receives a notification and can act on it.

---

## Monitor

### A. SHA-pin all `.github/workflows/*.yml` action references
**Why not yet:** Pinning requires a commit to `.github/workflows/` files, which needs a `workflows`-scoped PAT — the default `GITHUB_TOKEN` is blocked from pushing to workflow paths. Confirmed in Lessons Learned. Eligible once `GH_PAT` with `workflows` scope is added as a repo secret.
**Anchor:** FILE:.github/workflows/aeon.yml (uses `actions/checkout@v4`, `actions/setup-node@v4` — mutable floating tags across 8 workflow files)

### B. Smithery listing submission status
**Why not yet:** `docs/smithery.yaml`, `docs/smithery-manifest.json`, and `docs/smithery-submission.md` exist but the current submission status (draft, submitted, or live) is unknown without reading the file. If the path to listing requires opening a PR on the Smithery catalog repo or creating an account, it may fall outside autonomous scope. Read `docs/smithery-submission.md` to determine if this is a one-click action before scheduling it.
**Anchor:** FILE:docs/smithery-submission.md

---

## Fleet follow-ons

- aaronjmars/minitor: repo-pulse QUIET today (0 events in 24h window, 12 stars, 2 forks); MEMORY notes no remaining queued actions after #75 merged. If PR #76 (CI build workflow, external contributor) is still open and unreviewed, the same validate-and-merge pattern from idea #1 applies.

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** 2026-06-18 top pick "Add A2A server quickstart guide to apps/a2a-server/" → MERGED as #501 on 2026-06-19 — cleared
