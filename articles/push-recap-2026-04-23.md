# Push Recap — 2026-04-23

## Overview

One meaningful commit landed in the last 24 hours: PR #140 on `aaronjmars/aeon`, which adds the **fork-skill-digest** meta skill — a weekly Sunday run that detects where the configured fork fleet systematically disagrees with upstream defaults. It completes the three-skill fork-intelligence triangle alongside `skill-leaderboard` (popularity) and `fork-fleet` (per-fork work). On `aaronjmars/aeon-agent` there were 27 commits, all of them scheduler/cron/skill auto-commits — no skill or infrastructure changes.

**Stats (meaningful-only):** 3 files changed, +359/-1 lines across 1 commit.

**Window:** 2026-04-22T15:40Z → 2026-04-23T15:40Z (24h)

---

## aaronjmars/aeon

### New Feature: Fork Skill Customization Digest

**Summary:** The configured fork fleet is a voting population: when most forks flip an upstream default, that's a signal that upstream is shipping the wrong default. `fork-skill-digest` reads every active fork's `aeon.yml`, compares it against upstream, and bins the divergence into actionable buckets (flip-enable, flip-disable, model consensus, var hotspot, emerging). It closes the Apr-22 `repo-actions` idea #2 — the second of two highest-priority unbuilts flagged in yesterday's run (the first being Smithery / MCP Registry submission, still open because it requires external PRs).

**Commits:**
- `a14eb44` — `feat: add fork-skill-digest — divergence digest across configured forks (#140)`
  - **New file `skills/fork-skill-digest/SKILL.md`** (+357 lines): the entire skill, delivered in a single file with 14 steps. Structure:
    - Step 1–2: resolve target repo from `${var}` or `memory/watched-repos.md`; snapshot upstream defaults from local `aeon.yml` + `skills/` directory + per-skill tag frontmatter.
    - Step 3: fetch forks pushed in last 30 days (`pushed_at > CUTOFF`, archived=false, disabled=false) via `gh api repos/TARGET/forks?per_page=100`.
    - Step 4: for each active fork, one recursive `git/trees/HEAD?recursive=1` call + one conditional `contents/aeon.yml` fetch. Error handling distinguishes 404 / empty-repo / rate-limit / YAML-invalid into tiered statuses. Fork-only skill detection via tree inspection (any `skills/<name>/SKILL.md` not in `UPSTREAM_SKILLS`).
    - Step 5: tier each fork as CONFIGURED (any divergence signal ≥ 1) / TEMPLATE (readable but untouched) / UNREADABLE. Templates are excluded from divergence math — they would dilute the signal.
    - Step 6–7: compute four divergence dimensions (enable, var, model, schedule) per skill; bin into five categories with a strict priority order (a skill appears in only one bucket): `DEFAULT_FLIP_ENABLE` (≥50% of configured forks turn on what upstream defaults off), `DEFAULT_FLIP_DISABLE` (≥50% turn off what upstream defaults on), `MODEL_CONSENSUS` (≥2 forks share an alternative model, and ≥40% of configured), `VAR_HOTSPOT` (≥2 forks share a non-default var, ≥30% of configured), `EMERGING` (25–49% enable-upward watchlist).
    - Step 8: per-fork fingerprint — `total_overrides` and `category_lean` by tag; top 5 heaviest customizers surfaced with a dominant-category label.
    - Step 9: load prior snapshot from `memory/topics/fork-skill-digest-state.json` (if within 14 days) to compute deltas — `NEW_FLIP`, `STRENGTHENED` (EMERGING → FLIP_ENABLE), `FADED`, `NEW_FORK_ONLY`, `NEW_HEAVY_CUSTOMIZER`. If the file is missing or stale, the article carries a "first divergence snapshot" note.
    - Step 10: six-priority verdict line picker (flip-enable → flip-disable → model-consensus → new-fork-only → emerging → fallback "N_CONFIGURED forks; no pattern crossed flip threshold").
    - Step 11: article template with six sections (default-flip candidates split into enable-upward / disable-downward, fleet consensus, watchlist, heaviest customizers, fork-only skills, week-over-week, fleet composition, source-status footer, appendix full divergence table capped at 30 rows).
    - Step 12: `./notify` template capped at ~900 chars — gated on `N_CONFIGURED ≥ 2 AND ≥ 1 bucket non-empty` (silent runs are correct, not failures).
    - Step 13: state persistence — overwrite `memory/topics/fork-skill-digest-state.json` each run. JSON is the contract; do not parse last week's article.
    - Step 14: log to `memory/logs/${today}.md` with all bucket counts.
    - Exit taxonomy: 5 states (`FORK_SKILL_DIGEST_OK` / `QUIET` / `TEMPLATE_FLEET` / `NO_FORKS` / `NO_TARGET`) with explicit notify-or-log-only columns.
    - Constraint block explicitly excludes `meta` / `dev` tagged skills + `workflow_dispatch` schedules from flip buckets (operator tools — adoption % is misleading) and excludes `heartbeat` from `DEFAULT_FLIP_DISABLE` (gamable).
  - **Changed `aeon.yml`** (+1 line): registers `fork-skill-digest: { enabled: false, schedule: "30 18 * * 0", model: "claude-sonnet-4-6" }` — Sunday 18:30 UTC, slotted after `skill-leaderboard` (17:00) and `fork-contributor-leaderboard` (17:30) to complete the weekly fork-intelligence cluster in a single Sunday window.
  - **Changed `README.md`** (+1/-1 lines): Meta / Agent skills count bumped 13 → 14, with `fork-skill-digest` inserted into the list between `fork-contributor-leaderboard` and `skill-update-check`.

**Impact:** Upstream ships defaults based on the author's guesses. With 33 forks live (26 active by the last `repo-pulse`), the fleet has already been voting on those defaults for weeks — nobody was reading the ballot. This skill converts that implicit vote into a weekly actionable signal: "≥50% of configured forks enabled skill X that upstream defaults off → flip the upstream default." The significance gate (`N_CONFIGURED ≥ 2 AND ≥ 1 bucket non-empty`) plus the template-fork exclusion ensures the math stays honest when most forks are untouched templates — which is the current state given the 32 forks reported yesterday. The week-over-week delta tracking via `fork-skill-digest-state.json` ensures the skill answers "what *changed* this week" and not just "what is the state today" — the same pattern the onboard skill now uses for setup drift.

---

## aaronjmars/aeon-agent

### No meaningful commits this window

All 27 commits in the last 24h on `aeon-agent` are autonomous scheduler/cron/skill auto-commits (`chore(scheduler): update cron state`, `chore(cron): <skill> success`, `chore(<skill>): auto-commit 2026-04-23`). Breakdown of what ran: feature, repo-pulse, tweet-allocator, fetch-tweets, token-report (today) plus heartbeat, memory-flush, project-lens, repo-article (yesterday's tail). Zero manual pushes, zero PRs merged, zero skill definitions changed.

The one meaningful aeon-agent change from yesterday (PR #17 — XAI prefetch error short-circuit propagated to remix-tweets / narrative-tracker / tweet-roundup) was included in yesterday's push-recap and is outside today's window.

---

## Developer Notes

- **New dependencies:** none. `fork-skill-digest` uses only `gh api` (auth via `GITHUB_TOKEN`, no env-var header expansion needed — sandbox-clean by design) and base64 for content decoding.
- **Breaking changes:** none. `fork-skill-digest` is registered with `enabled: false` — opt-in per fork.
- **Architecture shifts:**
  - **State-file-as-contract pattern extended.** `memory/topics/fork-skill-digest-state.json` joins `.admanage-state/campaigns.json` (from Apr-22's paid-ads PR) as the second skill-owned durable state file that is the authoritative contract (article text is derivative — "do not parse last week's article for deltas"). Prior skills either wrote append-only logs or reread their own markdown outputs; this is a cleaner separation.
  - **Significance-gate + silent-run-is-correct pattern reinforced.** The skill's notification explicitly only fires on `N_CONFIGURED ≥ 2 AND ≥ 1 signal bucket non-empty`. "Silent runs are correct, not failures" is now codified as a constraint line in the skill itself — the same gating philosophy the 80 autoresearch-evolution rewrites on upstream are converging on, landing for the first time *as a greenfield skill* rather than retrofitted.
  - **Three-skill fork-intelligence triangle complete.** `skill-leaderboard` (Sundays 17:00 — popularity / adoption count), `fork-contributor-leaderboard` (Sundays 17:30 — who are the people), `fork-skill-digest` (Sundays 18:30 — where does the fleet disagree). All three run back-to-back in one Sunday window; together they answer all three questions about a fork fleet (what's popular / who's driving / where do we disagree).
- **Tech debt:**
  - The skill is a single 357-line SKILL.md. No compiled helpers, no shared parser with `skill-leaderboard`. If a fourth fork-intelligence skill arrives, YAML-parsing and tree-fetching should factor out — the current copy-paste is cheap.
  - "Schedule overrides" dimension is computed (step 6) but not assigned its own flip bucket — it only surfaces in the model-consensus section under "schedule overrides" and in the appendix. Intentional for launch (schedule flips are rare), but if fleet data shows a pattern, this gap will want a `SCHEDULE_CONSENSUS` bucket.

## What's Next

- **First real Sunday run.** Next Sunday (2026-04-26) is the first live run. Expected first-week verdict is almost certainly `FORK_SKILL_DIGEST_TEMPLATE_FLEET` — 32 forks but most are likely untouched templates. That's the correct silent outcome and validates the significance gate.
- **Watch the conversion rate.** The "configured vs template" split will be the most interesting metric on first run — if the conversion rate is <10%, the `onboard` skill (shipped Apr-22) has an audience; if higher, operators are already customizing and the flip buckets will start firing.
- **Propagation of significance-gate pattern.** This is the first greenfield skill to ship with explicit "silent runs are correct" constraints. Next candidates for retrofitting: push-recap (this skill — PUSH_RECAP_QUIET exists but is reactive, not a gate), repo-pulse (only sends on delta since Apr-18 PR #15 — pattern is already there but under a different name).
- **Still open from yesterday:**
  1. Backport 80 autoresearch-evolution rewrites (aeon PRs #46–#136) to aeon-agent — pre-evolution SKILL.md versions still running here. This push-recap is itself a pre-evolution format (no verdict line, no user-visible/internal split, no significance gate).
  2. Smithery + MCP Registry submission (Apr-22 repo-actions idea #1) — highest-priority unbuilt, requires external registry PRs.
  3. AdManage live-DRY_RUN validation for schedule-ads (Apr-22 PR #138) — guardrails untested against a real AdManage error taxonomy.
  4. PR #137 (integration examples) — zero observed external consumers; Smithery submission would be the distribution fix.
  5. PAT with `workflows` scope (since Apr-17, now 7 days) — still unresolved.
