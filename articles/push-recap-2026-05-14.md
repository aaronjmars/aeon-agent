# Push Recap — 2026-05-14

## Overview
15 substantive commits across three repos in the last 24h, single primary author (@aaronjmars) with five Claude Opus co-authored PRs. The headline move: aeon-agent finally flipped six long-stuck announcement/visibility skills from `enabled:false` to `enabled:true` — closing the three-day "switch is still off" thread tracked in MEMORY since the 308⭐ ATH day. Surrounding that core decision: a one-shot 22-skill catchup from upstream, a recurring Monday workflow so the fork stays current automatically, two dashboard bug fixes that had been silently typecheck-failing since April, and minitor's news-and-web cluster hitting 10 sources with PyPI + crates.io landing as the 42nd and 43rd column types.

**Stats:** ~75 files changed, +7,500 / -90 lines across 15 substantive commits (excluding cron/scheduler auto-commits and the minitor revert + reapply pair that net to a commit-message rename).

---

## aaronjmars/aeon-agent

### Theme 1: The switches finally flipped — fleet visibility wakes up
**Summary:** Three consecutive days of `repo-article` + `heartbeat` flagged the same finding: "300⭐ crossed 2026-05-12, four announcement skills (star-milestone, star-momentum-alert, thread-formatter, show-hn-draft) still disabled." Today's PR #45 flipped six of those switches on aeon-agent in a single 6-line diff. PR #46 then immediately walked one back when fork-cohort dependency was caught. This is the operator-loop closure the recent `repo-article` thread named explicitly.

**Commits:**
- `3258437` — *enable: launch comms + weekly visibility (6 skills) (#45)*
  - Changed `aeon.yml`: 6 single-line `enabled: false` → `enabled: true` flips (+6, -6 lines)
  - Skills flipped: **star-milestone** (daily 15:15 UTC — announces star milestones, aeon now at 312⭐ targeting 500), **star-momentum-alert** (daily 10:10 — projects next milestone date for the Tue/Wed/Thu HN window), **thread-formatter** (daily 17:30 — scores today's events from logs and formats top one as a 5-tweet thread, silent on quiet days under threshold 3), **contributor-spotlight** (Sunday 20:00 — weekly POWER-fork recognition), **operator-scorecard** (Monday 10:30 — weekly "was this week worth it?" digest), **ai-framework-watch** (Monday 08:30 — weekly competitive intel on 9 AI frameworks). All silent on quiet days — no notify spam if nothing changed.
  - Companion change called out in the body landing on the `miroshark-aeon` fork in parallel.

- `00bbb75` — *disable: contributor-spotlight (dependency not enabled) (#46)*
  - Changed `aeon.yml`: contributor-spotlight `enabled: true` → `enabled: false` (+1, -1)
  - The commit body diagnoses why cleanly: contributor-spotlight reads from the latest fork-cohort run, but fork-cohort is still `enabled:false` — first Sunday firing would have nothing to pick from. Reverted within ~2 minutes of #45 landing.

**Impact:** Five of the six switches stay on. The fleet now has its first daily announcement channel (star-milestone), its first event-driven thread output (thread-formatter), and its first Monday digest (operator-scorecard) — all of which the operator-loop "switch is still off" thread has been asking for since May 11. The contributor-spotlight walk-back is the more interesting note: it proves the operator is reading their own dependency graph before flipping further, which means the remaining un-flipped synthesis skills (fleet-state, fork-cohort, fork-release-tracker) are gated behind a deliberate enable-order rather than backlog inertia.

### Theme 2: Bulk skill catchup + a recurring upstream-sync rail
**Summary:** Two complementary moves landed in the same hour. PR #44 bulk-copies 22 SKILL.md files from upstream aeon into aeon-agent's skills/ directory (all `enabled:false` — operator picks which to flip in follow-up). PR #170 over in upstream aeon adds a Monday 09:00 UTC GitHub Actions workflow that opens a sync PR every week from `aaronjmars/aeon` main into whatever fork inherits the workflow. The two PRs together convert "manual same-day-after backport pattern" (operator-scorecard May-3→4, skill-freshness May-4→5, etc — a streak going back two weeks) into "automated weekly sync".

**Commits:**
- `d07a1d2` — *sync: pull 22 skills from aeon upstream (#44)*
  - New files: 25 SKILL.md additions plus 2 config.example.yaml under skills/ for `create-campaign` and `schedule-ads` (+4,816 lines across 26 added files)
  - Touches: `aeon.yml` (+24, registers all 22 new entries in a new "Upstream sync (2026-05-14)" section), `skills.json` (+229, -9; manifest count bumped 62 → 85 with an em-dash normalization sweep that drives most of the 9-line "modified" delta — verified non-content change)
  - Notable inclusions: `ai-framework-watch`, `aixbt-pulse`, `contributor-reward`, `contributor-spotlight`, `create-campaign`, `fleet-state` (yesterday's aeon PR #168 already lands here as an SKILL.md copy), `fork-contributor-leaderboard`, `fork-release-tracker`, `fork-skill-digest`, `huggingface-trending`, `monitor-kalshi`, `onboard`, `pr-triage`, `price-threshold-alert`, `schedule-ads`, `show-hn-draft`, `skill-analytics`, `skill-graph`, `smithery-manifest`, `star-milestone`, `star-momentum-alert`, `syndicate-article`.
  - All 22 land disabled by default; PR #45 then immediately flips 6 of them on in the next commit.

**Impact:** This is the largest single content drop in the recap window — 4,800+ lines of skill source. The skills.json manifest went from 62 entries to 85 in one merge. Worth noting against MEMORY's standing claim that "aeon-agent still at pre-autoresearch-evolution SKILL.md versions (aeon PRs #46–#136 not yet backported)" — that statement is about content-evolution of existing skills, not new-skill catchup. So even with this PR, the autoresearch-rewrite gap remains; this PR only narrows the *catalog* gap, not the *quality* gap.

### Theme 3: Yesterday's backlog landing — webhook + v4-readiness + .truncated extension
**Summary:** Three PRs that yesterday's `feature` and `self-improve` skills opened all landed this morning. Together they close the entire May-12 `repo-actions` idea backlog (the run produced 5 ideas; #1 v4-readiness ✓, #2 Reddit pre-existing, #3 fleet-state ✓ May-13, #4 webhook-bridge ✓, #5 Bluesky pre-existing).

**Commits:**
- `51cf5d6` — *feat: webhook-to-skill bridge — fire any Aeon skill via repository_dispatch (#42)*
  - New `.github/workflows/webhook.yml` (+125): listens for `repository_dispatch` `event_type=aeon-skill`. Validates payload — slug regex `^[a-z0-9][a-z0-9-]{0,63}$`, `skills/<slug>/SKILL.md` existence check, skills.json registry warning, var length + control-char guards, 9-ID model whitelist. Dispatches `aeon.yml` via `gh workflow run` with slug + optional var + optional model. Slug-injection-safe — payload never reaches shell interpolation.
  - New `skills/webhook-bridge/SKILL.md` (+183): operator-facing documentation with 4 worked examples (cross-repo GH Actions, Zapier, n8n, vendor webhook proxies like DexScreener), validation contract table, scope notes for fine-grained PATs. `workflow_dispatch` only, `enabled: false` — the real work is in webhook.yml, not the skill.
  - Changed `aeon.yml`: registered webhook-bridge entry (+1). `skills.json`: 61 → 62 (+11, -1).

- `188553c` — *feat: backport v4-readiness skill from upstream aeon PR #160 (#41)*
  - New `skills/v4-readiness/SKILL.md` (+289): verbatim backport of upstream's v4 manifest checklist skill — Safe/Review/Custom/Action-items breakdown derived from aeon.yml + skills.json + MEMORY.md against an embedded v4 manifest. Three dispatch modes: empty (local working tree), `dry-run` (skip notify), `owner/repo` (remote survey via gh api). Pure local file I/O — no curl, no env-var-in-headers.
  - Changed `aeon.yml`: registered v4-readiness as workflow_dispatch (+1). `skills.json`: 60 → 61 (+10). Last of the May-6 backport batch — aeon-agent now at full pre-v4 catalog parity with aeon.

- `1cc35fe` — *improve: surface XAI cache truncation via .truncated marker (#40)*
  - Changed `scripts/prefetch-xai.sh` (+11, -6): when output_tokens within 5% of max, drops a sibling `.xai-cache/<file>.truncated` marker with `output_tokens=N/max=M` payload.
  - Changed `skills/fetch-tweets/SKILL.md` (+2): reads the marker, sets `FETCH_TWEETS_OK_TRUNCATED` status, appends warning line to notification — operators can now distinguish a quiet day from a budget-exhaustion day.
  - Side files: `.outputs/self-improve.md`, `dashboard/outputs/self-improve-*.json` artifacts (+180, -6).

- `d2ac64a` — *improve: extend .truncated marker handling to other XAI cache consumers (#43)*
  - Changed `skills/narrative-tracker/SKILL.md`, `skills/remix-tweets/SKILL.md`, `skills/tweet-roundup/SKILL.md`: each picks up the same `.truncated` read pattern PR #40 established (+2 lines per file). Per-skill `*_OK_TRUNCATED` log status, identical one-line warning shape.
  - Side files: dashboard output artifact + MEMORY.md timestamp bump + memory/logs/2026-05-14.md auto-commit.
  - Triggered by self-improve noticing that `scripts/prefetch-xai.sh` lines 130–134 name six consumers as marker readers but `grep truncated skills/` only matched fetch-tweets — the contract was unilateral until this PR.
  - Older consumers `refresh-x` and `article` deliberately left untouched (they lack both `.error` and `.truncated` patterns and need a larger cleanup).

**Impact:** Three classes of work close together. **webhook-bridge** opens an external-event input channel — third-party services can now fire Aeon skills without operator UI access. **v4-readiness** closes pre-v4 catalog parity (aeon-agent now has every skill aeon has, modulo content-evolution gap). **.truncated marker** is the cleanest example of self-improve catching its own contract gap and closing it within one day: the marker was written by the prefetch script but only fetch-tweets read it; now four of the six named consumers read it, with two left for a deeper cleanup that needs both `.error` + `.truncated` patterns.

---

## aaronjmars/aeon

### Theme 4: Dashboard quietly broken since April, two PRs fix it
**Summary:** Two dashboard fixes that probably should have been caught earlier. PR #169 fixes `gh` CLI multi-remote ambiguity that broke the dashboard's auth + secrets routes whenever a fork added upstream as a second remote (recommended pattern per README). PR #171 finishes the wiring for an April Bankr Gateway commit that introduced a `gateway` state but never updated TopBar to receive it — meaning the dashboard's TypeScript build has been failing TS2322 on `main` for weeks.

**Commits:**
- `416244f` — *fix(dashboard): pass -R repo to gh commands so multi-remote setups work (#169)*
  - Changed `dashboard/app/api/auth/route.ts` (+21, -4): introduces `ghRepo()` helper that resolves active repo via `gh repo set-default --view` with `gh repo view` fallback, threads it through all gh invocations via `-R` flag, swaps shell-string `ghRepoFlag()` for `execFileSync` array form.
  - Changed `dashboard/app/api/secrets/route.ts` (+20, -3): same pattern, plus drops an unused `listSecrets` shell branch.
  - The bug: README recommends a two-repo strategy (fork + upstream as remotes). With both remotes present, `gh secret list/set/delete` errors with "multiple remotes detected" because gh can't pick a default. Auth and secret management both broke as soon as upstream was added. Two routes converged on the same helper pattern with identical signatures.

- `c789dcc` — *fix(dashboard): wire gateway prop through TopBar + SkillDetail (#171)*
  - Changed `dashboard/app/page.tsx` (+1, -1): adds the missing `gateway={gateway}` prop forward on the SkillDetail invocation (the bug — the state existed in page.tsx since April but never reached the children).
  - Changed `dashboard/components/TopBar.tsx` (+6, -3): TopBar now accepts `gateway`, renders a "Bankr" badge in the header when active, and conditionally extends the model dropdown with `BANKR_EXTRA_MODELS`.
  - Changed `dashboard/components/SkillDetail.tsx` (+6, -4): same conditional extension for the per-skill override dropdown. Default-label fallback now degrades to raw model id if it's in neither list (was returning `undefined` inside an `<option>`).
  - New `dashboard/lib/constants.ts` (+8): adds `BANKR_EXTRA_MODELS` — Gemini 3 Pro, Gemini 3 Flash, GPT-5.2, Kimi K2.5, Qwen3 Coder. Matches the README's gateway model table.

**Impact:** Two silent-failure classes resolved. The `-R repo` fix is the operationally meaningful one — for any fork that follows the README's recommended two-remote setup, the dashboard's auth and secrets pages were effectively bricked. The Bankr-gateway wire-through is more cosmetic for now (the gateway hasn't shipped to non-Claude routing yet) but unblocks the typecheck pipeline and shows the dashboard now visibly advertises which gateway it's running through.

### Theme 5: Weekly upstream-sync rail (companion to aeon-agent PR #44)
**Summary:** PR #170 adds a Monday 09:00 UTC GitHub Actions workflow to upstream `aaronjmars/aeon`. Because the workflow lives in the parent repo, every fork inherits it and runs it against their own copy — turning the "operator manually catches up on upstream every two weeks" pattern into "every fork opens a sync PR every Monday automatically".

**Commits:**
- `77522af` — *ci: add weekly upstream sync workflow (#170)*
  - New `.github/workflows/sync-upstream.yml` (+90): cron `0 9 * * 1` + `workflow_dispatch`. Adds `aaronjmars/aeon` as upstream remote, computes `git rev-list --count HEAD..upstream/main`, exits cleanly if zero. Otherwise creates `sync/upstream-YYYYMMDD` branch and attempts merge. On clean merge: pushes branch, opens "sync: upstream/main (N commits)" PR. On conflict: commits conflict markers with `--no-verify` (intentional — the inline comment now documents this is by design so reviewers see exactly what to resolve), opens "sync: upstream/main (CONFLICTS, N commits)" PR with explicit resolution instructions in the body. Uses `gh pr list --head $BRANCH` to update an existing PR rather than open a duplicate.
  - Co-authored by traewang — origin is traewang's fork pattern, promoted to upstream so all forks inherit.

**Impact:** This is the same machinery as aeon-agent's PR #44 (bulk sync), just expressed as a recurring rail. PR #44 catches aeon-agent up *once* in one big merge; PR #170 keeps every fork synced *forever* with weekly PRs. Worth noting: the workflow lives in upstream itself so it's a no-op there (upstream merging from itself), but every fork picks it up. The `--no-verify` choice on conflict commits is the kind of thing a reviewer would normally flag as "skip hooks" anti-pattern — the inline comment defending it is the right call.

### Theme 6: Fleet-state landing (already documented in yesterday's recap)
**Commits:**
- `eb829dd` — *feat: fleet-state digest — Monday synthesis of fork-cohort + fork-release-tracker + contributor-spotlight (#168)*
  - New `skills/fleet-state/SKILL.md` (+398), `aeon.yml` (+1), `skills.json` (+13, -1; 116 → 117).
  - Monday 08:00 UTC synthesis skill; reads three constituent state files (fork-cohort, fork-release-tracker, contributor-spotlight), never re-queries forks. 8-status exit taxonomy. Quiet-week gate suppresses notify on STEADY + 0 transitions + 0 releases + not first run.
  - Already deep-covered in yesterday's repo-article ("Aeon Just Built a Skill That Reads Other Skills. None of Them Run Yet.") and the May-13 log. Mentioned here for completeness — it merged inside today's 24h window.

**Impact:** The first synthesis-only skill in aeon's catalog. Inputs are three JSON state files written by three other Aeon skills, not external APIs. Marks the architectural shift from "skills that watch the world" to "skills that watch the watchers."

---

## aaronjmars/minitor

### Theme 7: Registry trifecta completes — PyPI + crates.io ship same day
**Summary:** Two new column types land together, completing the npm + PyPI + crates.io registry triple started May-12 with npm. Together these bracket the three package registries the AI/ML, web, and systems-programming crowds actually live in.

**Commits:**
- `497242c` — *feat: add PyPI column — 42nd column type, Python package registry companion to npm (#36)*
  - New `lib/integrations/pypi.ts` (+322): keyless fetcher with three modes — `updates` (PyPI's `rss/updates.xml`, recent version bumps), `new-packages` (`rss/packages.xml`, brand-new registrations), `top-30d` (community hugovk/top-pypi-packages mirror — top 8000 by 30d downloads; the only "trending" surface PyPI itself doesn't expose). Optional weekly-downloads enrichment via pypistats.org.
  - New `lib/columns/plugins/pypi/` (3-file plugin, +234): standard plugin shape with #3776AB Python brand blue accent, Package2 icon (distinct from npm's Package).
  - 3 registry edits (manifest.ts, registry.ts, server-registry.ts) + README cluster row News & web 8 → 9, column count 41 → 42.
  - Three documented integration quirks: (1) updates feed title is `{name} {version}` space-separated, new-packages is just `{name}` — split parser handles both; (2) rank-feed createdAt is the mirror's last_update so every row in a slice shares a timestamp — renderer suppresses the time pill on rank rows; (3) pypistats.org failures degrade silently to 0 so one dead row doesn't kill the page.

- `2d3b4e2` + `1f86e08` + `f0f9e7c` + `12957de` — *feat: crates.io column — 43rd column type (#38, then #39 commit-message rename)*
  - Net result: new `lib/integrations/crates.ts` (+182), `lib/columns/plugins/crates/` (+241 across 3 files), 3 registry edits, README News & web 9 → 10, column count 42 → 43.
  - The four-commit shape is a commit-message correction: the original #38 squash claimed "cluster 8 → 9, count 41 → 42" but PyPI had already landed first as the 42nd column, so crates.io is actually 43rd. PR #39 reverts the original squash, then reapplies the identical tree with the corrected message. The tree at `f0f9e7c` is identical to the tree at `2d3b4e2` — only the commit message changes.
  - Keyless `GET /api/v1/crates` fetcher with 5 sort axes (recent-downloads default — 90d trending / downloads — all-time / recent-updates / new / alpha). Optional `q=` search across name + description + keywords.
  - Three integration quirks: (1) User-Agent header is non-optional — anonymous requests without UA return 403 per crates.io's documented policy, so `minitor/1.0` is set on every call; (2) `recent_downloads` is a fixed 90d window (different from npm's last-week endpoint) — UI labels it "/90d" to avoid confusion; (3) `max_stable_version → max_version → newest_version` fallback chain renders pre-release-only crates correctly.
  - #DEA584 Rust ember orange accent (distinct from npm #CB3837 red, pypi #3776AB blue), `Box` icon visually evokes a crate (distinct from npm's `Package` and pypi's `Package2`).

**Impact:** News & web cluster expands from 8 → 10 in one day. Column count crosses 43. The three-axis registry coverage is the genuinely new surface — until this week minitor had one package registry (none); now it has three covering ~95% of the package ecosystems that AI tooling discussions reference. The commit-message-correction dance is operator hygiene catching itself in real time — the original squash message was inaccurate, and a separate PR fixed it cleanly without rewriting history.

### Theme 8: Substack handle parser accepts custom domains
**Summary:** A small but high-value bug fix that had been silently dropping pluralistic.net, astralcodexten.com, noahpinion.blog and other custom-domain Substacks. Bonus tell: the dialog placeholder text was suggesting `stratechery.com` — which isn't even on Substack and would have been rejected anyway.

**Commits:**
- `2c02247` — *fix(substack): accept custom-domain Substacks (pluralistic.net, astralcodexten.com) (#37)*
  - Changed `lib/integrations/substack.ts` (+39, -15): `ParsedHandle` now carries `host` (canonical hostname for the feed) alongside `handle` (display label). `handleFromInput` accepts any URL/host with a valid hostname, strips leading `www.`, defensively rejects bare `substack.com`. `parseHandles` dedups by host instead of handle so `mattyglesias` and `mattyglesias.substack.com` collapse to one feed. `tagWithPublication` uses real host for `publication`/`handle` so meta + author display reflect the actual publication.
  - Changed `lib/columns/plugins/substack/client.tsx` (+6, -4): placeholder swapped from non-Substack `stratechery.com` to real custom-domain Substack `pluralistic.net`; help text now documents the custom-domain case.
  - The fetch path already worked (all Substack hosts expose `/feed`) — only the input parser and dedup were limited.

**Impact:** Three of the most-cited independent newsletters (Doctorow's Pluralistic, Scott Alexander's Astral Codex Ten, Noah Smith's Noahpinion) were silently inaccessible until this fix. The placeholder swap is the more telling change: it implies the original feature was shipped without anyone actually trying to paste a high-profile Substack into it. Useful pattern to watch for in other column types.

---

## Developer Notes

- **New dependencies:** None added today. All new code is keyless or uses existing `gh`/curl/WebFetch primitives. Notable: the 22-skill aeon-agent sync (PR #44) and the upstream-sync workflow (aeon PR #170) both rely entirely on standard GitHub Actions + `gh` CLI machinery.
- **Breaking changes:** None. The dashboard prop additions (`gateway` on TopBar + SkillDetail) are additive — existing callers ignored — but `dashboard/app/page.tsx` was already passing the prop, so the wiring fix just removes a typecheck error that had been silently failing.
- **Architecture shifts:**
  - **aeon-agent inherits a weekly upstream-sync rail** (via the parent-repo workflow in aeon PR #170). This converts the "operator manually backports SKILL.md files every few days" pattern into "every fork opens a sync PR every Monday." The 22-skill bulk sync (PR #44) is a one-time catch-up; the workflow is the recurring rail.
  - **Six aeon-agent skills crossed the enabled threshold** — first time the fork has its own daily announcement channel (star-milestone), event-driven thread output (thread-formatter, score-gated), and Monday digests (operator-scorecard, ai-framework-watch).
- **Tech debt:**
  - aeon-agent's autoresearch-rewrite gap (aeon PRs #46–#136 not yet content-backported) is still unaddressed. Today's PR #44 closed the *catalog* gap but not the *quality* gap on existing skills.
  - aeon-agent's `refresh-x` and `article` skills still lack both `.error` and `.truncated` marker handling (called out in PR #43 body) — needs a deeper cleanup that adds both patterns at once rather than a one-line read.
  - The `--no-verify` in the upstream-sync workflow's conflict-commit path is now inline-documented (per the PR #170 second commit) — fine here because the commit is by design a "show reviewers what to resolve" marker, not a real commit.

## What's Next
- **fork-cohort enable** is the next obvious switch — PR #46 walked back contributor-spotlight specifically because fork-cohort is still off. Flipping fork-cohort enables both contributor-spotlight and fleet-state to actually do useful work on Sunday. Without it, contributor-spotlight has nothing to spotlight and fleet-state's NO_SOURCES exit is the most likely Monday outcome.
- **show-hn-draft enable** — still listed URGENT in MEMORY Next Priorities, not in PR #45's 6-skill batch. 300⭐ crossed; Show HN is the natural next move now that star-milestone and star-momentum-alert are firing.
- **aeon-agent autoresearch-evolution backports** — 80+ upstream PRs of content rewrites still pending. PR #44 closed the catalog gap; the quality gap is the next campaign.
- **`refresh-x` + `article` skill cleanup** — explicitly named in PR #43 body as needing a combined `.error` + `.truncated` patch.
- **Branches created but not merged today:** none — every PR opened in this window also closed in this window. PR #43 was opened 2026-05-14 morning, merged same afternoon; PRs #40, #41, #42 were yesterday's `feature`/`self-improve` PRs and merged today; PRs #169, #170, #171 in aeon were opened and merged within an hour of each other. The auto-merge loop is visibly working — 7 of the 15 substantive commits closed via auto-merge eligibility paths.
