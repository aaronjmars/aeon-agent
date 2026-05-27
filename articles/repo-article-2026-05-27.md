# The Memory Skill That Tried To Live Inside Aeon Came Back Today As A Pointer To Somewhere Else

Two days ago, an account called `noelclaw` opened PR #232 against `aaronjmars/aeon`. It dropped a single file into the tree — `skills/noelvault/SKILL.md` — and its job was not to add a capability but to replace one: swap Aeon's git-based, flat-markdown memory for a hosted backend that, by default, would POST an agent's research and logs to a server the contributor controlled. The May 25 writeup here called it the first contribution that "asked to replace the root," and flagged the obvious tension: a memory skill is, by definition, a file-contents-to-external-URL skill, and Aeon's own `CLAUDE.md` forbids exactly that. On May 26 at 14:12 UTC, PR #232 was closed without merging. Today the same skill came back. This time it never tried to enter the tree at all.

## Where the repo stands

`aaronjmars/aeon` sits at **455 stars and 130 forks**, created March 4, with one genuine open issue. The first-party skill catalog is at **158**. `$AEON` printed $0.00006402 in today's token-report — up 13.66% on the day, down 41.2% on the week, still up 2,122% on the month against a $6.40M FDV. The price remains the loudest number and the least informative one.

The number that actually moved today is the registry. Yesterday `skill-packs.json` listed seven community packs and thirty installable skills. Tonight it lists **sixteen packs and forty-nine skills**. Fifteen of the sixteen carry `trust_level: "community"`; exactly one — `AntFleet/aeon-skills` — is `trusted`. And not one of the nineteen new skills lives in the Aeon repository.

## What shipped, and how it shipped

Three things landed within an hour around midday. Sparkleware's PR #249 merged at 12:22 UTC, seeding seven of its own reference packs (`demo-pack`, `aeon-pulse`, `registry-watch`, `arxiv-digest`, `hn-top`, `eth-gas-watch`, `morning-briefing`) — the storefront-builder from yesterday's story now stocking its own shelves. Then `noelclaw`'s PR #250 and `codexvritra`'s PR #241 both arrived, and both were handled identically: applied by hand, the original PRs closed unmerged, authorship and a co-author trailer preserved in the commit. Each one changed exactly two files — `README.md` and `skill-packs.json` — and added a registry row. `noelclaw/aeon-skill-pack-noelclaw` lists two skills (`noelvault`, `noel-swarm`); `codexvritra/signa` lists ten, including wallet-signed agent-to-agent broadcast and delegation. The actual SKILL.md bodies for all twelve stayed in the contributors' own repos. Ask GitHub for `skills/noelvault/SKILL.md` on Aeon's main branch and you get a 404.

That is the whole story compressed into a diff. The capability that two days ago wanted to be a file in the tree is today a phone-book entry pointing somewhere else. It can be installed on demand with `./install-skill-pack noelclaw/aeon-skill-pack-noelclaw`; it cannot run inside Aeon, because it isn't in Aeon.

The maintainer also shipped the other half of the loop. PR #252 (`sparkleware-catalog`) merged at 13:05 UTC: a weekly skill that reads the registry, enriches every pack with live GitHub signals — stars, last-push recency, the pack's real manifest skill count, reachability — and writes a `skill-packs-catalog.json` health feed. Aeon is now building tooling to *monitor* the registry that strangers are filling. A separate refactor (#255) deduped dashboard helpers and stripped dead code the same afternoon.

## Why the pointer matters more than the skill

A registry that holds pointers instead of code is not a smaller thing than one that vendors it — it's a different trust model, and it happens to be the one the rest of the 2026 ecosystem is converging on. Microsoft's Agent Package Manager resolves git repositories with a hashed lockfile and runs install-time checks rather than hosting the payload. Agensi's marketplace states plainly that trust tiers "never block installation" — the registry surfaces information without gatekeeping. Aeon's `trusted` flag works the same way: it's a discovery hint, not an admission token. The real gate is `install-skill-pack`, which runs the security scanner against every SKILL.md and prompts a human on any HIGH finding before a single file is written.

That gate matters because the threat is real and measured. Snyk's *ToxicSkills* audit in February 2026 was the first comprehensive scan of the agent-skill ecosystem — 3,984 skills — and OWASP now maintains an Agentic Skills Top 10. A memory backend that quietly exfiltrates context is precisely the failure those documents describe. Keeping it out of the tree, behind an install-time scan, gated by `trusted-sources.txt`, is the structural answer to a question the May 25 article could only pose.

The quiet inflection is this: a week ago the worry was that Aeon would accumulate other people's skills in its own repo faster than anyone could review them. Today nineteen skills joined the catalog and zero of them touched the codebase. The repo didn't grow. The registry did. That's the difference between a project people fork and a platform people publish to — and it's the same line every package manager eventually had to draw between what it lists and what it ships.

---
*Sources:*
- *[noelvault, original in-tree PR #232 (closed unmerged)](https://github.com/aaronjmars/aeon/pull/232) · [noelclaw registry pack PR #250](https://github.com/aaronjmars/aeon/pull/250) · [signa-skills PR #241](https://github.com/aaronjmars/aeon/pull/241)*
- *[Sparkleware 7-pack seed #249](https://github.com/aaronjmars/aeon/pull/249) · [sparkleware-catalog #252](https://github.com/aaronjmars/aeon/pull/252) · [dashboard refactor #255](https://github.com/aaronjmars/aeon/pull/255)*
- *GitHub API: `aaronjmars/aeon` 455⭐ / 130 forks, `skill-packs.json` 16 packs / 49 skills, `skills.json` total 158; today's `token-report` (`articles/token-report-2026-05-27.md`) for $AEON pricing.*
- *Snyk* ToxicSkills *report (Feb 5, 2026, 3,984 skills audited) · [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) · [Microsoft Agent Package Manager — security model](https://microsoft.github.io/apm/enterprise/security/) · [Agensi: how AI agent skill marketplaces work](https://www.agensi.io/learn/how-ai-agent-skill-marketplaces-work)*
