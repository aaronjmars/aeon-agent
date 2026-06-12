# Push Recap — 2026-06-12

## Verdict
> SHIPPING — operator-onboarding suite (SOUL + STRATEGY tabs + builder skills) plus two community x402/on-chain skills

**Shape:** 12 user-visible commits · 5 internal · 3 infra · ~34 bot-filtered (automation churn)
**Volume:** ~81 files changed, +2,568/−220 lines across 18 merged PRs by 4 authors
**Merged PRs:** 18 — aeon #444–#459 + #419 + #353 (16), aeon-agent #97 (1), minitor #71 (1)

> Note: aeon #443 (`wc-resale` digest-every-run) merged at 16:10Z, inside this window's edge, but was already covered in the 2026-06-11 recap — excluded here to avoid double-counting.

---

## Top impact today
1. `d7a2359` — **dashboard: SOUL.md tab + soul-builder skill (#448)**. Adds a whole identity-authoring surface to the dashboard: SOUL.md/STYLE.md editors, a template picker, and a "build my soul from X/name/links" form wired to a new `soul-builder` skill. The single largest change of the day. (12 files, +1,011/−8)
2. `6397ff2` — **dashboard: STRATEGY.md tab + strategy-builder (#451)**. Mirrors the soul flow for the operator's north-star: a 6-template picker and a "build my strategy" form backed by a no-API-key `strategy-builder` skill that grounds the draft in goal + README + memory. (8 files, +546/−7)
3. `19078a6` — **dashboard: auto-sync config edits + default model → Sonnet 4.6 (#447)**. Local config edits now auto-commit-and-push so scheduled GitHub runs see them, closing a silent UI-vs-main divergence; also collapses 72 per-skill model pins into one global default. (8 files, +120/−91)

---

## aaronjmars/aeon

The day's center of gravity. Two threads dominated: a self-service **onboarding/config UI** for operators (soul + strategy authoring), and **two new ecosystem skills from outside contributors**.

### Operator onboarding — author your soul & strategy from the dashboard

**What this is:** Operators can now write the two files that steer every Aeon run — `soul/` (voice/identity) and `STRATEGY.md` (north-star) — directly from the dashboard, with templates, one-click real-soul installs, and AI builders. No more hand-editing files and remembering to push.

**Shipped to users**
- `d7a2359` — dashboard: SOUL.md tab + soul-builder skill (#448)
  - `apps/dashboard/components/SoulPanel.tsx`: new 268-line panel with SOUL.md/STYLE.md editors, a template picker, and a multi-source "build my soul" form (+268/−0)
  - `apps/dashboard/lib/soul-templates.ts`: blank scaffold + Founder/Researcher/Creator archetypes (+343/−0)
  - `skills/soul-builder/SKILL.md`: new `workflow_dispatch` skill that drafts SOUL.md/STYLE.md from an X handle / name / links via xAI prefetch + WebSearch (+236/−0)
  - `apps/dashboard/app/api/soul/{route,build/route}.ts`: GET/PUT both files; dispatch the builder with a URL-safe brief (+117/−0)
- `6397ff2` — dashboard: STRATEGY.md tab + strategy-builder (#451)
  - `apps/dashboard/components/StrategyPanel.tsx`: template picker (blank + 5 archetypes) + "build my strategy" form (+123/−3)
  - `apps/dashboard/lib/strategy-templates.ts`: Indie SaaS / OSS / Researcher / Crypto-Agent / Creator archetypes (+202/−0)
  - `skills/strategy-builder/SKILL.md`: no-API-key builder enforcing the ~2000-char budget so STRATEGY.md stays cheap to load every run (+146/−0)
- `9b2ed03` — dashboard: one-click install real souls from the soul.md gallery (#449): an "install a real soul" grid (karpathy, garry-tan, steipete, vivian-balakrishnan) that copies a full SOUL/STYLE/examples set into `soul/` and commits. Also fixed misleading "then hit Push" save copy — saves already auto-push. (+106/−5)
- `19078a6` — dashboard: auto-sync config edits + default model → Sonnet 4.6 (#447): config writes now commit+push in local mode; global model default set once instead of 72 per-skill pins. (+120/−91)
- `6fd9685` — dashboard: hide Claude Code Connect button once auth is set (#446): the OAuth Connect button no longer renders when either auth path (OAuth token or API key) is already configured. (+5/−1)
- `7b29a2d` — docs: document STRATEGY.md + SOUL.md builders in the README (#453): new Strategy section and a rewritten Soul section leading with the four dashboard paths. (+19/−5)

**Under the hood**
- `66d35e0` — soul-builder: guard against cross-person conflation (#452): adds a provenance step so every bio fact must trace to a source about the subject, and bans the subject's own tool/gallery repos as bio sources — the bug was the builder stitching another person's bio in from sample souls. (+12/−1)
- `scripts/prefetch-xai.sh`: new `soul-builder` case pulling a wide 12-month X sample (part of #448).

### New ecosystem skills — x402 inference & on-chain automation

**What this is:** Two community-authored skills landed, both crypto/Base-flavored and both inert until an operator opts in with the right secrets.

**Shipped to users**
- `f210fb7` — feat(skill): beamr-route — pay-per-call inference over x402 with onchain receipt (#419, by SahilParikh03)
  - `skills/beamr-route/scripts/beamr-pay.mjs`: buyer-side x402 client (`createSigner` → `wrapFetchWithPayment`) that pays for one inference call in USDC on Base, capped by `BEAMR_MAX_PAY_USDC`, emitting one JSON line (+88/−0)
  - `skills/beamr-route/SKILL.md`: unlike the silent gateway path, each run produces a verifiable onchain artifact (the settlement tx hash) reported alongside the answer (+58/−0)
  - Self-guards: skips cleanly (exit 0) when `BEAMR_*` secrets are unset.
- `f32b27d` — skills: add CTRL — on-chain automation on Base (#353, by daxaur)
  - `skills/ctrl/SKILL.md`: compiles natural-language intents (DCA, price-gated swaps, launchpad sniping) into a CTRL workflow; the wallet signs an EIP-5792 batch once, the CTRL keeper handles triggers after, bounded by signed per-swap/per-day caps. Agents never hold keys — activation returns a hosted `signUrl`. (+224/−0)

### Dashboard reliability

**Shipped to users**
- `b29c752` — fix(dashboard): gate skill runs on provider key, fix NaNd-ago, refresh on pull (#459)
  - `apps/dashboard/lib/utils.ts` + `utils.test.ts`: fixes "NaNd ago" in the feed — output filenames stamp time with hyphens (`...T14-30-00Z`, since `:` is illegal in paths), which `new Date()` can't parse; the outputs route now converts back to ISO and `timeAgo()` returns "" for anything unparseable, with a regression test (+10/−1)
  - The "Run now" button now blocks and flashes an error when no provider key (`AUTH_SECRETS`) is set, instead of firing a run that can't authenticate; "Pull from GitHub" now refreshes the whole dashboard. (+15/−3 across page/sidebar/outputs route)

### Internal: skills.json drift gate (CI)

**What this is:** A recurring failure class — `skills.json` going stale when a generator input changes without a regen — got a permanent CI guard plus the cleanup it surfaced.

- `9f66864` — ci: add ci-skills-json gate enforcing skills.json regen-in-PR (#457): regenerates the manifest from `skills/*/SKILL.md` + `aeon.yml` and fails any PR that changed a generator input without committing the refresh. Handles two correctness traps: `fetch-depth: 0` (per-skill sha/updated come from `git log --follow`) and normalizing the `generated` timestamp out of the diff. (+57/−1)
- `1681192` — ci(skills-json): normalize per-skill sha/updated in the gate + heal manifest (#458): squash-merging a skill PR rewrites that skill's sha, which would false-fail the *next* innocent skills PR — so the gate now compares only semantic catalog fields. (+22/−13)
- `0b16302` — fix: categorize wc-resale as productivity in get_category() (#456): `wc-resale` was the lone skill falling through to the `other` backstop (absent from the dashboard's category map); now resolves to `productivity`. (+2/−2)
- `e16c74a` — skills: fix 3 notify ISS-009 violations, name log paths, drop dead var declarations (#444): conformance sweep across 198 skills — three skills switched from `./notify "$(cat ...)"` to `./notify -f`, two got named log paths, nine dropped no-op `var: ""`. (+16/−12, 14 files)
- `82e85ad` — chore: regenerate skills.json after #444 (#445). (+1/−1)
- `5d41d7f` — ecosystem: add Hivra (#450). (+1/−0)

---

## aaronjmars/aeon-agent

Mostly automation churn (cron-state + per-skill auto-commits — ~34 commits, filtered). Two substantive changes:

### Internal: skill + config fixes

**Shipped to users**
- `10b7630` — fix(token-report): use keyless public Base RPC for treasury balances (#97)
  - `skills/token-report/SKILL.md`: step 2b's treasury fetch repointed from the deprecated keyless `api.basescan.org` to a public, keyless Base JSON-RPC `eth_getBalance` against `${BASE_RPC_URL:-https://mainnet.base.org}` — the pattern the sibling Base skills already use. An earlier attempt at Etherscan v2 (`?chainid=8453`) was abandoned because that endpoint is paid-tier-only for Base. Resolves yesterday's `treasury=fetch_fail`. (+14/−10)

**Infra**
- `8e81799` — chore(messages): disable inbound message handling: turns off the TG/Discord/Slack message→skill path (poll collection + processing job); the cron scheduler is unchanged so scheduled skills/chains keep running. Reversible via inline comments.

---

## aaronjmars/minitor

### The build fix (critical)

**What this is:** `main` did not build. This PR fixes it.

**Shipped to users**
- `66b2a92` — fix: move non-action exports out of "use server" actions.ts so the app builds (#71)
  - `app/actions.ts` carried `"use server"` (async-function exports only) but also exported six plain values (`REFRESH_INTERVAL_OPTIONS`, `isAllowedRefreshInterval`, `TAB_GROUP_MAX`, `COLOR_HEX_RE`, `normalizeColumnColor`, `DECK_EXPORT_VERSION`), which made the whole module fail to load and cascaded into 62 "module has no exports at all" build errors.
  - Fix: hoisted the constants + sync validators into a new plain module `lib/deck-rules.ts`, re-imported them into `actions.ts`, and repointed the client store. `next build` now compiles all routes; `tsc` + eslint clean. `tsc` never caught this — only `next build` enforces the rule. (+76/−54, 3 files)

---

## Developer notes
- **New dependencies:** none added to lockfiles. `beamr-route` installs `x402-fetch` on-demand at runtime (not a committed dep).
- **Breaking changes:** none for end users. Internal: the global default model moved to `claude-sonnet-4-6` and 72 per-skill `model:` pins were removed (#447) — every skill now tracks the single default. `minitor` importers of the six hoisted constants must now import from `lib/deck-rules.ts` (#71).
- **New public surface:** dashboard Soul + Strategy tabs; API routes `/api/soul`, `/api/soul/build`, `/api/strategy/build`, `/api/soul/examples`; two new skills (`soul-builder`, `strategy-builder`) + two ecosystem skills (`beamr-route`, `ctrl`); secrets `BEAMR_GATEWAY_URL`, `BEAMR_PAYER_KEY`; var `BASE_RPC_URL` declared in token-report `requires`.
- **Tech debt added:** none visible in the diffs.

## Open threads
- **minitor Dexscreener column plugin** — built, tsc/lint-clean, held back behind the #71 build fix (per 2026-06-12 memory log). #71 is now merged and `main` builds, so the fast-follow PR is unblocked.
- Two external contributors (SahilParikh03, daxaur) shipped skills this window — ecosystem contribution momentum worth tracking.

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: ~34 (aeon-agent cron/scheduler/auto-commit automation)
- diff-truncated: 0
