# Repo Action Ideas — 2026-05-22

Generated from analysis of aaronjmars/aeon (423⭐, 103 forks, 3 open issues), aaronjmars/aeon-agent (9⭐, 1 fork), and aaronjmars/minitor (9⭐, 0 forks). `install-skill-pack` shipped this morning (PR #213); within hours three community packs appeared: AntFleet/aeon-skills added to trusted-sources (PR #211, merged), zer0-skill-pack (PR #208, open), gitbounty-skill-pack (PR #212, open). That velocity shapes ideas 1 and 2. H1 is the last open High from AntFleet Issue #184. contributor-spotlight still has the same FORK_DEFAULT_BRANCH bug that aeon PR #206 fixed May-21.

---

### 1. Machine-readable skill pack registry
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** Three packs were submitted within hours of `install-skill-pack` shipping. They all add rows to a README table — human-readable, not queryable. Without a machine-readable index there's no `./install-skill-pack --list`, no pack discovery without reading the README, and no stable surface for third-party tooling. A `skill-packs.json` at the repo root turns the growing table into a real package index. The install script gets a `--list` flag; future forks get a discovery API without polling GitHub search.

**How:**
1. Create `skill-packs.json` at repo root with an entry for each known pack: `{repo, description, skills: [slug], category, trust_level: "trusted"|"community"}`. Seed with 5 entries: AntFleet/aeon-skills (trusted, pr-review-antfleet), baseddevoloper/aeon-skill-pack-vvvkernel, danbuildss/luca-aeon-skills, zer0-skill-pack (from open PR #208), gitbounty-skill-pack (from open PR #212).
2. Add `--list` flag to `./install-skill-pack`: reads `skill-packs.json` (from local repo if present, else WebFetch fallback from raw.githubusercontent.com), prints a formatted table (repo / description / skills count / trust badge).
3. Update `docs/community-skill-packs.md` — add the `skill-packs.json` schema to the pack-maintainer checklist so new pack PRs know to include a registry entry in their PR body.

---

### 2. Close H1: v4-readiness manifest gaps
**Type:** Bug fix
**Effort:** Small (hours)
**Impact:** H1 is the last open High from AntFleet Issue #184. The v4-readiness skill carries an embedded Safe/Review/Removed table in its SKILL.md. H1 = the Removed table has gaps — capabilities that were actually removed in v4 but aren't listed, so operator checklists silently give false-safe signals. With 103+ forks now running pre-upgrade workflows, a stale Removed table means real operators miss real breakage. One targeted edit closes the last High and makes the checklist trustworthy.

**How:**
1. Read `skills/v4-readiness/SKILL.md` and extract the current Safe/Review/Removed table.
2. Cross-reference against the `aeon.yml` changelog, recent breaking-change PRs (look for `feat!`/`fix!` commit prefixes and `BREAKING` in PR bodies), and any capabilities that shipped in v3 but are absent from v4's current `aeon.yml`. Identify removed hooks, deprecated env var names, and retired skill APIs.
3. Update the Removed table with confirmed gaps; add a `Last audited: 2026-05-22` footer line to the table so future maintainers know when the manifest was last verified. Open PR against `aaronjmars/aeon`, reference Issue #184 H1 in the PR body.

---

### 3. Backport contributor-spotlight FORK_DEFAULT_BRANCH fix
**Type:** Bug fix
**Effort:** Small (hours)
**Impact:** aeon PR #206 (merged 2026-05-21) fixed a missing `FORK_DEFAULT_BRANCH` extraction in contributor-spotlight: step 4 wrote `default_branch` into `/tmp/contrib-repo.json` but never extracted it, so step 5's `?ref=${FORK_DEFAULT_BRANCH}` always sent an empty ref. aeon-agent's `skills/contributor-spotlight/SKILL.md` was forked from the same upstream lineage and has the identical bug. ENABLED_COUNT and OPERATOR_AUTHORED — the two most newsworthy data points in the weekly article — are wrong on every non-`main`-branch fork. Continues the same-day-after backport cadence.

**How:**
1. Apply the same two-line fix from aeon PR #206 to `skills/contributor-spotlight/SKILL.md` in aeon-agent: after the `/tmp/contrib-repo.json` write at step 4, add `FORK_DEFAULT_BRANCH=$(jq -r '.default_branch // "main"' /tmp/contrib-repo.json)` and a second guard for the literal string `null`.
2. Tighten the step 5 fallback from `|| true` to `|| echo '' > /tmp/fork-aeon.yml` so `grep -E` downstream always has a file under `set -e`.
3. Open PR against `aaronjmars/aeon-agent`, note upstream aeon PR #206 as the source and continuing the backport cadence note.

---

### 4. Column refresh intervals
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Every column in minitor currently refreshes on the same cadence (mount + manual). Crypto/price columns (CoinGecko, DeFiLlama) need 1–5 min polling; GitHub stars don't need more than hourly. Without per-column intervals, operators either over-poll slow APIs (rate limits) or under-poll fast ones (stale data). This is the most-requested ergonomics improvement that requires zero changes to any existing column plugin — the interval lives at the column-row level, not in plugin config.

**How:**
1. Add a nullable `refresh_interval_seconds` column to the `columns` table (additive migration, `drizzle/0002_refresh_interval.sql`). Add to `Column` type in `lib/columns/types.ts`. Add a "Refresh interval" dropdown to `configure-column-dialog.tsx` with options: Every minute / 5 min / 15 min / 60 min / Manual only (default); saves via existing `updateColumnConfig` server action.
2. In `column-card.tsx`: `useEffect` reads `column.refresh_interval_seconds`, sets a `setInterval` that calls `fetchColumn(column.id)` on the configured cadence. Clears on unmount. Renders a small clock badge in the column header showing the current interval.
3. Deck export/import round-trips the new field backward-compatibly (absent field → defaults to manual-only on import).

---

### 5. /gallery public deck page
**Type:** Growth
**Effort:** Small-Medium (1 day)
**Impact:** The starter deck templates (PR #47, open) live inside a modal — a returning operator can find them via ⌘K, but a first-time visitor with no account sees nothing. A `/gallery` route is a public-facing, SEO-crawlable page that any link can land on: operator shares a URL, colleague opens it, sees curated decks, one-click imports, starts monitoring. Builds entirely on top of the share-link (PR #46) + templates (PR #47) infrastructure — no new schema, no new server routes.

**How:**
1. Create `app/gallery/page.tsx` (server component, no auth required). Import `TEMPLATES` from `lib/deck-templates.ts` (same source as the modal in PR #47). Render a responsive card grid: each card shows template name, tagline, description, column-type pills colored by plugin brand. "Import deck" button encodes the template payload as a `#deck=...` URL fragment and navigates to `/?deck=...` (the existing hash-import handler in `deck-view.tsx` handles the rest).
2. Add a "Browse community decks" link in the sidebar footer (below the existing ⌘K commands) — surfaces `/gallery` without requiring users to know the URL exists.
3. Add a `<link rel="canonical">` and `<meta description>` with the template name + column-type summary in the page's `<head>` so search engines can index individual deck types.
