---
type: Article
---

# Push Recap — 2026-06-22

## Verdict
> SHIPPING — phylax-audit gates external skill installs; docs-sync auto-publishes changelogs

**Shape:** 2 user-visible commits · 8 internal · 1 infra · 42 bot-filtered (5 dependabot + 37 automation)
**Volume:** ~20 files changed, ~+600/−126 lines across 11 non-automation commits by 3 authors (aaronjmars, Phylax, aeonframework)
**Merged PRs:** 11 human (#537, #539, #531, #530, #529 on aeon; #110, #111, #112, #113, #114 on aeon-agent; #78 on minitor) + 5 dependabot

---

## aaronjmars/aeon

### [New skill: phylax-audit — pre-install security verdict]

**What this is:** Phylax (external contributor) shipped a new `phylax-audit` skill that issues an ALLOW / WARN / DENY verdict on any external skill before it gets installed. It runs a static scan for prompt-injection patterns and secret-exfiltration indicators, probes the skill's claimed x402 endpoint, and runs a Base contract audit if the skill references an onchain address — merged into one deterministic score. Complements the in-repo `skill-scan` by catching external threats at the gate, before `./add-skill` runs. Registered as `workflow_dispatch`, disabled by default.

**Shipped to users**
- `764cd11` — feat(skill): add phylax-audit (#537)
  - `skills/phylax-audit/SKILL.md`: new skill definition — accepts a skill ref (`owner/repo/<name>`, raw SKILL.md URL, or local path) and returns ALLOW / WARN / DENY with a scored breakdown across static analysis, contract probing, and endpoint verification (+~120/−0)
  - `aeon.yml`: phylax-audit registered in the hound pack as `workflow_dispatch` (+1/−0)
  - `packs.json` / `skills.json`: regenerated from full git history, correcting stale per-skill `sha`/`updated` fields that a prior shallow-checkout run had set to a uniform stale value (+2/−2)
- `bbc35ba` — docs: add Phylax to ECOSYSTEM.md (#539)
  - `ECOSYSTEM.md`: one line — Phylax listed as an ecosystem contributor (+1/−0)

**Under the hood**
- `beefa58` — chore(skills): remove stale references to pruned skills (#531): cleaned up 78 lines of dangling cross-references to three skills pruned in the June 15 sweep (ecosystem-entrants, competitor-radar, token-report) across SKILL.md files, aeon.yml, docs/status.md, and the bug-report issue template. References were repointed to surviving equivalents (launch-radar, ecosystem-pulse, etc.) or removed where no equivalent exists.
- `b8a860b` — docs(readme): sync skill count to 183 (#530): README had three stale counts (182 in the intro, a stray 197 in the hero, 13 core skills in the catalog row) — corrected to 183/183/14 after `install-skill` joined core.
- `f87fb2d` — chore: update LICENSE copyright to Aeon Inc (#529): copyright holder updated (+1/−1).

---

## aaronjmars/aeon-agent

### [New skill: docs-sync — auto-publish merged PRs as a website changelog]

**What this is:** The aeon-agent repo gained a `docs-sync` skill that turns the product repo's merged PRs into a changelog entry on the marketing website, submitted as a draft PR. It is config-driven (`memory/docs-sync.md` sets `product_repo` / `website_repo`), idempotent by PR number, and handles a "bootstrap" path that creates the full changelog surface (page, nav link, docs teaser) when none exists. Scheduled daily at 08:00 UTC. Requires `GH_GLOBAL` for cross-repo write access.

**Shipped to users**
- `7c25c06` — feat(skill): add docs-sync (#110)
  - `skills/docs-sync/SKILL.md`: 179-line skill spec — PR fetch → idempotency dedup → classify highlights vs noise → write `ChangelogEntry` → branch + commit + PR on the website repo; bootstrap path wires full page, nav, and docs teaser to site conventions (+179/−0)
  - `aeon.yml`: docs-sync registered `enabled: true`, `schedule: "0 8 * * *"` (+1/−0)
  - `memory/docs-sync.md`: new config file setting `product_repo: aaronjmars/aeon`, `website_repo: aaronjmars/aeon-website`, `lookback_days: 7`, `draft: true` (+10/−0)

**Infra**
- `c1a7930` — fix(attribution): always commit cross-repo work as aeonframework (#114)
  - `.github/workflows/aeon.yml` + `chain-runner.yml`: changed `git config` to `git config --global` so freshly cloned repos in a run inherit the `aeonframework@proton.me` identity instead of falling back to an improvised email (+4/−4)
  - `skills/docs-sync/SKILL.md`: added explicit `git config user.name/email` lines inside the clone step with a note explaining why the workflow-level setting doesn't carry over (+4/−0)

**Under the hood**
- `c6e470e` — feat: validate --hours is a positive integer in skill-runs (#112)
  - `scripts/skill-runs`: guards `--hours` with a positive-integer regex immediately after arg parsing; bad values (non-numeric, negative, zero) fail fast with a clear message rather than passing through to GNU/BSD `date` and producing a cryptic abort under `set -euo pipefail` (+7/−0)
- `379a4f2` — docs-sync: hide PR link from notification output (#113): removed the `PR: <url>` line from the step-6 notify template in `skills/docs-sync/SKILL.md`; the link stays in `memory/logs/` for traceability but no longer clutters the channel notification (+0/−3)
- `7a10bfc` — feat(shiplog): 2026-06-22 article (#111): auto-generated daily shiplog covering the pack pipeline arc and six external contributors.

---

## aaronjmars/minitor

### [Internal: search query validation across Grok-backed columns]

**What this is:** Five Grok-powered columns (x-search, news-search, facebook, instagram, google-news) now trim the configured search query and throw `"Search query is required."` if it's blank or whitespace-only. Before this, an empty query fired a Grok API call that returned an opaque error with no pointer to the real cause. Farcaster and bing already had this guard; this brings the rest in line.

**Under the hood**
- `133ffc9` — feat: validate non-empty search query in Grok-backed columns (#78)
  - `lib/columns/plugins/x-search/server.ts`, `news-search/server.ts`, `facebook/server.ts`, `instagram/server.ts`, `google-news/server.ts`: each adds a two-line `trim() / if (!q) throw` guard before calling the Grok fetcher, and passes the trimmed value downstream (+20/−14 across 5 files)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none
- **New public surface:** `phylax-audit` skill (workflow_dispatch, hound pack) — input: skill ref or URL, output: ALLOW/WARN/DENY verdict; `docs-sync` skill (daily 08:00 UTC) — cross-repo changelog publisher; `scripts/skill-runs --hours` now validates its argument
- **Tech debt added:** none (phylax-audit's shallow-checkout manifest bug was caught and fixed in the same PR)

## Open threads
- **PR #418** (feat(gateway): BEAMR LLM gateway) — stalled since 2026-06-16, no activity in window
- **PR #510** (LENS skill pack, external contributor) — open, under review
- **CODE_OF_CONDUCT.md** (PR #538) — opened and closed without merge on 2026-06-22; reason unclear from diff data; re-queued

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 42 (5 dependabot + 37 aeon-agent automation chore commits)
- diff-truncated: 0 (phylax-audit patch was large but readable; docs-sync patch loaded fully)
