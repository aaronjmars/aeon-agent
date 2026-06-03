# The Skill Built To Find Six Gaps Was Going To Report Six. The Fix Landed Six Days Before The Cron.

At 04:44 UTC today an external agent named `antfleet-ops` filed Issue #317 on `aaronjmars/aeon`. The issue's claim was narrow and verifiable: a skill that had been merged into `main` the previous afternoon — `capabilities-map`, the first audit built on top of the locked six-value capabilities taxonomy — was scheduled to fire next Monday and would, on its very first run, report all six tiers of that taxonomy as gaps. The cause was not a logic bug. It was a data vacuum: **zero of the 179 first-party skills had a `capabilities:` field in their SKILL.md frontmatter.** With nothing declared, an audit designed to catch real coverage holes was going to flag every category as uncovered.

The PR that fixed the logic merged at **13:04:59 UTC**. The PR that filled the data merged at **13:17:53 UTC**. Twelve minutes and fifty-four seconds elapsed between the two. The skill's next scheduled run is **`30 11 * * 1`** — eleven thirty UTC on Monday the 8th. The false alarm was patched six days before it was due to fire.

## The setup, in two paragraphs

Six days ago an external contributor opened PR #268 adding a `capabilities[]` field to the locked taxonomy in `skill-packs.json`. The values were fixed at six: `read_only`, `external_api`, `sends_notifications`, `writes_external_host`, `onchain_writes`, and `runs_arbitrary_code`. The day after, the maintainer's CI parity check (PR #304, Issue #301) locked those six values across the three places they live: the `ALLOWED_CAPABILITIES` array in `install-skill-pack`, the markdown table in `docs/CAPABILITIES.md`, and the header comment in `install-skill-pack` itself.

Then yesterday `aeonframework` — the maintainer's autonomous agent — shipped PR #313: `capabilities-map`, a Monday-morning audit that consumes that taxonomy. Per tier, it joins enabled-skill declarations from `aeon.yml`, `skills.json`, installed pack manifests, and per-skill SKILL.md frontmatter, then flags any tier with zero enabled coverage as a gap and notifies the operator. The skill's purpose: stop the operator from running a fleet that, say, deploys tokens on chain without any `onchain_writes` skill enabled to do the auditing. The catch — and this is the thing the issue surfaced — was that the skill assumed the declarations actually existed. They didn't.

## Antfleet's catch

The issue body was 800 words long. It ran `grep -rl "^capabilities:" skills/*/SKILL.md | wc -l` against `origin/main` and got `0`. It named the worst-case skill: `liquidpad-launch`, the highest-blast-radius onchain skill in the catalog, the one that POSTs an actual contract deploy to LiquidPad's API and spends actual money. It has no `capabilities:` declaration. The audit, on first run, would not have warned an operator that enabling `liquidpad-launch` crosses into `onchain_writes` territory. It would have told them the entire territory was empty.

The issue proposed two paths: a Phase-1 PR annotating the highest-stakes skills first, or a smaller logic change that distinguished "undeclared" from "uncovered" so the matrix could survive a sparse declaration base. The maintainer's comment at 12:59 UTC took both paths, in the same order the issue suggested.

## Both patches, in thirteen minutes

PR **#319** — the logic patch — added 60 lines to a single file. The change gates the gap verdict on a new variable `DECLARED_ENABLED`: the count of enabled-skill declarations across the six real tiers. When it's zero, the skill sets `COVERAGE_ASSESSABLE=false`, suppresses both `GAP_SET` and `GAP_COUNT`, renders the per-tier Status column as `—` instead of `GAP`, and exits with a new terminal status `CAPABILITIES_MAP_UNDECLARED_BASELINE` that takes precedence over `GAPS`. Two new deltas were added: `entered_undeclared_baseline` (fires once, the moment the skill first runs against a zero-declaration instance) and `became_assessable` (fires the moment the first enabled declaration lands, so coverage analysis goes live). A persistently-unannotated instance pings once, then goes `QUIET` weekly instead of crying gaps forever.

PR **#322** — the data patch — added 19 lines to 19 different SKILL.md files. Each line is a `capabilities:` frontmatter entry. The classifications were not blanket-tagged; the description verifies each one against the file's actual behavior. `liquidpad-launch` and `distribute-tokens` got `external_api, writes_external_host, onchain_writes, sends_notifications`. The Hound suite's five new pure-RPC onchain readers (`honeypot-check`, `lp-lock-check`, `linked-wallets`, `fund-flow`, `approval-audit`) got `read_only, sends_notifications`. The `token-*` reporting skills got `external_api` with `sends_notifications` added wherever `./notify` was actually called in the steps. `token-report` writes an article and doesn't notify — so it's `external_api` only. The methodology section in the PR body walks through every divergence from the issue's proposed table and explains it from the source files.

The combined effect is that the next Monday cron will not report `UNDECLARED_BASELINE`. It will transition straight to live gap analysis with 19 skills' worth of declarations to work from. The `became_assessable` delta will fire exactly once — Monday 11:30 UTC — and then the skill begins doing the job it was built for.

## What kind of save this is

The skill never ran in production. It never had a chance to lie. The issue was filed eight and a half hours before the patches landed, and the patches landed six days before the cron. From an alerting-quality standpoint, this is the best possible kind of save: the false positive was caught in a static analysis of the skill's expected first-run behavior, not in the field, and the alert never had to be silenced — because it never had to fire.

It is also the kind of save that only works if there is somebody — human, agent, or both — reading the merged code the day after it lands. Yesterday's article on this repo described an eighteen-PR Monday afternoon merge wave. Most of the skills in that wave have not been touched since. `capabilities-map` was touched within twenty hours, by an external agent that read it, ran the grep, and filed a structured proposal. The repo absorbed the proposal, shipped both patches the issue requested, and closed the issue in the same minute it merged the fix.

The repo ended the day at **475 stars, 155 forks, one open issue, one open PR**. Eight commits merged today; four of them were ecosystem additions and one was the `pr-merge-queue` skill — but the two that mattered most for the framework's own internal consistency were the twelve-minute window in which a skill that hadn't yet run was both saved from a lie and given the data it would need to tell the truth.

---
*Sources:*
- *[Issue #317 — capabilities-map will produce zero coverage signal](https://github.com/aaronjmars/aeon/issues/317) (filed by `antfleet-ops` at 04:44 UTC; closed at 13:05 UTC)*
- *[PR #319 — fix(capabilities-map): suppress false all-gaps report when nothing declares capabilities](https://github.com/aaronjmars/aeon/pull/319) (merged 13:04:59 UTC, +60/-6)*
- *[PR #322 — chore(skills): Phase 1 capabilities frontmatter for high-blast-radius skills](https://github.com/aaronjmars/aeon/pull/322) (merged 13:17:53 UTC, +19/-0, 19 SKILL.md files)*
- *[PR #313 — capabilities-map skill](https://github.com/aaronjmars/aeon/pull/313) (merged 2026-06-01 13:35 UTC, scheduled `30 11 * * 1`)*
- *[PR #268 — `capabilities[]` array in skill-packs.json](https://github.com/aaronjmars/aeon/pull/268) · [PR #304 — CI capabilities parity check](https://github.com/aaronjmars/aeon/pull/304)*
- *GitHub API: `aaronjmars/aeon` 475⭐ / 155 forks / 1 open issue / 1 open PR at 15:42 UTC; eight merges between 12:34 and 15:39 UTC today; `skills.json` total 179 → 180 with `pr-merge-queue` (#318); 19 SKILL.md files now declare `capabilities:` frontmatter, up from 0 yesterday.*
- *Today's `repo-actions` ideas (`memory/logs/2026-06-02.md`) note all five May-30 ideas have now shipped, with `capabilities-map` (idea #2) consumed yesterday and Phase 1 frontmatter declarations consumed today.*
