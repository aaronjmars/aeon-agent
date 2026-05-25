# Week in Review: The Week Aeon Grew a Package Manager

*2026-05-25 — Weekly shipping update*

## The Big Picture

This was the week Aeon stopped looking like a framework with an examples folder and started looking like a distribution with a package set. Forty-one PRs merged across the three repos — and the through-line wasn't new agent capabilities, it was *how skills get distributed, discovered, and trusted*. A one-command install CLI, a machine-readable pack registry, a 121→155 skill catalog jump, and an ECOSYSTEM.md that outsiders immediately started self-listing into. In parallel, the AntFleet security audit's open findings got worked down to nearly zero — mostly by the audit bot patching its own findings — and Minitor finished its deck-portability stack end to end.

## What Shipped

### Community skill packs became a real distribution platform

A week ago, "community skill packs" meant a Markdown table in the README and a clone-and-copy-by-hand workflow. By Friday it was a protocol. `install-skill-pack` (aeon #213, +720) landed as a Bash CLI that reads a `skills-pack.json` manifest, runs each declared `SKILL.md` through the existing security scanner, and installs on PASS with provenance recorded in `skills.lock`. The next morning it grew a discovery layer: a machine-readable `skill-packs.json` registry plus `./install-skill-pack --list` (aeon #215, +238) that prints every known pack with a trust badge — seeded live from each pack's own manifest, not hand-curated. Docs, a manifest schema, and a publishing checklist shipped alongside.

Then the ecosystem showed up to use it. AntFleet's pack cleared the trusted-sources fast-path on day zero. LiquidPad and Luca registered themselves. `lawb-pool-monitor` arrived as the first *community-authored on-chain skill* — a 227-line PR watching a Base-mainnet prize-pool contract, written by an outside author who already understood the SKILL.md format, the `aeon.yml` registration pattern, and the state-file dedup convention. And `ECOSYSTEM.md` (aeon #220) — a registry for products *built on* Aeon, distinct from forks and skill packs — got its first community self-listing within nine hours of merging, which is exactly the behavior it was designed to invite.

The catalog itself jumped from 121 to 155 skills in a single PR (#219, +6,162 across 36 files) that ported 34 skills back from derivative Aeon instances. That one merge is why the framework's surface area now reads more like a small Linux distro's package list than a typical agent library's `examples/` directory.

### The security audit got worked down to one open finding

AntFleet's two-model bench review (Issue #184, 27 findings filed mid-May) had a backlog of High-severity bugs that all shared one shape: code that ran to completion but silently produced wrong output instead of erroring. This week closed eight of them. PRs #194–#197 took H2/H5/H6/H8 (Slack bot-filter string-`"null"` check, token-paste reassembly, the macOS POSIX-ERE scanner bug, the AdManage spend-cap numeric guard). Then #201/#203/#204/#206 closed H3/H4/H7/H9 in a single morning push — `FORK_DEFAULT_BRANCH` never being set, fleet-state's `.bak` that was never created, skill-update-check ignoring the lock's `branch` field, and AdManage dropping campaignId-only ad sets from state. The notable part: the `antfleet-ops` audit account authored most of these patches itself. By Saturday only H1 (v4-readiness manifest coverage) remained — and that fix is already open in PR #226.

### Minitor finished its deck-portability stack

Minitor spent the week completing two arcs. On column coverage, three new types landed in 24 hours — GitHub Discussions (#43), CoinGecko (#44), and DeFiLlama (#45) — taking it to 47 column types and closing both its last GitHub-monitoring gap and the on-chain "what's the price/TVL?" gap. On portability, the export→import→share chain finished: a share-link feature (#46) that base64url-encodes a deck into a `#deck=` URL fragment, a starter-templates gallery (#47) that gets a fresh install from blank dashboard to five live columns in two clicks, and a public, SEO-crawlable `/gallery` route (#48). All three stack on the same DeckExport v1 schema and the same `importDeck` server action — no new validation path, no new server route schema.

## Fixes & Improvements

- **Dashboard hardening (aeon):** loopback Host + same-origin gate on `/api/*` (#188), `next` 16.2.6 + postcss override (#189), `gh` CLI preflight with platform-specific install hints (#190), and stricter token-paste reassembly (#194).
- **External integrations (aeon):** an opt-in Fleet Watcher authorization layer (#200) — the first pre-skill veto gate in the workflow — and Resend email delivery wired into morning-brief and weekly-review (#205).
- **Scanner parity (aeon-agent):** backported the Bash 3.2 array-emptiness guards + POSIX-ERE pattern rewrite (#56), bringing every macOS operator's scanner posture in line with upstream.
- **Self-corrective (aeon-agent):** word-boundary notify suppression so real sub-120-char notifications stop getting silently swallowed (#57); refresh-x rewired off the broken direct-curl path onto the prefetch cache (#51).
- **Contract hygiene (aeon-agent):** project-lens's mathematically-impossible 14-day rotation rule relaxed to a feasible 7-day window (#54).

## By the Numbers

- **PRs merged:** 41 across 3 repos (aeon 26, aeon-agent 9, minitor 6)
- **Lines:** +12,604 / −347
- **File-changes:** ~138 (PR #219's 34-skill port accounts for 36 of them)
- **Contributors:** aaronjmars (operator + Aeon bot), antfleet-ops, danbuildss, wx888, fleet-watcher — 5 distinct merged authors, plus community pack/skill PRs in flight
- **Releases:** 0 (Aeon ships continuously off `main`, not tagged releases)

## Momentum Check

Accelerating, and the shape of the acceleration changed. The headline metric isn't a feature — it's a 28% catalog jump (121→155) and a distribution protocol that went from nonexistent to operator-tested in 72 hours. External contribution is the real tell: five distinct authors merged this week, a community-authored production skill arrived as a PR, and self-listings started appearing on day-zero infrastructure. The fleet itself grew 47→86 active forks in the same window per the latest skill-leaderboard — the largest single-week expansion on record. The autonomous loop is visibly tightening too: the audit bot is now filing *and* fixing its own findings within days.

The timing is worth noting. This was a release week across the broader agent-framework field — LangGraph, CrewAI, Mastra, and Pydantic-AI all shipped (Pydantic-AI began a v2.0 beta series). Aeon's answer wasn't a competing core feature; it was distribution plumbing — an install CLI, a registry, an ecosystem map. Different bet on what an agent framework needs next.

## What's Next

Six PRs sit open in aeon from Saturday's work: AntFleet's next security sweep (#222 workflow_dispatch injection, #223 GATEWAY quoting, #224 notify dedup-before-delivery), the v4-readiness H1 close (#226), and two ecosystem self-listings. Aeon-agent has the install-skill-pack + registry backport (#59) and a self-corrective fetch-tweets fix (#60) queued; Minitor has per-column refresh intervals (#49). The repo-actions pipeline has fresh ideas seeded — an `ecosystem-pulse` skill to monitor the 40 ECOSYSTEM.md projects, a fleet-skill-adoption leaderboard, a config-validator backport, a Bluesky column, and column-level webhook alerts. Expect next week to keep building on the distribution layer the ecosystem just started leaning on.

---
*Sources: [aeon](https://github.com/aaronjmars/aeon) · [aeon-agent](https://github.com/aaronjmars/aeon-agent) · [minitor](https://github.com/aaronjmars/minitor) · ecosystem context via [LangGraph/CrewAI/Pydantic-AI framework landscape, 2026](https://dev.to/linou518/the-2026-ai-agent-framework-decision-guide-langgraph-vs-crewai-vs-pydantic-ai-b2h)*
