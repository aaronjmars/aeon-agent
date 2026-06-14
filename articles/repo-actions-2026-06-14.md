# Repo Actions — aaronjmars/aeon — 2026-06-14

**Top pick for tomorrow:** #1 — Add glim.sh to the dashboard's featured MCP catalog (DX, Small)
**Verdict:** One HIGH-priority idea anchored to the only open issue; a README quickstart gap and supply-chain security hole fill the remaining HIGH slots; all five are clear to build as soon as one of the three open PRs (#465/#466/#418) merges and drops the PR ceiling back below 3.

## Actions

### 1. Add glim.sh to the dashboard's featured MCP catalog
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** ISSUE:#464 "Add glim.sh (live-data MCP, pay-per-call via x402 + MPP) to the featured MCP catalog"
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Glim.sh is an x402-native pay-per-call MCP — the same payment rail Aeon's `beamr-route` skill uses; listing it in the dashboard catalog means every new forker sees a working live-data MCP with on-chain billing, which directly demonstrates the x402 ecosystem Aeon is building toward and increases the discoverability surface that drove the #464 issue.
**How:**
1. Read `apps/dashboard/lib/catalog.ts` to find the array/object where existing featured MCP entries are defined (pattern follows the BlueAgent entry added in PR #438)
2. Add a glim.sh entry matching the existing field schema: `name`, `description`, `url`, `capabilities` (live data + pay-per-call), `paymentRail: "x402"`, and any required `tags` or `category` fields present on peer entries
3. Open a PR targeting main with the single-file change; include a link to ISSUE:#464 in the PR description to close it
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/apps/dashboard/lib/catalog.ts --jq '.size'` returns a value larger than before the commit; opening the dashboard → MCP catalog shows glim.sh with its description; ISSUE:#464 is closed by the PR.

---

### 2. Add a copy-pasteable bootstrap block to the README Install section
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md (Install section lists steps 1–4 as prose but has no single executable shell block)
**Score:** L=4 C=3 N=5 (total 12/15)
**Impact:** The STRATEGY marks onboarding friction as a priority-zero bug — every new live instance is a north-star metric. The current install flow is a numbered prose list ("Fork", "Configure", "Pick skills", "Run"); a developer evaluating Aeon on mobile or in a 30-second skim can't copy-paste their way in. A shell snippet cuts that to three commands and removes the "figure out the order" friction for the 170-fork cohort.
**How:**
1. Locate the "Quickstart" or numbered-steps install block in `README.md`; insert a `bash` code block immediately after (or inside) the fork step:
   ```bash
   # 1. Fork and clone
   gh repo fork aaronjmars/aeon --clone && cd aeon

   # 2. Add your provider key (pick any supported provider)
   gh secret set ANTHROPIC_API_KEY

   # 3. Enable a skill and push so Actions picks it up
   # Edit aeon.yml: flip `enabled: false` → `enabled: true` on any skill, then:
   git add aeon.yml && git commit -m "feat: enable heartbeat" && git push
   ```
2. Add a brief note: "That's it — GitHub Actions will run the skill on its next cron tick. Open the dashboard (`npm run dev` in `apps/dashboard/`) to configure more."
3. Open as a PR; no other files need changing
**Definition of done:** `curl -s https://raw.githubusercontent.com/aaronjmars/aeon/main/README.md | grep -c "gh repo fork"` returns ≥1 inside a fenced bash block; a cold reader can clone-configure-push without opening any other doc.

---

### 3. SHA-pin GitHub Actions in all .github/workflows/*.yml files
**Priority:** MED
**Type:** Security
**Effort:** Small (hours)
**Anchor:** FILE:.github/workflows/aeon.yml (uses `actions/checkout@v5` and `actions/setup-node@v5` — mutable floating tags, not pinned SHAs)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** A compromised or tag-hijacked `actions/checkout@v5` would silently execute malicious code inside every Aeon skill run with access to all repository secrets — including `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, and any other operator secrets. SHA-pinning freezes the exact commit each action resolves to, making supply-chain attacks auditable without breaking CI.
**How:**
1. For each workflow in `.github/workflows/` (aeon.yml, chain-runner.yml, ci-capabilities-parity.yml, ci-skills-json.yml, messages.yml, sync-upstream.yml), find all `uses:` lines with floating major-version tags
2. For each action, resolve its current SHA: `gh api repos/actions/checkout/git/ref/refs/tags/v5 --jq .object.sha` (and the same for `actions/setup-node`, `actions/upload-artifact`, etc.)
3. Replace `actions/checkout@v5` → `actions/checkout@<SHA> # v5` (keep the tag as a comment for readability); repeat for all actions across all six workflow files; open one PR with all six changes
**Definition of done:** `grep -r "uses: actions/" .github/workflows/ | grep -v '#'` returns no lines with `@v` or `@main` patterns — every action reference is a full 40-character commit SHA with a `# vN` comment.

---

### 4. Add CODE_OF_CONDUCT.md using Contributor Covenant 2.1
**Priority:** MED
**Type:** Community
**Effort:** Small (hours)
**Anchor:** MISSING:CODE_OF_CONDUCT.md
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** With CONTRIBUTING.md (PR #465) and issue templates (PR #466) pending merge, CODE_OF_CONDUCT.md is the last file needed to hit 100% on GitHub's Community Standards checklist — a signal visible to every potential contributor who clicks "Insights → Community Standards" before submitting a PR. A 511-star, 170-fork repo with active external PRs (#418) has no declared conduct standard.
**How:**
1. Create `CODE_OF_CONDUCT.md` using Contributor Covenant 2.1 (boilerplate text available at https://www.contributor-covenant.org/version/2/1/code_of_conduct/); set the enforcement contact email to the email on Aaron's GitHub profile or a `conduct@aeon.fun` placeholder if no public address is listed
2. Open as a PR targeting main; no other files need changing (GitHub detects the file automatically and surfaces it in the Community Standards tab)
3. No link from README needed — GitHub renders the CoC link automatically once the file exists
**Definition of done:** `gh api repos/aaronjmars/aeon/community/profile --jq .files.code_of_conduct` returns a non-null object; the "Community Standards" tab shows a green checkmark for Code of conduct.

---

### 5. Add SECURITY.md with responsible disclosure policy and GitHub private vulnerability reporting
**Priority:** MED
**Type:** Security
**Effort:** Small (hours)
**Anchor:** MISSING:SECURITY.md
**Score:** L=3 C=4 N=4 (total 11/15)
**Impact:** Aeon runs as an autonomous agent with access to operator secrets, executes external code, and fetches untrusted content from the web — a class of software where security researchers legitimately probe for vulnerabilities. Without a SECURITY.md, researchers have no declared disclosure channel and may either go silent or post publicly; a policy also enables GitHub's "Report a vulnerability" button which routes disclosures privately without a public issue.
**How:**
1. Create `SECURITY.md` with three sections: (a) Supported versions (current main branch; older forks not maintained), (b) Reporting a vulnerability (link to the GitHub private security advisory form: `https://github.com/aaronjmars/aeon/security/advisories/new`; expected response time: 7 days), (c) Security model (Aeon is an autonomous agent that executes fetched content as instructions — only the `CLAUDE.md` and skill SKILL.md files are trusted; all fetched external content is untrusted data as documented in CLAUDE.md)
2. Enable GitHub's private vulnerability reporting: `gh api --method PUT repos/aaronjmars/aeon/private-vulnerability-reporting` (requires the admin token; note this as a post-PR manual step if the token scope doesn't cover it)
3. Open as a PR
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/SECURITY.md --jq .size` returns a non-null size > 0; the "Security" tab on the repo shows "Security policy" as defined.

---

## Monitor
<!-- Ideas that failed the implementability gate. Surfaced for human decision. Max 3. -->

### A. Rebase PR #418 to resolve BEAMR gateway merge conflicts
**Why not yet:** The PR lives on `SahilParikh03`'s fork — rebasing requires either (a) the contributor to rebase their own branch, or (b) a maintainer with push access to the fork branch. `external-feature` can't autonomously push to a contributor's fork. The cleanest path is a comment on the PR guiding SahilParikh03 through `git fetch upstream && git rebase upstream/main`, but that requires a human maintainer to post it or for `aaronjmars` to trigger a repo-dispatch that does so.
**Anchor:** PR:#418 "feat(gateway): add BEAMR as an LLM gateway"

---

## Fleet follow-ons

- aaronjmars/minitor: PR #72 (Dexscreener DEX-pair column) is 1d old and awaiting review — add a `TESTING.md` one-liner smoke test (`NEXT_PUBLIC_... npm run build`) to the PR description to reduce reviewer setup friction and pull it across the finish line.

---

**Source status:** gh=ok code_search=rate_limited memory_topics=missing articles_dir=ok watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** "Rebase PR #418 to unblock BEAMR gateway integration" (2026-06-12 top pick — PR still open, not novelty-eligible this cycle; Monitor section A covers it)
