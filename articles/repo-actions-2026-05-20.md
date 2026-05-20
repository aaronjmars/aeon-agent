# Repo Action Ideas — 2026-05-20

Generated from analysis of aaronjmars/aeon (404⭐, 88 forks), aaronjmars/aeon-agent (9⭐, 1 fork), and aaronjmars/minitor (9⭐, 0 forks). Today's run closes AntFleet H3 and H7 (two of the five remaining Issue #184 Highs), adds the community skill pack install protocol that baseddevoloper's Issue #185 implied, and gives minitor its first growth-oriented feature (shareable deck links) plus a blank-slate eliminator (starter deck templates).

---

### 1. Fix AntFleet H3: FORK_DEFAULT_BRANCH undefined in contributor-spotlight
**Type:** Bug fix
**Effort:** Small (hours)
**Impact:** contributor-spotlight's step 5 fetches the fork's `aeon.yml` via `gh api repos/${FEATURED_FORK}/contents/aeon.yml?ref=${FORK_DEFAULT_BRANCH}`. The `default_branch` field is fetched at step 4 into `/tmp/contrib-repo.json` but never extracted into the shell variable — so `FORK_DEFAULT_BRANCH` is always unbound (empty string). This silently sends `?ref=` to the API, which either returns the wrong branch or errors; skill-enabled-count and operator-authored-skill detection are both wrong. With 88 active forks now running divergent default branches (some use `master`, some `develop`, some custom), this hits every contributor-spotlight run silently.

**How:**
1. After the `/tmp/contrib-repo.json` write (step 4), add: `FORK_DEFAULT_BRANCH=$(jq -r '.default_branch // "main"' /tmp/contrib-repo.json)` — one line.
2. Open a PR against `aaronjmars/aeon`, close Issue #184 H3 in the PR body.
3. Verify the fix by running contributor-spotlight with `var=dry-run antfleet-ops/aeon` (antfleet-ops is known to use `main`, so a passing run plus a non-empty enabled-skill list confirms the extraction works).

---

### 2. Community Skill Pack Install CLI (./install-skill-pack)
**Type:** Feature / Community
**Effort:** Medium (1-2 days)
**Impact:** baseddevoloper opened Issue #185 proposing a community skill packs ecosystem; aaronjmars merged PR #187 adding a Community Skill Packs README section. The missing piece is the protocol: right now "installing a community skill pack" means cloning a repo and manually copying files. A one-command install makes skill packs a real distribution channel — the difference between "interesting README note" and "type one command and you're running it."

**How:**
1. Write `./install-skill-pack` bash script: takes a GitHub `owner/repo` argument (optional `--path skills/<name>` for subdirectory packs). Fetches `skills-pack.json` from the remote root — a manifest listing skill slugs and their paths. Falls back to scanning the remote `skills/` directory if no manifest exists.
2. For each skill: download the `SKILL.md`, run `./skills/skill-security-scan/scan.sh` on it (the existing scanner), prompt operator to confirm any HIGH findings. Copy approved skills to local `skills/`, add entries to `skills.json` (same format as `./add-skill` output).
3. Write a companion `skills-pack.json` format spec (10-line JSON schema in `docs/community-skill-packs.md`). baseddevoloper's aeon-skill-pack-vvvkernel is the first test case — run the install against it to validate the format.

---

### 3. Honor Branch Constraint in skill-update-check (AntFleet H7)
**Type:** Bug fix
**Effort:** Small (hours)
**Impact:** `skills.lock` entries carry a `branch` field so operators can pin an imported skill to a specific upstream branch (e.g. a vendor's `stable` branch instead of `main`). skill-update-check's step 2 fetches the latest upstream commit for the locked path via `gh api "repos/${source_repo}/commits" -f path="${source_path}" -f per_page=1` — without passing `-f sha=${branch}`. The API defaults to the repository's default branch, so a skill pinned to `stable` always compares against `main`. Operators with branch-pinned skills see perpetual false "update available" alerts.

**How:**
1. In `skills/skill-update-check/SKILL.md`, step 2: change the `gh api` call to `-f sha="${branch}"` when the lock entry has a `branch` field. Add a null-guard: if `branch` is empty or `"main"`, omit the flag (API default suffices).
2. Update the "Per-changed-skill enrichment" step (step 3) similarly — `compare/${locked_sha}...${current_sha}` already uses SHAs directly, so no change needed there. Only the initial "fetch latest SHA" call needs the branch constraint.
3. Open a PR against `aaronjmars/aeon-agent`, reference Issue #184 H7 (filed against upstream but the skill lives in aeon-agent).

---

### 4. Deck Share Link (URL-Fragment-Encoded Config)
**Type:** Feature / Growth
**Effort:** Small-Medium (1 day)
**Impact:** minitor has 9 stars and 0 forks. The deck export/import primitive (PR #40) allows sharing decks via JSON copy-paste, but there's no shareable link. Adding a "Share Deck" button that encodes the active deck config as a base64 URL fragment (`minitor.instance/#deck=...`) turns every operator's monitoring setup into a distribution channel. Shared links appear on X/Discord/forums; anyone who clicks gets the import dialog pre-filled and is one click from a live dashboard. No server-side persistence, no new auth, purely client-side. The viral loop: operator tweets "my AI research dashboard" → link → installs.

**How:**
1. In the deck store / nav header (same location as the existing "Export Deck" ⌘K command): add "Share Deck" — serializes to the existing DeckExport v1 JSON, `btoa(JSON.stringify(export))`, sets `window.location.hash = "deck=" + encoded`.
2. On app initialization (`app/page.tsx` or `lib/store/use-deck-store.ts`): read `window.location.hash`, detect `#deck=`, base64-decode, pass to the existing `importDeck` server action, activate the imported deck. Same Zod validation path as manual import — forward-compat already guaranteed.
3. Add a "Shared deck imported" toast on success; clear the hash from the URL after import so refreshing doesn't re-import.

---

### 5. Starter Deck Templates Gallery
**Type:** DX / Growth
**Effort:** Medium (1-2 days)
**Impact:** A new minitor install starts completely blank — the operator sees an empty column list and has to know which of the 50+ column types to add. The blank-slate problem is the #1 conversion killer for developer tools. A templates screen shown on first launch ("AI Research", "Base Ecosystem", "Crypto DeFi", "Startup Tracker") gives operators a meaningful starting point in two clicks instead of an exploration task. Each template is a static JSON file using the existing DeckExport v1 shape — no new schema, no new API. After the deck-share link (idea #4 above) is built, templates are just pre-written share links.

**How:**
1. Write 4 JSON template files to `public/templates/` using the DeckExport v1 shape: `ai-research.json` (HN + arXiv + GitHub trending + Hugging Face + X/AI terms), `base-ecosystem.json` (GitHub stars for aeon/aeon-agent + CoinGecko AEON watchlist + DeFiLlama + wallet-tx), `crypto-defi.json` (DeFiLlama gainers + Polymarket + CoinGecko top + X/crypto terms), `startup-tracker.json` (GitHub trending + Product Hunt + HN Show + devto + Reddit r/startups).
2. On first launch (empty `decks` list), render a templates overlay in the main app layout: 4 cards with name, description, column-type pills. "Use this deck" → POST to existing `/api/decks` + import flow. "Start blank" → dismiss.
3. Add a "Browse templates" ⌘K command so returning operators can import templates into an existing workspace.
