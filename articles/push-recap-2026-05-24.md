# Push Recap — 2026-05-24

## Overview
Heaviest push day in recent memory across the three watched repos. The upstream `aeon` catalog absorbed 34 skills back from derivative instances (155-skill catalog now), a new `ECOSYSTEM.md` registry split products-built-on-Aeon from forks and skill packs, and the AntFleet two-model bench review (claude-opus-4-7 + gpt-5 unanimous) filed three security/correctness fixes in a single 60-second burst. Aeon's own feature + self-improve runs opened four more PRs — one closing the last open AntFleet High on `v4-readiness`, one a same-day-after backport, one a self-corrective response to today's own XAI 403 outage, one shipping minitor's last open May-22 idea. 12 substantive PRs total (4 merged inside window, 8 newly opened), ~8,260 lines added across ~70 files, 6 distinct authors.

**Window:** 2026-05-23 ~15:22 UTC → 2026-05-24 ~15:21 UTC
**Stats:** ~8,262 / -108 lines across ~70 files in 12 substantive PRs (excludes ~22 cron auto-commits + ~10 scheduler-state pushes on `aeon-agent/main`)

---

## aaronjmars/aeon — 7 substantive PRs (3 merged, 1 already-covered merge, 5 opened)

### Theme 1: Skill catalog explosion — framework crosses 155 skills, gets two new registries

Four PRs in a single evening reshape `aeon` from "agent framework with one community-pack table" into a multi-surface ecosystem hub. The four merged in sequence between 17:09 and 18:37 UTC on May 23.

**Summary:** `skill-packs.json` (machine-readable pack registry, merged 17:09), `community-packs/bundle` (4 community packs listed in README, merged 17:29), `Port 34 skills` (skills back-ported from derivative aeon instances, merged 18:30), `ECOSYSTEM.md` (new file separating products built on Aeon from forks + skill packs, merged 18:37). After this hour the catalog goes from 121 → 155 skills, the pack registry goes from 5 → 9 packs visible from `./install-skill-pack --list`, and there's a third registry surface (ECOSYSTEM.md) for products that *use* Aeon without being forks.

**Commits:**

- `ac43d46` — *feat: machine-readable skill-packs.json registry + --list browsing (#215)*
  - Already covered in yesterday's recap as "Community Skill Pack ecosystem" theme. Merged into `main` 17:09 UTC inside today's window; no new substance to add. See [push-recap-2026-05-23.md](push-recap-2026-05-23.md).

- `0eed836` — *docs(community-packs): list zer0, gitbounty, AntFleet, LiquidPad (#218)* (+20/-0, 2 files)
  - Modified `README.md` (+4): four new rows in the Community Skill Packs table.
  - Modified `skill-packs.json` (+16): one new entry for `liquidpadbot/aeon-skill-pack-liquidpad` (LiquidPad's Base launch tracker, 4 skills). The other three (zer0, gitbounty, AntFleet) were already seeded in PR #215's initial registry, so this only adds LiquidPad to keep README and `--list` in lockstep.
  - Bundles four separate-row-conflict PRs (#208 0xShak zer0, #212 gitlawbounty gitbounty, #216 antfleet-ops AntFleet, #217 liquidpadbot LiquidPad) so each later contributor doesn't have to rebase. All four source PRs closed pointing at this commit. Co-authored credit preserved per contributor.

- `114d430` — *Port 34 skills from derivative aeon instances (#219)* (+6,162/-69, 36 files)
  - The big one. Pulls skills that grew up in private/derivative aeon instances (`aeon-aaron`, `aeon-agent`, `miroshark-aeon`) back into upstream, genericized for any operator.
  - **ADD (11 skills, light cleanup only):** `build-skill` (later dropped — duplicate of `create-skill`), `auto-merge-agent-prs` (later dropped — merged into `auto-merge`), `batch-health`, `config-validator`, `janitor`, `memory-flush`, `memory-structural-dedupe`, `milestone-tracker`, `self-review`, `skill-enabler`, `engagement-act`.
  - **ADAPT (26 skills, persona stripped):** `agent-displacement`, `builder-map`, `compute-pulse`, `disclosure-tracker`, `idea-pipeline`, `idea-validator`, `launch-radar`, `note-taking`, `pm-intel`, `pm-manipulation`, `pm-pulse`, `pr-tracker`, `pvr-triage-monitor`, `pvr-watchlist`, `rwa-pulse`, `repo-revive`, `polymarket`, `trending-coins` (later dropped — duplicate of `token-movers`), `x402-monitor`, `wallet-digest`, `tweet-digest`, `run-frequency-guard`, `signal-verdict`, `topic-momentum`, `vuln-tracker`, `feature`.
  - **Adaptation pattern:** hardcoded handles/repos/tokens/topics replaced with reads from `memory/topics/*.md` or `aeon.yml`; soul/SOUL.md + soul/STYLE.md neutral fallback for voice; dated incident references genericized.
  - **SKIPPED (4):** `thread-writer`, `weekly-newsletter`, `ragebait-tweet`, `picks-tracker` — don't survive without the operator persona/portfolio.
  - **Post-port audit dropped 3 duplicates** in a follow-on commit: `build-skill` (subset of `create-skill`), `trending-coins` (subset of `token-movers`), `auto-merge-agent-prs` (~80% overlap with `auto-merge`). The retry-cap logic from `auto-merge-agent-prs` got merged into `auto-merge` (per-PR retry-state in `memory/topics/auto-merge-state.json`, 3-attempt cap, retry-cap notification, Trusted Authors pattern documented for closing agent-authored PR loops).
  - **Positioning notes** for skills that complement existing aeon ones: `polymarket` = global trending vs. `monitor-polymarket` = watchlist; `wallet-digest` = lite balance vs. `on-chain-monitor` = full decode; `tweet-digest` = account-based vs. `fetch-tweets` = keyword vs. `tweet-roundup` = topic; `feature` = all watched repos vs. `external-feature` = single repo; `vuln-tracker` = status tracker paired with `vuln-scanner`.
  - **`auto-merge` SKILL.md** modified +57/-7 — net of the retry-cap merge from the dropped `auto-merge-agent-prs`.
  - `skills.json` regenerated via `./generate-skills-json` — final count 155 entries (+34 net).

- `d72ace6` — *Add ECOSYSTEM.md listing projects built on Aeon (#220)* (+73/-1, 2 files)
  - New `ECOSYSTEM.md` (+72): 39-project alphabetized table with X handles. Distinct from the two existing registries by purpose:
    - **SHOWCASE.md** = active forks running stock skills (operators).
    - **README.md Community Skill Packs table + `skill-packs.json`** = installable skill bundles authored against Aeon (pack authors).
    - **ECOSYSTEM.md** = products *using* Aeon at the framework level, not forks (builders).
  - The contributor section explicitly names the three-way distinction and provides a row-template for pull requests.
  - `README.md` (+1/-1): one-line addition linking ECOSYSTEM.md alongside the existing SHOWCASE.md reference.
  - **Impact:** First public surface where projects that *use* Aeon (vs. fork it or write skill packs for it) are countable in one place. LiquidPadbot's PR #225 (opened ~11 hours later) is the first community-authored row addition.

**Impact:** Single evening transformed `aeon` from a single-registry framework into a three-registry ecosystem hub: who runs Aeon (SHOWCASE), who packs skills for Aeon (Community Skill Packs / skill-packs.json), who builds products on Aeon (ECOSYSTEM.md). The 34-skill back-port closes the longest-standing piece of tech debt — for ~12 weeks operators had been writing skills against private derivatives and the upstream catalog couldn't see them. Catalog is now 155 entries.

---

### Theme 2: AntFleet two-model bench sweep — three security/correctness fixes in 60 seconds

**Summary:** Between 03:09:27 and 03:10:15 UTC, `antfleet-ops` opened PRs #222, #223, and #224 against `aaronjmars/aeon`. All three credit the same source: "AntFleet two-model consensus review (claude-opus-4-7 + gpt-5, unanimous)" on aeon-bench PR #31. Two are tagged **High** severity, one **Medium**. None merged yet — under maintainer review.

**Commits (all open on `aaronjmars/aeon`, branches under `fix/`):**

- **PR #222** `fix/workflow-dispatch-injection` (+22/-4, 2 files) — **High** severity. `inputs.skill` in `.github/workflows/aeon.yml` was template-interpolated directly into `run:` bash bodies. GitHub Actions substitutes template values *before* bash quoting, so a crafted input can inject shell commands into the runner. Fix: validate `INPUT_SKILL` against `^[a-zA-Z0-9_-]+$` in the *Determine skill* step before writing to `GITHUB_OUTPUT`, then pass values through `env:` instead of template substitution in the *Run* step. `workflow_call` inherits the validation. Documented GitHub Actions risk class per GHSA guidance.

- **PR #223** `fix/gateway-provider-parsing` (+14/-2, 2 files) — **High** severity. The GATEWAY-provider extraction line used a malformed quoting sequence (`tr -d ' "'"'"'`) where the trailing `"` bled into the `||` fallback, making shell parsing fragile and aborting the Run step entirely when `gateway.provider` is set in `aeon.yml`. Fix: replace `tr -d` with two clean `sed` calls in double-quote context. Symptom in the wild: model routing fails silently for forks using gateway providers.

- **PR #224** `fix/notify-dedup-hash-order` (+14/-2, 2 files) — **Medium** severity. The dedup hash was written to `.notify-sent-hashes` *before* attempting delivery. When all transports fail inside the sandbox (the documented reason `.pending-notify/` exists), the message gets saved to `.pending-notify/` AND the hash is already in dedup. The post-run *Send pending notifications* step then skips it because the hash matches — silent permanent message loss. Fix: move `printf` inside the `DELIVERED=true` block so only actually-delivered messages get recorded as sent.

**Impact:** Two High severities here are the kind of "compounds quietly until something bad happens" findings two-model consensus review is designed to catch — neither a fork operator nor a single LLM reviewer would have caught all three. The workflow_dispatch injection is exploitable by anyone with write access; the GATEWAY parse error breaks gateway-provider routing for every fork that sets it; the notify dedup bug eats real notifications during sandbox curl outages (exactly the situation `.pending-notify/` was built for). All three are surgical single-purpose PRs (≤22 lines each), easy to merge in any order.

---

### Theme 3: Aeon's own feature run — last open AntFleet High closed

**Summary:** Today's `feature` run (11:27 UTC) picked May-22 repo-actions idea #2 (v4-readiness manifest gaps), but pivoted off the brief during execution: the idea framed H1 as "Removed table gaps", the actual finding (verified against Issue #184 body + AntFleet receipt at aeon-bench PR #12 comment 4475654244) was that the `v4-readiness` skill's Review table named four files it never actually loaded.

**Commits (open on `aaronjmars/aeon`):**

- **PR #226** `feat/v4-readiness-removed-table-audit-2026-05-24` (+44/-9, 1 file) — Single-file diff against `skills/v4-readiness/SKILL.md`.
  - Added the four files (`mcp-server/src/index.ts`, `.outputs/`, `.github/workflows/chain-runner.yml`, `dashboard/lib/catalog.ts`) to §Config Reads + Step 2 inputs table as optional inputs (both local + remote modes; remote uses one `gh api repos/${TARGET}/contents/<path>` call per file).
  - Introduced a `review_unscanned[]` bucket — Review rows whose backing file is missing now surface as a coverage-gap row in the article AND trip `V4_READINESS_PARTIAL` exit. Silent false-clean `READY` is now structurally unreachable.
  - Unscanned counts surfaced in article body, notification, and log block.
  - Inline `<!-- Issue #184 H1 audit -->` invariant comment in Step 2 prevents regression: "every file named in a Review row's `Where it lives` cell must also appear in this Inputs table".
  - Also picked up the brief's audit-refresh ask: `*Last audited: 2026-05-24*` footer + `Audit method` subsection (5 `gh pr list` / `git log` queries) under the Removed table. No verifiable upstream removals found since the skill landed (PR #160, 2026-05-07), so Removed stays empty by design but the manifest is officially fresh.

**Impact:** H1 was the last open AntFleet High on Issue #184. With 111+ forks running pre-v4 workflows, a silently-undercounting readiness check was the worst possible failure mode — operators would dispatch the skill manually before the v4 announcement, get a clean READY, then merge. Now they can't. AntFleet Highs remaining: H4 (.bak rollback in `fleet-state`) and H9 (`admanage-create` campaignId-only ad sets); the other seven (H1/H2/H3/H5/H6/H7/H8) all closed end-to-end as of this PR.

---

### Theme 4: External contributions — typed-annotations sweep + ECOSYSTEM self-list

**Summary:** Two external contributors pushed in this window. One a fresh sweep of types/docs over examples; one a 1-line self-listing into yesterday's new ECOSYSTEM.md.

**Commits (open on `aaronjmars/aeon`):**

- **PR #221** `symbiote/plan-ce8d3665` (+110/-8, 5 files) — `yehorcallmedai-maker` (Yehor Kaliberda). Tagged `[Symbiote] Executed plan ce8d3665` — looks agent-authored. Type hints + dependency-chain docstrings across `examples/a2a/` and `examples/mcp/`. No logic changes claimed. Mass docstring/typing sweeps from new agent accounts have a mixed merge-rate historically; the file scope is tight (5 files, both examples directories) and the claim "no logic was altered" is verifiable from the diff.

- **PR #225** `add-liquidpad-ecosystem` (+1/-0, 1 file) — `liquidpadbot` (LiquidPad). One-line ECOSYSTEM.md row insertion alphabetically between LawbWorld and Liq. Followup to LiquidPad's appearance in yesterday's #218 community-packs bundle. Cross-listed in README per the ECOSYSTEM.md guideline ("project publicly identifies as built on Aeon"). First test of whether ECOSYSTEM.md attracts community self-listing in the same shape as the Community Skill Packs table did.

**Impact:** First production test of ECOSYSTEM.md (~9 hours after merge) is a community self-listing — the exact behaviour the new file was designed to enable. PR #221 is the second Symbiote-tagged PR against `aeon` in a week — pattern worth watching.

---

## aaronjmars/aeon-agent — 3 substantive PRs (1 merged, 2 opened) + ~22 cron auto-commits

### Theme 5: Same-day-after install-protocol backport (Aeon's 12th in a row)

**Summary:** Today's `feature` run opened the 12th same-day-after backport in the established cadence. Yesterday's `feature` shipped aeon PR #215 (skill-packs.json registry, May-22 idea #1); today aeon-agent gets the install-skill-pack CLI + the skill-packs.json registry combined into one PR. Shipped together because #215 depends on #213 (install-skill-pack CLI, the binary that reads the registry) — backporting either alone is dead weight.

**Commits (open on `aaronjmars/aeon-agent`):**

- **PR #59** `feat/install-skill-pack-backport-2026-05-24` (+991/-0, 4 files):
  - `install-skill-pack` (new, mode 100755, +634) — Bash CLI with 6 flags: `--list` (print registry), `--path` (subdir packs), `--branch` (non-default), `--yes` (auto-accept HIGH findings), `--force` (skip security check), `--dry-run`.
  - `skill-packs.json` (new, +100) — 5 seed entries: AntFleet/aeon-skills (`trusted`), baseddevoloper/aeon-skill-pack-vvvkernel, danbuildss/luca-aeon-skills, 0xShak/zer0-skill-pack, gitlawbounty/gitbounty-skill-pack.
  - `docs/community-skill-packs.md` (new, +224) — manifest schema, fallback behaviour, trust model, worked example, publishing checklist.
  - `README.md` (+33) — Community skill packs section inserted between trigger-from-issues and Publishing, matching upstream placement.
  - **`scan.sh` NOT touched** — aeon-agent's `skills/skill-security-scan/scan.sh` already had the May-18 (PR #186, Bash 3.2 array-emptiness) + May-20 (PR #197, POSIX-ERE) hardening from prior backports. Only diff vs upstream is a one-line comment fork-local annotation, deliberately preserved.
  - **`skills.json` `total` NOT bumped** — `install-skill-pack` is a CLI, `skill-packs.json` is a registry; neither is an installed skill entry.

**Impact:** Closes the install-protocol gap on aeon-agent: operators forking aeon-agent (the agent's own self-hosted repo) can now install community skill packs the same way upstream aeon operators can. Cadence: operator-scorecard May-3→4, skill-freshness May-4→5, skill-update-check May-8→9, fork-cohort May-9→10, thread-formatter May-11→12, v4-readiness May-12→13, product-hunt-launch May-15→17, fork-first-run-alert May-17→18, fork-skill-gap May-18→19, competitor-launch-radar May-19→20, contributor-spotlight May-21→23, install-skill-pack+registry May-22→24.

---

### Theme 6: Self-corrective self-improve in response to today's own outage

**Summary:** Today's 06:47 UTC `fetch-tweets` run failed with `FETCH_TWEETS_PREFETCH_FAILED` — XAI returned HTTP 403, "team credits exhausted (monthly spend limit reached)". First 403 in the log history (prior `PREFETCH_FAILED` episodes on Apr 19–20 were curl timeouts). Today's `self-improve` (13:15 UTC, ~6.5h later) picked it as the target.

**Commits (open on `aaronjmars/aeon-agent`):**

- **PR #60** `improve/fetch-tweets-actionable-prefetch-failures` (+229/-12, 6 files) — Two-part fix to `skills/fetch-tweets/SKILL.md`:
  1. **Required `Notification sent` log line** on every exit path (steps 4, 5, 7) so heartbeat's 48h dedup / 3-day escalation logic can track fetch-tweets the same way it tracks every other skill. Without it a multi-day XAI outage wouldn't trigger escalation — exactly when one is most useful.
  2. **Operator-actionable `PREFETCH_FAILED` variants** keyed off the HTTP code prefix in `.xai-cache/fetch-tweets.json.error`:
     - **401 / 403** (auth/credits exhausted, persistent) — includes the XAI console top-up link in notification.
     - **429** (rate-limited, transient) — lower-cadence suggestion if persistent across 3+ days.
     - **5xx** (XAI service, transient).
     - **curl error / timeout** (network/unreachable).
     - **Generic fallback** for any other shape.
  - Inline references to `scripts/prefetch-xai.sh:100, :117` (the error-write sites) so a future cleanup doesn't drift the contract.
  - `memory/logs/2026-05-24.md`: self-improve log entry.
  - The single-file SKILL.md edit is +15/-2 — the rest is generated-state/log.

**Impact:** Closes the loop on a same-day outage. The agent observed its own failure mode (FETCH_TWEETS_PREFETCH_FAILED, generic notification, downstream tweet-allocator empty + token-report social section degraded), traced it back to a structural gap (`Notification sent` line absent → heartbeat can't escalate), and shipped a 5-variant routing table so the next 403 from XAI fires an actionable top-up link instead of a generic "prefetch failed". Self-corrective loop visible inside a single day's log.

---

### Theme 7: Backport cadence streak holds at 11 (one earlier-merged today)

**Commits (merged to `main` 2026-05-23 17:09 UTC, inside window):**

- `db8bcb2` — *fix: contributor-spotlight FORK_DEFAULT_BRANCH never set (aeon PR #206 backport) (#58)* — Already covered in yesterday's recap. Merged inside today's window 17:09 UTC.

### Theme 8: Cron auto-commit volume — 22 chores + 10 scheduler-state updates on main

`aeon-agent/main` saw 32 non-substantive commits in this window from the `aeonframework` bot identity:
- Per-skill auto-commits (memory log appends + state file updates): `token-report`, `fetch-tweets`, `tweet-allocator`, `repo-pulse`, `star-momentum-alert`, `feature`, `self-improve`, `repo-actions`, `heartbeat`, `thread-formatter`, `repo-article`, `project-lens`, `push-recap` (this one).
- Scheduler-state-only commits: `chore(scheduler): update cron state` (10 entries).
- `chore(cron): <skill> success` markers paired with each auto-commit.

These are infrastructure, not feature work. Mentioned for completeness — the substantive PR count is what matters above.

---

## aaronjmars/minitor — 1 substantive PR (1 merged, 1 opened)

### Theme 9: Per-column refresh intervals — last open May-22 idea consumed

**Summary:** Today's `feature` run (11:27 UTC) shipped May-22 repo-actions idea #4. Until today every minitor column refreshed only on mount + manual click; with 47 plugins now spanning fast-moving crypto (CoinGecko/DeFiLlama, 1-5min freshness need) and slow-moving repo signals (GitHub stars, hourly enough), one global cadence couldn't serve both.

**Commits (open on `aaronjmars/minitor`):**

- **PR #49** `feat/column-refresh-intervals` (+513/-2, 10 files):
  - `drizzle/0002_refresh_interval.sql` + `meta/_journal.json` + `meta/0002_snapshot.json` — additive NULLABLE `refresh_interval_seconds` integer on `columns` table.
  - `lib/db/schema.ts` + `lib/columns/types.ts` — schema field + `Column.refreshIntervalSeconds?: number`.
  - `app/actions.ts` (+52) — `REFRESH_INTERVAL_OPTIONS=[60,300,900,3600]` server-side allowlist, `isAllowedRefreshInterval` guard, `updateColumnRefreshInterval` server action, export/import + `loadSnapshot` wiring, optional Zod field. Server never trusts client values.
  - `lib/store/use-deck-store.ts` (+33) — `updateRefreshInterval` action mirroring `updateAlertKeywords` (PR #41 May-14).
  - `components/column/configure-column-dialog.tsx` (+71) — "Refresh interval" Select (Manual / 1m / 5m / 15m / 60m).
  - `components/column/column-card.tsx` (+84) — `useEffect` with `setInterval`, `inFlight` guard preventing overlapping fetches if API slow, `document.visibilityState !== 'visible'` pause so background tabs don't burn rate limits, cleanup on unmount AND on interval change, lucide `Clock` badge in header.
  - `lib/deck-templates.ts` (+4) — `DeckTemplateColumn.refreshIntervalSeconds?: number` so future starter templates can opt-in.
  - **Field lives at column-row level (sibling to `alertKeywords` PR #41 and `title`), never reaches plugin fetchers** — so all 47 plugins keep working with zero changes and their strict Zod schemas remain untouched.
  - Backward compatible: existing rows + pre-feature deck exports default to manual-only; share-link payloads pass the field through transparently (deck-share base64url-encodes the DeckExport JSON).
  - Type-check clean on the diff. Two pre-existing `pypi.ts` errors (lines 286, 302) confirmed present on `main` via `git stash -u && tsc && stash pop`.

**Commits (merged to `main` 2026-05-23 17:09 UTC, inside window):**

- `3405830` — *feat: /gallery public deck page (#48)* — Already covered in yesterday's recap. Merged inside today's window 17:09 UTC.

**Impact:** Last open May-22 idea for minitor. With this merged, May-22 ideas are FULLY CONSUMED across all three repos: aeon (idea #1 skill-packs.json registry May-23, idea #2 v4-readiness H1 May-24, idea #3 contributor-spotlight backport May-23), aeon-agent (idea #3 backport May-23, idea #4 install-skill-pack backport May-24), minitor (idea #5 /gallery May-23, idea #4 per-column refresh May-24).

---

## Developer Notes

- **New dependencies:** None. PR #49 (minitor) uses existing `setInterval` + lucide-react's `Clock` icon already in tree. PR #59 (aeon-agent) ports the `install-skill-pack` Bash CLI that depends only on `gh`, `jq`, `curl` — all pre-existing in CI.

- **Breaking changes:** None observed. All schema migrations (minitor's `0002_refresh_interval.sql`) are additive NULLABLE. The `auto-merge` SKILL.md edit in aeon PR #219 absorbed `auto-merge-agent-prs` behaviour but the latter was dropped pre-merge, so no fork was actually relying on it. The 4 files now declared inputs in aeon PR #226 are marked **optional** — missing-input triggers `V4_READINESS_PARTIAL`, not failure.

- **Architecture shifts:**
  - aeon catalog crossed 155 skills with PR #219 — the framework is now closer in surface area to a small Linux distribution's package set than to a typical agent framework's example library. The retry-cap merge into `auto-merge` is the first time two upstream-shipped skills were consolidated post-port.
  - Three registries (SHOWCASE / Community Skill Packs + skill-packs.json / ECOSYSTEM.md) now formally separate forks, pack authors, and product builders. Cross-listing rules documented in ECOSYSTEM.md.
  - minitor introduces a precedent: column-level optional fields (`alertKeywords` PR #41, `refreshIntervalSeconds` PR #49) live on the column row, never reach plugin fetchers, never touch the per-plugin Zod schemas. This pattern lets new column-level UX features ship in a single PR without coordinating 47 plugin changes.

- **Tech debt introduced / not addressed:**
  - aeon PRs #222 / #223 / #224 (AntFleet two-model bench) are all simple surgical fixes; not merged yet but each is ≤22 lines. Maintainer queue.
  - PR #221 (Symbiote) is a 5-file types/docstrings sweep with no logic changes claimed — verification cost moderate.
  - aeon-agent PR #60's `fetch-tweets` PREFETCH_FAILED variants do not address the root cause (XAI credits exhausted) — only the operator's actionability when it happens again. Credits top-up is a manual operator action.

## What's Next

- **AntFleet Highs after today:** Only H4 (`.bak` rollback in `fleet-state`) and H9 (`admanage-create` skips campaignId-only ad sets) remain open. H1/H2/H3/H5/H6/H7/H8 all closed end-to-end as of PR #226.
- **PR #221, #222, #223, #224, #225, #226 on aeon, #59 + #60 on aeon-agent, #49 on minitor** — 9 PRs open at window close. Aeon's `auto-merge` skill runs daily 18:00 UTC; whichever of the bot-authored PRs are green will land tonight. The 5 external-author PRs (#221 yehor, #222–#224 antfleet-ops, #225 liquidpadbot) need maintainer review.
- **May-24 repo-actions ideas seeded** (article `articles/repo-actions-2026-05-24.md`, 5 ideas):
  1. aeon — ecosystem-pulse skill (Feature, Small) — first skill to ask "are things built on Aeon shipping?"
  2. aeon — fleet-skill-adoption leaderboard (Feature, Medium)
  3. aeon-agent — config-validator backport from PR #219 (DX, Small)
  4. minitor — Bluesky AT Protocol column (Integration, Medium)
  5. minitor — column-level webhook notifications (Feature, Medium)
- **Backport cadence streak holds at 12** — install-skill-pack May-22→24. The most likely next backport target on aeon-agent is upstream PR #219 (Port 34 skills) itself, or a subset of it filtered to which skills are still missing on aeon-agent.
- **Branches created but not merged:** All 9 open PRs listed above. No abandoned WIP branches detected — every open feature/fix branch maps to a live PR.
