# Repo Action Ideas — 2026-06-04

*Generated from analysis of aaronjmars/aeon (482⭐, 161 forks, 3 open issues), aaronjmars/aeon-agent, and aaronjmars/minitor.*

---

## Context

**aeon** is 18 stars from the 500⭐ milestone (star-momentum puts arrival at ~June 12). The ECOSYSTEM.md is now a visual catalog — logos batch merged last week, 30+ entries. Three install paths are live: `add-skill`, `install-skill-pack`, `install-from-atrium`. The HoundFlow security pack shipped six keyless onchain skills two weeks ago; `wallet-risk-weekly` (PR #340) became their first scheduled consumer today. Phase 1 capabilities frontmatter (PR #322) locked declarations onto ~30 high-blast-radius skills; the `(undeclared)` row in capabilities-map covers the remaining ~150.

**aeon-agent** completed its 21st consecutive same-day-after backport today (narrative-convergence from upstream PR #272). Two skills remain in that batch: mcp-pulse and fleet-scorecard. Three shell-substitution anti-pattern sites persist in SKILL.md files: repo-article (line 26), repo-actions (line 29), star-momentum-alert (~line 69, 3 sites). PRs #71 + #67 + #63 + #77 fixed the other four; the remaining three were explicitly flagged as "for future runs."

**minitor** is on the 7th rung of the per-column UX axis (tab groups → collapse → JSON export → quick-search → pin-to-front → duplicate). No open issues. The per-column work has been exclusively view-state and DB-backed logic; the next orthogonal surface is visual organization at the deck level.

---

### 1. `ecosystem-links` skill (aeon)
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** The ECOSYSTEM.md visual catalog now has 30+ entries with GitHub repos, X handles, and project URLs. As the project count grows, dead links and archived repos accumulate silently — ecosystem-pulse measures activity for projects *already known good*, but nothing catches the entries that have gone 404 or abandoned. A weekly link-health auditor closes that gap. Together, the three ecosystem skills form a closed loop: `ecosystem-entrants` (new arrivals) + `ecosystem-pulse` (liveness for known entries) + `ecosystem-links` (URL validity across the full catalog). The first time a merged project's GitHub repo goes archived or their domain lapses, this skill is the signal.

**How:**
1. New `skills/ecosystem-links/SKILL.md` — weekly Monday schedule (e.g. 11:55 UTC, after ecosystem-entrants at 11:45). Parse `docs/ECOSYSTEM.md` to extract all GitHub repo paths (`github.com/{owner}/{repo}`) and project URLs from each row. For each GitHub entry: `gh api repos/{owner}/{repo} --jq '{archived, disabled}'` to detect archived/disabled repos. For non-GitHub URLs: `curl -sI --max-time 10 --location {url} | head -1` to get HTTP status; WebFetch fallback if curl is blocked.
2. Bucket findings: DEAD (HTTP 4xx or 5xx + no redirect chain resolving), ARCHIVED (GitHub `archived: true`), MOVED (redirect to a different domain), OK. Write `memory/topics/ecosystem-links-state.json` keyed by canonical URL.
3. Notify when DEAD or newly-ARCHIVED entries appear. Silent + article-only when all OK. Article written every run for the record.

---

### 2. Atrium catalog watcher (aeon)
**Type:** Integration
**Effort:** Small (hours)
**Impact:** `install-from-atrium` (PR #335) became the third skill install path yesterday. The Atrium catalog at `atriumhermes.tech/.well-known/skills` is now a live upstream source — but the operator has no signal when new packs appear there. A lightweight watcher that diffs the catalog weekly and notifies on new entries closes the feedback loop: when Atrium publishes a new skill pack, the operator sees it the same week rather than discovering it by chance. This is the supply-side complement to `sparkleware-catalog` (which tracks what skills *exist in the framework*) and `skill-update-check` (which tracks version drift for *already-installed* skills).

**How:**
1. New `skills/atrium-catalog-watcher/SKILL.md` — weekly schedule (e.g. Friday 12:00 UTC). Fetch `https://atriumhermes.tech/.well-known/skills` via WebFetch (the install-from-atrium script already uses this endpoint as its source of truth). Parse the JSON response to get a list of skill pack names + versions + category tags.
2. Diff against `memory/topics/atrium-catalog-state.json` (prior snapshot). Surface: new packs (never seen before), updated versions (same name, higher semver), removed packs (were in snapshot, gone now). Write updated snapshot.
3. Notify on new or updated packs. List: pack name, category, version, `install-from-atrium {slug}` install command. Silent + article-only when catalog is unchanged. This gives the operator one-click actionability on each notification line.

---

### 3. mcp-pulse backport (aeon-agent)
**Type:** DX
**Effort:** Small (hours)
**Impact:** The 22nd consecutive same-day-after backport. mcp-pulse is one of two remaining unbackported skills from upstream PR #272 (merged 2026-05-29). It monitors the MCP server ecosystem — npm `@modelcontextprotocol/*` package releases and GitHub repos tagging `modelcontextprotocol` — for new server releases, deprecations, and adoption signals. aeon-agent currently has no signal about the MCP tooling landscape, which matters increasingly as the operator evaluates whether to add MCP servers to the agent's configuration. The backport chain for PR #272 completes at fleet-scorecard (which depends on `memory/instances.json` not yet present on this fork) — mcp-pulse is the last clean one.

**How:**
1. Verbatim copy of `skills/mcp-pulse/SKILL.md` from upstream aaronjmars/aeon (`gh api repos/aaronjmars/aeon/contents/skills/mcp-pulse/SKILL.md`). Add backport-note block at top citing upstream PR #272 + each adaptation.
2. Key adaptations: (a) `./notify` call rewritten as positional `$1` arg style (aeon-agent's root notify reads `MSG="$1"` not `-f file`); (b) WebFetch fallback added for any npm registry calls (sandbox blocks curl to external hosts intermittently).
3. Register in aeon.yml disabled (same schedule as upstream). Add to skills.json (total 99→100, category research or dev depending on upstream classification). First skill to push aeon-agent past 100.

---

### 4. $(date) batch self-fix — 3 remaining sites (aeon-agent)
**Type:** DX
**Effort:** Small (hours)
**Impact:** The `$(date)` shell-substitution anti-pattern has been systematically fixed across four skills (weekly-shiplog PR #63, push-recap PR #67, heartbeat PR #71, repo-pulse PR #77). Three sites remain, explicitly flagged as "for future runs" in PR #71 and PR #77 notes: `repo-article` (line 26 — 7d window used as an API filter), `repo-actions` (line 29 — 14d window as a commits-since filter), `star-momentum-alert` (~line 69 — most complex: `for D in $(seq 13 -1 0); do DATE=$(date ...)` block generating 14 daily timestamps). Each of these runs daily or on even days; every run improvises a date computation in a runner context that blocks `$(...)` shell expansion. The batch fix eliminates that friction in one PR.

**How:**
1. In `skills/repo-article/SKILL.md` line 26: replace `$(date -u -d '7 days ago' ...)` with `${today_minus_7}` (or a literal 7-day-ago UTC date derived from `${today}` using a bash arithmetic offset the runner *does* allow: `date -u -d "${today} -7 days"` pre-computed in the template, or just a hardcoded 7-day-prior in the skill text).
2. In `skills/repo-actions/SKILL.md` line 29: same pattern — replace 14d-ago `$(date)` with `${today_minus_14}`.
3. In `skills/star-momentum-alert/SKILL.md` ~line 69: replace the `for D in $(seq 13 -1 0); do DATE=$(date -u -d "${today} -${D} days" +%Y-%m-%d)` block with a pre-built date array that the skill template injects (or compute each offset as `{today minus D} for D in 0..13` via shell arithmetic that doesn't require `$(date)`).

---

### 5. Column color labels (minitor)
**Type:** Feature
**Effort:** Small (hours)
**Impact:** At 10–15 columns per deck, visual scan time becomes the bottleneck. Operators mentally group columns (DeFi tokens, dev repos, news feeds, social) but have no in-app marker for it — the only grouping affordance is tab groups (which hide/show), while collapse folds a column to 48px. A per-column color label (a hex color swatch visible in both the expanded header and the collapsed strip) lets operators apply a group-level color code at a glance: all DeFi columns orange, all GitHub repos blue, all social columns purple. No new columns to create, no tab to switch — the deck stays as-is but becomes scannable in 200ms rather than 2 seconds. Follows the tab groups → collapse → pin axis: color is the last missing "at-a-glance" layer.

**How:**
1. New migration `drizzle/0008_column_color.sql` — additive `color varchar(7)` nullable column on `columns` (stores 6-char hex e.g. `#f97316`; null = no color = default brand accent). Add field to `lib/db/schema.ts`, `lib/columns/types.ts`, `app/actions.ts` (`updateColumnColor` server action), and export/import/share-link round-trip (same pattern as `pinned` from PR #59).
2. In `components/column/configure-column-dialog.tsx`: add a color picker row — 8 preset swatches (neutral gray + 7 accent colors) plus a hex input for custom values. Save fires `updateColumnColor`.
3. In `components/column/column-card.tsx`: (a) expanded header — render a 10px circular color dot next to the column title if `color` is set; (b) collapsed strip — use `color` as the accent line color at the left edge (replacing the static brand color on the vertical strip). This makes every collapsed column instantly identifiable by color alone without reading the rotated title.
