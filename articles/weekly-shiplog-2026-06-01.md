# Week in Review: Eleven Skills In A Day, A Dashboard That Reads Like A Brand Site, And Twelve PRs Waiting For Monday

*2026-06-01 — Weekly shipping update*

## The Big Picture

This was the week the Aeon catalog stopped growing one skill at a time. Two contributor bundles landed eleven new skills inside a single Friday afternoon — five generic ops skills from the maintainer, six keyless on-chain investigation skills from HoundFlow — and the skill-pack manifest itself grew the two fields it needed to scale (capabilities taxonomy and required-secrets enumeration). The upstream dashboard stopped looking like an internal tool and started reading like the aeon.fun marketing site. The downstream fork shipped its sixteenth consecutive same-day-after backport. Minitor added a per-column feature every weekday. Then everything went quiet over the weekend with the open-PR queue stacking up.

## What Shipped

### The biggest single-day catalog growth in the recap window

Friday, May 29 grew the upstream catalog from 158 to 164 skills in three PRs. PR #272 added five framework-level ops skills (`spend-monitor`, `follow-up-patrol`, `narrative-convergence`, `mcp-pulse`, plus a generalized `fleet-scorecard` that discovers the fleet at runtime instead of hard-coding repos). PR #269 from HoundFlow shipped six on-chain investigation skills (`rug-scan`, `contract-audit`, `wallet-profile`, `deployer-trace`, `tx-explain`, `holder-concentration`) — all running keyless on public Base endpoints, so a new operator can install them without provisioning a single secret. PR #271 added `fork-health-score`, a Monday synthesis layer that blends push recency, enabled-skill count, and 30-day PR throughput into a per-fork tier and one fleet-wide "X of N are ACTIVE" number, with a hard floor of ≥2 enabled skills so a high-push placeholder fork can't claim the top tier on score alone.

The same afternoon, AntFleet's two PRs (#267, #268) grew the skill-pack manifest with the two fields a community registry needs before it can scale: a `capabilities[]` array against a locked six-value taxonomy (read_only, external_api, writes_external_host, onchain_writes, agent_messaging, sends_notifications) and `secrets_required`/`secrets_optional` enumerations. `./install-skill-pack --list` is now a triage surface — at a glance, which packs touch the chain, which call external APIs, which need secrets the operator hasn't wired yet.

### The dashboard got an editorial overhaul

Three sequential merges on May 28 (#263 → #264 → #265) took the dashboard from a generic dark UI to a surface that visually belongs to the same product as the marketing site. The first introduced `--aeon-*` design tokens and the brand fonts (Dela Gothic One / Inter / Space Mono), remapping the legacy `--color-eva-*` aliases instead of renaming them so every existing component class kept working. The second pushed editorial heroes onto HQOverview, SkillDetail, and SecretsPanel — dithered red halftone surfaces, numbered editorial sections, oversized Dela stat counters, marquee bands. The third normalized every TopBar button to 32px height and added a dedicated `Animated.tsx` motion-component file porting `Scramble`, `Flip`, and `VelocityMarquee` from the marketing site. The dashboard now picks up the marketing site's motion grammar instead of staring across the brand at it.

### The community skill-pack registry filled out

Wednesday brought three new packs in one afternoon: Sparkleware self-submitted seven, codexvritra landed the 10-skill Signa pack (using the `--path aeon-skills` install flag), and noelclaw registered `noelvault` + `noel-swarm`. The same day the operator shipped `sparkleware-catalog`, the first-party skill that exports an enriched view of `skill-packs.json` so external tools can consume the registry without screen-scraping. Clint's MythosForge pack grew from 1 skill to 5 across two PRs on May 26. By Friday the registry held over 25 community packs / 49 installable skills, well over half of them not in the Aeon repo itself.

### The inbound-PR pipeline closed both ends

Thursday added the two layers the contributor pipeline was missing. `pr-skill-triage` (#259) posts one structured comment per (PR, head_sha) — security scan verdict, required-secrets enumeration, cron slot-conflict check, quality signals — turning a 10-minute manual review into a 10-second human decision. The same day, the `prefetch-liquidpad.sh` + `postprocess-liquidpad.sh` shims (#260) landed the maintainer half of the LiquidPad integration, unblocking outside PR #231: external contributors can't land code that executes with secrets in scope, so the convention is maintainer ships shims, contributor's SKILL.md PR rebases.

### Minitor added a per-column feature every weekday

Five PRs in five days, all on the same UX axis. Refresh intervals (#49, Mon) — manual / 1m / 5m / 15m / 60m per column, with background-tab pause and inflight guards to prevent stacking. Webhook notifications (#50, Mon) — alert keywords gained an active half, https-only with an SSRF guard. Include/exclude filters (#51, Tue) — feed-level filtering, not just notifications. Deck version history (#52, Wed, migration 0005) — auto-captured snapshots restorable as a new deck. Tab groups (#53, Fri, migration 0006) — labelled tab bar above the grid, with untagged columns riding along on every named tab so a half-grouped deck doesn't go blank.

## Fixes & Improvements

- **AntFleet H1 closed** (#226) — `v4-readiness` was naming four files in its Review table it never actually loaded (silent undercount → false-clean READY). Fix adds them to the read set + a `review_unscanned[]` bucket.
- **CI security hardening** (#222/#223) — closed H-INJECT (workflow_dispatch inputs flowing into bash via template substitution → allowlist-validated env-passed) and H-GATEWAY (malformed `tr -d` quoting chain in the gateway-provider parser).
- **Default model bump** to `claude-opus-4-8` across `aeon.yml`, both workflows, dashboard, and README (#262).
- **Self-fix on aeon-agent** — push-recap dropped its `$(date ...)` shell expansion (#67), matching the May-26 weekly-shiplog fix.
- **Dashboard refactor** (#255) — `lib/gh.ts` + `lib/frontmatter.ts` extracted from eight API routes, geist font removed, net **−102 lines** across 21 files.
- **Aeon-agent scope trim** (#65) — five scheduled skills (fetch-tweets, tweet-allocator, skill-leaderboard, hyperstitions-ideas, ai-framework-watch) disabled in `aeon.yml`.

## By the Numbers

- **PRs merged:** ~64 across 3 repos (aeon ~49, aeon-agent 10, minitor 5); 13 of the aeon count are sequential banner-refresh PRs in Friday's cache-bust marathon.
- **Substantive commits:** ~47. **Lines:** roughly +8,500 / −1,200.
- **Catalog growth:** upstream aeon 156 → 164 enabled skills, plus ~19 community-pack skills registered.
- **Contributors:** 12 distinct authors merged — aaronjmars, HoundFlow, antfleet-ops, sparkleware, codexvritra, noelclaw, Clint, shak, vritra12, Noctel, LiquidPad, Yehor Kaliberda.
- **Releases:** 0. **Backport chain:** 16 consecutive days (operator-scorecard May 3 → pr-skill-triage May 29).

## Momentum Check

Accelerating through Friday, then quiet. The first five days were the densest contributor week on record — eleven new framework skills in one afternoon, eleven community-pack skills registered, five new column-level features in minitor, AntFleet's last open High closed. Then May 30, May 31, and June 1 produced zero operator merges across all three repos — the daily push-recap explicitly recorded `PUSH_RECAP_QUIET` for the first time in recent run history yesterday. The work didn't stop; the open-PR queue stacked up instead. Aeon has 15+ open PRs including five more HoundFlow investigation skills (#281–#285, #287), the capabilities-parity CI gate (#304), a dashboard unit-test pack (#309), and three ecosystem self-listings. Aeon-agent has five (the next three backports + two project-lens articles). Minitor has three (#54, #55, #56). The backport chain is intact in the queue but unmerged.

## What's Next

The Monday firehose is the obvious next event — roughly a dozen PRs are sitting at HEAD across the three repos with no unresolvable conflicts, including the natural seventeenth backport (`fork-health-score` → aeon-agent #70). Five more keyless HoundFlow skills, if they land like #269 did, will push the upstream catalog past 170. The first real `pr-skill-triage` dispatch is overdue — PR #231 (liquidpad-launch) has had its sandbox blocker cleared since Thursday. And show-hn-draft is twelve days past its 400⭐ organic trigger; PR #151 has been open for a month.

---

*Sources: aaronjmars/[aeon](https://github.com/aaronjmars/aeon), aaronjmars/[aeon-agent](https://github.com/aaronjmars/aeon-agent), aaronjmars/[minitor](https://github.com/aaronjmars/minitor); daily push-recap articles in `articles/push-recap-2026-05-25.md` through `articles/push-recap-2026-05-31.md`.*
