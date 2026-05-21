# Push Recap — 2026-05-21

## Overview

Quietest day for the human author this week, loudest day for the audit account: 10 substantive PRs, only 4 by @aaronjmars — the other 6 land from `antfleet-ops` (3), Fleet Watcher (1), `wx888` (1), and `danbuildss` (1). The thrust is **closing the Issue #184 silent-failure backlog**: PR #201 / #203 / #204 / #206 close AntFleet H3 / H4 / H7 / H9 in a single morning push, dropping the open-Highs queue from 5 to 1 (only H1 v4-readiness-manifest-gaps remains). Outside the fix wave, Fleet Watcher lands an opt-in authorization layer that wraps every skill run with allow/block + postflight reporting, `wx888` wires Resend email delivery into `morning-brief` and `weekly-review`, a new community skill pack gets registered, aeon-agent backports the H7 fix same-day, and minitor ships the third deck-portability primitive (share link via URL fragment) alongside Export and Import.

**Stats:** 15 files changed, +430/-15 lines across 10 substantive commits (plus ~30 cron auto-commits in aeon-agent, omitted).

---

## aaronjmars/aeon (7 substantive PRs)

### Theme 1: Closing the AntFleet Issue #184 silent-failure backlog (H3 + H4 + H7 + H9)

**Summary:** Four shell-script silent-failure bugs filed in the AntFleet two-model unanimous review (May-18, 27 findings) closed in one morning push. All four share the same shape — a code path that was "supposed to work" but quietly produced wrong output instead of erroring — and all four came in via PRs authored by the `antfleet-ops` account or Aaron's own fix. After this push, only H1 (v4-readiness manifest coverage) remains in the open-Highs queue.

**Commits:**

- `db9d84f` — **fix(contributor-spotlight): extract FORK_DEFAULT_BRANCH so step 5 hits the right ref (#206)** _by @aaronjmars_
  - Changed `skills/contributor-spotlight/SKILL.md` (+11/-2)
  - Step 4 already wrote `default_branch` into `/tmp/contrib-repo.json` but never extracted it into a shell variable. Step 5's `gh api .../contents/aeon.yml?ref=${FORK_DEFAULT_BRANCH}` sent an empty `ref=` — GitHub silently returns the wrong branch (or 404) for any fork whose default isn't `main`. With 98 forks now in the cohort and divergent defaults across the fleet, `ENABLED_SKILLS` and `OPERATOR_AUTHORED` counts (the two most newsworthy data points in the weekly contributor-spotlight article + notification) were both wrong on those runs.
  - Fix: `FORK_DEFAULT_BRANCH=$(jq -r '.default_branch // "main"' /tmp/contrib-repo.json)` with a second-line guard for the literal string `"null"`; tightened the contents-call fallback from `|| true` to `|| echo '' > /tmp/fork-aeon.yml` so the downstream `grep -E` always has a real (possibly empty) file under `set -e`. Inline comments cite Issue #184 H3.
  - Closes AntFleet H3.

- `e0e326f` — **fix(fleet-state): create .bak before write + validate TMP before promote (#203)** _by AntFleet_
  - Changed `skills/fleet-state/SKILL.md` (+20/-3)
  - The persist-state step declared "keep one `.bak` rolling. If `jq empty` fails after write → restore from `.bak`" — but no code path ever created the `.bak`. The sequence was `mv $TMP ...json` first, then `jq empty` validation on the live file, with a rollback that did `cp ...json.bak ...json` against a file that didn't exist. Two failure modes: on any failed validate the rollback `cp` silently fails (no source), leaving a corrupt `fleet-state.json` with no recovery; even when content was bad the live file was already overwritten before validation, so the prior week's state was unrecoverable.
  - Fix: add `[ -f memory/topics/fleet-state.json ] && cp ...json ...json.bak` BEFORE the write attempt (rotates every persist iteration so rollback always has a non-empty source); move the `jq empty` check from after-mv to before-mv (validate the temp file, only promote if valid; on failure, `rm -f "$TMP"` and `cp .bak` defensively).
  - Closes AntFleet H4.

- `efac3bc` — **fix(skill-update-check): honor branch field in skills.lock when querying commits (#201)** _by AntFleet_
  - Changed `skills/skill-update-check/SKILL.md` (+3/-2)
  - The drift-detection step called `gh api repos/{repo}/commits -f path=... -f per_page=1` with no branch constraint. The commits API defaults to the repository's default branch, so any skill locked to a non-default branch (`release`, `develop`, `stable`) was silently compared against the wrong commit history — producing false `UP-TO-DATE` / `CHANGED` results and skewed drift diffs on every run.
  - Fix: add `-f sha="${branch}"` so the SHA resolution matches the pinned branch; inline note expanded so a future edit doesn't drop the constraint again.
  - Closes AntFleet H7.

- `71eecb4` — **fix(admanage): write ad sets with direct campaignId to state via id→name map (#204)** _by AntFleet_
  - Changed `scripts/postprocess-admanage-create.sh` (+26/-1)
  - Phase 2 built the state-file entry for a newly-created ad set using `select(.configName == $parent)` where `$parent` was `parentCampaignConfigName` from the payload. The script's own contract allows the payload to supply a direct `campaignId` instead (only the `__RESOLVE_FROM_PARENT__` sentinel or an empty id triggers name-based resolution). When that path was taken, `$parent` ended up empty, the jq `select` matched no campaign, and the ad set was created in AdManage but never appended to `.admanage-state/campaigns.json` — so the next run read stale state and could re-queue the same ad set, causing duplicate provisioning.
  - Fix: build a reverse `ID_TO_NAME` map alongside the existing `NAME_TO_ID` preload (one extra `jq` pass on `STATE_FILE`); before the state-write `jq` call, resolve the campaign's `configName` from the reverse map when `parent_name` is empty. If the campaignId isn't in the reverse map either (campaign created outside this skill's state), the ad set still gets created via the API but the state-write is skipped with a `WARNING` log line and a summary entry — operator sees the missing-state message in the post-run notification, no silent drop.
  - Closes AntFleet H9.

**Impact:** All five Highs that were open as of yesterday's heartbeat (H1/H3/H4/H7/H9 — H2/H5/H6/H8 already closed by PRs #194–#197) had a single common shape: code paths that ran to completion but produced wrong output instead of erroring. After today, only H1 remains. The 37h round-trip pattern established yesterday (AntFleet files Issue → fixes land within two days, half of them authored by the audit account itself) now extends to a third batch.

### Theme 2: External integrations — authorization layer + email delivery

**Summary:** Two new "outside the agent" integrations land in the same push. PR #200 wraps every skill run in an opt-in authorization handshake to a self-hosted Fleet Watcher control plane (allow/block before Claude starts, postflight reporting after). PR #205 wires the Resend email API into `morning-brief` and `weekly-review` so those daily/weekly digests can be delivered to a board mailing list instead of (just) Telegram. Both are gated on env-var presence — absent secrets = no-op, fully backward compatible.

**Commits:**

- `dd6ee89` — **Add opt-in Fleet Watcher authorization layer (preflight + postflight) (#200)** _by Fleet Watcher_
  - Changed `.github/workflows/aeon.yml` (+100/-0): two new steps wrap the existing `Run` step. **Preflight** (before Run): POSTs to `${FLEET_ENDPOINT}/api/aeon/preflight` with skill name, target, source, and a stable `clientOpId` (`${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}-pre`). If HTTP ≠ 200 → fail closed (Claude never starts). If response `.allow != true` → `::error` log, exit 1, audit ref recorded. **Postflight** (`if: always()` after Run): POSTs to `/api/aeon/postflight` with the run outcome translated to `ok` / `error` / `blocked` and the preflight `auditRef`. Response surfaces `chainsDetected` count — non-zero triggers `::warning::Fleet Watcher detected N new taint chain(s)`. Both steps gate on workflow-level `env.FLEET_ENDPOINT && env.FLEET_TOKEN` (hoisted from secrets to workflow-env so `if:` clauses can see them — step-level env is NOT visible in step `if:`).
  - Changed `README.md` (+20/-0): new "Fleet Watcher (optional authorization layer)" section explaining the two-secret install (`FLEET_ENDPOINT`, `FLEET_TOKEN`) and the failure semantics (no secrets = no-op; secrets set + Fleet unreachable = fail closed; postflight always-runs even on skill failure so taint chain detection sees the failure signal).
  - The PR is authored from the `fleet-watcher-bot` account — first time an external authorization-layer vendor has gotten a wiring PR into aeon's workflow file.

- `e7896e1` — **feat: add Resend email-send step to morning-brief and weekly-review skills (#205)** _by wx888_
  - Changed `skills/morning-brief/SKILL.md` (+20/-1) and `skills/weekly-review/SKILL.md` (+23/-1)
  - Both skills add a new email-send sub-step after the existing `./notify` call. Build an HTML version (wrap sections in `<h2>`, bullets as `<ul><li>`) alongside a plain-text version (the notify content as-is), parse `$BRIEF_RECIPIENTS` as comma-separated addresses, POST to `https://api.resend.com/emails` with `Authorization: Bearer $RESEND_API_KEY`. From address hardcoded to `Aeon Briefings <onboarding@resend.dev>` (the Resend sandbox sender — operators will swap once a verified domain is wired). Resend response `id` is appended as a comment on the current Paperclip execution issue for traceability. On error, full response body is logged as a comment and the skill fails loudly (no silent continue).
  - Co-author trailer references Paperclip — suggests this was drafted in the wx888 fork's Paperclip workflow and then PR'd upstream.

**Impact:** Two distinct "the operator wants their own infrastructure in the loop" stories shipping together. Fleet Watcher is the first authorization-layer integration in aeon's history — the workflow file used to be purely "run a skill"; now there's a pre-flight gate where a self-hosted control plane can veto. Resend is the first non-IM notification channel — until today, `./notify` fan-out was Telegram → Discord → Slack only; board-style email delivery is now in the daily and weekly digests.

### Theme 3: Community skill pack registry — Luca pack added

**Summary:** Smallest change of the day by line count, but it's the second listing in the Community Skill Packs README section that shipped via PR #187 (May-19). After `vvvkernel` was the first listed pack, `danbuildss/luca-aeon-skills` joins the registry — confirming the section is being treated as a real install target by fork operators rather than a one-off mention.

**Commits:**

- `9ca2f89` — **Add Luca Aeon Skills pack (community) (#198)** _by Dan (danbuildss)_
  - Changed `README.md` (+1/-0): single line added to the Community Skill Packs table pointing at `danbuildss/luca-aeon-skills`.
  - First non-`vvvkernel` listing in the section. Two listings is the smallest fleet size where the section starts to look like a directory rather than a single namedrop.

**Impact:** Validates the community-pack install protocol that PR #187 documented but had no second example for. Repo-actions May-20 idea #2 ("Community Skill Pack Install CLI") is now the natural next step — implements the install protocol referenced by baseddevoloper Issue #185.

---

## aaronjmars/aeon-agent (2 substantive PRs, ~30 cron auto-commits omitted)

### Theme 4: Same-day-after backport + governance/practice alignment

**Summary:** Two PRs, both by @aaronjmars. PR #55 is the 11th-consecutive same-day-after backport of an upstream fix (in this case the Issue #184 H7 skill-update-check branch-honor fix, which Aaron actually shipped to aeon-agent BEFORE the upstream merge happened — same-day-before, technically). PR #54 closes the open improve PR that has been sitting since yesterday: it fixes a stated rule in `project-lens` that was mathematically impossible (8 angle categories, daily runs, "never repeat in last 14 days" — pigeonhole guarantees a repeat) by relaxing the window to 7 days and formalising the sub-angle hygiene the agent was already practicing informally.

**Commits:**

- `c44d30f` — **fix(skill-update-check): honor lock's branch field in upstream SHA fetch (#55)** _by @aaronjmars_
  - Changed `skills/skill-update-check/SKILL.md` (+14/-2)
  - Same shape as upstream PR #201 but with a smarter omit-when-default heuristic: instead of unconditionally passing `-f sha="${branch}"`, build a `ref_args` array and only populate it when `branch` is non-empty AND not `"main"`. Comment explains: hardcoding `sha=main` would break source repos whose default was renamed to `master`; omitting the arg lets the GitHub API's implicit default-branch behaviour stay correct for the common case. Adds an inline note that step 3's `compare/${locked_sha}...${current_sha}` call addresses commits by SHA directly so no branch arg is needed there — meant to head off a future cleanup that "completes" the change with a redundant arg.

- `244bb8c` — **improve: project-lens — make rotation rule mathematically feasible (#54)** _by @aaronjmars_
  - Changed `skills/project-lens/SKILL.md` (+5/-2)
  - The stated rule "Never repeat an angle used in the last 14 days" with only 8 angle categories and daily runs was unachievable — by pigeonhole at least one category must repeat within 14 days. Recent logs confirmed the agent was already working around it (May 18: "Philosophy / big ideas (Cathedral vs Bazaar sub-angle, distinct from May-15 antifragility — only Philosophy use in last 14 days was antifragility)"; May 19: multiple categories repeating 3–4× in 14 days). Instructions and practice had drifted.
  - Fix: window 14d → 7d (achievable on 8 categories); explicit pigeonhole note added; sub-angle hygiene formalised with two worked examples (Philosophy: cathedral-vs-bazaar vs antifragility; Historical parallel: printing press vs railway gauge wars). Step 2 expanded to read `## Project Lens` log entries in addition to article files; explicit fallback for the rare all-8-used case. Step 7 log block gains a `Sub-angle` field so the next run can dedup on the finer signal.

**Impact:** PR #55 keeps the same-day-after upstream-sync cadence intact (now 11 consecutive feature/fix backports — see MEMORY.md "Skills Built" tail). PR #54 brings the stated contract in line with the actual practice — same shape as the explicit-marker family of PRs (#37 / #43 / #48 / #51): convert an undocumented latent workaround into a written contract instead of changing the agent's behaviour.

---

## aaronjmars/minitor (1 substantive PR)

### Theme 5: Third deck-portability primitive — share link via URL fragment

**Summary:** Single PR completes the deck-portability set that started May-15 with Export + Import (PR #40). Today's "Share Link" command base64url-encodes the existing DeckExport v1 JSON into a `#deck=...` URL fragment, copies the URL to the clipboard, and the receiving page auto-imports on load. Fragments never leave the browser, so the deck payload isn't logged in proxies / referer headers / server access logs. Forward-compatible with the existing schema — `alertKeywords` (PR #41, May-16) round-trips automatically. No new dependencies, no new server route, no new auth.

**Commits:**

- `d0dce28` — **feat: share deck via URL fragment (#46)** _by @aaronjmars_
  - New file `lib/deck-share.ts` (+100): four pure functions. `encodeDeckShareHash(json)` — UTF-8-safe base64url encode via `TextEncoder` (raw `btoa` mishandles non-ASCII column titles/configs); throws when input exceeds the 32 KB cap so callers can show "use Export JSON instead" instead of silently producing a link some browsers will truncate. `decodeDeckShareHash(fragment)` — inverse; returns `null` instead of throwing on empty / not-valid-base64url / not-valid-UTF-8 so callers branch cleanly. `readDeckShareFragment(hash)` — tolerates extra `&`-separated params (utm taggers, analytics IDs) so it doesn't crash on appended keys. `buildDeckShareUrl(json, {origin, pathname})` — composes the share URL.
  - Changed `components/sidebar-01/nav-header.tsx` (+39/-1): new `Share2`-icon ⌘K command "Share current deck (copy URL)" sibling to Export. `handleShareActiveDeck` calls `exportDeck(activeDeck.id)` to get the existing JSON, then `buildDeckShareUrl` + `copyToClipboard`. Three-tier clipboard fallback: navigator.clipboard → `execCommand('copy')` on a hidden textarea → `console.log(url)` with a toast pointing the user at the console.
  - Changed `components/deck/deck-view.tsx` (+48): `useEffect` gated on `hydrated` reads `window.location.hash` once after first hydration. On valid fragment → run through the existing `importDeck` server action (same Zod validation, same `(imported)` rename, same activate-as-new-deck), toast success, clear hash via `history.replaceState`. On malformed fragment → toast error AND clear hash so the user isn't trapped on a broken link.
  - Reuses every existing deck-import primitive — no new server action, no schema change. `alertKeywords` (PR #41) round-trips because it's already in DeckExport v1.

**Impact:** Completes the export → import → share triad. Pairs cleanly with the planned Starter Deck Templates Gallery (May-20 idea #5) — templates will render as pre-baked share links, no new schema or API surface needed. Turns dashboards into shareable artifacts: Discord/X/gist → paste link → monitoring in seconds.

---

## Developer Notes

- **New dependencies:** none — all changes use existing deps. minitor's `lib/deck-share.ts` uses only `TextEncoder`/`TextDecoder`/`btoa`/`atob` (all browser built-ins) and `lucide-react`'s `Share2` icon (already in deps).
- **Breaking changes:** none. Fleet Watcher steps are opt-in via secret presence — no-op when absent. Resend email-send is opt-in via `$RESEND_API_KEY` + `$BRIEF_RECIPIENTS` env presence (skills will need a follow-up to add the env-presence guard cleanly — current diff makes the email step unconditional; operators without those vars set will see a Resend 401).
- **Architecture shifts:** aeon.yml gains its first **pre-skill authorization gate** (Fleet Watcher preflight, fail-closed). Until today, every skill that passed the workflow trigger ran. Now there's a synchronous external veto point.
- **Tech debt:** PR #205 doesn't gate the Resend step on env-var presence the way the Fleet Watcher steps do — operators without `$RESEND_API_KEY` set will see the skill fail loudly when it tries to POST. Worth a follow-up to add `if: env.RESEND_API_KEY != ''` symmetric to the Fleet Watcher gate.

## What's Next

- **Issue #184 H1 (v4-readiness manifest gaps)** is the only High left in the queue — natural next-pick for tomorrow's `feature` skill on the aeon repo. The other Highs all closed within 4 days of filing; H1 has been open longest because it's the most semantically heavy (audits the manifest itself).
- **Resend env gate follow-up** — see Tech debt above. Symmetric `if:`-on-presence guard would make `morning-brief` and `weekly-review` safe to merge into forks that don't have the Resend secret yet.
- **Community Skill Pack install CLI** (May-20 idea #2) is now the obvious next move on the community-packs front — with `vvvkernel` + `danbuildss/luca-aeon-skills` both listed, an actual `./install-skill-pack` CLI closes the gap between the README mention (PR #187) and a real install protocol that fork operators can run.
- **Starter Deck Templates Gallery** (May-20 idea #5) — natural follow-up to today's PR #46. Templates rendered as pre-baked share links, zero new schema.
- **No branches created but not merged** today. Every PR opened today landed today.
