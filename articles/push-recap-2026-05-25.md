# Push Recap — 2026-05-25

## Overview

13 substantive commits landed across the three watched repos in the last 24 hours (plus ~30 routine scheduler/auto-commit commits in aeon-agent that are excluded from the detail below). The day's thrust was **hardening and distribution, not new agent capability**: aeon took two CI-security patches from its AntFleet audit, closed the last open AntFleet High, registered the 34 skills that an earlier port had added to the catalog but never wired into the scheduler, and absorbed three community/ecosystem doc additions. aeon-agent backported the community skill-pack install protocol and a config validator, and made `fetch-tweets` fail loudly with operator-actionable guidance. minitor turned its dashboard columns from static panels into active, self-refreshing, alert-firing surfaces.

**Stats:** 46 files changed, +3,198 / -58 across 13 substantive commits by 4 distinct authors (Aeon bot/`@aaronjmars`, `AntFleet`/antfleet-ops audit account, `LiquidPad` bot, `Clint`).

| Repo | Commits | Diff | Files |
|------|---------|------|-------|
| aaronjmars/aeon | 8 | +556 / -33 | 14 |
| aaronjmars/aeon-agent | 3 | +1,459 / -11 | 12 |
| aaronjmars/minitor | 2 | +1,183 / -14 | 20 |

---

## aaronjmars/aeon

### CI Security Hardening — AntFleet two-model review (bench-aeon PR #31)

**Summary:** Two findings from AntFleet's two-model review of the run workflow were patched. Both are classic CI footguns: untrusted input flowing into a shell, and fragile quoting in a parser. Neither changes behavior on a well-formed input — they close the door on the malformed/hostile case.

**Commits:**
- `e01b739` — fix(ci): guard workflow_dispatch inputs against shell injection (#222)
  - Changed `.github/workflows/aeon.yml` (+9, -3): The "Determine skill" step previously did `echo "name=${{ inputs.skill }}" >> "$GITHUB_OUTPUT"` — i.e. GitHub Actions template-substituted the dispatch input *directly into the bash source* before the shell ran it. A skill name like `foo"; rm -rf . #` would have been interpolated verbatim into the script. The diff moves the value into a step-level `env: INPUT_SKILL: ${{ inputs.skill }}` and validates it against `^[a-zA-Z0-9_-]+$` (failing the run with `::error::` if it doesn't match) before writing it out. The same treatment is applied in the Run step: `SKILL_NAME` and `INPUT_MODEL` move from inline `${{ ... }}` interpolation to step-level `env:` so the values arrive through the environment, never the script text. `workflow_call` inherits the same path via `inputs.skill`.
  - Finding ID: H-INJECT.
- `ab40ef7` — fix(run): replace fragile tr-d quoting in GATEWAY provider parsing (#223)
  - Changed `.github/workflows/aeon.yml` (+1, -1): The AI-Gateway provider parse used `... | tr -d ' "'"'"` — a quoting chain trying to strip spaces, double-quotes, and single-quotes that was malformed and threw shell parse errors. Replaced with two clear `sed` passes: `sed 's/.*provider:[[:space:]]*//'` then `sed "s/[\"' ]//g"`, with the fallback shifted to `GATEWAY="${GATEWAY:-direct}"` on the next line.
  - Finding ID: H-GATEWAY.

**Impact:** The run workflow is the entry point every dispatched skill flows through and is reachable by anyone who can trigger a `workflow_dispatch`. Injection via the `skill` input is now structurally blocked (allowlist-validated, env-passed), and the gateway parser no longer crashes on its own quoting. Both patches were authored by the antfleet-ops audit account — the audit bot continuing to write the fixes for the findings it raises.

### Closing the Last Open AntFleet High

**Summary:** H1 was the final unresolved High on AntFleet's Issue #184 bench audit. It's a silent-undercount bug — the worst failure class for a readiness check, because it produces false-clean verdicts.

**Commits:**
- `3417c60` — fix(v4-readiness): close Issue #184 H1 — align manifest references with read set (#226)
  - Changed `skills/v4-readiness/SKILL.md` (+44, -9): The skill's Review table named four files (`mcp-server/src/index.ts`, `.outputs/*.md`, `chain-runner.yml`, `dashboard/lib/catalog.ts`) that its Reads section never actually loaded — so the audit literally could not detect usage in those files and silently undercounted Review items, letting an operator get a false-clean READY. The fix adds the four files as optional inputs in Config + Step 2, introduces a `review_unscanned[]` bucket so any Review row whose backing file isn't readable on a fork surfaces as a visible coverage-gap row instead of being silently dropped, and escalates the run to `V4_READINESS_PARTIAL` whenever any Review row is unscanned — making silent false-clean READY structurally unreachable. Also refreshes the Removed-table audit footer to `Last audited: 2026-05-24` with an embedded audit-method block, and adds an inline `<!-- Issue #184 H1 audit -->` invariant comment so a future manifest edit can't quietly re-break it.

**Impact:** With 111+ forks running pre-upgrade workflows, a readiness check that under-reports is actively dangerous. Per the repo's own tracking, this closes the last open AntFleet High (H4/H9 were already handled earlier in the week). The skill stays read-only, `workflow_dispatch`-only, `enabled: false`.

### New Skill — ecosystem-pulse

**Summary:** A new weekly liveness monitor for the projects listed in `ECOSYSTEM.md`. It answers "which ecosystem projects are alive, which went quiet, and who's new" without ever editing the curated list.

**Commits:**
- `45658de` — feat: add ecosystem-pulse skill (#227)
  - New file `skills/ecosystem-pulse/SKILL.md` (+402): Resolves each `ECOSYSTEM.md` project to a GitHub repo via an operator-maintained map (`memory/topics/ecosystem-pulse-map.json`) or a strict best-effort `gh search`, then buckets by last-push recency (ACTIVE ≤7d / RECENT ≤30d / COLD >30d / X-only / Unresolved), surfaces releases in the 7-day window, and reports week-over-week bucket transitions, star deltas, and new entrants. Designed read-only against `ECOSYSTEM.md` (curation stays a human PR) and never auto-populates the resolver map with guessed repos — a search hit is used for one run and flagged `(auto-matched, unverified)`. "X-only" is treated as distinct from COLD (no public repo = unmeasurable, not inactive). 7-status exit taxonomy (OK/QUIET/DRY_RUN/PARTIAL/NO_ECOSYSTEM_FILE/STATE_CORRUPT/BAD_VAR) with gated notify (QUIET once a baseline exists and nothing moved).
  - Changed `aeon.yml` (+1) and `skills.json` (+13, -1): registered disabled, Mon 11:00 UTC, sonnet-4-6; catalog total 155 → 156.

**Impact:** Slots into the Monday intelligence stack after `competitor-launch-radar` (10:00). Where `ai-framework-watch` tracks a fixed 9-framework cohort, this measures the open-ended ECOSYSTEM.md list — closing the "is the broader ecosystem actually alive?" blind spot. Disabled until the operator opts in.

### Wiring the 34 Ported Skills

**Summary:** PR #219 earlier in the week ("Port 34 skills") added 34 skill directories and bumped `skills.json` to 156, but never registered them in `aeon.yml` — so they couldn't be scheduled, couldn't run, and didn't appear as dashboard toggles. This commit closes that gap.

**Commits:**
- `4fb828f` — fix: wire 34 ported skills into aeon.yml + sync counts/image to 156 (#230)
  - Changed `aeon.yml` (+49): adds the 34 missing skills, all `enabled: false`, grouped by purpose, honoring schedules already declared in each skill's SKILL.md frontmatter and assigning sensible defaults to the rest; `heartbeat` stays last as the fallback. No duplicate keys.
  - Changed `README.md` (+19, -19): bumps the skill count 121 → 156 across all six references and refreshes the category table (Research 24 / Dev 41 / Crypto 27 / Social 14 / Productivity 18 / Meta 32).
  - Added `assets/skills-156.jpg`, removed `assets/skills.jpg`: cache-busting filename swap so the README graphic reflects the full 156-skill catalog rather than a CDN-cached old image.
  - The commit body explicitly leaves `docs/skill-graph.md` untouched (it's generator-owned, currently stale at "91+") and notes `skills.json` already reported 156 — a deliberate scope boundary, not an oversight.

**Impact:** The 34 ported skills are now schedulable and toggleable (still disabled by default). This is the kind of bug that hides in plain sight: the count was right everywhere a human looks (README, skills.json), but the runtime config that actually decides what can run was missing them.

### Ecosystem Self-Listing (community docs)

**Summary:** Three inbound documentation contributions — the ecosystem continuing to register itself against Aeon. Tiny diffs, but they're the social-proof signal the project tracks.

**Commits:**
- `5804fd8` — docs: add AntFleet, Gitlawb Terminal, MythosForge, Reg Terminal, USIC to ECOSYSTEM (#229)
  - Changed `ECOSYSTEM.md` (+5): five projects added, alphabetized; Bean/Powerloom/ResearchSwarm/SyntheticsAI/Signa skipped as already-listed under the same X handles.
- `a10bb58` — docs(ecosystem): list LiquidPad in ECOSYSTEM.md (#225) — authored by the LiquidPad bot
  - Changed `ECOSYSTEM.md` (+1): LiquidPad (independent token launchpad on Base, ships the `aeon-skill-pack-liquidpad` community pack merged in #218) self-lists alphabetically between LawbWorld and Liq.
- `b693c8f` — docs: add aeon-skill-pack-mythosforge to community skill packs (#228) — authored by `Clint`
  - Changed `README.md` (+1) and `skill-packs.json` (+11): registers the MythosForge skill pack in both the README table and the machine-readable registry — exactly the both-surfaces-in-one-PR discipline the registry's publishing checklist requires.

**Impact:** ECOSYSTEM.md and the skill-pack registry are the project's distribution map. That outsiders (LiquidPad, Clint) are opening these PRs themselves — and following the registry's dual-update rule — is evidence the community-pack protocol shipped earlier this week is being used as intended.

---

## aaronjmars/aeon-agent

### Community Skill-Pack Install Protocol — backport

**Summary:** The full one-command pack-install protocol, backported from upstream aeon. aeon-agent had neither half before today.

**Commits:**
- `34549f6` — feat: backport install-skill-pack CLI + skill-packs.json registry from aeon PRs #213 + #215 (#59)
  - New file `install-skill-pack` (+634, mode 0755): a bash CLI that reads a pack's `skills-pack.json` manifest, runs the existing security scanner against each declared SKILL.md, copies approved skills into `skills/`, records provenance in `skills.lock`, upserts catalog rows into `skills.json`, and appends disabled entries to `aeon.yml`. Six flags (`--list`/`--path`/`--branch`/`--yes`/`--force`/`--dry-run`).
  - New file `skill-packs.json` (+100): machine-readable community registry seeded with 6 packs.
  - New file `docs/community-skill-packs.md` (+224): manifest schema, trust model, registry schema, publishing checklist.
  - Changed `README.md` (+33): new "Community skill packs" section between "Trigger feature builds from issues" and "Publishing", matching upstream placement.
  - `#215` depends on `#213`, so they ship together — backporting one alone would be dead weight. `scan.sh` was deliberately *not* touched: it already carries the May-18/May-20 hardening. The commit notes this is the 12th consecutive same-day-after backport.

**Impact:** aeon-agent operators can now install community skill packs with one command (security-scanned, provenance-tracked, disabled-by-default) instead of cloning and copying files by hand.

### config-validator — backport with adaptations

**Summary:** A structural validator for `aeon.yml` + the run workflow, backported from upstream aeon PR #219 — but not a verbatim copy, because a verbatim copy would have false-positived on aeon-agent every run.

**Commits:**
- `cb317e1` — feat: backport config-validator skill from upstream aeon (PR #219) (#61)
  - New file `skills/config-validator/SKILL.md` (+229): checks checkout-before-Run ordering, duplicate skill keys (YAML keeps the last → silent shadow), and enabled skills missing a SKILL.md. CLEAN runs are silent; only ISSUES notify. Three adaptations called out in the body: (1) the checkout check is rewritten from upstream's "unconditional Early checkout first" to "a checkout step precedes the Run step" because aeon-agent checks out *conditionally* per event type (Early checkout for issues, Checkout repo for scheduled/dispatch) — the upstream rule would have fired every run; (2) the `validate-config.js` fast path is guarded behind a file-exists check since aeon-agent has no such shared script; (3) the notify call uses aeon-agent's single-positional-arg `./notify` (no `-f` flag).
  - Changed `aeon.yml` (+1) and `skills.json` (+11, -1): registered disabled, workflow_dispatch only; total 89 → 90.

**Impact:** A pre-push sanity check for the two config files most likely to silently break the scheduler. The adaptation work is the notable part — this is a backport that understood *why* the upstream rule existed rather than copying its letter.

### fetch-tweets — fail-loud resilience

**Summary:** A direct, same-week response to the May-24 incident where `fetch-tweets` hit an XAI HTTP 403 (team credits exhausted) and emitted a generic, non-actionable failure with no log marker.

**Commits:**
- `385cb16` — improve: fetch-tweets — operator-actionable PREFETCH_FAILED variants + Notification-sent log contract (#60)
  - Changed `skills/fetch-tweets/SKILL.md` (+15, -2 — the actual skill change): every ending state (steps 4/5/7) must now log an explicit `Notification sent: yes` / `no (reason)` line so heartbeat's 48h dedup / 3-day escalation can track fetch-tweets like every other skill; and PREFETCH_FAILED now branches on the HTTP code in `.xai-cache/fetch-tweets.json.error` — 401/403 → persistent auth/credits (with XAI console top-up link), 429 → rate-limit (lower-cadence hint if 3d+), 5xx → transient, curl error → unreachable, plus a generic fallback. Inline references to the two prefetch error-write sites (`scripts/prefetch-xai.sh:100,:117`) keep the contract from drifting.
  - The remaining +212 in this commit is bundled auto-commit state, not part of the fix: `dashboard/outputs/self-improve-2026-05-24T13-14-53Z.json` (+195), `.outputs/self-improve.md`, `memory/logs/2026-05-24.md`, `memory/token-usage.csv`. Worth flagging — the headline +227/-10 overstates the real surface area of the change.

**Impact:** The next time a prefetch fails, the operator gets a notification that says *what to do* (top up credits, lower cadence, wait it out) instead of "prefetch failed; no tweets", and heartbeat can actually see the failure to escalate it. Self-corrective loop closed within the same week the 403 first appeared.

---

## aaronjmars/minitor

### Active Columns — refresh intervals + alert webhooks

**Summary:** Two features that together turn a minitor column from a static, mount-only panel into a self-refreshing surface that can fire alerts on its own. Both round-trip cleanly through the existing deck export/import/share-link and starter-template machinery with zero changes to the 47 plugin fetchers.

**Commits:**
- `f33ef1c` — feat: per-column refresh intervals (#49)
  - New migration `drizzle/0002_refresh_interval.sql` (+1) + journal + `meta/0002_snapshot.json` (+254): additive nullable `refresh_interval_seconds` integer on `columns`.
  - Changed `app/actions.ts` (+52): server-side `{60, 300, 900, 3600}` allowlist + `updateColumnRefreshInterval` action; never trusts the client (optional Zod field).
  - Changed `components/column/column-card.tsx` (+83, -1): a `setInterval` tick with an in-flight guard (no overlapping fetches if an API is slow) and a `document.visibilityState !== 'visible'` pause so background tabs don't burn upstream rate limits, plus cleanup on unmount and on interval change.
  - Changed `components/column/configure-column-dialog.tsx` (+70, -1): the "Refresh interval" select (Manual / 1m / 5m / 15m / 60m).
  - Plus `lib/columns/types.ts`, `lib/db/schema.ts`, `lib/store/use-deck-store.ts`, `lib/deck-templates.ts` wiring. Decks without the field default to manual-only.
- `2a341ce` — feat: per-column alert webhook notifications (#50)
  - New file `lib/columns/webhook.ts` (+166): an SSRF-guarded URL validator + a bounded sender. The validator is https-only, blocks `localhost` and raw IP literals across the private/reserved ranges — `parseIPv4`/`isPrivateIPv4` cover 10/8, 127/8, 0/8, 169.254/16 link-local, 172.16-31, 192.168/16, 100.64/10 CGNAT, and 224+ multicast; `isPrivateIPv6` covers `::1`/`::`, `fc`/`fd` unique-local, `fe80` link-local, and IPv4-mapped `::ffff:…`. The sender is bounded to 5s (AbortController), never throws, and uses `redirect: "error"` so an allowed host can't 30x-bounce into an internal address. The module is environment-agnostic so the same validator runs server-side (before persist + before send) and client-side (live form feedback). The header comment honestly documents the limitation: hostnames aren't resolved, so DNS-rebinding isn't caught at validate time — mitigated by the no-redirect sender.
  - New migration `drizzle/0003_notify_webhook.sql` (+1) + `meta/0003_snapshot.json` (+260): nullable `notify_webhook_url`. **Note:** this landed as migration **0003**, not 0002 as originally scoped — because #49's refresh-interval migration merged first and took the 0002 slot. The sequence resolved itself correctly on main.
  - Changed `app/actions.ts` (+117, -4): `updateColumnWebhookUrl` (server-validates); `persistFetchedItems` fires the webhook only for NEW matched items (re-fetches never re-notify); DeckExport v1 *accepts* `notifyWebhookUrl` on import (re-validated through the SSRF guard) but `exportDeck` deliberately **omits** it — a webhook URL often embeds a Slack/Discord secret and the same export feeds the public share link, so emitting it would leak the secret.
  - Plus `lib/columns/keyword-match.ts` (+18, `matchedAlertKeywords()`), the configure-dialog field (shown only when keywords are set, live validation, Save blocked on invalid), and store/types/schema wiring.

**Impact:** Operators can now run fast crypto/price columns at 1-5min polling and slow GitHub-stars columns at manual/hourly without one global cadence forcing a choice between rate-limit burn and stale data — and a column with keywords + a webhook becomes an active alert channel (Slack/Discord/Zapier/n8n) that fires even when nobody's looking at the dashboard. The security posture is careful: SSRF guard on input, no-redirect on send, and the secret-bearing webhook URL is kept out of the shareable export. Per the PR note, Next 16 build/typecheck could not run in the offline sandbox — these landed on manual review only.

---

## Developer Notes

- **New dependencies:** None. Every change today is built on existing primitives — minitor's webhook/refresh features use only global `URL`/`fetch`/`AbortController` and the existing deck/store/Drizzle machinery; aeon-agent's backports add a bash CLI and JSON registry, no packages.
- **Schema/migration changes:** minitor added two additive, nullable columns via Drizzle — `refresh_interval_seconds` (0002) and `notify_webhook_url` (0003). Both backward-compatible; decks without them default to manual-only / no-webhook.
- **Breaking changes:** None. Every new aeon/aeon-agent skill is registered `enabled: false`; the CI workflow patches are behavior-preserving on well-formed input.
- **Security posture (the day's strongest thread):** workflow_dispatch input is now allowlist-validated and env-passed (no more template-into-bash injection); the gateway parser no longer crashes on its own quoting; minitor's webhook feature ships an SSRF guard, a no-redirect bounded sender, and a deliberate decision to keep secret-bearing URLs out of public exports.
- **Catalog accounting:** aeon 155 → 156 (ecosystem-pulse) and the 34 previously-orphaned ported skills are now actually wired into `aeon.yml`; aeon-agent 89 → 90 (config-validator). `docs/skill-graph.md` remains generator-owned and stale ("91+") by deliberate choice.
- **Tech debt / shortcuts:** minitor's two features could not be build/typechecked in the offline sandbox (manual review only) — worth a CI verification pass. The minitor SSRF validator's documented DNS-rebind gap is a known, mitigated limitation, not an oversight.

## What's Next

- **Verify minitor #49/#50 on real CI** — both landed without a Next 16 build/typecheck run. A typecheck + migration-apply pass against a real DB is the obvious follow-up before relying on the webhook sender in production.
- **The 34 newly-wired skills are still disabled** — #230 made them schedulable, but each is `enabled: false`. Expect a follow-on wave of selective enablement (and the long-standing Next-Priorities backlog of skills awaiting enable: show-hn-draft, pr-triage, fork-cohort, operator-scorecard, etc.).
- **AntFleet audit is effectively drained on Highs** — with H1 closed (#226), the open AntFleet work is now Mediums/Lows. Watch whether the antfleet-ops account pivots to those next.
- **ecosystem-pulse needs its resolver map** — the skill is shipped but disabled and depends on `memory/topics/ecosystem-pulse-map.json` for accurate repo resolution; first real run will lean on best-effort search until the operator seeds the map.
- **Community-pack protocol is now live in both repos** — with install-skill-pack + registry in aeon-agent too, and outsiders (LiquidPad, MythosForge) self-listing, the next signal to watch is a community pack actually being installed via the CLI rather than just registered.
