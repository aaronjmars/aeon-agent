# Push Recap — 2026-05-07

## Overview
Four substantive PRs landed across three repos in the last 24h: two in `aeon` (skill template library + a per-fork v4 readiness checklist), one in `minitor` (Stack Overflow column), and one production hardening fix in `aeon-agent` (xai-prefetch token-budget bug). Theme of the day is *operator surface area* — three of the four PRs are about lowering the cost of forking, upgrading, or extending the framework before the v4 release lands.

**Stats:** 22 files changed, +1,534 / −12 lines across 4 substantive commits. Plus 30 routine cron auto-commits in `aeon-agent` (skill executions writing back to the repo).

---

## aaronjmars/aeon

### Theme 1: Activation surface for new fork operators

**Summary:** A pre-built starter library and CLI bootstrapper that converts the question "I just forked aeon — how do I add my own skill?" from a multi-hour reverse-engineering exercise into a one-command operation. The activation gap had been called out as an "Open unbuilt" in MEMORY.md since April 18 and is one of the more expensive things a new operator pays for currently.

**Commits:**
- `8fcf2f5` — *feat: skill template library — six starters + ./new-from-template (#161)* — +755 / −0
  - New `templates/` directory with six runnable starter skills, each a complete `SKILL.md` keyed by `[REPLACE: KEY]` tokens — `crypto-tracker` (token price/volume daily report with anomaly alerts), `research-digest` (daily RSS + WebSearch digest), `code-reviewer` (first-touch external-PR review with verdict + welcome comment), `social-monitor` (X + Reddit mention sweep with sentiment), `deploy-watcher` (Vercel deploys vs. last-green baseline), `community-manager` (Discord/Telegram/Slack channel digest with open-question detection).
  - New `new-from-template` bash CLI (254 lines): `--list` enumerates templates, `<template> --tokens` prints the required `[REPLACE: KEY]` fields, `<template> <skill-name> --var KEY=VALUE...` copies the chosen template into `skills/<skill-name>/`, sed-substitutes every token, and registers a disabled entry in `aeon.yml` immediately before the fallback marker.
  - Each template ships with its own *Sandbox note* (prefetch / postprocess fallback) so the starter is runnable on GitHub Actions out of the box, not just locally.
  - Second commit on the PR fixes a bash-3.2 compat issue (replaced `declare -A` with parallel `VAR_KEYS` / `VAR_VALS` arrays so the script runs on stock macOS `/bin/bash`) and closes a sed-injection path by validating `--var KEY` against `^[A-Z_][A-Z0-9_]*$` before assembling the sed pipeline.
  - One-line addition to `README.md` points operators at `templates/` directly under the onboarding flow.

**Impact:** A new operator can now scaffold a working skill in roughly 30 seconds — `./new-from-template crypto-tracker my-eth-watch --var TOKEN_SYMBOL=ETH --var COINGECKO_ID=ethereum --var ALERT_THRESHOLD_PCT=10` and the skill is on disk, registered (disabled) in `aeon.yml`, and ready to flip on. The hardening on the second commit matters because the CLI runs untrusted user input through sed — without the regex validation, a crafted `KEY` like `'FOO]/g; s|.*|PWNED|; s|[='` would be a code-execution path.

### Theme 2: v4 upgrade safety net

**Summary:** A workflow_dispatch-only readiness checker that audits a fork's actual configuration against an embedded change manifest and emits a personalized Safe / Review / Custom / Action breakdown. With v4 announced for ~2 weeks out and 40+ forks running on the current architecture, this exists to surface breakages *before* operators pull, not after a cron fires on a now-removed key.

**Commits:**
- `3450b31` — *feat(v4-readiness): per-fork v4 upgrade readiness checklist (#160)* — +310 / −7
  - New skill `skills/v4-readiness/SKILL.md` (289 lines). Reads the fork's `aeon.yml`, `skills.json`, `MEMORY.md`, and `skills/*/SKILL.md` frontmatter and cross-references against an embedded v4 change manifest (Safe / Review / Removed tables) to emit a personalized readiness verdict per pattern.
  - Two run modes — local (pure file I/O over the working tree, no curl, no env-var-in-headers, no prefetch) and remote (`var=owner/repo` reads via `gh api repos/.../contents/...`, ~5 calls per fork, well under the 5,000/h `GITHUB_TOKEN` budget for ad-hoc fleet surveys).
  - Read-only across the fork by design — never auto-mutates `aeon.yml`, never opens a PR, never pulls upstream. Operator dispatches manually pre-announcement, at v4 announcement, during the upgrade, and post-upgrade. Ships `enabled: false` in `aeon.yml` — no cron at all, just `workflow_dispatch`.
  - The change manifest is embedded inside `SKILL.md` itself rather than a separate config file, so it travels per-fork. The Safe table is seeded today with the patterns confirmed stable (SKILL.md frontmatter, `./notify`, `memory/` layout, `articles/` output convention, `gh api` usage). The Review table is seeded with the patterns known to be in scope (chains runner interface, reactive triggers, schedule syntax, model selectors, gateway block, MCP tool naming, `add-skill`/`add-mcp`/`add-a2a` CLIs, `skills.json` schema, dashboard catalog shape). The Removed table is empty by design until the actual v4 PRs land — operators populate it row-by-row as the announcements come in, and each row has a one-line migration recipe.
  - `aeon.yml` gets a single new entry; `skills.json` is bumped 110 → 111 with a `productivity` category placement; `generate-skills-json` learns the new skill so future regenerations don't drop it.

**Impact:** Lead-time gap between a v4 announcement and the actual release is now actionable rather than aspirational. Each fork operator can dispatch this skill four times across the upgrade window (pre-announcement / at-announcement / mid-upgrade / post-upgrade) and watch the Action-items count shrink as they make changes. The fleet-survey mode (`var=owner/repo`) lets the upstream maintainer audit other operators' forks directly — useful for figuring out which v4 patterns will hurt the most before locking in the breaking changes.

---

## aaronjmars/aeon-agent

### Theme 3: Production hardening — xai-prefetch token budget

**Summary:** A one-line API parameter change with outsized impact: the shared XAI search helper was hitting the API default `max_output_tokens` and silently truncating fetch-tweets outputs to 2 results instead of the 10+ requested, because grok-4-1-fast spends most of the default budget on its reasoning trace before producing visible output.

**Commits:**
- `99af20a` — *improve(xai-prefetch): set max_output_tokens=16384 to prevent reasoning-induced truncation (#32)* — +6 / −1
  - Single edit to `scripts/prefetch-xai.sh`: adds `max_output_tokens: 16384` to the JSON payload sent to the XAI Responses API. The helper now requests ~16k of generation budget instead of the API default.
  - Five-line comment block above the change documents *why* — grok-4-1-fast is a thinking model that can spend 5–7k tokens on reasoning alone; the May 6 fetch-tweets run logged "Extracted 2 tweets — cache output was truncated at token limit (7,354 total tokens, 6,486 used for reasoning)" even though the prompt asked for 10+. 16384 leaves ~9k for output text after typical reasoning, enough for a 10–15 tweet numbered list.
  - Affects every consumer of the helper: `fetch-tweets`, `refresh-x`, `remix-tweets`, `tweet-roundup`, `narrative-tracker`, `article` — six skills that all share the same prefetch path.

**Impact:** Quality regression that would have silently degraded six skills until someone noticed signal loss is now closed before the next cron cycle. Verified on the current `2026-05-07` log: `fetch-tweets` returned 7 tweets this morning vs. the 2 it returned yesterday under the old budget — the helper is now producing the breadth its consumers need.

### Theme 4: Routine cron activity (not code changes)

30 auto-commits from skills executing on their normal schedules and writing their state back to the repo: scheduler state updates (8), per-skill `chore(<skill>): auto-commit` pairs (10), `chore(cron): <skill> success` markers (11), and one substantive tweet-allocator allocation commit (`eeafc1a` — distributed $10 in $AEON across 5 tweeters). These reflect the skill runtime working as expected — `feature`, `repo-pulse`, `tweet-allocator`, `fetch-tweets`, `token-report`, `heartbeat`, `memory-flush`, `project-lens`, `repo-article`, `push-recap` all ran cleanly in the window.

---

## aaronjmars/minitor

### Theme 5: Dashboard column expansion — Stack Overflow

**Summary:** Stack Overflow becomes the 36th column type in the keyless-feed dashboard, filling the Q&A surface gap in the dev/community-feed cluster (HN + Lobsters + Reddit had the news/discussion side covered but no question-answer surface).

**Commits:**
- `ad07685` — *feat(plugins): add stack-overflow column type (#29)* — +463 / −4
  - New `lib/integrations/stackoverflow.ts` (187 lines). Hits Stack Exchange API 2.3 `/questions` on the `stackoverflow` site, mapping the column's mode → SE's sort param (`hot`/`votes`/`creation`/`week`/`month`); newest aliases to `creation` to match the framework's mode vocabulary. Anonymous quota is 300 req/IP/day, well above polling cadence. Includes a targeted HTML-entity decoder for question titles (Stack Exchange escapes `&quot;` / `&#39;` / `&amp;` etc.) — small fixed entity set so a one-shot decoder beats pulling in a full HTML parser.
  - Tag normaliser converts user-supplied comma- or space-separated tag lists into Stack Exchange's `;` syntax, deduplicates, and caps at five tags (the API's AND-filter limit).
  - New three-file plugin under `lib/columns/plugins/stack-overflow/`: `plugin.ts` (51 lines, column metadata + mode/tag schema), `server.ts` (38 lines, fetch wiring), `client.tsx` (177 lines, item renderer with score / answers / views footer and an "accepted" badge when the question has an accepted answer).
  - Three registry edits — `manifest.ts`, `registry.ts`, `server-registry.ts` — wire the new plugin into the column-type registry on both client and server.
  - `README.md` bumped — column count `35 → 36`, news cluster `5 → 6`, hero paragraph and keyless-columns line both pick up Stack Overflow.
  - Brand orange `#F48024` keeps it visually distinct from HN orange and Reddit orange-red (a recurring constraint as the dashboard accumulates orange-spectrum sources).
  - Second commit on the PR adds a `User-Agent` header to SE API requests — matches the convention every other integration in the repo uses, and avoids cooperative-throttling issues SE silently applies to UA-less anonymous traffic from busy egress IPs.

**Impact:** First Q&A-shaped column in the dashboard. Stack Overflow's tag filter (e.g. tracking `[react] [typescript]` or `[rust] [async]`) gives operators something the existing news columns can't — a stream of *unsolved* technical questions, ranked by activity, useful both as a research surface and as a "what is the community currently stuck on" radar.

---

## Developer Notes

- **New dependencies:** None. All four PRs land without adding npm/cargo/pip packages — `new-from-template` is bash-only, `v4-readiness` is pure file I/O + `gh api`, the xai-prefetch fix is a single JSON field, and the Stack Overflow plugin uses native `fetch`.
- **Breaking changes:** None. The xai-prefetch change is API-compatible (raising a token cap can't reduce previously-working output). The new skills and column ship `enabled: false` (v4-readiness) or as additive plugin entries (stack-overflow) — neither displaces existing behavior.
- **Architecture shifts:** Two patterns worth flagging. (1) The `templates/` directory is the first time aeon stores deliberately-incomplete skills (token placeholders) — the convention `[REPLACE: KEY]` plus `--var KEY=VALUE` is a primitive that future skills could lean on. (2) v4-readiness is the first skill whose change-manifest table lives in its own `SKILL.md` rather than in a sibling state file — a deliberate choice so the manifest travels per-fork without an extra config layer.
- **Tech debt:** The v4-readiness Removed table is empty by design — it has to be filled in row-by-row as v4 PRs land upstream, and that hand-off is the operator's responsibility. If the manifest stays empty when v4 ships, the readiness verdict will be optimistically clean.
- **Security note:** The bash-3.2 compat fix on `new-from-template` came bundled with a sed-injection close-out — `--var KEY=` values now have to match `^[A-Z_][A-Z0-9_]*$` before they reach the sed pipeline. The fix is correct; worth flagging because the original pre-fix CLI was briefly merged without the validation.

## What's Next

- **v4 manifest population.** v4-readiness ships with a seeded Review table but an empty Removed table. The next step is whoever owns v4 starts populating it row-by-row as PRs land — each row needs a one-line migration recipe so the readiness verdict can convert it into an action item.
- **Enable the new skills upstream.** Per MEMORY.md "Next Priorities," several new skills are merged but `enabled: false` in `aeon.yml` (skill-freshness PR #157, star-momentum-alert PR #159, v4-readiness PR #160, skill-template-library PR #161 itself). Backports to `aeon-agent` are also outstanding for several of these.
- **xai-prefetch followup not needed locally.** The May-6 max_output_tokens incident is now closed in `aeon-agent` (this PR) and was already shipped upstream in `aeon` per MEMORY.md. No further action; just monitor the next 24h of `fetch-tweets` runs to confirm the breadth holds.
- **Templates wave 2.** The six starters cover crypto / research / code-review / social / deploys / community. Adjacent gaps: log-watcher, status-page-monitor, RSS-to-Telegram broadcaster, on-call-summary. Worth opening as a follow-up issue rather than a same-day extension PR.
