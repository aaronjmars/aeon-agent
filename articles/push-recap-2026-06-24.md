# Push Recap — 2026-06-24

## Verdict
> SHIPPING — phylax security screen, dashboard docs, and minitor column guards

**Shape:** 4 user-visible commits · 2 internal · 0 infra · ~52 bot-filtered
**Volume:** 21 files changed, +409/-24 lines across 6 commits by 1 author (@aaronjmars)
**Merged PRs:** 6 (#544, #543 aaronjmars/aeon; #116, #115 aaronjmars/aeon-agent; #80, #79 aaronjmars/minitor)

---

## Top impact today
1. `8606911` — feat: feature skill gets explicit compound-bash sandbox warning. The skill with the lowest success rate (0.85) clones repos into temp dirs, making `cd /tmp/... && cmd` chains the natural reflex — which the non-interactive sandbox auto-denies before running. The Sandbox Note now names this trap with a worked example. (6 files, +121/-3)
2. `ac5792f` — docs: apps/dashboard/README.md created. The dashboard was the last sub-app without a README — a2a-server, mcp-server, and webhook all have one. The new file covers what it is, quickstart via `./aeon` and direct npm, six views, configuration, the loopback/remote-access security gate, and how the API routes shell out to `gh`. Forkers land here after their first `./aeon`. (2 files, +86/-0)
3. `0346752` — feat: skill-triage now runs a Phylax onchain + endpoint pre-screen on incoming skill PRs. Pure-prompt skills (no Base address, no external endpoint) skip it and stay on the fast `gh api`-only path. Any skill that references a `0x…` address or a payment/data endpoint gets phylax-audit's onchain, endpoint, and obfuscation dimensions inline-executed; verdict folds into the triage receipt with DENY→BLOCK precedence. (1 file, +66/-16)

---

## aaronjmars/aeon

### Supply-chain security: Phylax pre-screen in skill-triage

**What this is:** skill-triage already ran `skill-scan` (static text heuristics) against every `SKILL.md` in an inbound PR. That scanner never resolved the Base contracts or x402 endpoints a skill points at. Step 6.5 closes that gap: surface-detect first (grep for `0x…40-hex` addresses and non-doc external URLs), then inline-execute phylax-audit's onchain, endpoint, and obfuscation dimensions for any skill that actually references one.

**Shipped to users**
- `0346752` — feat(skill-triage): add Phylax onchain + endpoint security pre-screen (#544)
  - `skills/skill-triage/SKILL.md`: adds Step 6.5 (67 new lines) — surface gate, per-skill `phylax_verdict` ∈ {N/A, ALLOW, WARN, DENY}, inline phylax execution for skills with onchain or endpoint surface, and skip logic for pure-prompt skills (+66/-16). Triage comment table gains a **Phylax** column. Verdict precedence updated: Phylax DENY → BLOCK, Phylax WARN → WARN. Notify taxonomy extended with Phylax DENY and WARN triggers. Exit taxonomy updated (`PR_SKILL_TRIAGE_WARN` and `PR_SKILL_TRIAGE_BLOCK` now include Phylax states). Sandbox Note extended for keyless Base RPC / Etherscan v2 / endpoint HEAD-probe path.

### Onboarding: dashboard finally documented

**What this is:** `apps/dashboard/README.md` existed nowhere — the first screen a forker sees after `./aeon` had no written explanation. The new file documents the full usage surface so the UI is self-contained from the repo root.

**Shipped to users**
- `ac5792f` — docs: add apps/dashboard/README.md (#543)
  - `apps/dashboard/README.md`: new 84-line file (ADDED) — what the dashboard is, quickstart via `./aeon` and direct npm with correct port notes (`:5555` via `./aeon`, `:3000` via bare `npm run dev`), views table (HQ/Packs/Strategy/Soul/MCP/Settings), configuration (GITHUB_TOKEN/GITHUB_REPO/PORT), remote-access gate (AEON_DASHBOARD_ALLOWED_HOSTS/ALLOW_ANY_HOST with security rationale), and how it works (frontend → API → `gh` → secrets/dispatch) (+84/-0)
  - `README.md`: one-line pointer to `apps/dashboard/README.md` added, matching the convention for a2a-server/mcp-server/webhook (+2/-0)

---

## aaronjmars/minitor

### Column input validation: guards before upstream calls

**What this is:** Four moded social/search columns — linkedin, bluesky, mastodon, youtube — passed `config.query` (and `handle`/`channel`/`playlist` inputs) straight to upstream with no empty-value check. An empty input fired a wasted Grok/AppView/Mastodon/YouTube call that returned an opaque upstream error instead of a clear user-facing message. Continues PR #78, which fixed the five Grok-backed search columns but left these four.

**Shipped to users**
- `b4d1685` — fix(columns): validate required inputs in linkedin, bluesky, mastodon, youtube (#79)
  - `lib/columns/plugins/linkedin/server.ts`: trims `config.query` and throws `"Search query is required."` before the Grok call; trimmed value passed downstream (+4/-1)
  - `lib/columns/plugins/bluesky/server.ts`: mode-aware guard — `handle` required in `author` mode, `query` required in `search`/`hashtag` mode (+6/-0)
  - `lib/columns/plugins/mastodon/server.ts`: same mode-aware pattern — `handle` in `author`, `query` in `hashtag` (+6/-0)
  - `lib/columns/plugins/youtube/server.ts`: per-mode guards — `query` in `search`, `channel` in `channel`, `playlist` in `playlist` (+5/-0)

### Template documentation: validation pattern formalized

**What this is:** PRs #78 and #79 closed the input-validation gap across all existing columns, but the `_template/` every new column is copied from never taught the pattern. A contributor scaffolding from scratch would inherit the same gap. The template and README now document the canonical guard.

**Shipped to users**
- `1085abb` — docs(plugins): teach required-input validation in the column template (#80)
  - `lib/columns/plugins/_template/server.ts`: comment-only addition at the top of `fetch` showing the canonical `config.query.trim()` check and noting that the hello-world demo intentionally skips it (+15/-0)
  - `lib/columns/README.md`: step 4 corrected (Zod `.default("")` guarantees presence, not non-emptiness); new "Validate required inputs" convention section with the exact pattern and a note that a throw is caught by the shared API route as a fetch-error toast (+17/-1)

---

## Internal: aaronjmars/aeon-agent

### Agent self-correction: two skill reliability fixes

**What this is:** Aeon's self-improve skill diagnosed two repeat failure modes — one in the feature skill's sandbox behavior and one in the repo-actions skill's idea-generation logic — and applied targeted patches to prevent recurrence.

**Under the hood**
- `8606911` — fix: warn feature skill against compound-bash in temp dirs (#115)
  - `skills/feature/SKILL.md`: adds "No compound bash" subsection to Sandbox Note explaining that the working dir persists across Bash calls, so `cd /tmp/… && cmd` chains should be split into separate calls or replaced with `git -C`; `$(…)` and `$VAR` also rejected. Evidence: cron-state `last_error` from 2026-06-16 was exactly `cd /tmp/feature-build-aeon-cod && git grep …`; feature skill has the lowest success rate at 0.85 (+5/-0)
- `b043f52` — fix: gate repo-actions against bash-to-LLM-gate idea proposals (#116)
  - `skills/repo-actions/SKILL.md`: Gate 3 (Implementability) gains a runtime-boundary checklist item: a deterministic bash caller cannot synchronously invoke an agentic LLM-only skill (SKILL.md with no executable entrypoint). Worked example: "wire phylax-audit into install-skill-pack" → demote to MONITOR or reframe as agent-to-agent. This idea was repo-actions' #1 Top Pick for two consecutive cycles (scored 13/15) before the feature skill caught it each time (+2/-0)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none
- **New public surface:** skill-triage now exposes a Phylax column and `phylax_verdict` field in its PR comment receipt; `PR_SKILL_TRIAGE_WARN` and `PR_SKILL_TRIAGE_BLOCK` exit codes now include Phylax-driven states. Operators who parse the triage comment structure should expect the extra column.
- **Tech debt added:** none

## Open threads
- `aaronjmars/aeon` PR #510 (LENS skill pack, external contributor) — open, stalled ~4 days
- `aaronjmars/aeon` PR #418 (BEAMR gateway, external contributor) — open, stalled ~13+ days

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: ~52 (aeonframework automation — chore(cron)/chore(scheduler)/chore(*): auto-commit)
- diff-truncated: 0
