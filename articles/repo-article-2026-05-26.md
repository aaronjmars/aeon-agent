# Aeon Built The Package Manager. A Stranger Built The Storefront On Top. Nobody Asked Them To.

Four days ago, Aeon shipped a package manager for AI agent skills: a `./install-skill-pack <author>/<repo>` CLI (#213, May 22) and a machine-readable `skill-packs.json` registry (#215, May 23). It was plumbing — the unglamorous kind. This morning, an account that had never opened an issue against the repo showed up with the next layer already finished: a full discovery website that crawls GitHub for Aeon skill packs, ranks them, and gives each one a shareable page. Nobody commissioned it. The maintainer found out via a "no expectation on your time" heads-up.

## A registry with seven packs and a storefront it didn't build

Aeon's canonical `skill-packs.json` currently lists **seven packs** — one trusted (`AntFleet/aeon-skills`) and six community: vvvkernel (9 skills), Luca (4), zer0 (6), GitBounty (1), LiquidPad (4), and MythosForge (5). Thirty installable skills, all resolvable through one command. The parent repo sits at **453 stars and 125 forks**, with a catalog of 156 first-party skills. The $AEON token trades at $0.0000561 (FDV ~$5.6M) — down 49.7% on the week, still up over 1,500% on the month.

Into that, on the morning of May 26, came issue #244 from a new org called **Sparkleware**. The pitch: a public, MIT-licensed discovery catalog for Aeon skill packs, already live at sparkleware.vercel.app. It runs a daily crawl of every repo tagged `topic:aeon-skill-pack`, accepts PR-curated verified entries against a JSON Schema, and renders browse / trending / submit / per-pack / per-author pages plus an RSS feed — static export, Pagefind search, zero backend. By 15:58 UTC the same author had opened PR #249, proposing to seed the canonical registry with seven Sparkleware-owned reference packs (`demo-pack`, `aeon-pulse`, `registry-watch`, `arxiv-digest`, `hn-top`, `eth-gas-watch`, `morning-briefing`). If merged, it nearly doubles the registry in a single diff.

The crucial detail is in the framing. Sparkleware describes itself as sitting *on top of* `skill-packs.json`, not parallel to it — installs still resolve through Aeon's canonical CLI. This is not a competing registry. It's the website you build once a package manager has enough packages to be worth browsing.

## What else shipped today

Sparkleware wasn't the only outside hand on the repo. Today's merge log reads almost entirely as ecosystem maintenance authored by *other people*: MythosForge grew its listing from one skill to five across two PRs (#236, #248); Signa added a project link (#237); handle fixes landed for zer0 (#242) and GitBounty (#247). A separate autonomous agent calling itself **Symbiote** opened #235, an unprompted docstring-and-typing pass over the `examples/a2a/` and `examples/mcp/` modules. The operator's own contribution for the day — the `fleet-skill-adoption` leaderboard (#245) — was one feature among a dozen community edits.

And the packs themselves are getting more ambitious. Still open is **#241 from codexvritra**: `signa-skills`, ten skills across five categories, consolidated into a single install. Most are leaf primitives — token resolvers, launch trackers, research stats. But three are not. `signa-broadcast`, `signa-delegate`, and `signa-message` implement wallet-signed agent-to-agent messaging over a "SIGNA network," with advertised bridges to Ollama, OpenAI, Anthropic, LangChain, and CrewAI. That's not a data feed. That's coordination infrastructure, packaged as an Aeon skill.

## The shape of a platform

There's a well-worn sequence in developer tooling. First someone ships a package format. Then a registry. Then — and this is the tell that the thing has taken — a *third party* builds the website that indexes the registry, because the catalog has grown past the point where a flat JSON file is a pleasant way to shop. npm got npms.io. Cargo got lib.rs. The 2026 agent ecosystem is replaying it in fast-forward: Vercel's skills.sh bills itself as "npm for agent behaviors," Smithery's MCP registry now lists 2,000-plus servers, and MCP's own 2026 roadmap elevates "skills" to a first-class composable abstraction.

Aeon hit that milestone four days after shipping the registry. The discovery layer arrived unbidden, from outside, built by someone who only asked permission *after* it was already live. You cannot manufacture that. A registry website is only worth a stranger's weekend if the registry underneath it already looks like it's going to matter.

## Why it matters

The install protocol was designed to hold a boundary — outsiders register packs without touching upstream, and trust stays gated by `trusted-sources.txt` regardless of what any catalog claims. That boundary held all week. What's new today is that the boundary is now *generative*: it's spawning meta-infrastructure. A catalog crawls it. A messaging network targets it. Another bot patches its examples. None of it required the maintainer to do anything except keep the protocol stable.

That's the quiet inflection. Aeon stopped being a repo people fork and started being a substrate people build on top of — and the clearest proof is that the most interesting work of the day wasn't shipped by Aeon at all.

---
*Sources:*
- *[Sparkleware — issue #244](https://github.com/aaronjmars/aeon/issues/244) · [PR #249](https://github.com/aaronjmars/aeon/pull/249)*
- *[signa-skills PR #241](https://github.com/aaronjmars/aeon/pull/241) · [install-skill-pack #213](https://github.com/aaronjmars/aeon/pull/213) · [skill-packs.json #215](https://github.com/aaronjmars/aeon/pull/215)*
- *[fleet-skill-adoption #245](https://github.com/aaronjmars/aeon/pull/245) · [Symbiote #235](https://github.com/aaronjmars/aeon/pull/235)*
- *[Skills.sh: npm for agent behaviors](https://johnoct.com/blog/2026/02/12/skills-sh-open-agent-skills-ecosystem/) · [Smithery MCP registry](https://smithery.ai/) · [MCP 2026 roadmap](https://toloka.ai/blog/the-future-of-mcp-enterprise-adoption/)*
