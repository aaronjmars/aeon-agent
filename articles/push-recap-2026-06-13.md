# Push Recap — 2026-06-13

## Verdict
> SHIPPING — collapsible dashboard panel + gateway sidecars now track the chosen model

**Shape:** 4 user-visible commits · 0 internal · 0 infra-only · 27 bot-filtered
**Volume:** 7 files changed, +84/-14 lines across 4 commits by 2 authors
**Merged PRs:** 4 (aeon #460 VENICE_BASE_URL override; #461 sidecar $MODEL tracking; #462 collapsible right panel; #463 scroll-to-top)

---

## Top impact today
1. `95350ec` — feat(dashboard): collapsible right panel (#462). Adds a collapse toggle that shrinks the Feed/Runs/Analytics panel to a 36px rail with a vertical label, persists the state in `localStorage`, and trims the expanded width 320→288px — operators reclaim screen for the main content. (1 file, +43/-3)
2. `ccd7204` — fix(gateway): sidecar providers track aeon's $MODEL (#461). Surplus and Venice sidecars no longer pin a hardcoded model — they derive it from the resolved `$MODEL` (UI/`aeon.yml` choice), with Venice gated to an allowlist it actually carries so a newer model can't 404. (1 file, +25/-6)
3. `e78cc33` — feat(gateway): VENICE_BASE_URL override (#460). External contributor `ashneil12` — lets forkers point the Venice sidecar at any Venice-compatible endpoint (self-hosted relay, billing proxy, regional mirror) via a repo variable. (4 files, +10/-3)

---

## aaronjmars/aeon

### Dashboard UX — operator surface gets tighter

**What this is:** Two changes to the framework's control-room dashboard that make the live operator view less cramped and less jumpy. Both ship straight to anyone running the dashboard.

**Shipped to users**
- `95350ec` — feat(dashboard): collapsible right panel
  - `apps/dashboard/components/RightPanel.tsx`: new `collapsed` state with a `localStorage`-backed toggle (`aeon-panel-collapsed`); collapsed mode renders a thin 36px rail with an expand chevron and a vertical "Feed · Runs · Analytics" label; expanded panel narrowed 320→288px; Refresh demoted to an icon button and a collapse `›` control added (+43/-3)
- `6b93a39` — feat(dashboard): scroll main content to top on tab / skill change
  - `apps/dashboard/app/page.tsx`: adds a `mainScrollRef` and an effect that scrolls the main column to top whenever `view` or `selectedSkill` changes, so every screen (Soul, Strategy, a skill view) opens at the top instead of inheriting the previous scroll position (+6/-2)

### Gateway — multi-provider sidecars stop hardcoding the model

**What this is:** The LLM gateway is how forkers run Aeon on a provider other than Anthropic-direct. Two changes make the OpenAI-compatible sidecars (Surplus, Venice) honor the model the operator actually picked, and let the Venice endpoint be repointed. Provider-independence is the spread story — these lower friction for non-Anthropic forks.

**Shipped to users**
- `ccd7204` — fix(gateway): sidecar providers track aeon's $MODEL instead of a hardcoded one
  - `scripts/llm-gateway.sh`: Surplus now derives its pinned model from `$MODEL` (strips a trailing `-YYYYMMDD`, converts `4-8`→`4.8` to Surplus's dot-form ids; `SURPLUS_MODEL` overrides; `opus-4.8` fallback). Venice does the same but only for an allowlist it's known to carry (`opus-4-6`, `sonnet-4-6`, `haiku-4-5`) and otherwise keeps the safe `opus-4-6` default — a newer model would 404 against Venice's smaller catalog (+25/-6)
- `e78cc33` — feat(gateway): VENICE_BASE_URL override for the Venice sidecar *(external contributor: `ashneil12`)*
  - `scripts/llm-gateway.sh`: the Venice sidecar URL now reads `${VENICE_BASE_URL:-https://api.venice.ai/...}`, so a self-hosted relay / proxy / regional mirror can be swapped in via repo variable (+5/-2)
  - `.github/workflows/aeon.yml`, `.github/workflows/messages.yml`: plumb `VENICE_BASE_URL` from `vars` into the three job envs (+4/-0)
  - `README.md`: gateway table note documents the new `VENICE_BASE_URL` variable (+1/-1)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none — all four changes are additive (new config vars default to prior behavior; model derivation falls back to the old hardcoded value)
- **New public surface:** `VENICE_BASE_URL` repo variable (Venice sidecar endpoint); sidecar model is now driven by the existing `$MODEL` / `SURPLUS_MODEL` / `VENICE_MODEL` vars; `aeon-panel-collapsed` localStorage key
- **Tech debt added:** Venice model allowlist is hand-maintained — the code comments flag "confirm/extend the allowlist when Venice is live-validated." No new TODOs/FIXMEs in the diffs.

## Open threads
- No new branches pushed unmerged in-window. Carried from prior days: external PR #418 (BEAMR gateway) still pending a maintainer-side rebase — not cleanly autonomous.
- **aeon-agent (this instance):** Aaron landed instance-config commits direct to main — adopting the `aaron` soul (`5680bb5`), tailoring `STRATEGY.md` to the stars+ecosystem+token north-star (`1c10224`), and syncing the SOUL/STRATEGY dashboard builder tabs from upstream (`31cf197`, `53a9bd5`). This is configuration of the agent's own repo, not framework shipping — noted, not ranked.
- **minitor:** quiet in-window (Dexscreener plugin #72 landed yesterday, already recapped).

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok (27 bot auto-commits filtered; 4 instance-config commits noted under Open threads)
- aaronjmars/minitor: empty
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 27
- diff-truncated: 0
