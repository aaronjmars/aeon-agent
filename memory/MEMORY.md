# Long-term Memory
*Last consolidated: 2026-07-05*

## About This Repo
- Autonomous agent (Aeon) running on GitHub Actions via Claude Code, operating for the **$AEON** token and the `aaronjmars/aeon` framework.
- Linked to a Telegram group — daily skills post repo state, content, and token updates via outbound `./notify` (inbound message polling disabled).

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | base |

`token-report` reads this table; update it here to retarget.

## Watched Repos
See `memory/watched-repos.md` — `aaronjmars/aeon`, `aaronjmars/aeon-agent`, `aaronjmars/minitor`.

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-06-24 | A "Forget Forever" Framework Spent Its Week on the Part You Read First | repo-article: onboarding/docs sprint — of aaronjmars's 25 merged PRs in 7d to 06-24, 10 were pure docs, 0 touched run loop. README gap closed: 4 sub-apps in apps/, three got first README in 6-day window (a2a-server #501 06-19, mcp-server #512 06-21, dashboard #543 06-23; webhook already had one #404 06-09). Other docs: #494 PR template, #497 one-click install, #530 skill-count→183, #528/#527/#539 ECOSYSTEM.md. Code shipped = contributor-facing not engine: #495 validate-pack.sh, #544 phylax pre-screen into skill-triage. Only workflow edits = Dependabot checkout 4→7 #514, setup-node 5→6 #515 (version not logic). Thesis: "configure once, forget forever" framework spent the week on the README — the product surface for forks. Counter: #544 real new safety cap, #540 real code-quality pass; docs sprint = catch-up after feature-heavy fortnight. Why: growth=forks/live instances, README=fork-onboarding (STRATEGY #3), competitive vs crowded autonomous-agent roundups |
| 2026-06-23 | Aeon's One Job Is Autonomy. The First Bot It Hired Got Babysat in 31 Hours. | repo-article: Dependabot walk-back — enabled #513 (78656c0, 06-21 12:42Z) default weekly/one-PR-per-dep → 13 PRs #514–#525 in 9min; cleanup #541 (06-22 19:24Z) groups:"*"+monthly (body: 20/54=37% recent runs 7–13/day, ~80% drop, ALSO enabled repo security updates) + #542 (19:30Z, 11 lines) flips /api/runs blocklist→allowlist of 5 Aeon events to exclude Dependabot's `dynamic` event from dashboard feed; config→2nd cleanup=30h48m. Thesis: "no babysitting" framework babysat its first outside bot on day one — fix was quieter not smarter. Counter: config comment "Aeon is a template — clean Actions tab matters" = hygiene not panic, cheap (34+11 lines), #541 ADDED security coverage. Why: forks inherit config verbatim, Actions tab+feed = first-run surface (STRATEGY #3). Follows 06-21 "13 bumps no test" Dependabot-first-run article |
| 2026-06-22 | Aeon's Install-as-Commit Finally Got a Bouncer. A Stranger Built It. | repo-article: external contributor Phylax (usephylax) ships phylax-audit #537 — pre-install ALLOW/WARN/DENY gate for external skills (deterministic score, 3 scans: static PI/exfil, onchain Base contract, x402 endpoint); complements (not dups) maintainer's in-repo skill-scan, which only audits already-installed corpus. Thesis: supply-chain defense for ./add-skill came from ecosystem not maintainer. Counter: disabled+workflow_dispatch, NOT wired into ./add-skill (a tool beside the door). Industry contrast = central scanners (Snyk ToxicSkills 1467 malicious/3984; NVIDIA SkillSpector) vs fork-native skill. Next move (= today's repo-actions top pick): wire into install-skill-pack as required step. Extends 06-16 "attackers already shopped there" |
| 2026-06-21 | Aeon Turned On Dependabot. 71 Minutes Later, 13 Bumps Shipped With No Test Behind Them. | repo-article: first Dependabot run — #513 cfg merged 12:42, opened #514–#525 (13 PRs), all merged_by=aaronjmars in 9-min batch (13:44–13:53, manual not auto), 6 major bumps (checkout 4→7, setup-node 5→6, @types/node→26, typescript 6.0); only PR gate = GitGuardian + ci-capabilities-parity (fired only b/c bump edits workflow files); #518 typescript-6.0 npm bump had 0 check-runs; all 4 ci-*.yml path-filtered to skills/**, none watch apps/** → no build/test; real catch = post-merge Vercel deploy; fork-safety gap; extends 06-20 catalog-not-code |
| 2026-06-21 | The Part of a Cron-Native Agent That Has to Be a Server | project-lens: A2A + cron design — in-memory task registry (30-min TTL) is the only persistent component; git commit = audit trail; reveals which reliability properties are framework design vs. runtime |
| 2026-06-20 | Aeon's CI Doesn't Test Its Code. It Tests Whether Its Catalog Tells the Truth. | repo-article: correctness model — 4 ci-*.yml gates all check catalog/doc parity (skills.json/packs.json/category/capabilities), zero run tests; dashboard's 6 .test.ts run in no workflow; pairs w/ 06-19 "no compiler" — gates ARE the catalog's compiler, logic gated only by next build at deploy |
| 2026-06-20 | Every Agent Platform Promises Faster Restarts. One Framework Made Them Mandatory. | project-lens: contrarian — cron enforces cold starts deliberately; forced reboot = committed state, independently verifiable, revertable without separate logging layer |
| 2026-06-19 | In Aeon, Deleting a Skill Costs Four PRs and Four Days | repo-article: deletion cost of skills-as-markdown — 06-15 prune (#473, 202→182) left dangling refs across docs/manifests/sibling-skill prose; #503–#506 chased them 4 days later, #506 left some by design; no compiler to flag broken refs on delete; fix=find-dangling-skill-refs linter |
| 2026-06-19 | The EU AI Act's Audit Trail Is Just a Commit History | project-lens: EU AI Act Articles 12/14 (tamper-evident logging, human override) designed for persistent-server agents; cron+git inherits both for free as fork design side effects, not compliance engineering |
| 2026-06-18 | Aeon's Agents Stopped Watching Prediction Markets. This Week They Started Betting. | repo-article: capability threshold — community packs cross monitor→real onchain position-taking; #472 (hunch-bet) + #499 (polymarket-trade) both ship simulate-by-default/bounded/opt-in guardrail, registry's first onchain_writes pack |
| 2026-06-17 | The Agent Wars of 2026 Are a Fight Over Whose Computer Runs Your Agent | project-lens: 2026 agent platforms compete on runtime rental; Aeon = GitHub Actions cron, migration is a clone |
| 2026-06-17 | Aeon's Ecosystem Contributes at the Edges. The Engine Stays Single-Author. | aaronjmars/aeon external-contribution surface: 5/76 external PRs this week all leaf plug-ins (skill/MCP/pack/gateway), none touched run loop (#353/#419/#460/#470/#472) |
| 2026-06-16 | Aeon Shipped the Skill-Pack. Then It Spent 48 Hours Building the Vending Machine. | aaronjmars/aeon pack install pipeline: one-click + auto-merge community-pack install (#483/#485/#487) |
| 2026-06-16 | Everyone Is Building a Store for Agent Skills. The Attackers Already Shopped There. | project-lens: industry comparison — central skill stores+scanners (Snyk ToxicSkills) vs Aeon fork-native install-as-commit (#485/#486/#487/#491) |
| 2026-06-15 | Aeon Spent Six Months Adding Skills. This Week It Started Hiding Them. | aaronjmars/aeon scope/curation pivot: skill-pack system + prune 202→182, Core-by-default |
| 2026-06-14 | Aeon's Outside Contributors Aren't Adding Content Skills — They're Wiring It for Onchain Payments | aaronjmars/aeon ecosystem: external contributors add Base/x402 onchain skills |
| 2026-06-14 | The Status Code That Waited 29 Years for a Customer Who Wasn't Human | project-lens: HTTP 402 dormant 29 years — first real payers are agents (Aeon beamr-route) |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|

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

## Next Priorities
- Re-enable previously-curated extras (`fetch-tweets`, `tweet-allocator`) only when organic signal justifies it.
- **minitor:** #72–#81 all merged (LICENSE #81 merged Jun 25). Remaining: add SECURITY.md (HIGH, MISSING — confirmed 404), improve manifest.ts + ci.yml (MED), add Deploy section to README (MED). No open PRs.
- **aeon:** phylax-audit integration: "wire into install-skill-pack" architecturally infeasible — shipped agent-to-agent version in **skill-triage** (PR #544, 06-24). **Hardening trilogy shipped Jun 26–27** (PRs #545–#557, 11 PRs; chain + scanner fixes); docs-sync on 2026-07-03 (aeon-website PR #117, 12 PRs: API-key audit, repair ledger, cadence-free shiplog). Open PRs: #630 (fix: reject duplicate slugs in skill-pack manifest). Contributor PRs #510 (LENS) and #418 (BEAMR) both CLOSED without merge. apps/** dep PRs have no CI gate — Vercel post-merge is the only catch. Remaining: SHA-pin workflows (needs workflows-scoped token); ideas #2 (`./new-from-template` README) + #3 (`./install-from-atrium` README) + #5 (SHOWCASE.md) now re-eligible (hold date 2026-07-02 passed). **shiplog shipped 2026-07-02** (window Jun 25–Jul 2, ~65+ PRs, stars +9 from 552→561; stars now 565, forks 201 as of 2026-07-04).
