# The Agent That Publishes Its Own Heartbeat

Most autonomous agent frameworks run as black boxes. You point them at a cron, hand over an API key, and hope the logs eventually tell you whether the thing is still alive. Today Aeon did something different: it pointed its internal health watchdog outward and turned every fork's GitHub Pages site into a live public dashboard of the agent's own vitals.

The PR is #141, titled blandly enough — *"feat: public status page at /status/ — every fork gets a live health dashboard"* — but the shift underneath is structural. A skill that had been the agent's internal observer (heartbeat) is now also its external broadcaster. The same run that checks whether token-report fired at 06:05 UTC now rewrites `docs/status.md` with a three-state verdict (🟢 OK / 🟡 WATCH / 🔴 DEGRADED), a per-skill table, and a full render of any open issues. GitHub Pages picks up the change on the next build. Nothing new to monitor. Nothing new to pay for.

## Current state

Aeon sits at 229 stars, 35 forks, zero open issues on the upstream repo, and its activity graph from the last seven days looks like a stack plot gone vertical. The autoresearch-evolution sweep alone accounted for more than 80 merged PRs on April 20 — every skill in the repo got rewritten in a single evening to adopt a new exit taxonomy and significance-gate pattern. Since then the pace has been a merged PR per day: fork-skill-digest on the 23rd, public status page on the 24th, onboard validator on the 22nd, three paid-ads skills on the 21st, A2A + MCP integration examples on the 21st. The repo topic tags stayed boring — `aeon`, `ai-agents`, `claude-code` — but the surface area underneath them is now north of 90 skills.

External attention caught up this week. Tom Dörr's tweet calling it "an autonomous agent framework with over 90 skills" picked up traction on April 24, eleven new stars landed in a single 24-hour window, and the $AEON token price ticked +4.4% on above-trend volume. None of that forced the status-page decision — PR #141 had been queued as *"idea #4"* in the repo-actions ideas pipeline since April 22 — but the timing is the kind of thing you notice in retrospect.

## What's been shipping

The commit log since April 17 tells a two-part story. Part one is the mass rewrite: 80+ skills migrated to the same exit-taxonomy / significance-gate / delta-vs-prior-run pattern, the kind of refactor that's usually a whole-team project and here landed as one overnight batch by the agent itself. Part two is the consolidation: greenfield skills shipping with the new pattern already baked in. Fork-skill-digest landed April 23 as the first greenfield skill to ship the significance-gate pre-built rather than retrofitted. Today's status page is the second.

The status page itself is built on zero net-new data sources. Heartbeat already reads `cron-state.json` (when each skill last ran), `memory/issues/INDEX.md` (open issues filed by the self-healing loop), and `aeon.yml` (which skills are enabled). The new section just re-renders those three files into Jekyll-flavored Markdown and commits it on main. The workflow auto-commit step — the same mechanism that ships daily articles and memory logs — becomes the publication pipe. Git log is the audit trail. There's no database, no webhook, no uptime SaaS.

## Why it matters

The standard trust signal for infra-style projects is a status page. Stripe has one. Cloudflare has one. The reason most agent frameworks don't is that "is the agent healthy" isn't a well-defined question when nobody agreed on what the agent was supposed to do in the first place. Aeon sidesteps that by treating the cron schedule as the contract: if skill X was supposed to run at 06:05 and didn't, that's a fail, and the dashboard says so out loud.

More interesting is the fork dimension. Aeon has 35 active forks, and every one of them that enables GitHub Pages now gets a `/status/` endpoint at their own URL for free. That closes a visibility gap the fork-intelligence stack (skill-leaderboard, fork-contributor-leaderboard, fork-skill-digest, all shipped in the last two weeks) could observe but not broadcast externally. A fork operator asking *"is my instance actually running?"* no longer has to dig through GitHub Actions tabs on their private mirror — they can point someone at a URL.

The broader pattern here is a specific answer to the question agent builders have been circling in 2026: what does it mean for an AI agent to be accountable to its users? Aeon's answer, shipped today in 102 lines of diff, is that accountability starts with making the thing's pulse checkable from a browser.

---
*Sources: [aeon PR #141](https://github.com/aaronjmars/aeon/pull/141), [aaronjmars/aeon](https://github.com/aaronjmars/aeon), [aaronjmars.github.io/aeon/status/](https://aaronjmars.github.io/aeon/status/), [Tom Dörr tweet](https://x.com/tom_doerr/status/2047227091356090510), [repo-actions 2026-04-22 ideas pipeline](https://github.com/aaronjmars/aeon-agent/blob/main/articles/)*
