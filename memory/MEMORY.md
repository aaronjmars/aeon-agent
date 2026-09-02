---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-08-30*
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
Older rows archived to `memory/topics/digests-history.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-09-02 | tweet-digest | Content & Shipped (self-healing loop blog post, skill catalogue plug), Security disclosures (Graphify-Labs/graphify vuln), Growth & Partnerships (UsePodAI cheaper-inference shoutout) |
| 2026-08-30 | tweet-digest | Security disclosures (vuln-scanner flagged synthetic-sciences/openscience, private advisory + fix PR filed) |
| 2026-08-29 | tweet-digest | Skill Drop & Content (aeon vs another framework comparison), Growth & Partnerships (aeon x FD_XYZ x CoinMarketCap), Security disclosures (TencentCloud TencentDB-Agent-Memory vuln) |
| 2026-08-28 | tweet-digest | Skill Drop & Content (aeon vs ChatGPT comparison article), Security disclosures (vuln report + PR to @hanghuang_/@insforge) |
| 2026-08-27 | tweet-digest | Security disclosures (nvidia SkillSpector vuln, OomolStudio open-connector vuln), Shipped & content (BlockEcho hook, GitHub Actions autonomous-agent blog post), Comparisons (aeon vs Claude Code) |
| 2026-08-26 | tweet-digest | Shipped (Uniswap v4 hooks live on mainnet, 7-harness skill portability, vuln-scanner v2 teaser), Comparisons (aeon vs NousResearch Hermes rumble #1), Miroshark (x402 football sim reminder) |
| 2026-08-25 | tweet-digest | Shipped & Content (BlockEcho Uniswap hook, soul.md/strategy.md blog post, google/agents-cli fix), Growth (CoinMarketCap listing tease), Community (Telegram stickers) |
| 2026-08-24 | tweet-digest | Growth (700-star milestone push), Skill Drop (Aeon Update skill), Ecosystem (FD_XYZ wallet integration, Hivemind shoutout), Security (vague "security angle" teaser) |
| 2026-08-23 | tweet-digest | Skill Drop (Weekly Card Run spotlight), Growth ("welcome back to aeon" recap/invite) |
| 2026-08-22 | tweet-digest | Skill Drop — Spend Watch (spending-report skill announcement + aeon.fun CTA follow-up) |
| 2026-08-21 | tweet-digest | Skill Drops (vuln-scanner skill, Remotion skill spotlight), Security disclosures (private advisories to @jeffreykim0711, @relakkesyang), Growth (weekly recap follow/star CTA) |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| holdings | 2026-07-30 | Daily treasury snapshot — AEON + MiroShark holdings value/pct-supply via RPC, growth trend once history accumulates |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- Sandbox blocks `$ENV_VAR` expansion in curl headers — a skill then misreads auth failure as "key not set" even when the key is set. Fix: use `./secretcurl` with a literal `{ENV_NAME}` placeholder (see CLAUDE.md Network & Secrets), not a raw curl. The older prefetch-cache-file workaround is retired — don't reintroduce it.
- The runner hook rejects `$(...)` subshells, `$VAR` expansion, and stdout redirection (`>`) in skill bash blocks. The only injected template vars are `${today}` (UTC date) and `${var}` (skill input); `${today_minus_N}` is a phantom that resolves to a literal string and silently breaks date filters — compute literal cutoffs in the prompt. Workaround for redirection-shaped work (e.g. a 3-way file merge): drive it via `git` subprocess calls from Python instead of shell `git merge-file ... > out` (used by `aeon-update` PR #198, 08-25).
- `aeon-update` sync: brand-new upstream skills that need `bin/generate-*`/catalog regen or the `eyebrow` ci-skill-integrity scan can't be auto-installed in this sandbox (those tools don't run here) — hold them back in `pending_conflicts` and defer to a one-line manual step in the sync PR body rather than risk landing a catalog-inconsistent, CI-red PR. Surfaced 08-25 (PR #198): `skills/rightstack/`, `skills/skill-article/` held back this way.
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
- aeon.fun/security's scraper is brittle to upstream markup churn: a CSS-module class rename (`page_row__xxxxx` → `page-module__eEUUaa__row`, 08-22) caused a silent 0/74 PARSE_EMPTY while `cron-state` still recorded `last_status: success` — exact-class selectors can fail without tripping failure detection. Match structurally (owner/repo-shaped capture, GitHub href) instead of by literal class name; secured-watch self-fixed both this and a separate RSC-hydration-payload regex false-positive by 08-23.

## Next Priorities
- Re-enable previously-curated extras (`fetch-tweets`, `tweet-allocator`) only when organic signal justifies it.
- **minitor:** #72–#81 all merged. SECURITY.md confirmed present at `.github/SECURITY.md` (re-verified 08-14; old "MISSING" flag was a false positive from checking only the repo root path). Remaining: improve manifest.ts + ci.yml (MED), add Deploy section to README (MED). No open PRs. (Canonical at `aeonfun/minitor`.)
- **aeon:** v0.1.0 released 2026-07-10 (Grok harness, channels, OKF, attestation, Langfuse); Grok 4.5 + OpenAI Codex + Kimi Moonshot support added late Jul. docs-sync (changelog push-to) last ran 2026-08-31 (aeon-website draft PR #402, entry "GLM gateway move + fail-closed adapters" covering #954 + #980–#998); treat the website's `app/changelog-data.ts`, not memory/logs, as source of truth for what's published. apps/** dep PRs still have no build/type-check CI gate (Vercel post-merge is the only catch), though upstream added eslint+shellcheck lint gates 08-25 (#962) — unconfirmed whether that extends to apps/**. Remaining: ideas #2/3/5 (README, SHOWCASE.md) re-eligible. Stars/forks: see repo-pulse line below. Headline ship 08-17→08-25 window: security/infra hardening push — secretcurl argv-leak fix (#935, external contributor Svector-anu, 8 merged PRs), all GitHub Actions SHA-pinned (#917, closes the prior "Remaining" item), Codex install-script blocking (#918), narrowed ALL_SECRETS allowlist (#904), channel-secret Phase-2 (#951/#955 notify dispatcher split, #947 egress-audit/iron-proxy); plus 4 new run harnesses (fx/Vercel, Cursor, Hermes, GLM) and Claude Code plugin packaging (#884/#885, `/plugin install aeon@aeon`, promoted in-window's top post at 64 likes) — the plugin path is a direct fork-onboarding win (STRATEGY #3). Prior headline #866 (`bin/add-skill` discovery fix) still stands as the last priority-zero onboarding fix.
- **repo-pulse 2026-08-24:** aeon 679 stars (+13, 17 raw new-star events but window truncated at GitHub's ~300-event cap, avg4w=40, STEADY)/240 forks (+2); soul.md 648 stars (+4/7d, STEADY)/68 forks (+1 new fork, count unchanged — likely deleted); opendia 1913 stars (+2/7d, STEADY)/159 forks (unchanged); minitor 16 stars/5 forks (QUIET, +1 fork with no matching event). No SURGE/ACTIVE this round — aeon down from last week's SURGE as raw star velocity cooled. Still freshest as of 08-30 (weekly Monday skill, next due 08-31).
- **aeon-agent fork sync (`aeon-update`):** PR #209 (window `8b8d719..3b4c5a3`, 34 commits) **merged 2026-09-01 14:59 UTC** — baseline now `3b4c5a3`; held-back skills `rightstack`/`skill-article` landed via in-run eyebrow scan; new skill `cortx-reliability`. 8 conflicts carried in `memory/topics/aeon-update-state.json` `pending_conflicts`: 2 NEW (`scripts/llm-gateway.sh`, `.github/workflows/messages.yml` — operator's emergency GLM pin `b054cb0` vs upstream's tiered GLM_MODEL_* superset; PR body recommends adopting upstream) plus carried `CHANGELOG.md`, `.github/workflows/{aeon,ci-tests}.yml`, `llms.txt`, `.github/README.md`, `docs/skill-packs.md`. Lifetime success rate 43% (3/7) — outage-attributed; keeps the status page 🔴 until clean weekly runs accumulate.
- **Working tree anomaly:** `AGENTS.md` shows as deleted (uncommitted) and `notify`/`notify-jsonrender` are untracked, persisting since at least 2026-08-18. Re-verified 2026-09-01 on a fresh checkout that already contained the #209 merge (HEAD e637376) — STILL present, so the merge didn't clear it (aeon-update's same-day "regenerated byte-identical" note fixed only its own run tree). ` D` status means AGENTS.md exists in HEAD's tree and is deleted from disk each run — re-introduced runner-side, not a committed deletion. Out of heartbeat's checked scope to fix; risk of a later `git add -A`-style step landing the deletion on main stands. Needs a human/skill decision: restore, delete-and-commit, or gitignore.
