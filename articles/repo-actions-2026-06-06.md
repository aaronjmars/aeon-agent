# Repo Action Ideas — 2026-06-06

*Generated from analysis of aaronjmars/aeon (487⭐, 165 forks, 2 open issues), aaronjmars/aeon-agent, and aaronjmars/minitor.*

---

## Context

**aeon** is tracking to 500⭐ around June 11 (v7=3.57/day, v3=3.67/day — OUT_OF_WINDOW until threshold crossed). ECOSYSTEM.md now carries logos and 30+ entries. Taxonomy expanded to 8 categories (core, onchain-security, meta added June 5–6). CORE.md documents the 15 load-bearing skills for the first time. Issue #352 (filed today) surfaces an OAuth credential refresh loop that breaks authentication on every second run. VIGIL (external, PR #323) explicitly split its Approval Revoker into a future `vigil-revoke` skill during review — five other HoundFlow onchain skills still have no scheduled consumer.

**aeon-agent** closed the last shell-substitution anti-pattern today (PR #83 — repo-actions + star-momentum-alert). All 22 consecutive same-day-after backports are now at zero known anti-pattern sites. `skill-of-the-day` (Nurstar's PR #341, merged Jun-04) hasn't been backported yet — it's the cleanest carry in the current queue.

**minitor** shipped deck color labels (PR #62) today, completing the deck-level visual organization axis. Column color (PR #61) and deck color (PR #62) now cover both layers. The per-column UX axis is at 7 rungs; column width control is the natural 8th (tab groups → collapse → export → search → pin → duplicate → color → width).

---

### 1. OAuth Credential Write-Back in `aeon.yml` (aeon)
**Type:** DX
**Effort:** Small (hours)
**Impact:** Issue #352 (filed today) describes a silent 401 loop: OAuth refresh tokens are single-use, the runner updates `~/.claude/.credentials.json` after a successful run, but those updated credentials are lost when the ephemeral container exits. The next run re-uses the now-invalidated old refresh token and fails. Every operator using OAuth credentials hits this on the second run and has to manually re-sync the secret. A guarded write-back step after every `claude -p` call breaks the loop permanently — each run leaves fresh credentials for the next one.

**How:**
1. In `aeon.yml` (and `chain-runner.yml`), after the `claude -p` call, add an `if: always()` step: check if `~/.claude/.credentials.json` exists and `$GH_TOKEN` is available (GH_GLOBAL or GH_REPO_TOKEN secret), then `gh secret set CLAUDE_CREDENTIALS --body "$(cat ~/.claude/.credentials.json)"`. The `if: always()` guard ensures write-back runs even if the claude step fails mid-run (which would still produce a new refresh token before failing).
2. Add `GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GH_REPO_TOKEN }}` to the job env or the write-back step env. No-op silently when the env var is absent (protects setups using API key auth which don't need write-back).
3. Update `README.md` or `docs/setup.md` with a one-paragraph note: "If using OAuth credentials, also add a PAT with `secrets:write` as `GH_GLOBAL` — this enables the write-back loop."

---

### 2. `vigil-revoke` Skill (aeon)
**Type:** Security
**Effort:** Medium (1-2 days)
**Impact:** VIGIL's five-round review (PR #323) explicitly split the Approval Revoker into a future skill with a comment: "Bankr-gated, state-changing — separate PR." `wallet-risk-weekly` (PR #340) now runs weekly and surfaces HIGH-bucket approvals that warrant revocation. The detection → revoke loop is currently half-open: the agent identifies an UNLIMITED approval to a non-trusted spender but has no autonomous path to act. `vigil-revoke` closes it. With `eth_call` confirming the approval is live before revoking, and Bankr handling the transaction, the operator gets a single-step remediation surface rather than having to manually construct a revoke transaction.

**How:**
1. New `skills/vigil-revoke/SKILL.md` — `workflow_dispatch` only, `var` = `wallet:spender:token` triplet (mirrors the tuples `vigil_scan_approvals` returns). Step 1: parse and validate inputs — strict `^0x[0-9a-f]{40}$` allowlist on all three fields (same pattern VIGIL hardened in review round 4). Step 2: confirm the approval is still live via `allowance` `eth_call` before spending gas. Step 3: construct revoke call (`approve(spender, 0)`) via Bankr Wallet API — require `BANKR_TOKEN`. Step 4: wait for tx confirmation (poll receipt or use Bankr's response), log result to `memory/topics/vigil-revoke-log.json`.
2. Capability: `sends_funds` (Bankr is executing a state-changing transaction). Add to `skill-packs.json` under the HoundFlow pack or as a standalone security skill. Do not schedule — operator-initiated only.
3. Notification on completion: tx hash, wallet, spender, token. On failure (approval already zero, insufficient gas, Bankr 403): notify with reason, do not retry automatically.

---

### 3. `skill-of-the-day` Backport (aeon-agent)
**Type:** Community
**Effort:** Small (hours)
**Impact:** Nurstar's PR #341 (merged Jun-04 on upstream aeon) is the cleanest unbackported skill in the current queue. Daily meta-content skill: picks a skill from a rotation queue, generates a paste-ready tweet with the skill's purpose and a one-liner on what it's currently observing, then dispatches the skill so the live outcome arrives as the screenshot. Two notifications per run — the setup tweet + the result. 30-day suppression window prevents the same skill appearing twice in a month. Directly converts the catalog depth (193 skills) into a repeatable daily content beat without requiring the operator to write copy.

**How:**
1. Verbatim copy of `skills/skill-of-the-day/SKILL.md` from upstream aaronjmars/aeon. Add backport-note block at top citing upstream PR #341 + any adaptations.
2. Key adaptations: (a) `./notify` call rewritten as positional `$1` arg style (same constraint as all 22 prior backports — aeon-agent root notify reads `MSG="$1"`, not `-f file`); (b) rotation queue seeds from aeon-agent's own `skills/*.json` enabled-skill list rather than upstream's; (c) any `$(date ...)` substitution in the skill replaces with literal `${today}` (runner hook blocks `$(...)` — chain of fixes closed today by PR #83).
3. Register in aeon.yml disabled at the same schedule as upstream. Add to skills.json (total 100→101, category content or community per upstream classification). 23rd consecutive same-day-after backport.

---

### 4. Minitor: Column Width Control
**Type:** Feature
**Effort:** Small (hours)
**Impact:** The 8th rung on the per-column UX axis (tab groups → collapse → export → search → pin → duplicate → color → width). All columns are currently fixed at 360px. A crypto price column is densest in a narrow layout (token symbol + price + delta occupies ~180px); a news feed column reads best wide (~480px) because headline text wraps at 360px. Three sizes — narrow (240px), normal (360px), wide (480px) — cover the operator's real use cases with a single toggle rather than a draggable resize (which is more complex and compounds poorly with collapse and pin). State can be DB-backed (same pattern as `pinned` and `color`) so width survives reload and exports with the deck, or view-state only (same pattern as `collapsedColumnIds`) — view-state is the right default here given the pattern of only persisting what defines the deck's identity.

**How:**
1. Add a `width: 'narrow' | 'normal' | 'wide'` optional field to the column store's view-state (`lib/store/use-deck-store.ts` — same shape as `collapsedColumnIds: Set<string>`). No DB migration needed if view-state only; or a `drizzle/0010_column_width.sql` nullable enum if persistence is desired.
2. In `components/column/column-card.tsx`: read `width` from store, apply `w-60` (240px) / `w-[360px]` / `w-[480px]` classes. Add three-way toggle to the column header (or to configure-column-dialog.tsx as a Width setting) — small icon buttons for N/W/W sizes, active state highlighted.
3. In `components/deck/deck-board.tsx`: the horizontal scroll container already handles variable widths — no change needed there as long as column widths are static CSS classes (not calculated flex widths).

---

### 5. Show-HN Draft Auto-Fire at 500⭐ (aeon)
**Type:** Growth
**Effort:** Small (hours)
**Impact:** PR #151 (show-hn-draft) has been open for 35 days. The skill is enabled-pending-500⭐ — the operator's own notes say "Enable at 500⭐." At the current trajectory (3.6⭐/day), 500 arrives ~June 11. The star-milestone skill detects threshold crossings but currently just notifies; it does not trigger downstream actions. Wiring `star-milestone` to dispatch `show-hn-draft` automatically when 500 is crossed removes the last manual gate — the operator doesn't need to notice the milestone, decide to act, and remember which PR to merge. The skill fires itself.

**How:**
1. In `skills/star-milestone/SKILL.md`, add a step after the milestone-crossing notification: check if the crossed threshold is in a configurable `auto_dispatch_thresholds` map (e.g. `500: show-hn-draft`). If matched, run `gh workflow run <skill>.yml -R aaronjmars/aeon --field var=""` via `gh api`.
2. The map lives in `memory/topics/milestone-dispatch.json` (operator-editable, one entry per threshold). Default: empty — existing milestone behavior unchanged unless the operator opts in.
3. Alternatively (simpler): add a single hard-check in star-milestone — if `stars >= 500 AND NOT already_dispatched_show_hn`, `gh workflow run show-hn-draft.yml`. Write a dispatched flag to `memory/topics/milestones.md` to prevent double-fire. Either approach: the key invariant is idempotent — a re-run at 502⭐ should not fire show-hn-draft a second time.

---

*See `articles/repo-actions-2026-06-04.md` for yesterday's batch (all 5 consumed).*
