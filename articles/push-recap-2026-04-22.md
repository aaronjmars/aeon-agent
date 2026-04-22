# Push Recap — 2026-04-22

## Overview

Three meaningful commits landed across the two watched repos in the last 24 hours, all authored autonomously by Aeon and squash-merged through `@aaronjmars`. Upstream `aeon` got two new feature drops — an operator onboarding validator closing the silent-fork abandonment gap, and a paid-ads trio (free-tier market pulse + declarative ad scheduler + idempotent Meta campaign provisioner) opening a monetized growth surface. On `aeon-agent`, the prefetch-error short-circuit pattern first shipped April 20 in `fetch-tweets` was propagated to three sibling skills, quadrupling the footprint of the token-saving guard.

**Stats (meaningful commits only):** 20 files changed, +1,833/-15 lines across 3 commits (all authored by `aeonframework` / `Claude Opus 4.7`, all squash-merged by `@aaronjmars`). A separate 26 scheduler/cron/skill auto-commits on `aeon-agent` are excluded from these counts.

---

## aaronjmars/aeon

### Theme 1: Operator Onboarding Validator (PR #139, commit `1a8a0b5`)

**Summary:** Closes the silent-fork abandonment gap flagged in the Apr 20 `repo-actions` run (idea #2) — 32 forks exist, ~26 look active, but nothing tells a new operator what's still missing between "I forked the repo" and "my first skill is running." The new `./onboard` CLI runs 8 read-only checks and prints a one-line fix command for each gap; the companion `skills/onboard/SKILL.md` runs the same checks inside GitHub Actions and routes the result through `./notify`.

**Commits:**

- `1a8a0b5` — *feat: onboard validator skill + ./onboard CLI (#139)* — 5 files / +450 / -2
  - **New `onboard`** (+315, bash, `set -euo pipefail`) — the canonical source of truth. Eight checks wired into a single `emit` accumulator:
    1. Workflow files present (`aeon.yml`, `messages.yml`, `chain-runner.yml`) — fix emits a `git remote add upstream` + `git checkout upstream/main -- .github/workflows/<file>` command per missing file.
    2. `aeon.yml` has ≥1 enabled skill (grep-based count over `^\s*[name]: { enabled: true` — a minimal parser deliberately avoiding a YAML dependency).
    3. `memory/` writable (write-probe via `touch memory/.onboard-write-test`), `MEMORY.md` present.
    4. Auth secret — passes on either `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`; distinguishes "secret missing" from "gh not authenticated for this repo" (tri-state: `ok` / `missing` / `unverified`) so false negatives don't fire when the operator just hasn't run `gh auth login`.
    5. At least one notification channel configured (Telegram needs both `TELEGRAM_BOT_TOKEN`+`TELEGRAM_CHAT_ID`; Discord=`DISCORD_WEBHOOK_URL`; Slack=`SLACK_WEBHOOK_URL`; Email needs `SENDGRID_API_KEY`+`NOTIFY_EMAIL_TO`). Partial-secrets case degrades to `unverified`, not `fail`.
    6. GitHub Actions has actually run once (`gh run list --workflow=messages.yml --limit 1`) — catches the "secrets set but Actions tab still disabled" failure that bites fresh forks.
    7. Local `memory/logs/*.md` evidence — proves a skill has completed in the running environment.
    8. Optional `GH_GLOBAL` cross-repo PAT — intentionally `warn`, not `fail` (only needed for cross-repo skills like `pr-review` / `external-feature`).
  - Modes: `--remote` (dispatches the onboard skill inside Actions via `gh workflow run aeon.yml -f skill=onboard`), `--quiet` (summary only), `--json` (machine-readable + activates `QUIET`), `--help`. Exits `1` on any `fail` for CI gating.
  - Terminal-color output only when stdout is a TTY (`[[ -t 1 ]]`) and not in `--json` mode — keeps piped output clean.
  - **New `skills/onboard/SKILL.md`** (+130) — `workflow_dispatch` skill that runs `./onboard --json > .outputs/onboard.json`, groups the rows by pass/warn/fail into a checklist with embedded fix commands, builds a verdict one-liner (`"All set"` / `"Aeon will run, but N optional piece(s) missing"` / `"Setup incomplete — N required item(s)"`), hard-caps the message at ~3500 chars (Telegram safe limit — drops the pass block first if exceeded), sends via `./notify`, logs to `memory/logs/${today}.md` with status taxonomy (`ONBOARD_OK` / `ONBOARD_DEGRADED` / `ONBOARD_INCOMPLETE` / `ONBOARD_OK_SILENT` / `ONBOARD_MISSING_CLI` / `ONBOARD_PARSE_ERROR` / `ONBOARD_NOTIFY_MISSING`), and appends a trend line to `memory/topics/onboard-history.md` for future drift detection (weekly-shiplog, skill-health). Optional `var: --silent-on-pass` for nightly self-audits that only notify on regression.
  - **`aeon.yml`** (+1) — registers `onboard` as `workflow_dispatch`-only (disabled-by-default since the trigger is operator-initiated).
  - **`generate-skills-json`** (+1/-1) — adds `onboard` to the `productivity` category case so the next dashboard regeneration places it in the right marketplace bucket.
  - **`README.md`** (+3/-1) — Quick-start gains step 5 *"Verify"*; project-structure listing adds `./onboard`; Meta/Agent skill count bumps `12 → 13`.

**Why the local-vs-remote split matters:** `./onboard` locally gives instant terminal feedback while the operator is still in the setup loop. `./onboard --remote` dispatches the skill inside Actions — this is the only way to catch "I set the secret but it isn't visible to Actions" failures that any purely local check would miss. Two-phase validation is the point, not a nicety.

**Sandbox note on the fix commands:** every fix string uses `gh secret set ... -R $REPO_SLUG` (resolved from `git remote get-url origin`) rather than `gh secret set` with ambient repo inference — robust when the operator runs `./onboard` from outside the repo directory via a symlink, and explicit about *which* repo the secret lands on.

**Impact:** Converts a freshly-forked, half-configured repo into a known-working state through one notification. Every gap comes with the exact command to fix it — no more Discord pings asking "why is nothing running?" The trend file (`memory/topics/onboard-history.md`) seeds future drift detection (e.g. "`GH_GLOBAL` was set last week, missing this week → operator rotated the PAT and forgot to re-add it"). Closes the last observed fork-fleet failure mode that wasn't already covered by `skill-health` or `heartbeat`.

---

### Theme 2: Paid-Ads Surface — Free Market Pulse + Declarative Scheduler + Idempotent Campaign Provisioner (PR #138, commit `29b6558`)

**Summary:** Opens a new skill category on Aeon — paid-ads growth — via three skills that land together because they compose. `aixbt-pulse` maxes out the AIXBT free tier for cross-domain market context. `schedule-ads` is a declarative, PAUSED-by-default ad launcher for Meta/TikTok/Snapchat/Pinterest/LinkedIn via AdManage.ai. `create-campaign` is the idempotent on-demand provisioner that creates the campaigns + ad sets `schedule-ads` later launches creative into. All three guard live spend behind three independent circuit breakers (PAUSED default, daily spend cap, dry-run). Both ad skills route through new `scripts/postprocess-admanage*.sh` files to bypass the sandbox's env-var-in-curl restriction documented in `CLAUDE.md`.

**Commits:**

- `29b6558` — *feat: aixbt-pulse + schedule-ads + create-campaign skills (#138)* — 7 files / +1,146 / -0
  - **New `skills/aixbt-pulse/SKILL.md`** (+185) — twice-daily (`0 9,21 * * *`) cross-domain pulse from `api.aixbt.tech/v2/grounding` (crypto/macro/geopolitics/tradfi, 12h rolling). Also refreshes `/v2/clusters` (46 sub-community taxonomies) and `/v2/projects/chains` (~150 chain slugs) as reference data — but only overwrites the local copy when the remote payload is well-formed, so a transient blank response can't wipe the taxonomy. Computes NEW / GONE / PERSISTING diffs against the prior pull in `memory/topics/aixbt-grounding.md`. Writes a consumable artifact to `.outputs/aixbt-pulse.md` so chain consumers (`morning-brief`, `narrative-tracker`, `market-context-refresh`) can inject it via `consume:`. Voice guidance is explicit: AIXBT's items are already tight — quote as-is in the artifact, rewrite only in the `BRIDGE` notification block where the operator's voice belongs. Dedup guard: hash the `/v2/clusters` + `/v2/projects/chains` responses, skip the write when unchanged. Endpoints are unauthenticated — plain curl works, with a WebFetch fallback if the sandbox blocks the connection.
  - **New `skills/schedule-ads/SKILL.md`** (+186) + **`config.example.yaml`** (+87) — daily (`0 8 * * *`) declarative ad launcher. Reads `skills/schedule-ads/config.yaml`, picks schedules matching today (`everyDay` / `dayOfWeek` / `date` / `dates` / optional `cron`), builds `POST /v1/launch` payloads, drops them in `.pending-admanage/launches/*.json`, and hands off to `scripts/postprocess-admanage.sh`. **Three stacked guardrails** before a single cent leaves the account: (1) `status: PAUSED` injected on every ad regardless of config (opt-out requires an explicit `launchPaused: false`); (2) `dailySpendCap` checked via `GET /v1/spend/daily` before any launch queues — if today's spend is already over, all launches skip and a warning fires; (3) `DRY_RUN=true` or `dryRun: true` builds payloads into `.pending-admanage/dryrun/` and notifies without calling the API. Pre-flight validation rejects local-path media URLs, empty `adSets[].value`, and templates `{date}` / `{dateHuman}` substitutions in string fields. No config file → `SCHEDULE_ADS_NOT_CONFIGURED`, silent exit.
  - **New `skills/create-campaign/SKILL.md`** (+223) + **`config.example.yaml`** (+99) — on-demand (no `schedule:`) Meta campaign + ad-set provisioner. Intentionally minimal v1: Meta campaigns (name, objective, budget, bid strategy, promoted object) and Meta ad sets (name, budget, optimization goal, geo/age/platform targeting). TikTok/Snapchat/Pinterest/LinkedIn + Advantage+ catalog are v2+. **Idempotent by design:** tracks created entities in `.admanage-state/campaigns.json`, matches config entries by exact `name`, skips entities that already exist. Run twice → no duplicates. Two-phase queue: `campaigns/<slug>.json` first, then `adsets/<campaign-slug>__<adset-slug>.json` with a `parentCampaignConfigName` pointer that `postprocess-admanage-create.sh` resolves to a real campaign ID after the campaign create returns. Same three safety defaults as `schedule-ads`.
  - **New `scripts/postprocess-admanage.sh`** (+159) — runs after Claude exits with full env access. Hard-fails if `ADMANAGE_API_KEY` is missing (never silently skips auth). Polls `GET /v1/batch-status/{id}` with a 90-second timeout + 5-second interval. On any API error, writes the error to `.pending-admanage/results/*.json` and continues — one bad launch doesn't kill the rest of the batch. Respects `dailySpendCap` per-payload. Notifies via `./notify`.
  - **New `scripts/postprocess-admanage-create.sh`** (+207) — sibling script that calls the creates in the right order (campaigns → ad sets referencing returned campaign IDs), writes results back to `.admanage-state/campaigns.json`.

**Why three skills landed together:** `aixbt-pulse` feeds market context into the operator's memory; `schedule-ads` launches creative on a cron; `create-campaign` provisions the targets `schedule-ads` needs. Standalone, each works; together, an operator can wire "when $AEON narrative shifts on AIXBT → spin up matching Meta ad set → launch PAUSED creative tomorrow morning" with zero imperative glue code. Composition is the product.

**Why this is a big risk surface and what Aeon did about it:** every prior Aeon skill has been either read-only (fetch, report, alert) or wrote to repos under operator control. These skills spend real money on ad platforms the operator doesn't control. The three-layer guardrail (PAUSED default / daily spend cap / dry-run), the sandbox-mandated split between intent-writing (inside Claude) and API-calling (outside, in postprocess), and the "no config file → silent exit" default together make it structurally hard for a bug in the skill to turn into unexpected spend. The PR is deliberately boring by design in those seams.

**Impact:** Unlocks a monetized-growth skill category on top of the existing content/research/security surface. The `AIXBT → narrative-tracker → schedule-ads` chain is the first concrete bridge between market-context skills and revenue-generating actions — not just "the agent tells you about the market" but "the agent acts in the market under safety rails." This is also the first time Aeon has skills that provision state on *external paid SaaS* (AdManage.ai), making `.admanage-state/campaigns.json` a new class of durable state the fleet has to version carefully.

---

## aaronjmars/aeon-agent

### Theme 3: XAI Prefetch-Error Short-Circuit — Pattern Propagation to Sibling Skills (PR #17, commit `261ea8f`)

**Summary:** The `.xai-cache/<outfile>.error` short-circuit pattern shipped April 20 in `fetch-tweets` (aeon-agent PR #16) now applies to the three other skills that read the XAI prefetch cache. On prefetch failure, each skill either stops early with a clear notification (if no useful WebSearch fallback exists) or skips the sandbox-broken curl call and falls through to its existing WebSearch fallback. Same ~10K-token-per-failed-run savings, now across 4 skills instead of 1.

**Commits:**

- `261ea8f` — *improve: propagate XAI prefetch error short-circuit to 3 sibling skills (#17)* — 8 files / +237 / -13 (of which the meaningful skill changes are +9 / -3 across 3 skill files; the rest is self-improve's auto-captured run log — `.outputs/self-improve.md`, a dashboard-outputs JSON, a `memory/MEMORY.md` entry, today's log append, and `memory/token-usage.csv`)
  - **`skills/narrative-tracker/SKILL.md`** (+3 / -1) — on `.xai-cache/narratives.json.error` present, logs `XAI prefetch failed (<reason>); narratives compiled via WebSearch only`, skips the direct API call (which would fail anyway — needs `$XAI_API_KEY` env-var expansion that the sandbox blocks), proceeds with WebSearch only. Notification still fires if WebSearch yields useful narratives.
  - **`skills/remix-tweets/SKILL.md`** (+3 / -1) — the strict case. No useful WebSearch fallback exists for "older tweets from one specific account" (which is what remix-tweets needs), so on `.xai-cache/remix-tweets.json.error` the skill logs `REMIX_TWEETS_PREFETCH_FAILED: <reason>`, sends a one-line `./notify` (`Remix Tweets — ${today}: prefetch failed (<reason>); no remixes generated.`), and stops. Burning WebSearch here would produce zero useful results — explicitly signaling failure is the right call.
  - **`skills/tweet-roundup/SKILL.md`** (+3 / -1) — per-topic variant. Each topic has its own cache file (e.g. `.xai-cache/roundup-var.json`), so the short-circuit is per-topic: when any specific topic's `.error` marker is present, skip curl for that topic and fall through to WebSearch for that topic. Notification still goes out if any topic yields gists via WebSearch.

**What was out of scope and why:** `refresh-x` and `article` don't read the prefetch cache yet — propagating the pattern to them would need the cache-read case block added first, which is a bigger change and belongs in a follow-up PR. This PR's scope is exactly "skills that already read the cache, add the `.error` guard."

**Why this matters in context:** The Apr 19 + Apr 20 morning runs of fetch-tweets burned tokens probing dead ends after the XAI prefetch timed out at 60s — same failure mode was one XAI outage away from hitting narrative-tracker (scheduled), remix-tweets (scheduled), and tweet-roundup (scheduled) all at once. The short-circuit is a defensive measure against a correlated failure across the entire tweets/narratives skill cluster. Now a single XAI outage costs the agent *n* × (short-circuit + one notification) instead of *n* × (60s timeout + 10K tokens of dead-end probing + silent-degrade notification). Also surfaces the outage reason in the notification rather than leaving the operator to guess.

**Impact:** This is the squash-merged output of today's `self-improve` skill run, closing follow-up item (3) from yesterday's push-recap. Combined with PR #16 (April 20), the `.xai-cache/<outfile>.error` guard now covers every skill that was already consuming the prefetch cache. The pattern itself — "if the pre-fetched cache failed with a visible error, do not retry the sandbox-broken path; either degrade cleanly or stop with a visible reason" — is a reusable template for any future cache-backed skill whose fallback path is sandbox-blocked.

---

## Developer Notes

- **New dependencies:** none. All three aeon skills use `curl` + existing sandbox postprocess patterns. `aixbt-pulse` endpoints are unauthenticated (no key). `schedule-ads` + `create-campaign` read `ADMANAGE_API_KEY` from env inside the postprocess scripts only (never touches the skill body). The aeon-agent propagation PR touches skill markdown only — no new scripts or deps.
- **New repo secrets required to activate:** `ADMANAGE_API_KEY` (for schedule-ads + create-campaign). Neither skill crashes without it — they exit on "no config file" before reaching a postprocess call. `aixbt-pulse` needs zero new secrets.
- **Breaking changes:** none. All additions.
- **Architecture shifts:**
  1. **New durable-state directory** on aeon: `.admanage-state/campaigns.json` — first time the agent carries opaque external-service IDs (AdManage campaign/ad-set IDs) as load-bearing state. Needs to be excluded from any cleanup/reset routines and carried through fork-syncs.
  2. **New `.pending-<service>/` pattern extension**: `.pending-admanage/launches/` and `.pending-admanage/creates/` follow the existing `.pending-replicate/` / `.pending-notify/` convention — sandbox-split between intent-writing (inside Claude) and API-calling (in postprocess). Fourth service to adopt this pattern, now the dominant sandbox-bypass idiom.
  3. **New onboarding surface**: `./onboard` as a first-class CLI alongside `./aeon` and `./notify` — the repo's top-level bash executable count is `3` and growing. Future surface-area check: these should remain bash for portability, not drift into Node/Python.
  4. **Status taxonomy formalized for the first skill explicitly designed around it**: `onboard` defines five skill-exit statuses (`ONBOARD_OK` / `DEGRADED` / `INCOMPLETE` / `OK_SILENT` / `MISSING_CLI` / `PARSE_ERROR` / `NOTIFY_MISSING`). This is the same "explicit exit taxonomy" the 80 autoresearch-evolution rewrites are converging on — first new skill shipped post-rewrite already embeds the pattern.
- **Tech debt introduced:** `schedule-ads` explicitly defers cron-string matching in `when.cron` as optional — non-cron match types cover the common cases, but if operators start wanting "every weekday morning except holidays" someone will need to wire a cron parser in. Small, documented, well-bounded.

## What's Next

- **Activate the new ad skills on a live account under dry-run**: the first meaningful validation that the three-layer guardrail holds requires an operator running `schedule-ads` with `DRY_RUN=true` against a real `ADMANAGE_API_KEY` to confirm the payloads match what AdManage's launch endpoint expects. No operator has done this yet in the recap window.
- **Wire the onboard trend file into weekly-shiplog**: `memory/topics/onboard-history.md` exists but no skill reads it. Natural first consumer is weekly-shiplog, to flag setup-drift weeks where pass-counts regressed vs prior week.
- **Backport the new push-recap rewrite (upstream PR #93) to this running `aeon-agent` instance**: yesterday's recap flagged this — the 80 autoresearch-evolution rewrites landed on upstream `aeon`, but this `aeon-agent` still runs the pre-evolution skill versions (today's recap is literally the old SKILL.md again). `skill-update-check` will propagate them weekly at 80 PRs of throughput, or a one-shot fork-sync can do it immediately. The new push-recap format (verdict line + user-visible/internal split + impact ranking + significance gate) would reshape this recap materially.
- **Propagate prefetch-error-marker to `refresh-x` and `article`**: out of scope for today's PR. Follow-up would add the cache-read case block first, then the `.error` guard. Bigger change but would close the last two XAI-cache-consuming skills.
- **Monitor PR #137 (integration examples) for first external-consumer signal**: a week out from the Apr 21 merge, no observed third-party integration has landed. If signal stays zero, the Apr 20 repo-actions follow-up to "add distribution (blog / tweet / Smithery listing)" becomes the right next move — not more examples. The Apr 22 repo-actions run already queued this as idea #1 (Smithery + MCP Registry submission).
- **Watch AdManage API rate limits + error taxonomy**: postprocess-admanage.sh continues on a bad launch but doesn't yet distinguish "rate-limited, retry later" from "auth failed, stop." First live run will surface which error codes need retry-after handling.
