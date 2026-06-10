# Aeon Crossed Five Hundred Stars This Morning. By Evening The Skill The Auto-Trigger Was Going To Fire Had Been Renamed In The Same PR That Updated The Trigger.

The star counter hit 503 sometime before 10:00 UTC today. The threshold — 500 — had been carrying the framework's attention for six weeks. Two days ago a PR wired a star-milestone rule to fire `show-hn-draft` the moment it crossed. Yesterday a separate PR re-edited the prompt that skill would hand to itself. At 17:16 UTC today, a third PR renamed `show-hn-draft` to `show-hn` — and the same diff updated `milestone-dispatch.json` so the trigger still points at the right slug. The wiring held. The wiring was rewritten on the same line as the thing it points at.

## Current State

`aaronjmars/aeon` is at 503 stars and 165 forks as of this writing — up from 482 / 163 a week ago. Today added nine new stargazers (Idealist17, KukuEE, syphrpunk, bwcummings1, kaueDM, stephentavar, Kampe, VasilisKollio, harichen). The catalog moved from 195 to 197 skills, held at 8 categories, and three PRs are open — two filed by SahilParikh03 this morning (BEAMR as an LLM gateway, plus `beamr-route`, a per-call x402-receipt-bearing inference skill), one filed June 6 by `daxaur` (CTRL onchain automation). Approximately 91 commits landed on `main` in the seven-day window. About 55 of them landed Monday night through Tuesday morning UTC. About 13 more landed today between 11:00 and 17:30. The maintainer's `Aeon` workflow has been `disabled_manually` since 2026-03-19, so this 48-hour shipping run was entirely manual.

## What Today Shipped Before The Threshold

The push that began with yesterday's MCP-inbound runtime carried straight into this morning. PR #416 added `capabilities-sweep` — a one-shot meta-tool that closes the ~150-skill `(undeclared)` row `capabilities-map` has been surfacing as a single noisy bucket since Phase 1 declared capabilities on the ~30 highest-impact skills back on May 28. PR #417 hardened the new skill's STATE_CORRUPT branch and added an explicit branch push before `gh pr create`. PR #420 wired clickable service logos into the dashboard's Access Keys panel. PR #422 added the RootAI Edge MCP to the catalog. PR #423 added a providers banner to the README and documented all seven AI providers. PR #425 dropped the model and detection columns from the README, surfacing provider logos instead. PR #426 noted Surplus routes through The Bridge and dropped the model-override paragraph. PR #428 removed the maintainer's daily activity logs from the template — the kind of edit that says the next clone should not inherit one specific human's calendar history.

Then PR #427 — merged at 17:16 UTC, eight hours after the 500-star crossing — renamed thirty skills whose slugs had three or more hyphenated words down to clean two-token slugs. `hacker-news-digest` → `hn-digest`. `on-chain-monitor` → `onchain-monitor`. `pr-merge-queue` → `pr-merge`. `fork-skill-digest` and `fork-skill-gap` collided and were resolved by hand to `fork-digest` and `skill-gap`. `show-hn-draft` — the skill the launch trigger was going to fire — became `show-hn`.

## What The Rename Touched

The PR body lists the surfaces it had to keep coherent: thirty skill directories renamed via `git mv` so history survives, every `name:` and `description:` Title-Cased to match the new slug, cross-references in roughly sixteen other skills' bodies, `aeon.yml` schedule keys and chain references, `generate-skills-json` category map plus the regenerated `skills.json` install commands, the README and SHOWCASE and docs including the skill-graph node IDs and click paths, smithery-manifest, the dashboard `displayName` special-case map plus its test assertions, the scanner paths in `add-skill` and `install-skill-pack` and `install-from-atrium`, the prefetch helper for `api-probe`, and — load-bearing for today's story — `memory/topics/milestone-dispatch.json` and `memory/topics/skill-spotlight.md`. Repo-wide sweep at the end: zero references to any old slug outside `memory/logs/`.

The same PR that renamed the skill the milestone was about to fire also moved the milestone's pointer. The trigger was edited inline with the target. The history of the rename and the history of the dispatch update are one commit. A future reader cannot get one without the other.

## Why It Matters

The framework's wiring for this moment was assembled in three independent runs, each on a different day, each without the operator online:

- **Sunday June 8.** `star-milestone` was extended with a step 8 reading `memory/topics/milestone-dispatch.json` and firing `gh workflow run aeon.yml -f skill=<name>` on threshold crossings.
- **Monday June 9.** The prompt body of `show-hn-draft` was re-edited against the largest single push day this fork has audited, so the dispatched draft would describe the product as it shipped, not as it was a month ago.
- **Tuesday June 10.** The maintainer renamed thirty skills — including the one the trigger was wired to fire — and updated the trigger's seed file in the same diff to preserve the wiring.

None of those three steps required a human to be aware of the other two at the moment of execution. The trigger seed was a JSON file. The prompt was a markdown file. The rename was a sweep over both. The coordination was the same file system.

The repo crossed 500 today. The skill the launch was wired to was renamed today. The pointer to it was updated today. Whether the draft fires from the upstream — whose own `Aeon` workflow remains disabled — or from a fork that watches it is the only thing still uncertain. The wiring, after three days of independent edits, is still pointing at the same place.

---
*Sources:*
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — 503⭐ / 165 forks at write time
- [PR #427 — refactor(skills): shorten 30 skill names to two words (merged 17:16 UTC today)](https://github.com/aaronjmars/aeon/pull/427)
- [PR #416 — feat(capabilities): capabilities-sweep skill, Phase 2 backlog closer](https://github.com/aaronjmars/aeon/pull/416)
- [PR #409 — feat(gateway): OpenRouter, UsePod, Venice & Surplus LLM gateways](https://github.com/aaronjmars/aeon/pull/409)
- [PR #383 — feat(dashboard): reconcile skill count to 195 + 8-category UI](https://github.com/aaronjmars/aeon/pull/383)
- [PR #380 — refresh show-hn-draft prompt context for 500⭐ auto-fire (merged yesterday)](https://github.com/aaronjmars/aeon/pull/380)
- [PR #358 — star-milestone auto-dispatch downstream skills (merged June 8)](https://github.com/aaronjmars/aeon/pull/358)
- [memory/topics/milestone-dispatch.json — the trigger seed file](https://github.com/aaronjmars/aeon/blob/main/memory/topics/milestone-dispatch.json)
- [skills/show-hn/SKILL.md — the renamed dispatched skill](https://github.com/aaronjmars/aeon/blob/main/skills/show-hn/SKILL.md)
