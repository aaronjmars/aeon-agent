---
type: Article
---

# Repo Actions — aaronjmars/aeon — 2026-06-22

**Top pick for tomorrow:** #1 — Wire phylax-audit into install-skill-pack as a pre-install security gate (Feature/Security, Small)
**Verdict:** Today's phylax-audit merge (#537) opens two HIGH-priority follow-ons — one wires it into the install path, one documents it for forkers; the remaining three close a dashboard onboarding gap and harden the supply-chain audit trail.

## Actions

### 1. Wire phylax-audit into install-skill-pack as a pre-install security gate
**Priority:** HIGH
**Type:** Feature / Security
**Effort:** Small (hours)
**Anchor:** FILE:install-skill-pack (`SCANNER="$ROOT_DIR/skills/skill-scan/scan.sh"` — current pre-install scanner; phylax-audit merged today as PR #537 at 2026-06-22T12:34:06Z)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** install-skill-pack's pre-install security step calls `skill-scan` for static heuristic checks. phylax-audit answers a different, deeper question — "is this skill safe to install *at all*?" — by scanning the external SKILL.md for prompt injection and secret exfil, auditing any Base contracts it references, and probing its x402 endpoints. Adding it as a pre-install gate means every `./install-skill-pack` call (across all 188 forks) runs phylax-audit's ALLOW/WARN/DENY verdict before anything lands in `skills/`. The DENY path exits before skill-scan even runs.
**How:**
1. Read `install-skill-pack` near the scanner invocation block to find where `$SCANNER` is called and how the exit code drives the `--force` / `--yes` flow. Identify the exact line(s) that run `$SCANNER` and where DENY would map in the existing HIGH/WARN/OK result taxonomy.
2. Add a phylax-audit pre-flight step: for each skill slug being installed, call the phylax-audit skill with `var` set to the raw SKILL.md URL (`https://raw.githubusercontent.com/$PACK_REPO/main/$SKILL_PATH/SKILL.md`). Parse the output for the ALLOW/WARN/DENY line. If DENY: print the evidence, abort install for that skill (or all skills if `--force` is not set). If WARN: surface the warning and continue unless `--force` was omitted and the user is interactive (prompt).
3. Add `--skip-phylax` flag to allow operators to bypass the new gate (mirrors the existing `--force` semantics — an explicit opt-out, not the default).
**Definition of done:** `./install-skill-pack aaronjmars/aeon/skills/phylax-audit --dry-run` shows a phylax-audit invocation line in the output; a test pack with a DENY-triggering SKILL.md (e.g. one containing "ignore previous instructions") causes install to abort with a `PHYLAX_DENY` exit message.

---

### 2. Add apps/dashboard/README.md
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** MISSING:apps/dashboard/README.md (apps/a2a-server got its README in PR #501, apps/mcp-server in PR #512, apps/webhook already has one at 3720 bytes — apps/dashboard is the only sub-app still undocumented)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** The dashboard is the primary interface forkers use to enable skills, configure packs, and monitor runs — yet it has no README. A developer who clones Aeon and runs `ls apps/` finds four sub-apps; three have READMEs, one doesn't. The one without docs is the UI they'll open first. Closing this gap removes the top onboarding friction point for UI-first evaluators (STRATEGY priority-zero bug) and gives the 188-fork cohort a single doc they can link new contributors to.
**How:**
1. Read `apps/dashboard/package.json` for the `dev` / `build` / `start` scripts and Node/Next version requirements; skim `apps/dashboard/src/` (or `app/`) to understand the main views (skills roster, pack browser, skill output feed).
2. Create `apps/dashboard/README.md` with: **What it is** (Next.js UI for managing Aeon — enable skills, browse community packs, watch real-time skill output), **Quickstart** (`cd apps/dashboard && npm install && npm run dev` — dashboard starts on localhost:3000; env: inherits repo's `.env` or GitHub Actions secrets, no extra vars), **Key views** (Skills roster, Community packs, Skill output / json-render feed), **Deploy** (Vercel — the repo auto-deploys `apps/dashboard/` on push to main; no manual step needed), **MCP / A2A** (link to `apps/mcp-server/README.md` and `apps/a2a-server/README.md` for the two agent interop surfaces).
3. Add a one-line pointer in the main `README.md` under the dashboard mention: "Run the dashboard locally with `npm run dev` in `apps/dashboard/` — see `apps/dashboard/README.md`."
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/apps/dashboard/README.md --jq .size` returns non-null; a developer who has forked Aeon can run the dashboard from a cold clone using only the README.

---

### 3. Document phylax-audit in README.md security architecture
**Priority:** MED
**Type:** DX / Security
**Effort:** Small (hours)
**Anchor:** FILE:README.md (README currently says "183 skills" with no mention of phylax-audit or the pre-install security model; skill-scan is the only security tool a reader can infer from the codebase) + FILE:skills/phylax-audit/SKILL.md (merged as PR #537, 2026-06-22)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Forkers evaluating Aeon's security posture read the README first. Right now they see `skill-scan` implied in the PR flow but no pre-install security narrative. phylax-audit is a user-visible capability that distinguishes Aeon's security model from "we scan what's already installed" to "we gate what comes in." Adding a short Security or "Installing skills safely" section closes this documentation gap and signals to forks building on Aeon that the framework has an opinionated answer to the "malicious community skill" threat model.
**How:**
1. Find the existing security mention in README.md (likely in CONTRIBUTING, CLAUDE.md, or a brief section in README itself). Identify where to insert or expand a "Security" subsection in README — ideally adjacent to the "Community skill packs" section.
2. Add a `## Security` or `### Installing skills safely` subsection (4–6 lines): "Before a skill lands in your repo, two gates run: **skill-scan** (static heuristics on the SKILL.md body) and **phylax** (pre-install audit that probes prompt-injection, secret-exfil patterns, Base contract risk, and x402 endpoint safety — returns `ALLOW / WARN / DENY`). Both run automatically via `./install-skill-pack`. To audit a skill manually before adding it: run the `phylax-audit` skill with `var: owner/repo/skills/skill-name`."
3. Update "183 skills" → "184 skills" in the same PR (phylax-audit merged today as #537).
**Definition of done:** `curl -s https://raw.githubusercontent.com/aaronjmars/aeon/main/README.md | grep -c "phylax"` returns ≥1; a fork evaluator reading the README understands the two-gate security model without opening any skill file.

---

### 4. Add commit-SHA pinning to install-skill-pack for supply-chain auditability
**Priority:** MED
**Type:** Security / DX
**Effort:** Small (hours)
**Anchor:** FILE:install-skill-pack (`SKILLS_LOCK="$ROOT_DIR/skills.lock"` is defined as a variable in the script but `skills.lock` is null — the file does not exist; packs are installed at HEAD with no version record written)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** install-skill-pack pulls the latest HEAD of a community pack repo at install time. If a pack maintainer pushes a supply-chain compromise after the operator installs, there is no record of what commit was installed — no audit trail, no drift detection, no way to pin or roll back. Recording the installed commit SHA in `skills.lock` gives operators a verifiable snapshot: `phylax-audit` can compare the installed SHA against current HEAD and flag divergence; forks get an auditable diff surface that aligns with Aeon's "commit-as-audit-trail" design.
**How:**
1. After each successful pack install in `install-skill-pack`, fetch the HEAD commit SHA of the installed pack: `gh api repos/$PACK_REPO/commits/HEAD --jq .sha` and write a record to `skills.lock` in the format `{"pack": "$PACK_REPO", "sha": "$SHA", "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)", "skills": [...slugs...]}`. Append (or upsert by pack key) — do not overwrite the entire file.
2. Add a `--check-lock` flag to install-skill-pack that reads `skills.lock` and, for each installed pack, calls `gh api repos/$PACK_REPO/commits/HEAD --jq .sha` and compares to the recorded SHA. Reports `CURRENT`, `DRIFTED`, or `UNTRACKED` per pack.
3. Commit `skills.lock` as part of the install PR (it already exists in the install flow's git-add sequence — just needs the file to be created).
**Definition of done:** After `./install-skill-pack aaronjmars/hunch-aeon-skills`, `cat skills.lock` contains a JSON record with `pack`, `sha`, `installed_at`, and `skills` keys; `./install-skill-pack --check-lock` prints `CURRENT` for the just-installed pack.

---

### 5. Wire skill-triage to invoke phylax-audit on inbound SKILL.md PRs
**Priority:** MED
**Type:** Security / Community
**Effort:** Medium (1–2 days)
**Anchor:** FILE:skills/skill-triage/SKILL.md (workflow_dispatch skill; currently runs skill-scan + frontmatter validation + cron-slot conflict detection, posts a structured triage comment) + FILE:skills/phylax-audit/SKILL.md (merged as PR #537)
**Score:** L=3 C=3 N=5 (total 11/15)
**Impact:** skill-triage catches structural problems in inbound SKILL.md PRs (missing tags, cron conflicts, secrets_required). It does not currently run a security pre-screen. After phylax-audit merged, integrating it into the triage report means every community skill submission automatically gets a ALLOW/WARN/DENY verdict alongside the structural checks — before any human review happens. This closes the window between "PR opened" and "maintainer notices it" for prompt-injection or secret-exfil patterns.
**How:**
1. Read `skills/skill-triage/SKILL.md` to find where skill-scan is invoked in the triage step sequence. Identify the output format of the triage comment (likely a structured table or checklist).
2. Add a phylax-audit step: after fetching the PR's SKILL.md content, invoke the phylax-audit skill inline (by reading `skills/phylax-audit/SKILL.md` and executing its intent with `var` set to the PR's raw SKILL.md URL). Parse the ALLOW/WARN/DENY line and include it in the triage comment under a new "Security pre-screen" row: `| Phylax | ALLOW ✅ |` / `| Phylax | WARN ⚠️ (prompt injection pattern detected) |` / `| Phylax | DENY ❌ — see evidence below |`.
3. If phylax returns DENY, add a `BLOCK` recommendation to the overall triage verdict so the maintainer knows not to merge without investigation.
**Definition of done:** Triggering skill-triage on a test PR containing a SKILL.md with a DENY-triggering pattern produces a triage comment that includes a "Phylax" row with a DENY verdict and the evidence summary; the overall triage verdict includes `BLOCK`.

---

## Monitor

### A. Enable pr-triage skill to auto-triage open PRs #418 and #510
**Why not yet:** Enabling pr-triage posts automated comments on contributor PRs (#418 SahilParikh03, #510 Tholynceus) — an action visible to external contributors. Turning on a daily cron that auto-triages all PRs is a live behavior change that the operator should sign off on before it runs. The skill is ready; it's an operator toggle decision.
**Anchor:** FILE:aeon.yml (pr-triage { enabled: false, schedule: "30 9 * * *" }) + PR:#418 (42d stale) + PR:#510 (3d open)

### B. SHA-pin all .github/workflows/*.yml action references
**Why not yet:** Writing to `.github/workflows/` requires a GH_PAT with `workflows` scope — the default GITHUB_TOKEN (and the Aeon agent's standard token) cannot push to workflow files. Noted in every run since 06-14. Eligible once `GH_PAT` with `workflows` scope is configured as a repo secret.
**Anchor:** FILE:.github/workflows/aeon.yml (uses floating tags `actions/checkout@v7`, `actions/setup-node@v6` after Dependabot bumped them)

### C. CODE_OF_CONDUCT.md — PR #538 closed without merge
**Why not yet:** The feature skill opened PR #538 (`docs: add Contributor Covenant Code of Conduct`) today (2026-06-22); it was closed without merging (state: CLOSED, mergedAt: null). The operator may have declined it or may have had a specific reason. Hold on re-attempting until intent is clear.
**Anchor:** MISSING:CODE_OF_CONDUCT.md (still absent after PR #538 closed)

---

## Fleet follow-ons

- aaronjmars/minitor: PR #78 (empty/whitespace query validation across 5 Grok-backed columns) merged today. Follow-on: add a `npm run build` CI check gated to `lib/columns/plugins/**` path changes — minitor has no build-time gate on column plugin changes, so a TypeScript error in a new column only surfaces at Vercel deploy (same gap aaronjmars/aeon has for apps/**).

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** 2026-06-20 top pick "Validate and merge PR #511 (Charon AEON skill pack)" → MERGED on 2026-06-21 — cleared
