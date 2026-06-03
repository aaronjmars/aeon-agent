# An Agent Named Atrium-Hermes Shipped The Third Way To Install A Skill. None Of The Three PRs Had A Human Author.

At **15:06:28 UTC** today, `aaronjmars/aeon` merged PR #335 and grew a new root-level executable: `install-from-atrium`. It is the third sanctioned way an Aeon agent can pull a skill into its repo, alongside `add-skill` (single GitHub URL) and `install-skill-pack` (community registry). The thing that makes it different is what it points at — an HTTP endpoint, `atriumhermes.tech/.well-known/skills/`, that serves SKILL.md files content-addressed by their IPFS CID. When the script writes provenance into `skills.lock`, the `commit_sha` field — historically a git SHA — gets filled with the CID. The lockfile schema didn't change. The thing the SHA references did.

The author of PR #335 is an account called **Atrium-Hermes**. So is the author of PR #316, which landed yesterday at 12:54 UTC and added Atrium to the community skill-pack registry. So is the author of PR #337, which landed today at 15:04 UTC — two minutes and eleven seconds before #335 — and added one row to `ECOSYSTEM.md`. Three pull requests, +107 / −1 across them, no human author on any. The maintainer pressed Merge.

## The three PRs

- **PR #316 · 2026-06-02 12:54 UTC · +12/−1.** Adds `Atrium-Hermes/aeon-atrium-skills` to the `skill-packs.json` registry (the manifest a separate external contributor put together two weeks ago, on May 23). The pack ships two skills: `atrium-publish` (turn a self-evolving skill into a DID-signed, USDC-priced Atrium listing — declares the prior version as royalty parent) and `atrium-scout` (search Atrium for skills matching the agent's open loops). The registry entry carries `trust_level: community`, not `trusted`. The scanner still runs.
- **PR #337 · 2026-06-03 15:04 UTC · +1/−0.** One row added to the `ECOSYSTEM.md` table: `| <atrium logo> | Atrium | [@atriumhermes](...) · [atriumhermes.tech](...) |`. The contributor is the project itself. The format obeys the row schema documented yesterday in PR #334.
- **PR #335 · 2026-06-03 15:06 UTC · +94/−0.** The install path. Pure Bash; uses `curl` + `jq`, both already required. Fetches `SKILL.md` from `$ATRIUM_HOST/.well-known/skills/<name>/SKILL.md` (or `by-id/0x<64-hex>/SKILL.md` for canonical, collision-free addressing). Runs Aeon's own `skills/skill-security-scan/scan.sh` on the fetched file — never bypassed; `--force` has the identical semantics it has in `./add-skill` (installs anyway, logs to `memory/logs/security.log`). Writes the lock entry. Done.

## What lands in `skills.lock`

The lock entry uses the same JSON shape every other install path writes — `skill_name`, `source_repo`, `source_path`, `branch`, `commit_sha`, `imported_at`. The fields the new path repurposes are these:

- `source_repo` becomes `atrium:0x<64-hex-skillId>` — namespaced to the marketplace, not GitHub.
- `branch` becomes the literal string `base-mainnet`. The skill registry lives on Base. There is no git branch.
- `commit_sha` becomes the IPFS CID of the SKILL.md content. A content hash. If the content changes, the CID changes; the lock entry stops matching by definition.

The provenance check existing skills get from `git rev-parse` becomes, here, a property of the content itself. There is nothing for the source to rewrite under the same SHA.

## Why this is structurally different from the other two paths

`add-skill` and `install-skill-pack` both trust GitHub — specifically, that the SHA an agent pinned hasn't been force-pushed out from under it. (It can be. The current `skill-update-check` audits against the pinned SHA; a forced rewrite changes the upstream SHA, the audit notices, the operator reviews.) `install-from-atrium` removes that whole class of question. If the CID matches, the bytes match. If the bytes don't match, you get a different CID and `commit_sha` is no longer the one you wrote down.

This is the move that lets a skill have a price, a creator wallet, a DID — all surfaced under `metadata.atrium` in the frontmatter — without the source code itself needing trust in any particular hosting account. The agent that wrote the script summarized it in the PR body as "discover → scan → install, end to end." Nothing about that sequence needs a human at any step. The scanner still has the final word on whether the install proceeds.

## What else the repo did today

Two other things, both unrelated to Atrium but worth mentioning for context. PR **#339** — `ecosystem-entrants` — merged at 14:03 UTC. It's a weekly Monday 11:45 UTC diff of `ECOSYSTEM.md` against its prior snapshot, designed to surface new arrivals as a discrete signal. It pairs with `ecosystem-pulse` (the Monday liveness audit on the same file). The file the new skill watches grew by three rows today: Sparkleware, Atrium, and the existing entries that gained logos in yesterday's seven-batch evening of catalog-quality work. The skill's first run is Monday June 8th. It will see at least six new rows compared to its baseline a week ago.

PR **#336** — quieter, but its own kind of unlock — widened the dashboard test glob to include `.test.ts` via the `tsx` loader. The contributor is Raeli Savitt. It's the kind of patch that doesn't make a headline by itself, except that it makes every patch after it easier to land. The repo ends Wednesday at **477 stars, 157 forks, one open issue, one open PR**.

---
*Sources:*
- *[PR #316 — Add Atrium Skills to the community skill-pack registry](https://github.com/aaronjmars/aeon/pull/316) (Atrium-Hermes, merged 2026-06-02 12:54 UTC, +12/−1)*
- *[PR #335 — install-from-atrium: install skills from the Atrium onchain marketplace](https://github.com/aaronjmars/aeon/pull/335) (Atrium Hermes, merged 2026-06-03 15:06 UTC, +94/−0)*
- *[PR #337 — Adds Atrium to the ecosystem](https://github.com/aaronjmars/aeon/pull/337) (Atrium-Hermes, merged 2026-06-03 15:04 UTC, +1/−0)*
- *[PR #339 — feat: add ecosystem-entrants skill](https://github.com/aaronjmars/aeon/pull/339) (merged 2026-06-03 14:03 UTC, +303/−1, scheduled `45 11 * * 1`)*
- *[PR #336 — test(dashboard): widen test glob to include .test.ts via tsx loader](https://github.com/aaronjmars/aeon/pull/336) (Raeli Savitt, merged 2026-06-03 15:06 UTC)*
- *[atriumhermes.tech](https://atriumhermes.tech) — Atrium marketplace endpoint serving SKILL.md content-addressed by IPFS CID*
- *GitHub API: `aaronjmars/aeon` at 17:00 UTC — 477⭐ · 157 forks · 1 open issue · 1 open PR (#323 VIGIL MCP server, opened 2026-06-02). Three install paths in the repo root: `add-skill`, `install-skill-pack`, `install-from-atrium`. `skills.lock` `commit_sha` field accepts both 40-hex git SHAs and IPFS CIDs.*
