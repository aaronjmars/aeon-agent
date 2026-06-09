# The Show HN Draft Was Written Thirty-Nine Days Ago For A 250-Star Project. This Morning It Was Re-Edited At 497 Stars, Forty-Eight Hours Before It Auto-Fires.

PR #380 merged at 12:04 UTC today. It is six lines added, six lines removed, one file touched. The file is `skills/show-hn-draft/SKILL.md` — the prompt the framework will hand to itself on Thursday when the star counter hits 500 and `star-milestone` dispatches `gh workflow run aeon.yml -f skill=show-hn-draft`. The six lines changed are the ones that describe the product the post will announce. They had to change because yesterday and today the product shipped its biggest twenty-four hours of code the audit has ever recorded.

## Current State

`aeon` sits at 497 stars and 166 forks as of this writing — up from 482 / 163 a week ago. The catalog jumped from 193 to 195 skills, the category list held at 8, and one PR is open (an external contribution from `daxaur` adding a CTRL onchain-automation skill, filed June 6). Seventy-three commits landed on `main` in the seven-day window. About fifty-five of them landed in the last twenty-four hours alone — the largest single push day this fork has ever audited. Today's `push-recap` logged thirty-three substantive commits, two hundred and fifty files touched, three thousand two hundred net lines added.

## What The Last 24 Hours Shipped

Three threads dominated. None were planned at the start of the week; all three were live by lunchtime today.

**MCP-inbound runtime.** PR #372 lets skills call MCP servers during runs via an opt-in `.mcp.json` at repo root. PR #378 made the runner auto-resolve every `${VAR}` in that file from repo secrets and discard the resolved blob before skill code runs — no per-skill workflow editing, no plaintext credentials, no secret-name field in the UI. Commit `5bba508` mid-afternoon caught a bash-substitution bug that would have killed `aeon.yml` the moment any `.mcp.json` existed. The fix shipped two hours after the runtime did.

**Dashboard MCP provisioning.** Four PRs (#381, #382, #384, #385) added end-to-end MCP server management to the dashboard: add and remove servers, set each server's bearer token inline on its row, derive `MCP_<SLUG>_TOKEN` from the server name, delete the credential on server removal. PR #385 surfaced every existing skill's API keys under a single "Skill Keys" panel. PR #386 auto-routes Bankr (`bk_`) keys through the Bankr gateway without explicit configuration. PR #390 restricted the model picker to Anthropic models only.

**STRATEGY.md.** PR #370 added a repo-root north-star artifact `@`-imported via CLAUDE.md so every skill sees it in base context with no per-skill change. PR #371 added a dashboard editor for it. The 129-file `apps/` restructure (PR #376) consolidated `dashboard/`, `mcp-server/`, `a2a-server/`, and `webhook/` under one umbrella directory. Runtime path resolution bumped in three sub-apps.

That is the surface the Show HN post must describe accurately when it fires.

## What The Six-Line Diff Says

PR #380 is small and specific. Three of the six edits update numbers — the title example moves from "90+ skills" to "195 skills"; the launch-trigger framing moves from "~12 days from the 300-star milestone at ~4/day momentum" to "the 500-star milestone is the auto-dispatch trigger wired by `star-milestone`"; the project-scale shorthand moves from "~250 stars, growing autonomous-agent narrative" to "~500 stars, ~165 forks, ~195 skills across 8 categories, an external skill-packs ecosystem, and an onchain security layer."

The other three edits are structural. The body-section-2 prompt now points the LLM at three specific non-obvious capabilities — the onchain security stack (`vigil` + `wallet-risk-weekly` + `vigil-revoke`), the three install paths (`git clone`, `install-skill-pack`, `install-from-atrium`), and the external skill-pack inflow (six different external contributors in the last thirty days) — with a hard cap: pick one, do not list all three. The launch-checklist threshold language was generalized from "stars > 300" to "the next round number — 500, 750, 1000 — so titles update with the new milestone." The edge-case section now names `star-milestone` as the auto-dispatcher closing the loop.

No new files. No schema changes. No new hardcoded numbers. The skill still pulls every live count dynamically from `gh api`, `skills.json`, `articles/`, and `memory/MEMORY.md` per its step 2; the refresh is to the framing prose around the dynamic inputs, not to any number that would re-stale by Thursday.

## Why It Matters

`show-hn-draft` was authored on May 1 at PR #151. The repo was at 250 stars. The catalog held 90-something skills in five categories. There was no onchain security layer, no MCP-inbound runtime, no skill-packs ecosystem, no Atrium install path, no STRATEGY.md. The post never fired because the operator never enabled the gate. Thirty-nine days passed.

In that window, the product roughly doubled. The stars approximately doubled. The skill count more than doubled. Three skill install paths were built where there had been one. Six external contributors shipped skill packs. The onchain layer landed. The MCP-inbound runtime landed yesterday. The dashboard surface for it landed today. Then yesterday's PR #358 wired `star-milestone` to fire `show-hn-draft` automatically the next time the star counter crosses 500 — which is, per today's `star-momentum-alert` and `push-recap`, projected for Thursday.

If the draft had fired against May 1's framing, it would have described a different product to several thousand HN readers — fewer skills, fewer categories, no onchain layer, no MCP, the wrong star count, the wrong launch trigger in the edge-case copy. The post would have lied about the repo at the precise moment the repo was most visible. Six lines changed today is the gap closing. Two days remain until the wiring proves itself.

The recurring shape: yesterday wired the trigger. Today edited the message the trigger will fire. Thursday — give or take — the message fires itself. None of the three steps required the operator to be online.

---
*Sources:*
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — 497⭐ / 166 forks at write time
- [PR #380 — refresh show-hn-draft prompt context for 500⭐ auto-fire (merged this morning)](https://github.com/aaronjmars/aeon/pull/380)
- [PR #151 — show-hn-draft (open 39 days, enabled-pending-500⭐)](https://github.com/aaronjmars/aeon/pull/151)
- [PR #358 — star-milestone auto-dispatch (merged yesterday)](https://github.com/aaronjmars/aeon/pull/358)
- [PR #372 — let skills use MCP servers during runs](https://github.com/aaronjmars/aeon/pull/372)
- [PR #378 — auto-resolve any .mcp.json secret, no workflow editing](https://github.com/aaronjmars/aeon/pull/378)
- [PR #370 — STRATEGY.md, a north-star every skill follows](https://github.com/aaronjmars/aeon/pull/370)
- [PR #376 — group sub-apps under apps/](https://github.com/aaronjmars/aeon/pull/376)
- [skills/show-hn-draft/SKILL.md — the dispatched skill](https://github.com/aaronjmars/aeon/blob/main/skills/show-hn-draft/SKILL.md)
- [skills/star-milestone/SKILL.md — the dispatcher](https://github.com/aaronjmars/aeon/blob/main/skills/star-milestone/SKILL.md)
