---
type: Article
---

# Repo Actions — aaronjmars/minitor — 2026-06-24

**Top pick for tomorrow:** #1 — Add a LICENSE file (Community, Small)
**Verdict:** Minitor has no license — legal grey zone for all 191 forks and every would-be contributor. That's the single highest-leverage fix this cycle; three remaining ideas close the deployment documentation gap and tighten CI before the contributor surface grows.

## Actions

### 1. Add a LICENSE file
**Priority:** HIGH
**Type:** Community
**Effort:** Small (hours)
**Anchor:** MISSING:LICENSE (confirmed absent — `gh api repos/aaronjmars/minitor/license` returns 404; without a license every fork lives in all-rights-reserved territory by default)
**Score:** L=5 C=5 N=5 (total 15/15)
**Impact:** Without a license, contributors can't legally fork, adapt, or redistribute Minitor — the most direct blocker to the "lower the barrier to fork" goal. MIT removes that barrier in a single file and signals to evaluators that the project is open for business.
**How:**
1. Create `LICENSE` at repo root using the standard MIT text, year=2026, copyright holder="Aaron J Mars".
2. Open a single-file PR on branch `docs/add-mit-license`. No other files require changes — GitHub auto-detects the file and renders the license badge on the repo header.
3. Confirm `gh api repos/aaronjmars/minitor/license --jq .license.spdx_id` returns `"MIT"` after merge.
**Definition of done:** The repo header shows a "MIT license" badge; `gh api repos/aaronjmars/minitor/license --jq .license.spdx_id` returns `"MIT"`.

---

### 2. Add a `github-notifications` column plugin (personal GitHub inbox feed)
**Priority:** HIGH
**Type:** Feature
**Effort:** Medium (1–2 days)
**Anchor:** FILE:lib/columns/plugins/manifest.ts (49 columns registered; 11 github-* columns cover trending/issues/PRs/stars/forks/commits/releases/actions/backlinks/search/discussions; the personal Notifications API `GET /notifications` — the unified inbox for mentions, review requests, CI alerts, and subscriptions — is absent)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Users who already set `GITHUB_TOKEN` (documented in README for all 11 github-* columns) can get their full GitHub notification stream as a Minitor column — review requests, CI failures, mentions across every watched repo — without leaving the dashboard. No new API key or external account needed; the column reuses the existing optional `GITHUB_TOKEN`.
**How:**
1. Copy `lib/columns/plugins/_template/` to `lib/columns/plugins/github-notifications/`. In `plugin.ts`: set `id="github-notifications"`, `label="GitHub Notifications"`, `category="other"`, `icon=Bell`, schema with `filter: z.enum(["all","unread"]).default("unread")` and optional `repo: z.string().default("")` to scope to a single repo.
2. In `server.ts`: call `GET https://api.github.com/notifications?all=<true|false>&per_page=20` with `Authorization: Bearer <GITHUB_TOKEN>`; map each notification's `subject.title`, `reason`, `updated_at`, and `subject.url` to `FeedItem`; declare `requiresEnv: ["GITHUB_TOKEN"]` in capabilities.
3. Add import + entry to `lib/columns/plugins/manifest.ts`, `lib/columns/registry.ts`, and `lib/columns/server-registry.ts`. Run `npm run build` to confirm the parity check passes.
**Definition of done:** `npm run build` succeeds; adding a `github-notifications` column in the UI with `GITHUB_TOKEN` set shows the user's unread GitHub notifications with reason labels (mention, review_requested, etc.); `GITHUB_TOKEN` absent shows the standard missing-key dim state.

---

### 3. Add a `## Deploy` section to README.md (plus document `GITHUB_TOKEN` in `.env.example`)
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** README:section:Deploy (absent; the README Quickstart covers `./minitor` for local dev and `./minitor build/start` for a local production server but has no section on Vercel deployment, driver selection for production, or env-var configuration for cloud runs — a forker evaluating self-hosting must piece this together from scattered notes) + FILE:.env.example (`GITHUB_TOKEN` not listed despite 11 github-* columns using it and the README explicitly calling it out as optional)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Self-hosting is the first decision a fork evaluator makes. No Deploy section means they're left guessing which `DATABASE_URL` driver to pick for Vercel vs. self-hosted, and whether there are extra env vars. The missing `GITHUB_TOKEN` entry in `.env.example` means users who clone and configure via that file run all 11 GitHub columns at 60 req/hr without knowing a free token triples the limit to 5000. Fixing both in one PR closes the deployment friction surface end-to-end.
**How:**
1. Insert a `## Deploy` section into README.md after the Stack section. Cover: **Vercel (recommended)** — fork, `vercel link`, set `DATABASE_URL` to a Neon serverless URL (free tier), paste `XAI_API_KEY` and any optional keys, push — Vercel auto-detects Next.js 16. **Self-hosted** — `./minitor build && ./minitor start` (PGlite is bundled; add `DATABASE_URL` only for a shared Postgres). **Env vars** — a compact table listing all 7 env vars with required/optional status, linking `.env.example`.
2. Add `GITHUB_TOKEN=` to `.env.example` with a comment: "# Optional. All 11 github-* columns work keyless at 60 req/hr; a personal access token raises the limit to 5000 req/hr. Generate at https://github.com/settings/tokens (classic, no scopes needed for public repos)."
**Definition of done:** `curl -s https://raw.githubusercontent.com/aaronjmars/minitor/main/README.md | grep -c "## Deploy"` returns 1; `.env.example` contains a `GITHUB_TOKEN` entry; a developer can deploy from a cold fork to a live Vercel instance using only the README.

---

### 4. Add a lint step to the CI workflow
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:.github/workflows/ci.yml (single `build` job; `package.json` line 6 declares `"lint": "eslint"` but it is not invoked in CI — ESLint errors only surface on a developer's local machine or silently skip in the pipeline)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** The CI workflow currently builds but never lints. An ESLint violation — unused import, any-typed variable, missing exhaustive switch — passes CI and merges silently. Adding `npm run lint` as a second step catches these before they accumulate; the build step already pays the `npm ci` cost so the lint step adds only ~10s.
**How:**
1. Read `.github/workflows/ci.yml` and locate the `Build` step (currently the final step). Add a `Lint` step immediately before it:
   ```yaml
   - name: Lint
     run: npm run lint
   ```
2. Verify locally that `npm run lint` exits 0 on a clean checkout (the ESLint config at `eslint.config.mjs` already exists). If the current codebase has lint errors, fix them in the same PR before adding the CI step.
**Definition of done:** A PR that introduces an ESLint violation (e.g. an unused import) fails the CI `Lint` step before reaching `Build`; the badge on `main` shows both `Build` and `Lint` passing.

---

### 5. Add SECURITY.md for responsible disclosure
**Priority:** MED
**Type:** Security
**Effort:** Small (hours)
**Anchor:** MISSING:SECURITY.md (confirmed absent; Minitor handles several API keys — `XAI_API_KEY`, `GITHUB_TOKEN`, `NEYNAR_API_KEY`, `YOUTUBE_API_KEY`, `COINGECKO_DEMO_API_KEY` — and processes user-supplied content via all 49 columns; no vulnerability disclosure policy exists)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** As fork count grows, the likelihood of a security researcher or fork operator discovering a vulnerability rises. Without SECURITY.md, they have no official channel — reports land as public issues or disappear. A short security policy with a contact address and a 90-day coordinated-disclosure timeline signals maturity to evaluators and gives researchers a path that doesn't embarrass anyone.
**How:**
1. Create `SECURITY.md` at repo root with: **Supported versions** (main branch; no prior release pinning), **Reporting a vulnerability** (private report via GitHub's "Report a vulnerability" button under the Security tab, or email to a configured address), **Response timeline** (acknowledge in 5 business days, coordinate patch within 90 days), **Out of scope** (API keys stored in `.env.local` by the operator — secrets management is the operator's responsibility, not the framework's).
2. Open as a single-file PR on branch `docs/add-security-policy`.
**Definition of done:** `gh api repos/aaronjmars/minitor/contents/SECURITY.md --jq .size` returns a non-null number; GitHub's Security tab shows "Security policy" as configured.

---

## Monitor

### A. SHA-pin .github/workflows/ci.yml action references
**Why not yet:** Writing to `.github/workflows/` requires a GH_PAT with the `workflows` scope — the standard `GITHUB_TOKEN` used by Aeon cannot push workflow file changes. Same blocker as aaronjmars/aeon. Eligible once `GH_PAT` with `workflows` scope is configured as a secret.
**Anchor:** FILE:.github/workflows/ci.yml (uses floating `actions/checkout@v5`, `actions/setup-node@v5` — pinning to SHA would prevent a compromised action version from affecting CI)

---

## Fleet follow-ons

- aaronjmars/aeon: PR #545 (usephylax, "fix(phylax-audit): format example threat strings as inline-code") opened today (14:00Z) — a formatting-only fix from the phylax author, trivial to triage and merge. Also: PR #510 (LENS skill pack, ThoLynceus, 5 days open) is the cleanest external-contribution unblock; LENS adds an AI/LLM skills category and the PR has had no maintainer response since 06-21.

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** 2026-06-22 top pick "Wire phylax-audit into install-skill-pack" → executed (reframed as agent-to-agent skill-triage PR #544, merged 2026-06-24) — cleared
