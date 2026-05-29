# Push Recap — 2026-05-29

## Overview
A heavy day across the three watched repos: 16 substantive commits from 5 authors (aaronjmars, HoundFlow, AntFleet, Noctel, plus ~40 cron auto-commits in aeon-agent). The main thrust: a dashboard editorial overhaul on upstream aeon, 11 brand-new skills added in two contributor bundles (5 generic ops skills + 6 keyless Base onchain investigators), the skill-pack manifest growing two new schema fields (capabilities taxonomy and secrets enumeration), the established same-day-after backport chain stretching to its 16th consecutive day, and minitor shipping per-column tab groups for deck navigation.

**Stats:** ~5,629 added / 444 removed across ~64 files in 16 substantive commits (aeon ~+4197/-388, aeon-agent ~+783/-12, minitor +649/-44).

---

## aaronjmars/aeon

### Dashboard editorial overhaul (PRs #263, #264, #265)
**Summary:** Three sequential merges that take the dashboard from a generic dark UI to a dashboard that reads like the aeon.fun marketing site — same palette, same typography, same editorial vocabulary, same motion library. Each PR layered on the previous: visual tokens → editorial content vocabulary → button normalization + motion components.

**Commits:**
- `913eb9d` — Restyle dashboard to match aeon.fun (+396/-214, 16 files)
  - `dashboard/app/globals.css`: introduces `--aeon-*` design tokens (bg, panel, fg, gray, red `#d24b40`, green, rule). Legacy `--color-eva-*` aliases are remapped instead of renamed so every existing component class (eva-orange, eva-black, etc.) keeps working — bulk-renames avoided entirely. Adds `.dither` (halftone red glow), `.brand-dot` (pulse), `.btn-solid` / `.btn-ghost`, dark card-hst / progress-bar / selected-indicator, dark scrollbar, film-grain overlay. Corner markers and warning stripes were removed — they didn't fit the new vocabulary.
  - `dashboard/app/layout.tsx`: loads Dela Gothic One (display), Inter (body), Space Mono (code/labels).
  - 14 component files (TopBar, LeftSidebar, HQOverview, SkillDetail, SecretsPanel, ScheduleEditor, RightPanel, SpecNode, ImportModal, AuthModal, ErrorScreen, LoadingScreen, page.tsx, utils.ts): bulk swap `bg-white` → `bg-aeon-panel`, `bg-eva-white` → `bg-aeon-bg`, light borders → dark hairlines (`border-2` thinned to `border`), amber/blue alert colors recolored for the dark theme. LoadingScreen and ErrorScreen rewritten around the new brand-dot + dither glow + Dela title.
- `c16a3c2` — Push dashboard restyle to match aeon.fun's editorial voice (+334/-112, 4 files)
  - Each of HQOverview, SkillDetail, SecretsPanel now opens with an editorial hero: dithered red halftone surface + massive Dela Gothic headline (clamped to 110px / 88px) + coral accent word + red-dash eyebrow + body dek.
  - HQOverview: oversized Dela stat counters, numbered editorial sections ("01 / Departments", "02 / Recent activity"), department cards with the spotlight cursor effect ported from the marketing site's skills grid, bottom marquee band ("AEON HQ ★ N ON DUTY ★ …").
  - SkillDetail: same numbered scheme (01 Shift / 02 Brief / 03 Capability / 04 Activity), btn-solid / btn-ghost actions, big Dela display values for schedule and brief, styled empty state instead of the prior "No activity" line.
  - SecretsPanel: hero + numbered groups ("01 / Core", "02 / Telegram", …) with per-group "set / total" counters.
- `d1d748` — Normalise TopBar button sizes; port aeon.fun motion (+392/-32, 6 files)
  - TopBar: every action (Auth, model select, + Hire, GitHub, Pull, Push) is now a uniform 32px height with consistent uppercase labels. Auth uses `.btn-solid-sm`, + Hire uses `.btn-ghost-sm`, GitHub/Pull/Push use `.btn-quiet`. Replaces the prior mismatched mix (btn-solid 10px pad vs px-3 py-2) that had AUTH towering over PULL/PUSH.
  - **New file** `dashboard/components/ui/Animated.tsx` (+271): three motion components ported wholesale from aeon.fun — `Scramble` (headline letters decode from random glyphs, ~440ms settle, wired into "AEON HQ" / "ACCESS KEYS" / skill-name heroes), `Flip` (odometer reel that rolls digits up when scrolled into view, wired into HQ stat strip + per-department team-size counters), `VelocityMarquee` (scroll-velocity boosted marquee, replaces the CSS-only `aeon-marquee` on the HQ bottom band).
  - `globals.css`: smoother button transitions (translateY-2px lift + coral box-shadow on hover for solid; -2px ghost; -1px quiet), unified cubic-bezier(0.2, 0.8, 0.2, 1) base transition on every interactive surface — the same ease the marketing site uses.

**Impact:** The dashboard now visually belongs to the same product as the marketing site instead of looking like a separate internal tool. Every interactive surface picks up the marketing site's motion grammar — Scramble titles, Flip counters, marquee bands — so operator workflows feel like they're inside the brand, not adjacent to it.

### New skill capacity (PRs #269, #271, #272)
**Summary:** Eleven new skills in two contributor bundles plus one operator-authored synthesis skill — the biggest single-day skill-set growth in the recap window. All registered `enabled: false` (the framework's standard ship convention) so they don't fire until an operator opts in.

**Commits:**
- `d601799` — Add 5 general-purpose ops skills, generalize fleet-scorecard (+1156/-2, 9 files; #272)
  - 5 new SKILL.md files under `skills/`: `spend-monitor/` (daily API spend watchdog vs `WEEKLY_BUDGET_CAP` default $200; OK/WATCH/WARN/ALERT tiers, silent under 50% — daily complement to weekly cost-report), `follow-up-patrol/` (weekly escalation audit of MEMORY.md follow-ups + issue tracker; ages items, alerts on CRITICAL/HIGH; falls back to "## Next Priorities" when "## Known Follow-ups" is absent), `narrative-convergence/` (daily cross-skill convergence detector with operator-editable category map at `memory/topics/signal-categories.md`), `mcp-pulse/` (weekly MCP ecosystem tracker — servers, npm/GitHub adoption, protocol evolution; pairs with x402-monitor), and a generalized `fleet-scorecard/` (the fleet is now discovered at runtime from `memory/instances.json` + self, no hardcoded repos).
  - **New file** `scripts/prefetch-fleet-scorecard.sh` (+226): generalized prefetch with no instance-specific assumptions; replaces the prior aeon-aaron-only version.
  - `aeon.yml` (+5), `generate-skills-json` (+3), `skills.json` (+62/-2 → total 159 → 164 via textual splice so the generated manifest's existing entries stay byte-identical).
  - Operator-voice gating is checked against `soul/` presence; no hardcoded repo links, no instance-specific examples or backstory — these are framework-level skills.
- `4e7c6c8` — feat(skills): add Hound onchain investigation skills (+693/-1, 9 files; #269)
  - 6 new SKILL.md files contributed by HoundFlow filling the security/forensics gap in the current crypto skill set (which had been monitoring/market only): `rug-scan/` (rug-pull risk verdict for a token, +119), `contract-audit/` (ownership/proxy/mint/freeze/drain capability matrix, +108), `wallet-profile/` (behavioral profile, funding source, risk flags, +99), `deployer-trace/` (every contract from a deployer + serial-rug detection, +90), `tx-explain/` (plain-English transaction decode + approval flags, +92), `holder-concentration/` (distribution, HHI, LP/lock exclusions, whale clusters, +103).
  - **All run keyless** on public endpoints (Etherscan v2 unified `chainid=8453` + Base RPC). Optional `ETHERSCAN_API_KEY` only raises the rate limit — does not unlock functionality. Means zero-secret install for new operators.
  - `aeon.yml` (+8), `generate-skills-json` (+1), `skills.json` (+73/-1 → 6 appended entries).
- `691fb5e` — feat(fork-health-score): add per-fork health-tier skill (+380/-1, 3 files; #271)
  - **New file** `skills/fork-health-score/SKILL.md` (+366): synthesizes push recency + enabled-skill count + 30d PR throughput into a single per-fork tier (ACTIVE/WARM/STALE/QUIET) plus a top-10 ACTIVE leaderboard and one "X of N forks are ACTIVE" fleet number.
  - Scoring weight: push 50% / skills 30% / PRs 20%, plus a **hard floor of ≥2 enabled skills** for ACTIVE so a high-push-recency-low-config placeholder fork cannot claim the tier on score alone.
  - All WoW deltas are computed on percentage points, not raw counts — denominator drift (forks activating/deactivating) cannot manufacture phantom movement.
  - Pairs with the Sunday fleet stack (fork-cohort 19:00, fork-skill-gap 21:00, fleet-skill-adoption 22:00) as the Monday-morning synthesis view at 10:45 UTC. Reuses `fork-cohort-state.json` when fresh (≤8d); live-API fallback otherwise. Hard 80-fork cap, bot allowlist filtered before scoring.
  - **Read-only** across the fleet — never opens PRs, never comments, never edits fork files. `aeon.yml` (+1) registers disabled; `skills.json` (+13/-1) totals 159 → 160.

**Impact:** The skill catalog jumped from 158 to 164 in upstream aeon in one day — a 4% catalog growth. The Hound bundle is the first contributor pack landing keyless-by-default onchain forensics; the ops bundle gives operators visibility into spend / follow-ups / cross-skill convergence / MCP ecosystem that the framework previously didn't have. fork-health-score is the synthesis layer that turns the existing Sunday fleet stack into a single Monday "fleet health" number.

### Skill-pack manifest maturation (PRs #267, #268)
**Summary:** Two AntFleet PRs add the two manifest fields that the skill-pack ecosystem needed before it can scale — capabilities (what side effects a skill has) and required secrets (what env vars a skill cannot run without). Both are additive schema changes: existing packs without the fields keep working.

**Commits:**
- `c87405f` — feat(skill-packs): add capabilities array with locked taxonomy (+202/-5, 3 files; #268)
  - **New file** `docs/CAPABILITIES.md` (+96): defines the locked six-value taxonomy — `read_only` · `external_api` · `writes_external_host` · `onchain_writes` · `agent_messaging` · `sends_notifications`.
  - `install-skill-pack` (+100/-3): new `ALLOWED_CAPABILITIES` constant mirroring the taxonomy. Validation is strict allow-list — `skills[].capabilities` is type-checked as array (or absent); non-array shapes abort with a `docs/CAPABILITIES.md` pointer instead of an opaque jq error. Each element iterated as `"(type) (.)"` so element boundaries survive (word-splitting on a joined string would silently swallow whitespace-bearing or empty entries). Element kind must be string; numbers, booleans, nested arrays are rejected with the same pointer. Element value must match one of the six taxonomy values exactly (case-sensitive). Validation fires **before any install action** — an invalid capability on one skill aborts the whole pack install.
  - Pack-level `capabilities[]` in `skill-packs.json` is discovery-only metadata — `./install-skill-pack --list` annotates each pack with `[caps: …]`, validates each entry against the same taxonomy at print time so registry drift surfaces in the listing, and refuses to print unknown values.
  - `docs/community-skill-packs.md` (+6/-2): field-reference rows for both schemas. Implements priority (1) from #258 (the third and final PR in that thread).
- `05c9cd0` — feat(skill-packs): add secrets_required / secrets_optional manifest fields (+100/-12, 2 files; #267)
  - Per-skill: `secrets_required: string[]` (env vars the skill cannot run without) + `secrets_optional: string[]` (env vars that tune behaviour). Pack-level: `secrets_required: string[]` aggregated across the pack, drives the new `--no-secrets` registry filter.
  - `install-skill-pack` (+92/-10): after the security scan clears and before each file copy, surfaces missing required secrets with one warn line per skill plus the "set this in `secrets:` of your workflow before the first scheduled run" hint. **Loud warning, no gate** — operator may install dry-run and wire the secret afterward. `--list --no-secrets` hides registry packs with non-empty `secrets_required`; `--list` without the flag continues to show every pack and now annotates `[needs N secret(s)]`.
  - Implements priority (2) from #258.

**Impact:** Together, these two fields make the skill-pack registry self-describing along the two axes that matter for trust and install-time UX — what does this skill do to the outside world, and what does it need from me before it can run? `./install-skill-pack --list` becomes a triage surface: operators can see at a glance which packs touch the chain, which call external APIs, and which need secrets they haven't wired yet.

### Skill-PR triage receipt (PR #259)
**Summary:** A new workflow_dispatch-only skill that turns the ~10-minute manual review of an inbound skill PR into a ~10-second human merge decision by posting a structured triage comment on the PR.

**Commits:**
- `35eca00` — feat: pr-skill-triage skill (+310/-1, 3 files; #259)
  - **New file** `skills/pr-skill-triage/SKILL.md` (+296): fans out `skills/skill-security-scan/scan.sh` verbatim across every SKILL.md in the PR diff (no forked patterns) for a PASS/WARN/BLOCK verdict + first-3 HIGH findings. Enumerates required secrets by extracting `$VAR` patterns and dropping the known-safe set. Checks cron slot conflicts vs existing `aeon.yml` schedules: exact match = CONFLICT, ±5min same DoW = ADJACENT, workflow_dispatch = OK. Gathers quality signals: description ≥40 chars, ≥3 steps, `./notify` call present, tags non-empty.
  - Verdict precedence: **BLOCK** (HIGH finding or hard cron conflict) > **WARN** (MEDIUM, missing fields, adjacent slot, or required secrets) > **OK**. Operator decides the merge — skill never auto-merges, never adds labels, never invokes the Reviews API.
  - **Dedup on (PR, head_sha)**: re-dispatch on the same head is a no-op, so the skill cannot storm a PR. Fallback artifact path `articles/pr-skill-triage-{N}-{today}.md` if `gh pr comment` fails so the operator can paste manually. Two external skill PRs are open right now (#231 liquidpad-launch from liquidpadbot, #241 signa-skills from codexvritra with 10 skills) — the receipt is built for them.
  - Separated from the existing general `pr-triage` so most PRs (no SKILL.md change) don't pay the scan cost.
  - `aeon.yml` (+1), `skills.json` (+13/-1 → 158 → 159, category dev).

**Impact:** Closes the structural gap in the contributor-PR pipeline: the security scan, the secrets enumeration, and the slot-conflict check were all already possible by hand, but no skill collated them onto the PR comment thread itself. Now they do, and the dedup contract means the receipt can't become noise.

### External-contributor enablement (PR #260)
**Summary:** Two prefetch/postprocess shims that move the sandbox-blocked authenticated calls out of skill bodies (which external contributors cannot land — sandbox boundary forbids secret-scope shell access in skills/) and into the workflow's prefetch/postprocess slots.

**Commits:**
- `a0a542e` — feat(scripts): land liquidpad prefetch + postprocess shims for #231 (+225/-0, 2 files; #260)
  - **New file** `scripts/prefetch-liquidpad.sh` (+113): authed reads (concept, agent-status) → `.liquidpad-cache/`. Runs before Claude with full env access, leaves cached JSON the skill can read.
  - **New file** `scripts/postprocess-liquidpad.sh` (+112): authed writes from `.pending-liquidpad/*.json` → POSTs, results to `.liquidpad-cache/<id>.result.json`. Payload validation (name/symbol/0x ownerAddress), 401/403 stop-line, 429 leave-for-next-run, `LIQUIDPAD_DRY_RUN=1` quarantine. Both no-op cleanly when `LIQUIDPAD_API_KEY` is unset.
  - **Unblocks #231**: the skill body + `skills.json` entry from liquidpadbot can now land standalone once they rebase against this commit — the auth-scoped code is already in `scripts/` (operator-landed), so the skill PR no longer needs to.

**Impact:** Same pattern aeon already uses for prefetch-xai / postprocess-replicate, now extended for liquidpad. Removes one of the two structural blockers on PR #231 — the other is the skill body itself, which can now be landed by an outside contributor without touching `scripts/`.

### Default-model bump + ECOSYSTEM growth (PRs #261, #262)
**Summary:** Two small housekeeping PRs.

**Commits:**
- `f3c260c` — chore: bump default model to claude-opus-4-8 (+8/-8, 5 files; #262) — `aeon.yml`, `.github/workflows/aeon.yml`, `.github/workflows/messages.yml`, `dashboard/lib/constants.ts`, `README.md` all advertise opus-4-8 as the top-level default + workflow-dispatch dropdown + messages-handler fallback + dashboard header option + README snippet. cost-report pricing tables and skill prose that reference opus-4-7 as historical context are left unchanged.
- `b29f275` — Add Noctel to ECOSYSTEM.md (+1/-0; #261) — one-line addition to the ecosystem list by Noctel.

**Impact:** Model bump is mechanical (text replace in five places), but it's the kind of change the dashboard model-select dropdown and the workflow_dispatch UI surface immediately. Noctel entry is the latest external project to claim a row in ECOSYSTEM.md — the read-only weekly `ecosystem-pulse` skill (May-24 backport here) will pick it up on the next Monday run.

---

## aaronjmars/aeon-agent

### Backport chain stretches to 16 days
**Summary:** Two backports landed on the established same-day-after cadence. The pr-skill-triage backport (May-29) is the 16th consecutive day this fork has shipped a verbatim backport of an upstream merge from the previous day; the sparkleware-catalog backport (May-28) was the 15th.

**Commits:**
- `dc504a4` — feat(pr-skill-triage): backport upstream aeon PR #259 (+323/-1, 3 files; #68)
  - **New file** `skills/pr-skill-triage/SKILL.md` (+311): verbatim copy of upstream pr-skill-triage with all `aaronjmars/aeon` references rewritten to `aaronjmars/aeon-agent` (gh api paths, gh pr comment invocations, exit-status descriptions, notify message PR URL).
  - `./notify` single-positional-arg call style was already aligned (no adaptation needed). `skills/skill-security-scan/scan.sh` shape matches upstream — May-18 PR #186 (Bash 3.2 + array-emptiness) and May-20 PR #197 (POSIX-ERE) hardening are intact, fork-local "upstream aeon AntFleet finding H6" comment preserved. `yq` fallback path (`grep -E` parse on `aeon.yml`) preserved as-is.
  - `aeon.yml` (+1) registers disabled, workflow_dispatch only, between pr-review and auto-merge (same neighbourhood as upstream). `skills.json` (+11/-1 → 94 → 95, alphabetical insert between pr-review and pr-triage).
- `ad2c4da` — feat: backport sparkleware-catalog skill from upstream aeon PR #252 (+300/-1, 3 files; #66)
  - **New file** `skills/sparkleware-catalog/SKILL.md` (+288): weekly enriched export of `skill-packs.json` that joins the curated registry to live GitHub signals (stars, last-push, live `skills-pack.json` manifest skill count) → machine-readable `skill-packs-catalog.json` at the repo root for external tools like Sparkleware (Issue #244) to consume without screen-scraping.
  - **Zero adaptation needed**: `./notify` arg style, output paths (`skill-packs-catalog.json` at root, `dashboard/outputs/` reserved for json-render specs), and `gh api` access pattern (no curl + env-var headers) all already match aeon-agent conventions. `skill-packs.json` was backported on May-24 (PR #59) so the input source is in place.
  - `aeon.yml` (+1) registers disabled, Tuesday 09:00 UTC schedule (matches upstream slot — first quiet weekday after the Monday intelligence stack). `skills.json` (+11/-1 → 93 → 94, category dev).

**Impact:** The backport chain is now a load-bearing operational pattern — 16 consecutive days of "upstream merge today, fork backport tomorrow." Operators of this fork get the same skill capabilities as upstream with a 24-hour lag, automatically.

### Self-fix on push-recap (PR #67)
**Summary:** This very skill (push-recap) fixed itself yesterday. The fix landed this morning and is — as far as I can tell — the reason this recap is using the literal `since=2026-05-28T00:00:00Z` instead of improvising the cutoff by hand.

**Commits:**
- `6174e20` — improve: drop $(date ...) shell expansion from push-recap step 2 (+160/-10, 6 files; #67)
  - `skills/push-recap/SKILL.md` (+7/-4): step 2 used `since="$(date -u -d '24 hours ago' …)"` to bound the commits API fetch, but the runner hook blocks shell command/variable expansion ("Contains simple_expansion"). The skill had been improvising the cutoff by hand on every recent run — explicit "Avoided $(date …) (runner shell-guard)" notes in the 2026-05-26 and 2026-05-27 push-recap logs, and a `for`+xargs variant on 2026-05-25. Replaced with a literal `since=YYYY-MM-DDT00:00:00Z` computed from `${today}` minus 24h — same fix PR #63 applied to weekly-shiplog. Inline citation of PR #63 so a future cleanup doesn't reintroduce the shell substitution. Step 1 also now documents the `(.payload.commits // [])` null-guard that push-recap had been adding by hand on every recent run for squash-merged pushes' empty-array case.
  - Memory, log, output, token-usage CSV: the routine self-improve trailing-side-effect commits.

**Impact:** Today's run (this one) is the first that didn't need the operator to think about the cutoff date or the null-guard. Two recurring workarounds in the daily log just stopped recurring.

### Cron auto-commit noise
**Summary:** ~40 `chore(cron): … success`, `chore(<skill>): auto-commit …`, and `chore(scheduler): update cron state` commits from `aeonframework` across the 24h window. These are scheduler heartbeats and per-skill state writes — no semantic content, not counted in the totals above.

---

## aaronjmars/minitor

### Per-column tab groups (PR #53)
**Summary:** Decks with 8+ columns become navigation-heavy. Tab groups let operators partition a deck into labeled sections (e.g. "DeFi", "Social", "Dev") without splitting into separate decks. Built entirely on top of the existing column infrastructure — no plugin schemas touched, so every existing plugin keeps working with zero changes.

**Commits:**
- `6954bf8` — feat(columns): per-column tab groups + tab bar above the deck grid (+649/-44, 10 files; #53)
  - **Schema**: `drizzle/0006_tab_groups.sql` (+1) adds nullable `tab_group` text column on `columns`; `drizzle/meta/_journal.json` (+7) bumps to entry 6; `drizzle/meta/0006_snapshot.json` (+352) is the post-migration snapshot. **Migration 0006, not 0007** — 0005 was deck_snapshots on May-27 and no migration landed between.
  - `lib/db/schema.ts` (+1) + `lib/columns/types.ts` (+9): `Column.tabGroup?: string` threaded through schema + Column shape.
  - `app/actions.ts` (+44): `TAB_GROUP_MAX = 50` const, `updateColumnTabGroup` server action with whitespace collapse + trim + length cap, Zod field on `importedColumnSchema`, `exportDeck` round-trip, `importDeck` re-normalization on import (so a hand-edited payload can't smuggle `"  AI  "` and `"AI"` as two distinct buckets past the server-side guard), `loadSnapshot` read.
  - `lib/store/use-deck-store.ts` (+43): `updateTabGroup` mirror action with identical normalization (optimistic state cannot drift from server normalization), `selectedTabByDeck` per-deck view state **deliberately NOT persisted** (clears on reload, restores on deck-switch within the same session — same shape as `autoFetchingIds`), `TAB_GROUP_ALL = "__all__"` sentinel exported so two files don't re-derive the string.
  - `components/column/configure-column-dialog.tsx` (+39/-1): "Tab group" text input under the show-only/hide section, LayoutGrid icon.
  - `components/deck/deck-board.tsx` (+148/-43, full rewrite of the grid): tab bar above the grid when ≥1 column has a group, derived in column-position order so the operator's column reorder is the visual tab order; per-tab badge with column count; useEffect-driven fallback to All when the selected tab's last column moves away.
  - `lib/deck-templates.ts` (+5): `DeckTemplateColumn.tabGroup?: string` so future multi-category starter decks can ship pre-grouped.

  **Key UX decision: untagged columns ride along with every named tab.** A half-grouped deck (e.g. 2 labeled "DeFi" + 6 unlabeled) stays usable instead of going blank when "DeFi" is clicked — otherwise the feature reads as broken on first use. An implicit "All" tab always shows everything.

**Impact:** Deck navigation scales past the horizontal-scroll point. With 47 plugins now in the registry, an operator running a 12-column deck mixing crypto + social + dev signals can now scope to one workstream at a time without losing the others — and the rest of the deck stays one tab-click away.

---

## Developer Notes
- **New dependencies:** none. Every new file is plain TypeScript / SQL / Bash / Markdown built on existing libraries.
- **New schema:** minitor migration `0006_tab_groups` (additive, nullable column).
- **Breaking changes:** none. Skill-pack capabilities + secrets fields are additive — existing packs without them keep working. Aeon framework's TopBar button class rewrite is internal; user-facing labels unchanged.
- **Architecture shifts:**
  - aeon dashboard now has a dedicated motion-component file (`dashboard/components/ui/Animated.tsx`) — first time the dashboard imports framer-motion-style behavior from the marketing site.
  - aeon `fleet-scorecard` lost its instance-specific assumptions; the fleet is now runtime-discoverable via `memory/instances.json` + self, which makes the skill portable across forks (no hardcoded repos).
  - aeon skill-pack manifest grew two new optional fields (`capabilities`, `secrets_required`/`secrets_optional`) — the registry is now self-describing along trust and install-UX axes.
- **Tech debt closed:** push-recap (aeon-agent) no longer needs hand-improvised cutoff dates on every run (PR #67). The "Avoided $(date …) (runner shell-guard)" recurring log line is gone.
- **Tech debt opened:** the new fork-health-score skill assumes `fork-cohort-state.json` is fresh ≤8d — if Sunday's fork-cohort run fails twice, fork-health-score Monday goes to live-API mode (still functional, just slower).

## What's Next
- **Two external skill PRs are open and now triage-ready:** #231 (liquidpad-launch from liquidpadbot, now unblocked by today's `a0a542e` shim landing) and #241 (signa-skills, 10 skills from codexvritra). The pr-skill-triage skill landed today (#259); next dispatch on either PR should post the first real triage receipt to a contributor.
- **fork-health-score's first dispatch** is the next Monday at 10:45 UTC (2026-06-01) — first "X of N forks are ACTIVE" number arrives then.
- **Dashboard editorial overhaul is complete on the three top-level surfaces** (HQOverview, SkillDetail, SecretsPanel). RightPanel, ScheduleEditor, SpecNode received only the palette swap — not the editorial heroes. If the editorial vocabulary continues, those are the next candidates.
- **Open branches not merged** in aeon during the window: `add-generic-ops-skills` (the branch behind #272), `land-noelclaw`, `feat/dashboard-motion`, `feat/dashboard-editorial`, `feat/dashboard-restyle` (the dashboard PRs' source branches, now merged). In aeon-agent: `improve/push-recap-since-literal` (the source branch of #67, merged). No long-lived feature branches visible at end of window.
- **Backport chain at 16 consecutive days.** Tomorrow's candidate is upstream aeon PR #272 (5 ops skills) or #269 (Hound onchain) or #271 (fork-health-score) — three substantial backport candidates landed today. Operator decision is which (or how many) to bring across.
