# Week in Review: The Catalog Finally Knew Its Own Size, And A Second Outsider Shipped An MCP Server

*2026-06-08 — Weekly shipping update*

## The Big Picture

This was the week the project stopped lying to itself about how big it was. On Friday the upstream catalog refresh shipped in eight back-to-back PRs and reconciled the README, `skills.json`, and the MCP-server tool labels onto the same number — 193 — across a new 8-category taxonomy with `core`, `onchain-security`, and `meta` finally split out from the muddle. Two brand-new external contributors landed substantive code (Nurstar's `skill-of-the-day` meta-content rotation, vigilcodes' VIGIL onchain-security MCP server). The HoundFlow keyless security pack that had been sitting workflow-dispatch-only since May-28 finally got a standing weekly consumer. The downstream fork extended its same-day-after backport chain from day 17 to day 23. Minitor incremented its per-column UX axis literally every weekday — eight rungs in seven days, and a deck-color sibling on Sunday.

## What Shipped

### The 8-PR taxonomy refresh on Friday

The upstream catalog had drifted. `README.md` said 156 skills, `skills.json` carried 193, and 65 of those 193 were sitting in an untyped `other` bucket that no dashboard filter could surface. In one stacked push (#342 → #350, Friday 12:43–19:01 UTC) the maintainer ported 8 skills from his private `aeon-aaron` fork (`fear-divergence-scout`, `beat-tracker`, `article-queue`, `picks-tracker`, `content-performance`, `api-health-probe`, `mention-radar`, `thread-writer`), rebuilt `generate-skills-json` so every previously-`other` skill mapped to a real category, expanded the taxonomy from 5 → 8 keys with a **first-match-wins core block** that elevates the 15 load-bearing self-evolution / fleet / autonomous-action skills out of `dev` and `productivity`, then wrote `docs/CORE.md` to document the mechanics of each. Even the README banner JPG got renamed so GitHub's camo CDN cache-busts on the new image. First time the three surfaces agree on the same numbers.

### Wallet-Risk-Weekly — HoundFlow finally has a runner

Six keyless Base-RPC investigation skills (`approval-audit`, `honeypot-check`, `lp-lock-check`, `linked-wallets`, `fund-flow`, `investigation-report`) landed on aeon's main on Monday (PRs #281–#287), closing the week-long HoundFlow review queue. They'd been sitting workflow-dispatch-only with no scheduled consumer since 2026-05-28. On Thursday `wallet-risk-weekly` (PR #340) became the first one: every Monday 11:15 UTC it scans the wallets in `.x402books/wallets.json` for live ERC-20 approvals, dedupes per unique token, runs an `eth_call`-only honeypot simulation from a sampled holder, and buckets into HIGH / MEDIUM / LOW / CLEAN. INCONCLUSIVE never escalates — false-flagging the operator's own wallets would erode the alert signal everywhere else. By Sunday the maintainer shipped the write-side companion (`vigil-revoke`, PR #354, still open at write time) — strict triplet allowlist, Bankr ownership pre-check, pre-revoke `allowance` short-circuit-to-NOOP, post-revoke receipt poll. Detection and revoke loops, both closed in the same week.

### Two new external contributors

Nurstar's `skill-of-the-day` (PR #341, Thursday) is a daily meta-content rotation that picks one skill, drafts a paste-ready "Aeon skill of the day 🌟" tweet, then dispatches the picked skill so the operator can screenshot the live notify as the `Result ⤵️` body. Queue + 30-day-covered window + blocklist, all operator-editable. First contribution from this account. vigilcodes' VIGIL (PR #323, also Thursday) is a 9-tool MCP-server submission at `https://mcp.vigil.codes` — onchain security scanning for Base via JSON-RPC `tools/call`. Five review cycles tightened it: endpoint moved from raw IP to TLS, capability declaration corrected from `read_only` to `external_api`, a critical shell-injection vector in the user-supplied wallet address closed with a strict `^0x[0-9a-f]{40}$` allowlist, and four more tools added to the catalog. The state-changing approval-revoke was deliberately split out into a separate future skill — VIGIL itself stays read-only.

### Capabilities taxonomy went load-bearing

Monday's catch-up wave landed the CI parity gate (#304) that makes adding a 7th capability value structurally impossible without updating all three sources of truth (`install-skill-pack` bash array, `docs/CAPABILITIES.md`, header comment). Same window: `capabilities-map` (PR #313), a Monday-morning audit that joins frontmatter declarations + `aeon.yml` + `skill-packs.json` to surface coverage gaps per tier. Within 24h the fix landed too (PR #319) — fresh-instance bootstraps were flagging all six tiers as gaps for the trivial reason that nobody had declared anything yet, training operators to ignore the signal; the fix introduces a `COVERAGE_ASSESSABLE` precondition so undeclared instances go quiet instead of false-alarming. Tuesday's Phase-1 sweep (PR #322) annotated 19 high-blast-radius skills in a single commit — every onchain skill plus every key-spending surface.

### Ecosystem catalog became visual

ECOSYSTEM.md had been a name-and-handle list since launch. In a single Tuesday evening (PRs #327–#334, 19:10–19:31 UTC) the table gained a Logo column and got walked alphabetically by seven batched PRs until every row carried a 36×36 square avatar. Most logos point at Twitter's stable `_400x400` URL; the Autonomopoly row uses CoinGecko because GeckoTerminal's `_next/image` proxy is hotlink-protected. Five X-handle corrections (Clerk, Liq, RootAi, Gitlawb Terminal, Precog) rode along — silently fixing the otherwise-permanent error where the table linked to wrong accounts. Four fresh entries joined: HivemindOS, Echo Oracle, Reppo, Atrium, Sparkleware, VIGIL, Hound Flow. Friday added 9 more (Aeon City, Charon, CTRL, DarkSol, Hunch, Prism, Sentysis, Venice Deity, XergAI). The new `ecosystem-entrants` weekly skill (PR #339, Wednesday) will diff every Monday from now on.

### Atrium's third install path closed its loop

Wednesday's `install-from-atrium` CLI (PR #335) made the Atrium onchain marketplace the third live way to install a skill, sitting alongside the curated `skill-packs.json` registry and direct `add-skill` URL fetch. Friday's `atrium-catalog-watcher` (PR #342) added the supply-side watcher — Friday 12:00 UTC weekly diff of the Atrium catalog, with copy-pasteable install commands on every added row. Three weekly digests now cover marketplace arrivals (Atrium), curated registry health (sparkleware-catalog), and installed-skill drift (skill-update-check) with zero overlap.

### Minitor: a per-column feature every weekday + two on Sunday

Eight rungs of the per-column UX axis incremented in seven days: collapse to 48px (Mon, #55) → JSON export (Mon, #56) → quick-search filter (Tue, #58) → pin-to-front (Wed, #59) → duplicate (Thu, #60) → column color labels (Fri, #61) → deck color labels + width control (Sun, #62, #63). Each one orthogonal to the others — a pinned collapsed orange column at narrow width stays all four. The DB-backed features (pin / color) round-trip through export / import / share-links / snapshots; the view-state-only features (collapse / search / width) reset on reload, matching the existing pattern. Two small fixes rode along: surfacing `COINGECKO_DEMO_API_KEY` in the Settings dialog (#54) and dropping a TS2783 duplicate-role warning on the collapsed strip (#57).

## Fixes & Improvements

- **PR #266** — `skill-update-check` ACCEPT-mode overwrites now re-scan the new version before writing. Closed the last open item in AntFleet bench finding #258.
- **PR #309** — first real dashboard unit-test coverage. 71 tests across `config`, `utils`, `frontmatter` libraries. node:test + node:assert, no framework deps.
- **PR #280** — first-class `ANTHROPIC_BASE_URL` support for Anthropic-compatible API endpoints (Bedrock proxies, Anthropic-shim providers). Auth route distinguishes 3 cases (API key / OAuth / Base URL).
- **PR #306** — `token-report` reads `.x402books/wallets.json` and reports treasury ETH. `⚠️ Treasury gas reserve low` notification override fires even on QUIET verdicts when the agent can't afford gas.
- **PR #318** — `pr-merge-queue` skill: morning brief bucketing every open PR by touched-file risk tier.
- **PR #231** — `liquidpad-launch` finally landed after the prefetch/postprocess shim shipped, becoming the first contributor PR through the new pr-skill-triage gate.
- **aeon-agent self-fixes** — heartbeat (#71), repo-pulse (#77), repo-article (#81), repo-actions + star-momentum-alert (#83) all swapped `$(date ...)` shell substitution for runner-injected `${today}`. Every known site in the anti-pattern chain is now closed.
- **PR #84** — `self-improve` now reads `memory/cron-state.json` directly instead of running the sandbox-blocked `./scripts/skill-runs`. Three consecutive runs had silently worked around the same blocker.

## By the Numbers

- **PRs merged:** ~57 across 3 repos (aeon ~30, aeon-agent 17, minitor 10).
- **Substantive feature PRs:** ~25.
- **Catalog growth (upstream aeon):** 156 → 193 enabled skills (+37), `other` bucket emptied from 65 to 0.
- **Lines:** roughly +7,000 / −1,000 of human-authored code (excluding the 8-PR catalog refresh's regenerated artifacts).
- **Distinct authors merged:** 15 — aaronjmars, vigilcodes, Nurstar, rsavitt, Atrium-Hermes, sparkleware, LiamVisionary, BuiltByEcho, AISynthetics, UIZorrot, BBridgeers, antfleet-ops, houndflow, liquidpadbot, mandateseal.
- **Backport chain (aeon-agent):** 17 → 23 consecutive same-day-after days.
- **Releases:** 0.

## Momentum Check

Densest contributor week on record. Last week's weekly-shiplog opened with "11 skills in a day" — this week opened with the same 6 HoundFlow skills actually merging into main, then layered an 8-PR catalog refresh, two brand-new external contributors, the first scheduled HoundFlow consumer, the first detection→revoke loop closure, and 8 per-column features on the dashboard frontend. The Monday firehose held — no weekend stalls this week — and the operator's open-PR queue stayed near-zero throughout. The pace is no longer just the maintainer's velocity; the contributor surface is doing real work.

## What's Next

Three open PRs are queued for review (aeon #354 vigil-revoke, aeon-agent #85 already landed, minitor #63 already landed). `aeon` sits at 487 stars with a projected 500⭐ crossing on Thursday 2026-06-11 — inside the 7-day Show HN dispatch window, so `show-hn-draft` won't fire thoughtfully before the milestone; the natural near-term wire-up is auto-dispatching `show-hn-draft` from `star-milestone` at the 500-cross. Four of the five remaining HoundFlow security skills (`lp-lock-check`, `linked-wallets`, `fund-flow`, `investigation-report`) still lack scheduled consumers — `vigil-revoke` closed the write-side gap, but the read-only inventory has more standing-runner opportunities. And the new Atrium / capabilities / ecosystem-entrants weekly skills will publish their first real diffs on Monday — the first week where the catalog instrumentation watches itself instead of being watched by hand.

---

*Sources: aaronjmars/[aeon](https://github.com/aaronjmars/aeon), aaronjmars/[aeon-agent](https://github.com/aaronjmars/aeon-agent), aaronjmars/[minitor](https://github.com/aaronjmars/minitor); daily push-recap articles `articles/push-recap-2026-06-01.md` through `articles/push-recap-2026-06-07.md`.*
