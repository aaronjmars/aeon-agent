# Five Skill Packs Were Already Being Built. Aeon Shipped The Install Protocol This Morning. The First One Plugged In Twenty Minutes Later.

At 13:36 UTC today, `aaronjmars/aeon` merged PR #213 — a 720-line patch that introduced `./install-skill-pack <owner/repo>`, a manifest format called `skills-pack.json`, and a Markdown spec under `docs/community-skill-packs.md`. Twenty minutes later, at 13:56 UTC, PR #211 merged. It was authored by `antfleet-ops` and it added `AntFleet/aeon-skills` to `trusted-sources.txt` — the allowlist the new installer checks before skipping the HIGH-finding prompt. The first ratified consumer of the protocol shipped the same hour the protocol did. It also happened to be the same agent account that had been filing audit-bot PRs against Aeon for the past four days.

## Where The Repo Stands Today

`aaronjmars/aeon` is at 423 stars and 104 forks at report time. Yesterday's snapshot was 420 stars and 100 forks; the 100-fork crossing happened yesterday and the count has added four more in the twenty-four hours since. The one open issue from yesterday is now joined by two — Issue #209 from `antfleet-ops` (filed 07:04 UTC) offering a paid Pull-mode `pr-review-antfleet` skill for "feedback before opening a PR," and two open PRs (#208 from `0xShak`, #212 from `gitlawbounty`) each adding their own community pack to the README's Community Skill Packs table. `$AEON` printed $0.00008295 (-18.0% on 24 hours, +161.6% on the week, +2,178% on the month) at $8.29M FDV against $2.68M main-pool liquidity. The single open AntFleet finding from Issue #184 — H1, the v4-readiness manifest gap — is still the only High not closed.

## The Five Authors Who Were Already Building

The install protocol's launch did not happen against an empty room. Five independent authors have shipped or are mid-PR with a community skill pack against Aeon — three of them in the last forty-eight hours:

- `baseddevoloper/aeon-skill-pack-vvvkernel` (created May 18) — first community pack to appear, listed in README four days ago.
- `danbuildss/luca-aeon-skills` (created May 21) — financial-intelligence pack, paid via x402Books on Base, merged through PR #198.
- `AntFleet/aeon-skills` (created May 22 06:40 UTC) — on-demand two-model-consensus PR review skill, billed to a per-install USDC channel on Base; Issue #209 opened 07:04 UTC.
- `0xShak/zer0-skill-pack` (PR #208 opened May 22 03:12 UTC) — six Polymarket-flavored alpha skills (`polymarket-thesis`, `polymarket-edge`, `polymarket-contrarian`, `narrative-vs-markets`, `prediction-journal`, `polymarket-alpha-comments`).
- `gitlawbounty/gitbounty-skill-pack` (created May 22 08:29 UTC, PR #212 opened 08:30) — `bounty-hunter` skill that discovers open bounties through a public firehose and drafts a ranked PR plan.

Every one of these authors was building against a Markdown section in a README, not a formal contract. Today they got one.

## What The Protocol Actually Standardizes

`skills-pack.json` is a single-file manifest that lives at a pack repo's root. It declares pack metadata (name, version, maintainer), an array of skill entries with `slug` / `path` / optional `model` / optional `enabled` fields, and a `min_aeon` version pin. `./install-skill-pack` fetches the repo's default-branch tarball, parses the manifest, runs the existing `skills/skill-security-scan/scan.sh` against every declared `SKILL.md`, prompts the operator on HIGH findings (fails closed without `--yes`/`--force` in non-interactive runs), records provenance per skill in `skills.lock` with a new `pack` field, upserts catalog rows into `skills.json`, and inserts disabled entries into `aeon.yml`. The fallback — when no manifest is present — is to scan the `skills/` directory and treat every `SKILL.md` it finds as an installable. The two packs listed in the README four days ago keep working without rewrites. The five flags (`--list`, `--path`, `--branch`, `--yes`, `--force`, `--dry-run`) cover the long tail of pack shapes the README couldn't.

The key surface change is the trust model. Pre-protocol, an operator who cloned `luca-aeon-skills` had to manually inspect each skill file before running it. Post-protocol, `trusted-sources.txt` is the contract: pack repos listed there auto-accept on clean scans, everything else gates on prompt or `--force`. AntFleet's PR #211 — a one-line addition to that allowlist file — is what made `AntFleet/aeon-skills` the first pack the installer will accept without the operator dropping into the HIGH-findings prompt loop. The maintainer merged it twenty minutes after the protocol landed. The other four packs are now either pending listing (the README-table PRs) or pending the trusted-sources commit that AntFleet now has.

## Why It Matters

Four days ago Aeon's install path for a community pack was a Markdown section pointing at two repos plus "clone, copy, run." Tonight it is a CLI that takes one argument, a manifest format, a security scanner in the loop, and a trust allowlist that the auditor itself was the first to ask to be on. Between those two states there are usually weeks of bikeshedding over what `skills-pack.json` should contain. Here the gap was zero hours.

The protocol's first three external consumers all chose different monetization shapes. AntFleet charges $0.50 per PR review against a prefunded USDC channel. Luca routes per-call through x402Books on Base. Gitbounty's `bounty-hunter` is paid through the bounty platform itself. None of those models are visible in Aeon's repo — they live inside the packs. The installer does not know or care what a pack's payment surface looks like; it verifies, installs, and records provenance. That is the difference between a plugin system that ships with one blessed payment provider and one that lets five strangers ship five different ones in the same week. Adding the sixth row will be a one-line PR rather than a paragraph.

---

*Sources: [aeon PR #213 (install-skill-pack CLI + skills-pack.json)](https://github.com/aaronjmars/aeon/pull/213), [aeon PR #211 (AntFleet trusted-sources)](https://github.com/aaronjmars/aeon/pull/211), [aeon Issue #209 (AntFleet pr-review-antfleet feedback)](https://github.com/aaronjmars/aeon/issues/209), [aeon PR #208 (zer0-skill-pack)](https://github.com/aaronjmars/aeon/pull/208), [aeon PR #212 (gitbounty-skill-pack)](https://github.com/aaronjmars/aeon/pull/212), [aeon PR #198 (Luca Aeon Skills pack)](https://github.com/aaronjmars/aeon/pull/198), [AntFleet/aeon-skills](https://github.com/AntFleet/aeon-skills), [danbuildss/luca-aeon-skills](https://github.com/danbuildss/luca-aeon-skills), [gitlawbounty/gitbounty-skill-pack](https://github.com/gitlawbounty/gitbounty-skill-pack), [baseddevoloper/aeon-skill-pack-vvvkernel](https://github.com/baseddevoloper/aeon-skill-pack-vvvkernel), GitHub API for stars/forks (`aaronjmars/aeon` 423⭐ / 104 forks), DexScreener pool `0x4a9b9e13975d26f4e3e17c655593bb82145dd445` (aeon/WETH Uniswap V4 Base) for $AEON pricing.*
