---
type: Article
---

# Repo Actions — aaronjmars/aeon — 2026-06-16

**Top pick for tomorrow:** #1 — Validate and merge external PR #472 (Hunch Prediction Markets skill pack) (Community/Growth, Small)
**Verdict:** Two structural gaps in the community pack contribution workflow dominate this cycle — PR #472 is a complete, well-formed external contribution that has sat unmerged for 24h, and the process that produced it (public-repo pack format) has no tooling to guide future contributors or auto-validate submissions.

## Actions

### 1. Validate and merge PR #472 (Hunch Prediction Markets skill pack)
**Priority:** HIGH
**Type:** Community / Growth
**Effort:** Small (hours)
**Anchor:** PR:#472 "Add Hunch Prediction Markets skill pack (crypto)" by rajkaria
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Every merged external pack PR is a counted ecosystem metric (STRATEGY: "merged external PRs"). Hunch is the first pack in the catalog where an agent can take an onchain position (not just watch markets), which anchors the x402 payment rail narrative that Aeon's BEAMR/glim.sh work established. Merging signals to the 175-fork cohort that external packs do get accepted.
**How:**
1. Verify pack structure: `gh api repos/rajkaria/hunch/contents/aeon-skill-pack/skills-pack.json` — check `name`, `skills[]`, `category` fields; confirm `MIT` license via `gh api repos/rajkaria/hunch --jq .license.spdx_id`; spot-check one skill for SKILL.md: `gh api "repos/rajkaria/hunch/contents/aeon-skill-pack/skills/hunch-intel/SKILL.md"` returns non-null.
2. Verify endpoints are public: the PR lists `/api/partner/intel` and `/api/mcp` on `playhunch.xyz` — `curl -sf https://www.playhunch.xyz/api/partner/intel` should return a 4xx (missing params) not a 401 (auth wall).
3. If validation passes: `gh pr review 472 --repo aaronjmars/aeon --approve --body "Pack structure verified — public APIs, MIT license, SKILL.md per skill, simulate-by-default bet skill. Merging."` then `gh pr merge 472 --repo aaronjmars/aeon --merge`.
**Definition of done:** `gh pr view 472 --repo aaronjmars/aeon --json state -q .state` returns `"MERGED"`; the community packs section of README lists Hunch.

---

### 2. Add `.github/PULL_REQUEST_TEMPLATE.md` for community pack contributions
**Priority:** MED
**Type:** Community / DX
**Effort:** Small (hours)
**Anchor:** MISSING:.github/PULL_REQUEST_TEMPLATE.md
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** PR #472 arrived with a detailed description because rajkaria read the docs carefully — the next external contributor may not. A PR template pre-populates the sections that matter for pack review (pack name, skills list, API endpoint summary, simulate-by-default confirmation, install command) and halves review latency by making every submission immediately scannable.
**How:**
1. Create `.github/PULL_REQUEST_TEMPLATE.md` with four sections: **Pack summary** (name, category, pack repo URL, `./install-skill-pack` command), **Skills** (one-line per skill with read-only vs write-action tag), **API endpoints** (list all external calls; note if any require operator secrets), **Guidelines checklist** (`[ ] public repo` / `[ ] MIT or Apache license` / `[ ] skills-pack.json at pack root` / `[ ] SKILL.md per skill` / `[ ] all read skills work without secrets` / `[ ] write skills are default_enabled: false`).
2. Keep the file under 40 lines — GitHub renders it verbatim in the PR compose box; too long and contributors skip it.
3. Open as a PR with `closes` referencing no issue (self-contained new file).
**Definition of done:** Opening a new PR on `aaronjmars/aeon` pre-populates the description with the template; `gh api repos/aaronjmars/aeon/contents/.github/PULL_REQUEST_TEMPLATE.md --jq .size` returns non-null.

---

### 3. Add `scripts/validate-pack.sh` — local pre-flight validator for community pack authors
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:CONTRIBUTING.md (pack submission section lacks a runnable validation helper)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** The friction point before PR #472-style submissions isn't the PR format — it's "does my pack actually meet the requirements?" A one-command validator (`./scripts/validate-pack.sh /path/to/pack-dir`) that checks the invariants `external-feature` would check manually gives external contributors confidence before they open a PR, and gives maintainers a reference definition of "valid pack" to point to in reviews.
**How:**
1. Create `scripts/validate-pack.sh` that accepts a local pack directory path and checks: (a) `skills-pack.json` exists and has `name`, `skills[]`, `category`; (b) each skill slug in `skills[]` has a corresponding `skills/{slug}/SKILL.md`; (c) root of the pack has `LICENSE` or `LICENSE.md`; (d) every `SKILL.md` frontmatter has `name`, `description`, `tags`; (e) no skill has `default_enabled: true` if it makes network POST/write calls (check for `enabled: true` + presence of keywords `POST`, `PUT`, `DELETE`, `bet`, `send`, `transfer` in the SKILL.md body — conservative heuristic, flag as WARNING not ERROR).
2. Print a ✅/❌/⚠️ summary per check; exit code 0 if no ERRORs, 1 on any ERROR.
3. Add two lines to `CONTRIBUTING.md` referencing it under the pack submission section: "Before opening a PR, run `./scripts/validate-pack.sh /path/to/your-pack-dir` to catch structural issues locally."
**Definition of done:** `bash scripts/validate-pack.sh aeon-skill-pack 2>/dev/null` exits 0 on a valid pack directory; on a directory missing `skills-pack.json` it exits 1 with a clear ERROR message; the script is referenced in CONTRIBUTING.md.

---

### 4. Add README section: one-click community pack install via dashboard
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md (the Install / Quickstart section does not document the dashboard's new one-click pack install or `./install-skill-pack` CLI added in PRs #483 and #485)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** The dashboard's community pack install (PR #483) and zero-touch auto-merge (PR #485) are the biggest onboarding improvements shipped this week — a forker can extend Aeon without touching code. But the README's quickstart still describes the manual `aeon.yml` toggle flow. Forks that discover community packs via the dashboard and wonder "can I install more?" have no path documented.
**How:**
1. Open `README.md`; find the existing "Packs" or "Quickstart" section (the packs table updated in PR #488); insert a sub-section "Add community packs" immediately after the Core pack description with two methods: (a) Dashboard: "Click **+ Add packs** in the dashboard sidebar — browse community packs and click Install. Aeon opens a PR and auto-merges it." (b) CLI: `./install-skill-pack owner/pack-repo [--path subdir]` — note that this also auto-merges.
2. Add one line: "Installed packs appear in their own **Installed** group in the dashboard roster (PR #486)."
3. No other files need changing; open as a single-file PR.
**Definition of done:** `curl -s https://raw.githubusercontent.com/aaronjmars/aeon/main/README.md | grep -c "install-skill-pack"` returns ≥1; a cold reader can discover and install a community pack without reading any code.

---

### 5. Add GitHub Actions workflow to auto-comment a validation checklist on community pack PRs
**Priority:** MED
**Type:** DX
**Effort:** Medium (1–2 days)
**Anchor:** MISSING:.github/workflows/community-pack-review.yml
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** As community pack submissions scale (PR #472 is the second external pack PR after glim.sh), manual review becomes a bottleneck. An automated comment posted within seconds of PR open sets the bar explicitly, reduces back-and-forth, and makes `external-feature`'s review step in idea #1 reproducible and codified.
**How:**
1. Create `.github/workflows/community-pack-review.yml` with trigger: `pull_request: types: [opened, reopened]`. In the job, detect if the PR modifies `README.md` (community pack table) or any file under a new `community-packs/` path using `git diff --name-only HEAD^ HEAD` pattern. If detected, post a comment via `gh pr comment ${{ github.event.pull_request.number }} --body "$(cat .github/community-pack-checklist.md)"`.
2. Create `.github/community-pack-checklist.md` with the machine-readable checklist: "**Community pack submission checklist** — `scripts/validate-pack.sh` passes on the referenced pack repo; pack repo is public; license is MIT or Apache-2.0; all write/bet skills have `default_enabled: false`; `./install-skill-pack` command in the PR description is correct."
3. Use `permissions: pull-requests: write` so the bot can post the comment; no new secrets required (`GITHUB_TOKEN` suffices).
**Definition of done:** Opening a draft PR that touches `README.md` triggers the workflow and posts the checklist comment within 60 seconds; `gh run list --workflow=community-pack-review.yml --repo aaronjmars/aeon` shows a successful run.

---

## Monitor
<!-- Ideas that failed the implementability gate. Max 3. -->

### A. SHA-pin all GitHub Actions workflow files
**Why not yet:** Pinning requires pushing to `.github/workflows/*.yml` — the default `GITHUB_TOKEN` lacks the `workflows` scope (noted in Lessons Learned). Needs a `GH_PAT` with `workflows` permission configured as a repo secret before `external-feature` can execute this autonomously.
**Anchor:** FILE:.github/workflows/aeon.yml (uses `actions/checkout@v4`, `actions/setup-node@v4` — mutable floating tags)

### B. Rebase PR #418 (BEAMR gateway) to clear merge conflicts
**Why not yet:** The branch lives on SahilParikh03's fork — rebasing requires either the contributor to rebase or a maintainer with push access to the fork. `external-feature` cannot push to a contributor's fork branch. The automation path is a maintainer comment on the PR guiding the rebase, which requires a human to initiate.
**Anchor:** PR:#418 "feat(gateway): add BEAMR as an LLM gateway"

---

## Fleet follow-ons

- aaronjmars/minitor: PR #74 (github-commits column) merged 2026-06-15 — with 49 built-in columns and 0 contributor documentation, next up is a `CONTRIBUTING.md` with a step-by-step column plugin guide (pattern: `lib/columns/plugins/_template/`, registration in `manifest.ts` + `registry.ts` + `server-registry.ts`, `lib/integrations/` for data fetching).

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** "Add CODE_OF_CONDUCT.md using Contributor Covenant 2.1" (2026-06-14 idea #4 — undone, but N=1 this cycle; eligible from 2026-06-21 once it clears the 7-day quiet window)
