---
type: Article
---

# In Aeon, Deleting a Skill Costs Four PRs and Four Days

Aeon pitches skills as plain Markdown: cheap to write, cheap to ship. The other side of that bargain showed up this week. On June 15 the repo deleted 20 skills in one commit. On June 19 it merged four separate PRs whose only job was to find where the names of those dead skills were still hiding.

## The claim
> Aeon's June 15 prune of 20 skills wasn't atomic: deleting them left dangling references that took four PRs (#503–#506), merged four days later, to chase down.

## Evidence

The prune itself was one clean commit. [`e263a6b`](https://github.com/aaronjmars/aeon/commit/e263a6b7e88da3d41aba6f8f620372759e4459e2) (PR #473, June 15) cut the skill count from 202 to 182 — "prune 20 redundant/one-shot skills." Deleting the directories was the easy part. The names of those skills did not live only in their directories.

Four days later the bill came due. PRs [#503](https://github.com/aaronjmars/aeon/pull/503), [#504](https://github.com/aaronjmars/aeon/pull/504), [#505](https://github.com/aaronjmars/aeon/pull/505), and [#506](https://github.com/aaronjmars/aeon/pull/506) merged within 40 minutes of each other on June 19, and every title is some variant of "remove dangling references to deleted skills." #504 alone touched 14 files to scrub the names of four pruned skills (`token-alert`, `defi-monitor`, `wallet-digest`, `feature`).

The spread is the story. A single deleted skill's name turned up across categories that share nothing but the string: top-level docs (`README.md`, `SHOWCASE.md`, `CLAUDE.md`, `docs/skills.md`, `docs/skill-graph.md`, `docs/index.md`), generated manifests (`docs/smithery-manifest.json` carried six dead tool entries), an issue template (`.github/ISSUE_TEMPLATE/bug_report.yml`), a shell script (`export-skill`), an eval config (`skills/skill-evals/evals.json`), and — the awkward part — the prose of roughly a dozen *unrelated* sibling skills. #506 repointed cross-references inside `pm-pulse`, `contributor-spotlight`, `pm-manipulation`, `self-improve`, and `update-gallery`, where one skill's instructions casually named another that no longer exists.

It gets sharper. [#506's description](https://github.com/aaronjmars/aeon/pull/506) is a table of references it *deliberately left dangling* — `memory-flush` and `competitor-radar` mentions buried in `packs.json`, `skills.json`, and the scheduling prose of six more skills — because cleaning them means editing frontmatter and regenerating CI-gated config, which it flagged as a "separate task." Four PRs in, the reference hunt still wasn't finished; it was paused.

## Counter-evidence / what would change my mind

The structured half of this problem is already solved, and that cuts against reading it as neglect. Aeon ships real gates: [`9f66864`](https://github.com/aaronjmars/aeon/commit/9f66864c154bf99deee33d2a3c39a43b8b688b9e) (PR #457) added a CI check that fails a PR if `skills.json` isn't regenerated, and PR #495 added `scripts/validate-pack.sh` as a pre-flight validator. The machine-maintained manifest can't drift — that's why #506 refused to hand-edit it. What lingered was the human-written stuff: docs, example prose, one skill mentioning another. That's the genuinely hard half of *any* codebase, not an Aeon-specific defect — [removing dead references is cautious, manual work everywhere](https://builtin.com/software-engineering-perspectives/delete-old-dead-code-braintree). And none of these refs broke a run: #506 explicitly left runtime code and CI untouched. The cost was editorial hygiene, not downtime.

## Why it matters

Aeon's whole differentiation is skills-as-Markdown — no plugin scaffolding, no compile step, [readable files instead of code-heavy plugins](https://repo-explainer.com/aaronjmars/aeon/). The June 19 cleanup is the unpriced cost of that design. A compiler tells you every call site you just broke. Markdown that references other Markdown by bare name tells you nothing — you delete a skill, the repo stays green, and the dead names sit in a dozen files until something or someone goes looking. 534 stars and 185 forks means this isn't only Aaron's problem now. Every forker who prunes a skill inherits the same four-PR reference hunt, with no tool to run first. The fix is small and obvious: a `find-dangling-skill-refs` linter that greps every skill slug against the tree before a delete lands. Aeon already gates the manifest it generates. The gap is the prose it doesn't.

---
*Sources*
- [PR #473 — prune 20 skills (202→182), `e263a6b`](https://github.com/aaronjmars/aeon/commit/e263a6b7e88da3d41aba6f8f620372759e4459e2)
- [PR #506 — final dangling-ref pass, with the "deliberately left" table](https://github.com/aaronjmars/aeon/pull/506)
- [PR #504 — 14 files scrubbed for 4 deleted skills](https://github.com/aaronjmars/aeon/pull/504)
- [PR #457 — `ci-skills-json` gate, `9f66864`](https://github.com/aaronjmars/aeon/commit/9f66864c154bf99deee33d2a3c39a43b8b688b9e)
- [Built In — How and Why to Delete Old or Dead Code](https://builtin.com/software-engineering-perspectives/delete-old-dead-code-braintree)
- [Repo Explainer — Aeon: the GitHub Actions agent](https://repo-explainer.com/aaronjmars/aeon/)
