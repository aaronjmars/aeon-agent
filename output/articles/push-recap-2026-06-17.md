---
type: Article
---

# Push Recap — 2026-06-17

## Verdict
> SHIPPING — pack validator, PR template & CONTRIBUTING ship across all three repos

**Shape:** 4 user-visible commits · 2 internal · 0 infra · 25 bot-filtered
**Volume:** ~20 files changed, +735/-17 lines across 6 human commits by 1 author (@aaronjmars)
**Merged PRs:** 6 (aeon #495 validate-pack.sh, #494 PR template; aeon-agent #107 prefetch fix, #105 track own X, #100 content-filter fix; minitor #75 CONTRIBUTING)

---

## Top impact today
1. `a2947c2` — feat: add `scripts/validate-pack.sh` (#495). A 282-line pre-flight validator that runs the *same* structural invariants `install-skill-pack` enforces — valid `skills-pack.json`, `[A-Za-z0-9_-]`-only slugs, no `..` in paths, present per-skill `SKILL.md`, locked capability taxonomy — sourced from install-skill-pack's `ALLOWED_CAPABILITIES` so there's one definition of "valid pack." Exits `1` on blocking errors, `0` with advisory warnings. Pack authors now catch rejections before a reviewer does. (3 files, +292/−1)
2. `df68b63` — fix(tweet-digest): prefetch via canonical `prefetch-xai.sh` (#107). Adds a `tweet-digest` case to the script the workflow actually globs, so scheduled runs no longer start with an empty `.xai-cache/` and fall back to live (sandbox-blocked) fetches. (7 files, +234/−12)
3. `70f3523` — docs: add PR template (#494). New `.github/PULL_REQUEST_TEMPLATE.md` with a four-way "type of change" split (new skill / new LLM gateway / community pack listing / core fix) and a matching checklist per type. (1 file, +49/−0)

---

## aaronjmars/aeon

### Lowering the barrier to contribute a skill pack

**What this is:** The two highest-friction moments for an outside contributor — "is my pack actually valid?" and "what does a good PR look like?" — both got a runnable, checked-in answer. Together they make the community-pack path self-service instead of reviewer-mediated.

**Shipped to users**
- `a2947c2` — feat: add scripts/validate-pack.sh local pre-flight validator (#495)
  - `scripts/validate-pack.sh`: new 282-line bash validator. ERROR tier (exit 1) mirrors what `install-skill-pack` would reject — bad/missing manifest, illegal slugs, path traversal, missing `SKILL.md`, off-taxonomy capabilities. WARNING tier (advisory) covers publishing-checklist items: missing recommended manifest fields, no LICENSE, missing `SKILL.md` frontmatter. Capability list is *imported* from install-skill-pack, so the two can't drift. (+282/−0)
  - `CONTRIBUTING.md`: documents the validator as the pre-PR step, with the `--path <subdir>` flag for nested manifests. (+8/−0)
  - `docs/community-skill-packs.md`: inserts the validate-pack step into the publishing checklist (now a 7-step flow). (+2/−1)
- `70f3523` — docs: add pull request template (#494)
  - `.github/PULL_REQUEST_TEMPLATE.md`: new contributor-facing surface. What/Why sections + a "Type of change" radio (new skill, new LLM gateway, community pack listing, core fix) each with its own checklist — e.g. the new-skill path enforces `SKILL.md` frontmatter fields, a Sandbox note, `./notify` usage, and running the generators. (+49/−0)

## aaronjmars/aeon-agent

### The agent starts keeping a daily record of itself

**What this is:** The operating instance now watches its own X account every day — and the plumbing that feeds it was repaired so scheduled runs actually get data inside the sandbox.

**Shipped to users**
- `7c0bac2` — feat(tweet-digest): track our own X account daily (#105)
  - `aeon.yml`: flips `tweet-digest` from `enabled: false` to `true` (daily 17:00 UTC). Config-only — reuses the existing account-axis skill, no new skill added. (+1/−1)
  - `memory/topics/tracked-accounts.yml`: new seed file, one account (`aeonframework`), with a `why:` note. Each run fetches recent tweets, dedups against the last 2 days of logs, themes them, notifies. (+6/−0)

**Under the hood**
- `df68b63` — fix(tweet-digest): prefetch via canonical prefetch-xai.sh (#107): adds a `tweet-digest` case to `scripts/prefetch-xai.sh` that loops handles from `tracked-accounts.yml`, honors the `${var}` single-handle override, and writes one `.xai-cache/tweet-digest-<handle>.json` per account before Claude runs. Before this, the workflow only globbed `prefetch-*.sh` and had no tweet-digest case, so every scheduled run hit an empty cache and tried (and failed) to fetch live in the sandbox. Skill's Sandbox Note updated to point at the real path.
- `c8fb707` — fix(feature): avoid output content-filter abort on governance docs (#100): the `feature` skill kept re-selecting `CODE_OF_CONDUCT.md` and re-failing — generating a CoC body trips the model's *output* content-filter (harassment/abuse boilerplate), aborting the whole run (observed run 27617695161). Fix adds step-6 guidance: fetch canonical governance text **straight to disk with `curl -o`** so the body never passes through model output, customize only the non-sensitive enforcement-contact line via a targeted `Edit`, and keep the final summary/notify descriptive. (+5 to `skills/feature/SKILL.md`)

## aaronjmars/minitor

### Onboarding for the dashboard fork

**What this is:** The most-requested minitor contribution — a new column type — now has a guide. Same fork-the-barrier theme as the aeon work, applied to the sibling repo.

**Shipped to users**
- `17f082a` — docs: add root CONTRIBUTING guide with column-plugin walkthrough (#75)
  - `CONTRIBUTING.md`: new 66-line guide. Leads with local setup (Node 20+, PGlite bundled — no Docker/DB/migrations), `git clone … && ./minitor`, then the project layout and a step-by-step "add a column" walkthrough. (+66/−0)

---

## Developer notes
- **New dependencies:** none.
- **Breaking changes:** none. `tweet-digest` enablement (#105) is additive — a new daily notification, no change to existing skills.
- **New public surface:** `scripts/validate-pack.sh` (aeon, new contributor CLI tool); `.github/PULL_REQUEST_TEMPLATE.md` (aeon, shows on every PR); `tweet-digest` case in `scripts/prefetch-xai.sh` (aeon-agent); `memory/topics/tracked-accounts.yml` (aeon-agent, new config file); minitor `CONTRIBUTING.md`. No new HTTP routes, CLI flags, or schema fields.
- **Tech debt added:** none observed in the diffs.

## Open threads
- No branches pushed-but-unmerged in the window — all six human commits landed via merged PRs the same day.
- The content-filter fix (#100) unblocks `CODE_OF_CONDUCT.md` on aeon — the pinned next-pick in MEMORY. Expect the CoC PR to be re-attempted now that `feature` won't abort on it.
- `tweet-digest` (#105/#107) is live but unproven — first scheduled 17:00 UTC run with the new prefetch path is the real test of whether the cache populates in the sandbox.

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 25 (aeonframework automated `chore(cron)`/`chore(scheduler)`/`auto-commit` commits in aeon-agent)
- diff-truncated: 0
