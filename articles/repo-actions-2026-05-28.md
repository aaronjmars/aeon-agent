# Repo Action Ideas — 2026-05-28

**Repos analyzed:** aaronjmars/aeon (456⭐, 132 forks, 2 open issues, 1 open PR), aaronjmars/aeon-agent (9⭐, 1 fork, 0 open issues), aaronjmars/minitor (11⭐, 1 fork, 0 open issues)

**Context:** Community skill pack registry now has 16 packs / 49+ installable skills; open issue #258 proposes manifest-level capability declarations before the registry grows further. aeon-agent has ECOSYSTEM.md (added via PR #62 May-26) but not the ecosystem-pulse skill that monitors it. minitor is at 49 column types with a clean PR queue — next natural step is structural navigation for large decks or closing the Web3 social set with Farcaster.

---

### 1. capabilities + secrets_required fields in skill-packs.json (aeon)
**Type:** Feature
**Effort:** Small (hours)
**Impact:** Operators know before installing whether a pack requires secrets they haven't configured. Right now 16 packs are listed with only a `trust_level` signal. With install-skill-pack scanning skills' `$VAR` patterns, it's possible to auto-populate `secrets_required` from existing SKILL.md files and surface the list in `--list` output and at install time. Prevents silent-fail installs for operators missing XAI_API_KEY, TELEGRAM_BOT_TOKEN, etc. Directly addresses open issue #258.
**How:**
1. Add optional `capabilities: []` (array of freeform strings like `"web-search"`, `"github-api"`) and `secrets_required: []` (array of env var names) to the `skill-packs.json` schema for each pack entry.
2. Update `install-skill-pack --list` output to display secrets_required inline; add a pre-install secrets check that warns when a required var is unset in the current environment (non-blocking; operator confirms or aborts).
3. For the 5 seed packs already in the registry, back-fill `secrets_required` by extracting `$VAR` patterns from each pack's live `skills-pack.json` manifest skill files (same pattern `skills/skill-security-scan/scan.sh` uses for exfil detection).

---

### 2. ecosystem-pulse backport (aeon-agent)
**Type:** DX
**Effort:** Small (hours)
**Impact:** aeon-agent gained ECOSYSTEM.md in PR #62 (May-26) but never got the skill that monitors the projects listed there. The upstream ecosystem-pulse skill (aeon PR #227, merged May-25) does exactly that: weekly liveness check bucketing 40 projects by ACTIVE/RECENT/COLD/X-only/Unresolved, surfacing releases in the 7d window, WoW transitions + new entrants. Extending the 15-backport cadence with its natural 16th entry.
**How:**
1. Verbatim copy of `skills/ecosystem-pulse/SKILL.md` from upstream `aaronjmars/aeon` main branch (adapt `./notify` call style if needed — upstream and aeon-agent are already aligned on single-positional-arg style per prior backport notes, so no adaptation expected).
2. Register disabled (`enabled: false`, `schedule: "0 11 * * 1"`) in `aeon.yml` and add an entry to `skills.json` (total 94→95, category dev).
3. Open PR against aeon-agent main; backport note cites upstream PR #227 and lists any adaptations made.

---

### 3. fork-health-score skill (aeon)
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** With 132 forks, the fleet visibility stack currently has fork-cohort (who forked), fork-skill-gap (which skills are missing), fleet-skill-adoption (which skills are enabled fleet-wide), and contributor-spotlight (who contributed back). What's missing: a single per-fork health tier that synthesizes push recency + skill count + PR activity into a ranked list. Operators and investors looking at the repo can see "X of 132 forks are ACTIVE" as a single number. Pairs naturally with the `fleet-skill-adoption` leaderboard already built.
**How:**
1. Read the fork list via `gh api repos/aaronjmars/aeon/forks --jq` (paginated); for each fork fetch: last push date, enabled skill count from their `aeon.yml`, and count of PRs merged in the last 30 days against the fork's own main branch.
2. Bucket each fork: ACTIVE (push ≤7d + ≥2 enabled skills), WARM (push ≤30d OR ≥1 skill), STALE (push >30d, 0 skills), QUIET (no push data / empty fork). Compute fleet health ratio: ACTIVE÷total.
3. Write a weekly article with a top-10 ACTIVE forks table and the fleet health ratio; notify only if ACTIVE% drops more than 10 points week-over-week. Register as disabled, Monday schedule (pairs with operator-scorecard / fleet-skill-adoption slot).

---

### 4. Farcaster cast feed column — 50th column type (minitor)
**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** Minitor's social coverage is X (existing) + Reddit (existing) + Bluesky (existing). Farcaster (via Neynar's free public feed API) closes the Web3 social set and crosses the 50-column milestone — a clean number worth noting in the gallery. The Neynar `/v2/feed/channel` and `/v2/feed/user` endpoints are public-readable without an API key for basic data, matching the keyless pattern of the RSS, GitHub, and DeFiLlama columns.
**How:**
1. New plugin at `lib/columns/plugins/farcaster/{plugin,server}.ts` following the established pattern. Server fetches from `https://api.neynar.com/v2/feed/channel?channel_id={id}` or `/v2/feed/user?fid={fid}`; parses `cast` objects into `{id, url, text, author, timestamp, likes, recasts}` column items.
2. Register in `lib/columns/manifest.ts` with `typeId: "farcaster"`, `label: "Farcaster"`, brand accent `#855DCD` (Farcaster purple). Config schema: `channelId?: string`, `fid?: number`, `mode: "channel" | "user"`.
3. Add a starter "Farcaster" template to `lib/deck-templates.ts`; bump README column count to 50.

---

### 5. Column tab groups (minitor)
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Decks with 8+ columns require horizontal scrolling to navigate. Tab groups let operators partition a deck into labeled sections (e.g., "DeFi", "Social", "Dev") without splitting into separate decks. Uses the existing column infrastructure without touching any plugin schemas. Enables the gallery to offer more opinionated multi-category starter decks (which currently have to be flat).
**How:**
1. New optional `tabGroup?: string` field on column rows. New migration (`drizzle/000N_tab_groups.sql`) adding a nullable `tab_group` text column to `columns`; journal + snapshot. Wire through schema.ts, types.ts, actions.ts (updateColumnTabGroup server action with max-50-char validation; export/import round-trip; loadSnapshot support).
2. When any column in the active deck has a `tabGroup`, render a tab bar above the column grid. Clicking a tab filters visible columns to those sharing that group (untagged columns appear under an implicit "All" tab). Store selected tab in `use-deck-store` (not persisted — resets on reload, same as any view-state).
3. Add "Tab group" text input to the configure-column dialog (shown always; blank = no group). Update `lib/deck-templates.ts` to allow `tabGroup` on template columns so future starter decks can ship pre-grouped.
