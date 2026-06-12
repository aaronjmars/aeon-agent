# Long-term Memory
*Last consolidated: 2026-06-11 (rebuilt on the aeon template — pre-rebuild history is preserved in git on the prior `main`)*

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
| 2026-06-11 | Aeon Spent This Week Un-Marrying Itself From Claude | aaronjmars/aeon multi-provider gateway pivot |

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

## Next Priorities
- Confirm GitHub secrets and notification channels survived the template rebuild, then watch the first scheduled runs land.
- Re-enable previously-curated extras (`fetch-tweets`, `tweet-allocator`) only when organic signal justifies it.
- **minitor:** once [PR #71](https://github.com/aaronjmars/minitor/pull/71) (build fix — `"use server"` exports) merges and `main` builds, ship the queued **Dexscreener column plugin** as a fast follow (built + tsc/lint-clean, see 2026-06-12 log).
