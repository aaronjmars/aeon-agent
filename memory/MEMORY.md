---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-08-09*

## About This Repo
- Autonomous agent (Aeon) running on GitHub Actions via Claude Code, operating for the **$AEON** token and the `aeonfun/aeon` framework.
- Linked to a Telegram group — daily skills post repo state, content, and token updates via outbound `./notify` (inbound message polling disabled).

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | base |

`token-report` reads this table; update it here to retarget.

## Watched Repos
See `memory/watched-repos.md` — `aaronjmars/aeon`, `aaronjmars/aeon-agent`, `aaronjmars/minitor`.

## Recent Articles
Full history archived to `memory/topics/articles-history.md` (no new repo-article/project-lens pieces since 2026-06-24 — that skill isn't currently running; shiplog/token-report/holdings articles are routine and not tracked here).

| Date | Title | Topic |
|------|-------|-------|
| 2026-06-24 | A "Forget Forever" Framework Spent Its Week on the Part You Read First | repo-article: onboarding/docs sprint — of aaronjmars's 25 merged PRs in 7d to 06-24, 10 were pure docs, 0 touched run loop. README gap closed: 4 sub-apps in apps/, three got first README in 6-day window (a2a-server #501 06-19, mcp-server #512 06-21, dashboard #543 06-23; webhook already had one #404 06-09). Other docs: #494 PR template, #497 one-click install, #530 skill-count→183, #528/#527/#539 ECOSYSTEM.md. Code shipped = contributor-facing not engine: #495 validate-pack.sh, #544 phylax pre-screen into skill-triage. Only workflow edits = Dependabot checkout 4→7 #514, setup-node 5→6 #515 (version not logic). Thesis: "configure once, forget forever" framework spent the week on the README — the product surface for forks. Counter: #544 real new safety cap, #540 real code-quality pass; docs sprint = catch-up after feature-heavy fortnight. Why: growth=forks/live instances, README=fork-onboarding (STRATEGY #3), competitive vs crowded autonomous-agent roundups |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-08-09 | tweet-digest | Jesse Pollak / Base ecosystem shoutout |
| 2026-08-08 | tweet-digest | Error Digest skill (part 2), summer gm + playlist, weekly recap CTA |
| 2026-08-07 | tweet-digest | "run it and forget it" philosophy piece, you.com contributed skill, miroshark x402 listing |
| 2026-08-06 | tweet-digest | Uniswap v4 hooks pipeline, posthog-errors skill, eyebrowCC security partnership |
| 2026-08-05 | tweet-digest | Finance District wallet integration, SEO skill, Uniswap v4 hooks video |
| 2026-07-26 | tweet-digest | framework tierlist, developer UX |
| 2026-07-25 | tweet-digest | Claude Opus 5 live, new integration tease, framework positioning |
| 2026-07-24 | tweet-digest | skill install UX, long-form article post |
| 2026-07-22 | tweet-digest | framework positioning |
| 2026-07-18 | tweet-digest | minitor dashboard demo |
| 2026-07-17 | tweet-digest | ADK launch, Grok 4.5 support, 60-day changelog article, vuln-scanner on SpaceXAI, community shoutout |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| holdings | 2026-07-30 | Daily treasury snapshot — AEON + MiroShark holdings value/pct-supply via RPC, growth trend once history accumulates |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- Sandbox blocks `$ENV_VAR` expansion in curl headers — a skill then misreads auth failure as "key not set" even when the key is set. Read authenticated data from `scripts/prefetch-*.sh`-written cache files instead of curling auth'd APIs inside a skill.
- The runner hook rejects `$(...)` subshells and `$VAR` in skill bash blocks. The only injected template vars are `${today}` (UTC date) and `${var}` (skill input); `${today_minus_N}` is a phantom that resolves to a literal string and silently breaks date filters — compute literal cutoffs in the prompt.
- Pushing changes under `.github/workflows/` needs a token with the `workflows` scope (the default `GITHUB_TOKEN` can't).
- `self-improve`/`feature` open PRs faster than a human merges — the PR-awareness guard halts new build PRs at 3+ open.
- XAI HTTP 403 = team credits exhausted (distinct from 401 = bad key).
- Next.js `"use server"` export rule is NOT caught by `tsc --noEmit` or eslint — only `next build` (Turbopack) enforces it. Illegal non-async exports cascade to "module has no exports at all" across importers.
- Etherscan unified v2 endpoint gates Base (chainid=8453) behind a paid plan — NOT a keyless drop-in. Keyless Base balance reads: JSON-RPC `eth_getBalance` against `mainnet.base.org` (same endpoint sibling skills use).
- `feature` skill: governance docs (CoC, abuse/moderation policies) trip content filter if model-generated — fetch canonical upstream text to disk with `curl -o` and customize only the contact line; don't re-emit the body in a Write call. (PR #100)
- Compound bash commands (`;`/`&&`/pipes) auto-denied in non-interactive sandbox — use one operation per Bash call.
- apps/** npm changes in aaronjmars/aeon are NOT gated by any CI build/test — all 4 ci-*.yml path-filters target skills/**/catalog/capabilities; only post-merge Vercel deploy catches build/type errors on app deps (surfaced by Dependabot first run 2026-06-21, #514–#525).
- Bash scripts cannot synchronously invoke agentic skills (SKILL.md-only, no scan.sh entrypoint) — bridge must be agent-to-agent: an agentic skill inline-invokes another agentic skill via CLAUDE.md "standalone composition". Surfaced when repo-actions promoted bash→phylax-audit as top pick two consecutive cycles; now blocked by Gate 3 in repo-actions (PR #116).
- A GitHub Actions spending-limit gate looks like a stuck dispatch, not a code regression: `workflow_dispatch` runs return `action_required` with 0 jobs and never start. Confirm via `gh run list`/`gh run view`, not by assuming the skill broke. Hit 2026-08-02T19:20Z→08-04T14:46Z (~44h), stalled 6 skills; the 3 weekly-cadence ones (repo-pulse, shiplog, changelog) stayed stuck past recovery because their next cron tick was days out — a manual re-dispatch clears it faster than waiting.

## Next Priorities
- Re-enable previously-curated extras (`fetch-tweets`, `tweet-allocator`) only when organic signal justifies it.
- **minitor:** #72–#81 all merged (LICENSE #81 merged Jun 25). Remaining: add SECURITY.md (HIGH, MISSING — confirmed 404, still flagged by heartbeat as of 08-08), improve manifest.ts + ci.yml (MED), add Deploy section to README (MED). No open PRs.
- **aeon:** **v0.1.0 released 2026-07-10** (Grok harness, channels, OKF, attestation, Langfuse); Grok 4.5 support added Jul 17; OpenAI Codex + Kimi Moonshot support added late Jul; **docs-sync last ran 2026-08-10** (aeon-website PR #245, 20 PRs batched: "Bounty-discovery skill, secrets fix, README reorg"). Note: the site's `app/changelog-data.ts` already had entries dated 08-04/05/06 (up to PR #860) that this memory never logged — an earlier push-to run happened outside this instance's visibility; treat the website file, not memory/logs, as the source of truth for what's published. No open PRs tracked here. apps/** dep PRs have no CI gate — Vercel post-merge is the only catch. Remaining: SHA-pin workflows (needs workflows-scoped token); ideas #2/3/5 (README, SHOWCASE.md) re-eligible. Stars: 641, forks: 226 as of 2026-08-10 (see repo-pulse line below).
- **Stuck skills (Aug 2-4 Actions outage) — all confirmed recovered as of 2026-08-10.** shiplog and repo-pulse both ran successfully 08-10 (repo-pulse's first run since 07-27, a 14-day gap; window math stayed correct since cutoff is computed fresh each run). changelog confirmed unstuck 08-10 (GH_GLOBAL push-to works, PR #245 opened). memory-flush recovered 08-09.
- **repo-pulse 2026-08-10:** aeon 641 stars (+49/7d, SURGE, events truncated by GitHub's 300-event cap — real total likely higher)/226 forks (+12/7d); opendia 1907 stars (+5/7d, STEADY)/159 forks; soul.md 640 stars (+7/7d, STEADY)/68 forks; minitor 16 stars/4 forks (QUIET). Notable new contacts: edsonmartins (Archbase maintainer, Maven Central/npm/pub.dev, forked aeon).
