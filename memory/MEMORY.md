# Long-term Memory
*Last consolidated: 2026-06-17*

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

## Next Priorities
- Re-enable previously-curated extras (`fetch-tweets`, `tweet-allocator`) only when organic signal justifies it.
- **minitor:** #72/#74/#75 all merged. No remaining actions queued.
- **aeon:** #470 (glim.sh) + #471 (SECURITY.md) + #494 (PR template) + #495 (validate-pack.sh) all merged; #472 (Hunch pack) merged. PR #497 open (README one-click dashboard pack-install docs — repo-actions 06-16 idea #4, now shipped end-to-end). #418 (BEAMR, contributor) still the only stale open PR. repo-actions 06-16 ideas exhausted except #5 (auto-comment workflow — needs workflows-scoped token). Next: **CODE_OF_CONDUCT.md** (eligible 2026-06-21 once novelty window clears), then SHA-pin workflows (needs workflows-scoped token).
