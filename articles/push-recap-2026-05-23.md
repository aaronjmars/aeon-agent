# Push Recap — 2026-05-23

## Overview
Six substantive PRs opened in the last 24h across three repos — and four of the six are community ecosystem moves. The day after `install-skill-pack` shipped, the registry surface grew up: a machine-readable `skill-packs.json` mirror landed, two new community packs (AntFleet table row, LiquidPad row) registered themselves, and the first community-authored on-chain skill (`lawb-pool-monitor`) opened a PR with hourly Base-mainnet prize-pool surveillance. Aeon-agent picked up another backport in the same-day-after chain, and Minitor turned its deck-templates work into a public SEO-crawlable gallery.

**Stats:** ~10 files changed, +664 / -8 lines across 6 substantive PRs (plus ~35 cron auto-commits on aeon-agent main that aren't counted here)

---

## aaronjmars/aeon

### Community skill pack registry: README → machine-readable
**Summary:** The morning after the `install-skill-pack` CLI shipped, the registry surface got a JSON twin. `skill-packs.json` at the repo root now mirrors the README's Community Skill Packs table for both the CLI and any future dashboard / third-party indexer, and two community packs registered themselves into the table in the same window.

**Commits:**
- `c9e2c31` — feat: machine-readable skill-packs.json registry + --list browsing (PR #215, +238/-5)
  - New file `skill-packs.json` (+84): five seed entries with full schema — AntFleet/aeon-skills (trust_level=trusted), baseddevoloper/aeon-skill-pack-vvvkernel (9 skills), danbuildss/luca-aeon-skills (4 skills), 0xShak/zer0-skill-pack (6 skills, PR #208 still open), gitlawbounty/gitbounty-skill-pack (PR #212 still open). Slug lists were sourced live from each pack's own `skills-pack.json` or its `skills/` directory listing, not hand-curated.
  - Changed `install-skill-pack` (+92/-4): adds a new no-repo-arg branch so `./install-skill-pack --list` prints the registry (repo, skill count, trust badge, one-line description) without dragging in the install flow. Detector is strict — any other flag or positional argument falls through to the existing single-pack path, so prior behaviour is preserved. Reads local `skill-packs.json` first, falls back to `https://raw.githubusercontent.com/aaronjmars/aeon/main/skill-packs.json` when the script runs outside a clone.
  - Changed `docs/community-skill-packs.md` (+59/-1): new "Browse the registry" section, full registry schema with worked JSON example, field reference table (repo/name/description/author/license/homepage/category/trust_level/skills), and a publishing-checklist update mandating that new pack PRs add BOTH a README row AND a `skill-packs.json` entry in the same diff.
  - Changed `README.md` (+3): Community Skill Packs section now leads with the `--list` command and the bullet list of submission rules gains the new dual-update requirement.

- `32ad66b` — docs: add AntFleet skill pack to community packs table (PR #216, +1) — `antfleet-ops` adds the `AntFleet/aeon-skills` row to the README table on the same day. AntFleet was already on the trusted-sources allowlist (PR #211, yesterday), but the README didn't have a row pointing at the pack yet. PR opens with a single-line table addition.

- `ce75c2d9` — docs(community-packs): list aeon-skill-pack-liquidpad (PR #217, +1) — `liquidpadbot` registers `liquidpadbot/aeon-skill-pack-liquidpad`, a new 4-skill pack consuming only LiquidPad's public CORS endpoints (`/api/burn`, `/api/stats`, `/api/token-stats`, `/api/verify`) — no auth, no rate-limit token, no upstream dependency on Aeon infrastructure beyond the manifest install protocol. Commit message explicitly notes "LiquidPad is an independent third-party project on Liquid Protocol's open primitives, not affiliated with Aeon or Liquid Protocol."

**Impact:** Yesterday the install protocol existed but the discovery surface was a Markdown table. Today there's a JSON registry that `./install-skill-pack --list` reads, the publishing checklist forces both surfaces to stay in sync on every new pack PR, and two more packs (AntFleet's existing one, LiquidPad's brand-new one) are sitting against the new requirement. The first time the dual-update rule will get tested in production is whichever of #216 or #217 merges first.

### First community-authored on-chain skill
**Summary:** lawbworld-tech opened PR #214 with `lawb-pool-monitor` — an hourly cron skill watching the LawbFishing prize-pool contract on Base mainnet. This is Aeon's first community-contributed skill that calls a smart contract directly (existing crypto skills like `token-report` read CEX/aggregator APIs).

**Commits:**
- `03da78c` — feat(skills): lawb-pool-monitor — watch LawbFishing prize pool health on Base
- `cfad83d` / `451ba4d` — rename and naming-convention fixes (lawb-pool-monitor folder/SKILL frontmatter match)
- `a5407d3` — chore(lawb-pool-monitor): auto-commit (the bot ran on the feature branch)
- `aa5c7fe` / `d689c52` / `1079725` / `39455e5` / `9ea0aee` / `d4153b0` / `0f789d4` — cleanup commits: contributor accidentally committed bot-generated outputs (`.outputs/`, `dashboard/outputs/`, `memory/`, `scripts/postprocess-devto.sh`) on the feature branch, then deleted them and restored `postprocess-devto.sh`. Net effect: only `aeon.yml` and the SKILL file remain changed.

**Final diff** (+228 lines, 2 files):
- New file `skills/lawb-pool-monitor/SKILL.md` (+227): contract proxy `0x48b2db9E89542Baa217bf8dc6269164b7887fE57` on chain 8453, four read-only selectors documented (`prizePool()` `0x719ce73e`, `shopVault()` `0x29c2aa0a`, `paused()` `0x5c975abb`, `MIN_PRICE()` `0xad9f20a6`), plus the `Redeemed(address,uint256,bytes32)` event topic for burn tracking. Calls go via `https://mainnet.base.org` with Etherscan v2 as the documented fallback. State persisted to `memory/lawb-pool-monitor-state.json` with `last_block`, `last_pool_wei`, `last_run`, and four `alerted_conditions` keys (low_pool / shop_vault_nonzero / paused / high_burn) for dedup. Alerts fire only when thresholds trip — silent by default.
- Changed `aeon.yml` (+1): hourly cron `0 * * * *`, `enabled: false`, with an inline comment naming the threshold-gated behaviour.

**Impact:** The skill ships as `enabled: false` like every new skill — the operator decides whether to flip it on. But the contribution itself is notable: an external author already understood the SKILL.md format, the `aeon.yml` registration pattern, and the state-file convention (last-block + alerted-conditions dedup) well enough to ship a 227-line skill in one PR. The shape of community contributions just expanded from "table-row PR" to "production skill PR."

---

## aaronjmars/aeon-agent

### Backport cadence continues — contributor-spotlight FORK_DEFAULT_BRANCH
**Summary:** Verbatim backport of upstream aeon PR #206 (merged May 21). 11th same-day-after backport in the established chain (operator-scorecard, skill-freshness, skill-update-check, fork-cohort, thread-formatter, v4-readiness, product-hunt-launch, fork-first-run-alert, fork-skill-gap, competitor-launch-radar, and now this).

**Commits:**
- `951155c` — fix: contributor-spotlight FORK_DEFAULT_BRANCH never set (aeon PR #206 backport) (PR #58, +12/-2)
  - Changed `skills/contributor-spotlight/SKILL.md`: step 4 now extracts `FORK_DEFAULT_BRANCH=$(jq -r '.default_branch // "main"' /tmp/contrib-repo.json)` with a second-line null-string guard (`[ -z "$FORK_DEFAULT_BRANCH" ] || [ "$FORK_DEFAULT_BRANCH" = "null" ] && FORK_DEFAULT_BRANCH=main`). Step 5's `gh api .../contents/aeon.yml?ref=${FORK_DEFAULT_BRANCH}` now resolves to the right branch on forks whose default isn't `main` (operators on `master`, `develop`, or custom defaults previously got silent 404s).
  - Step 5's fallback tightened from `|| true` to `|| echo '' > /tmp/fork-aeon.yml`. Reason: the next line greps the file under `set -e`, and an absent file would abort the skill. An explicit empty file keeps the run going with zero enabled-skill count rather than crashing.
  - Inline comment names upstream Issue #184 H3 + PR #206 so the guard doesn't get cleaned up by a future refactor.

**Impact:** Without this fix, `contributor-spotlight`'s two most newsworthy data points — `ENABLED_COUNT` (how many Aeon skills the featured fork has flipped on) and `OPERATOR_AUTHORED` (whether the fork has skills upstream doesn't) — were silently wrong on every fork that renamed its default branch. PR #58 keeps the backport chain unbroken at 11 in a row.

---

## aaronjmars/minitor

### /gallery — public, SEO-crawlable deck catalog
**Summary:** Builds entirely on the existing share-link (PR #46, May 21) + templates (PR #47, May 22) infrastructure — no new schema, no new server routes, no new validation surface. The /gallery page renders deck-template cards server-side with deterministic share URLs, and the existing landing-page hash-import path imports them on click.

**Commits:**
- `bbb6714` — feat: /gallery public deck page (PR #48, +184/-1, 2 files)
  - New file `app/gallery/page.tsx` (+173): server-component route with `Metadata` export (Open Graph title/description, canonical `/gallery`), responsive card grid keyed off `TEMPLATES` from `lib/deck-templates.ts`. Each card renders as a plain anchor pointing at `/#deck=<base64url(payload)>`. The payload deliberately omits `exportedAt` so each template generates a stable URL across requests — the page is cache-friendly and individual template URLs are shareable on their own (the URL itself contains the deck).
  - Changed `components/sidebar-01/nav-footer.tsx` (+11/-1): adds a `LayoutTemplate`-icon "Browse deck gallery" `<Link>` above the existing Add-new dropdown so returning operators discover the gallery from inside the dashboard.

**Impact:** PR #46 made deck sharing a one-click copy. PR #47 made starter templates a built-in. PR #48 closes the loop: starter templates now have a public URL surface that Google indexes, that gets pasted into Twitter/Discord, and that imports into the visitor's session via the same hash-fragment path the share-link feature uses. No new validation, no new route schema, no new server action — three primitives stacking cleanly.

---

## Developer Notes
- **New dependencies:** None across any PR. PR #48 reuses `lucide-react` (already in dependencies) for the new `LayoutTemplate` icon.
- **Breaking changes:** None. PR #215 is additive (new file + new CLI mode + new docs section); PR #58 is a bugfix; PR #48 is a new route.
- **Architecture shifts:**
  - aeon now has TWO surfaces for community packs: the README table (humans) and `skill-packs.json` (machines). Yesterday it had one. The publishing checklist now enforces both stay in sync.
  - aeon-agent's backport cadence is at 11-in-a-row, mostly bugfix backports — the chain is becoming load-bearing for upstream→downstream skill parity.
- **Tech debt:** PR #214's commit history is noisy (11 commits, half are "Delete X" cleanups of bot-generated files committed by accident on the feature branch). Net diff is clean, but if the maintainer merges without squash the commit log will reflect that. The squash flow on aeon's `--auto`-merge skill (PR #38) handles this automatically.

## What's Next
- The community-packs registry just became a coordination surface for at least 5 packs. Two PRs (#216 AntFleet, #217 LiquidPad) opened today add table rows but **not** corresponding `skill-packs.json` entries — which means PR #215's dual-update rule will see its first test the moment either of those merges. Maintainer may need to ask the contributors to add the JSON entry, or accept the table-only PRs and update the JSON in a follow-up.
- PR #214's `lawb-pool-monitor` is the first PR-shaped community SKILL contribution; if it merges cleanly it sets the template for "skill PRs that aren't pack-shaped" — direct contributions into `skills/` rather than into a third-party pack repo.
- PR #208 (zer0-skill-pack) and PR #212 (gitbounty-skill-pack) are still open with no new commits in the window — they'll need rebases against PR #215 if the maintainer wants their `skill-packs.json` entries to land in their own PRs rather than in #215.
- The two community pack docs PRs (#216, #217) opened nine minutes apart from different authors. Combined with #214's full-skill contribution and yesterday's three community pack PRs, that's seven distinct external authors contributing across the last 48 hours.
