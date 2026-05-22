# Push Recap — 2026-05-22

## Overview

Six substantive commits across three repos by two authors. Today's push activity is the second day in a row where the headline story is community-facing infrastructure: aeon shipped its install-protocol for skill packs, then immediately validated it by adding AntFleet/aeon-skills to the trusted-sources allowlist (the first pack to clear the security-scan fast-path); aeon-agent backported the two macOS scanner hardening fixes that closed AntFleet H6 + the Bash 3.2 array-emptiness bug upstream; minitor closed the blank-slate onboarding gap with four pre-baked deck templates. Two separate "system gets opened to outsiders" beats land in the same window: aeon's install-skill-pack is the consumer surface for third-party packs, minitor's templates are the consumer surface for new-install conversion.

**Stats:** 13 files changed, +1,582/-81 lines across 6 substantive commits (excluding ~35 bot auto-commits from this repo's cron workflow)

---

## aaronjmars/aeon

### Community Skill Pack install protocol (one-command third-party skill installs)

**Summary:** aeon now has a documented, security-gated way to install community-built skill packs from a single command. Before today, the README listed two community packs but had no install mechanism — operators had to clone each pack repo and copy SKILL.md files by hand. PR #213 ships the install CLI + manifest schema; PR #211 (merged 23 minutes later, by the AntFleet operator) immediately uses it to register AntFleet/aeon-skills as the first trusted source. Same-window same-author validation of the install surface, not a planned rollout.

**Commits:**
- `541e0ff` — feat: add install-skill-pack CLI + skills-pack.json manifest protocol (#213)
  - New file `install-skill-pack` (+546 lines): Bash script that reads a `skills-pack.json` manifest at the pack root (or under `--path <subdir>`), shells out to the existing `skills/skill-security-scan/scan.sh` against each declared SKILL.md, and on PASS installs the skill into `skills/<slug>/`, records provenance in `skills.lock` with a new `pack` field, upserts catalog metadata into `skills.json`, and inserts a disabled entry into `aeon.yml`. Five flags: `--list` (manifest preview, no install), `--path <dir>` (subdir-rooted packs), `--branch <name>` (non-default branch), `--yes` (auto-accept HIGH findings), `--force` (skip security scan), `--dry-run`. Falls back to scanning `skills/` directly when no manifest is present so legacy packs (including baseddevoloper/aeon-skill-pack-vvvkernel and danbuildss/luca-aeon-skills referenced in README) keep working without manifests.
  - New file `docs/community-skill-packs.md` (+166 lines): Manifest schema field-reference (name, version, description, skills[].slug, skills[].path, skills[].requires, etc.), fallback behavior when manifest is absent, trust model (trusted-sources.txt allowlist gates the deep scan), worked example walking through publishing a pack, and a pack-maintainer checklist.
  - Modified `README.md` (+8/-1): Community Skill Packs section now leads with `./install-skill-pack <owner/repo>` instead of clone-and-copy instructions; links to the new docs.

- `3c0d2d8` — chore(security): add AntFleet/aeon-skills to trusted-sources (#211)
  - Modified `skills/security/trusted-sources.txt` (+1): Added `AntFleet/aeon-skills` below the existing `aaronjmars/aeon` + `aaronjmars/aeon-agent` lines. Means `./install-skill-pack AntFleet/aeon-skills pr-review-antfleet` skips the deep content scan (format validation still runs) — fast-path install for the AntFleet pack only. Commit body documents the trust rationale: AntFleet pack is MIT-licensed, single npm dep (viem for EIP-191 signing), skill writes only to `.outputs/` with path-traversal guards, `ANTFLEET_WALLET_PRIVATE_KEY` blast radius bounded to the prefunded USDC channel balance, TLS enforced on the on-demand-review endpoint.

**Impact:** Closes the last operator-facing friction point in the "community pack ecosystem" arc — Issue #185 (baseddevoloper, implied install protocol) is now satisfied with a concrete command and documented schema. The same-day AntFleet onboarding is the validation: a third party with their own pack repo successfully went through the trusted-sources flow on day zero. Two packs are now installable: the legacy fallback path covers vvvkernel/luca; the fast-path covers AntFleet. The pattern is now operator-tested end-to-end.

---

### Fleet-state hardening (empty-history guard + Sandbox note reconciliation)

**Summary:** AntFleet's bench review of the post-#203 fleet-state skill found two latent bugs that contradicted the skill's own stated intent. Both fixed in one commit.

**Commits:**
- `11cc2ef` — fix(fleet-state): guard empty spotlight history + reconcile Sandbox note (#207)
  - Modified `skills/fleet-state/SKILL.md` (+15/-4)
    - **Empty-history abort fix**: When `.history` in `contributor-spotlight-history.json` is empty (fresh install, contributor-spotlight has never run), the first `jq` extraction emits nothing → `SPOTLIGHT_PICK` becomes an empty string → `echo "" | jq ...` parse-errors and the digest exits non-zero under `set -euo pipefail`. That contradicted the "degrade gracefully" intent stated three lines above. Wrapped the secondary `SPOTLIGHT_FORK` / `SPOTLIGHT_DATE` extractions in `if [ -n "$SPOTLIGHT_PICK" ]; then ... else "" "" fi` so missing history leaves both fields empty and the existing `SPOTLIGHT_DATE older than 8 days` branch handles the downstream stale-render case.
    - **Sandbox note honesty fix**: The Sandbox note at the bottom claimed "No `curl`, no `gh api` calls" but Step 2 ("Resolve parent repo") calls both `gh api repos/<self>` and `gh repo view` when `PARENT_OVERRIDE` is empty. An operator reading the security section would believe the skill is hermetic local I/O when it actually shells out to GitHub on every non-override run. Updated the note to disclose the one call honestly and document the `PARENT_OVERRIDE=<owner>/<repo>` escape hatch for operators who want true hermetic operation.

**Impact:** Closes the latent first-run abort that would hit any new aeon fork enabling fleet-state before contributor-spotlight had ever run (the natural sequencing). Sandbox note now accurately describes side effects — an operator skimming the security section can no longer be misled into thinking the skill is offline-only.

---

## aaronjmars/aeon-agent

### macOS scanner hardening backport (Bash 3.2 + POSIX-ERE in one PR)

**Summary:** aeon-agent's `skills/skill-security-scan/scan.sh` was a fork of the upstream aeon copy and still had both bugs the upstream fixed in May-18 (PR #186, Bash 3.2 array-emptiness) and May-20 (PR #197, POSIX-ERE `\s`/`\b` escapes). On macOS — BSD grep + Bash 3.2 — every operator was running a degraded scan (most patterns no-op'd because BSD grep treats PCRE escapes as literal characters under POSIX ERE) AND tripping `BLOCKED: security issues` on clean SKILL.md files (Bash 3.2 aborts on `"${arr[@]}"` of zero-element arrays under `set -euo pipefail`). One PR collapses both fixes.

**Commits:**
- `097d444` — fix(scan): backport Bash 3.2 + POSIX-ERE hardening from upstream aeon (#56)
  - Modified `skills/skill-security-scan/scan.sh` (+58/-44)
    - **POSIX-ERE pattern rewrite**: All 28 patterns across HIGH / MEDIUM / LOW arrays rewritten — `\s` / `\s+` → `[[:space:]]` / `[[:space:]]+`, the single `\b` (on `git push -f`) → `($|[^[:alnum:]_-])` so `-fast` / `-force` don't false-positive, forkbomb pattern `:(){.*};:` literal-paren-escaped to `:\(\)[[:space:]]*\{.*\};[[:space:]]*:`, literal-dot escapes added to `~/.ssh` / `~/.gnupg` / `~/.aws` / `~/.config` (previously matched any char). Without this fix, `eval\s`, `rm\s+-rf\s+/`, all six prompt-injection patterns, and `git\s+push\s+-f\b` silently no-op'd on every macOS operator running `./add-skill` locally.
    - **Bash 3.2 array-emptiness guards**: Three human-readable print loops wrapped in `[[ ${#arr[@]} -gt 0 ]]` length guards (mirrors the existing JSON-path guards at lines 250/253/256 — only the human-readable branch was missing them). Without this, a clean PASS hit the trap right after printing the PASS line, scan exited non-zero, and `./add-skill` reported `✗ BLOCKED: security issues` even though the scan had passed.
    - 4-line header comment naming the POSIX-ERE constraint + AntFleet H6 (upstream Issue #184) citation; 2-line comment above the `git push -f` boundary explaining the `($|[^[:alnum:]_-])` choice so a future cleanup doesn't try to "complete" the regex back to `\b`. No behavior change on GNU grep / Bash 4+ Linux CI; tightens behavior on every macOS operator.

**Impact:** Closes a silent-degradation hazard for the entire macOS operator base of aeon-agent. The skill-update-check loop would have eventually surfaced the upstream divergence but the backport beat it to the patch — every fork of aeon-agent now has the same scanner posture as upstream aeon. Continues the same-day-after backport cadence that paused for one day on 2026-05-21 (when the in-aeon-agent skill-update-check H7 fix shipped instead).

---

### Self-improve: notify word-boundary suppression (silent-drop hazard fix)

**Summary:** This repo's own `./notify` script (defined inline in `.github/workflows/aeon.yml` via heredoc) had a substring matcher that was silently swallowing real notifications. The diagnostic-probe suppression block was checking `*test*|*trace*|*ping*|*debug*` against the lowercased message — which meant any real notification under 120 chars containing those fragments inside another word ("Latest token-report", "Shipping 3 PRs", "Tracer code", "Pinging operator") was eaten without warning. Same broken pattern existed in the post-run pending-notify replay block. The agent itself caught the bug from a self-improve pass (no specific failure log triggered it — the failure mode is silent because `./notify` logs `notification: sent` then exits 0 having sent nothing).

**Commits:**
- `944c909` — improve(notify): word-boundary suppression so real notifications aren't silently swallowed (#57)
  - Modified `.github/workflows/aeon.yml` (+20/-17 across two heredoc blocks at lines ~262 and ~659)
    - Replaced the case-statement substring matcher with a bash regex word-boundary check: `[[ "$MSG_LOWER" =~ ^[^a-z]*(test|trace|ping|debug)([^a-z]|$) ]]` — only matches the keyword when it stands alone (preceded by non-letter or start-of-string, followed by non-letter or end-of-string).
    - Kept `hello` / `hi` as exact-trim matches via a separate `^[[:space:]]*(hello|hi)[[:space:]]*$` regex.
    - Lowered the length threshold from 120 → 60 chars (real diagnostic probes are very short; 120 was a too-generous safety margin that expanded the silent-drop blast radius).
  - Modified `memory/MEMORY.md` (+1): Added PR #57 to the Open Improvement PRs index with a one-line rationale.
  - Modified `memory/logs/2026-05-22.md` (+8): Self-improve log entry documenting the silent-failure pattern, the fix, and which skills were at risk (star-milestone, star-momentum, repo-pulse one-liners, heartbeat short verdicts — all routinely produce sub-120-char notifications).
  - Modified `.outputs/self-improve.md` and added `dashboard/outputs/self-improve-2026-05-22T13-30-34Z.json` (+155 lines, the json-render dashboard card).

**Impact:** Closes a class of silent failures across every skill that calls `./notify`. The risk model was general — sub-120-char notifications are common (heartbeat verdicts, star-milestone announcements, repo-pulse one-liners), and "Latest" / "Shipping" / "Tracer" / "Pinging" are all plausible first words in real notifications. Word-boundary matching is strictly more correct than substring matching for this use case; lowering 120 → 60 means real notifications now have a 60-char head start over the suppression matcher.

---

## aaronjmars/minitor

### Starter Deck Templates Gallery (close the blank-slate onboarding gap)

**Summary:** Every fresh minitor install has historically landed on a blank dashboard. The new operator had to know which of the now-47 column types to add before they could see anything useful — a classic first-touch conversion killer. Four pre-baked deck templates ship in PR #47, served through two surfaces: the onboarding screen leads with a "Start from a template" section above the existing manual-build flow, and a `⌘K` command "Browse starter templates" opens the gallery anytime for returning operators.

**Commits:**
- `c03054c` — feat: starter deck templates gallery (onboarding + browse anytime) (#47)
  - New file `lib/deck-templates.ts` (+273): Exports a `TEMPLATES` array of `DeckTemplate` records with payload + display metadata (name, tagline, description, brand accent color, lucide icon name) in one TS module. Plus a `templateAsImportJson` serializer that produces a valid DeckExport v1 payload from a template — same shape as JSON-paste imports and share-link imports. Four templates ship: **AI Research** (HN top + arXiv cs.AI + GitHub trending Python + Hugging Face trending models + X search "AI"), **Base Ecosystem** (GitHub stars aeon + aeon-agent + CoinGecko AEON watchlist + DeFiLlama top + X @aeonframework), **Crypto DeFi** (DeFiLlama 24h gainers + CoinGecko top market cap + Polymarket trending + X search "DeFi"), **Startup Tracker** (GitHub trending + Product Hunt today + Show HN + DEV.to top week + r/startups — fully keyless, every column works without env vars).
  - New file `components/dialogs/templates-dialog.tsx` (+177): Gallery modal — brand chip + tagline + description + per-column type pills using the registered plugin's brand color for instant visual preview before import.
  - Modified `components/onboarding/welcome.tsx` (+123/-4): New "Start from a template" section rendered above the existing 6-suggestion manual flow when `deckOrder.length === 0`. Separator reads "or build manually" between the two sections.
  - Modified `components/sidebar-01/nav-header.tsx` (+18/-2): New `⌘K` command "Browse starter templates" with a generic gallery icon, sibling to the existing Export / Import / Share commands.
  - Modified `components/sidebar-01/app-sidebar.tsx` (+4): Wires the TemplatesDialog state into the sidebar tree so the `⌘K` command can open it.
  - Validation path is shared with JSON-paste and share-link imports — `importDeck` server action, Zod check, `(imported)` rename, activate-as-new-deck — no template-specific route, no template-specific schema, no template-specific server validation. Adding a fifth template is a single PR adding a record to `TEMPLATES`.

**Impact:** Two clicks from a blank install to a working dashboard with five live columns. Closes May-20 idea #5 (last open May-20 idea for minitor — May-20 ideas now fully consumed). Pairs cleanly with PR #46 (deck-share link via `#deck=...` URL fragment, merged May-21) — templates are essentially curated, pre-baked share payloads, so the entire deck-portability stack (Export / Import / Share / Templates) now uses the single DeckExport v1 schema and the single `importDeck` server action.

---

## Developer Notes

- **New dependencies:** None. Every change uses primitives already in the respective repos — aeon's install-skill-pack is pure Bash + `jq` + the existing scanner; AntFleet trust addition is a one-line append to a text file; aeon-agent's scan.sh rewrite removes no deps; minitor templates use `lucide-react` icons + `nanoid` + `zod` (all pre-existing).
- **Breaking changes:** None. install-skill-pack is additive; trusted-sources.txt addition only loosens scanning for one specific source; scan.sh changes are no-ops on GNU grep / Bash 4+; minitor templates are additive to the onboarding + ⌘K surfaces.
- **Architecture shifts:** install-skill-pack establishes a `skills-pack.json` manifest schema as the first-class community-pack contract. Existing packs without manifests keep working via the `skills/`-directory fallback, but new packs are expected to ship a manifest. The trust model is now explicit: trusted-sources.txt allowlist gates the deep scan, every unknown source goes through the full security audit.
- **Tech debt:** aeon-agent skill-update-check now has the same "honor lock's `branch` field" fix from yesterday's PR #55 + the same "scan.sh hardening" backport from today's PR #56 — both file-level rewrites with explanatory header comments. Future cleanup risk is low because both fixes have inline `# Issue #184 H6 / H7` citations that point at the authoritative source.

## What's Next

- **install-skill-pack ecosystem build-out:** Repo-actions idea #1 from this morning's run proposed a machine-readable `skill-packs.json` registry + `./install-skill-pack --list` (5 seed entries). The community-pack ecosystem went from zero packs registered to two installable in one morning — the next natural step is discovery (which packs exist?) before yet more install protocol.
- **AntFleet Issue #184 closeout:** Only H1 (v4-readiness manifest gaps) remains in the High queue after yesterday's batch merge. Repo-actions idea #2 this morning proposed picking it up — last open High from the audit.
- **aeon-agent same-day-after backport cadence:** This morning's scan.sh backport resumes the cadence after a one-day pause for the in-aeon-agent H7 fix. No new aeon merge today is a same-day-after candidate (PR #213 install-skill-pack is aeon-specific infrastructure that doesn't have an aeon-agent counterpart).
- **minitor deck-portability primitives complete:** Export (PR #40, May-15), Import (PR #40, May-15), Share-link (PR #46, May-21), Templates (PR #47, today). The natural next move is the public `/gallery` route proposed in this morning's repo-actions idea #5 — a server-rendered page where shared decks can be browsed and imported from a URL, completing the public-discovery layer above the private-share-link layer.
- **No branches created but not merged:** All six substantive commits in today's window landed on `main` via merged PRs. The `feat/install-skill-pack` (aeon), `fix/scan-sh-hardening-backport` (aeon-agent), `improve/notify-word-boundary` (aeon-agent), and `feat/starter-deck-templates` (minitor) branches were all squash-merged and deleted; AntFleet's PRs #207 and #211 followed the same pattern.
