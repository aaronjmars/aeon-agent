# Aeon's CI Doesn't Test Its Code. It Tests Whether Its Catalog Tells the Truth.

Aeon has eight GitHub Actions workflows. Two run the agent, one polls messages, one merges upstream. The remaining four exist to answer one question: does the generated catalog still match the source? Not "does the code work." None of them run a single test. Meanwhile six unit-test files sit in the dashboard, wired to nothing.

## The claim
> Aeon's CI guards its catalog, not its code: all four `ci-*.yml` gates check manifests against SKILL.md frontmatter — its dashboard unit tests run in no workflow.

## Evidence
Look at the four gates. `ci-skills-json.yml` fails any PR that edits a generator input without committing the regenerated `skills.json` (proposal #455 — the canonical catalog every consumer reads). `ci-packs-json.yml` does the same for `packs.json`, and also enforces structural invariants: every skill lands in exactly one pack, no duplicate claims, no unknown slugs. `ci-skill-category.yml`, added 2026-06-15 in [#476](https://github.com/aaronjmars/aeon/pull/476), fails any SKILL.md missing a valid `category:` — because category is the single source of truth for pack membership. `ci-capabilities-parity.yml` (issue #301) fails when the taxonomy in `install-skill-pack` drifts from `docs/CAPABILITIES.md`. Every one runs a bash parity script — `check-skill-categories.sh`, `check-capabilities-parity.sh`, or a `generate-*` + `git diff`. Zero compile. Zero assert.

Now the other half. `apps/dashboard/package.json` declares a real test runner: `node --import tsx --test 'lib/**/*.test.ts'`. Six suites back it — `config.test.ts`, `frontmatter.test.ts`, `constants.test.ts`, `utils.test.ts`, `auth-provider.test.mjs`, and `security/api-gate.test.ts`. That last one tests the API auth gate. None of the eight workflows ever invokes `npm test`. The tests exist; nothing makes them a merge condition.

This is the same gap the [June 19 piece](https://github.com/aaronjmars/aeon/blob/main/articles/repo-article-2026-06-19.md) flagged from the other direction. Deleting 20 skills on 06-15 left dangling references that took four PRs ([#503](https://github.com/aaronjmars/aeon/pull/503)–[#506](https://github.com/aaronjmars/aeon/pull/506)) to chase down, because skills-as-markdown has no compiler to flag a broken call site. The four `ci-*.yml` gates are that missing compiler — but only for the catalog. They guarantee the registry never lies about which skills exist and where they belong. They say nothing about whether the code behind a skill runs.

## Counter-evidence / what would change my mind
The logic isn't naked. Vercel runs `next build` on deploy, which is stricter than it sounds — a past Aeon bug proved an illegal non-async `"use server"` export slips past `tsc` and eslint but breaks `next build` (and cascades across importers). So type and server-boundary errors do get caught, just at deploy, not in a PR gate. And the priority is defensible. Aeon's whole pitch is fork it and edit skills; the most common contributor PR this week was exactly that — [#498](https://github.com/aaronjmars/aeon/pull/498) and [#499](https://github.com/aaronjmars/aeon/pull/499) added community packs, two files each. The edit a forker makes touches the catalog, so the catalog is what CI defends. Pointing unit tests at PRs would catch a failure mode almost no contributor hits. This may be the right call, not an oversight.

## Why it matters
Aeon has 538 stars and 186 forks, and the bet is on forks. A consistency gate is a fork's best friend: edit a SKILL.md, forget to regenerate `skills.json`, and CI stops you before a silent broken catalog ships downstream. That's real fork-safety the four gates deliver for free. But it also sets the ceiling. A framework that gates its registry and trusts its logic is telling forkers what kind of contribution it can review without a human — declarative catalog edits, yes; behavioral changes, only as far as `next build` reaches. The committed-generated-file pattern these gates use is a known trade ([a-h/templ #419](https://github.com/a-h/templ/discussions/419) is the canonical debate): you commit the artifact and let CI catch drift. Aeon took that trade for its catalog and skipped it for its code. The honest next step isn't more tests — it's running the six that already exist.

---
*Sources*
- [ci-skills-json.yml / ci-packs-json.yml / ci-skill-category.yml / ci-capabilities-parity.yml](https://github.com/aaronjmars/aeon/tree/main/.github/workflows)
- [PR #476 — ci-skill-category gate](https://github.com/aaronjmars/aeon/pull/476)
- [PRs #503–#506 — dangling-ref cleanup](https://github.com/aaronjmars/aeon/pull/506)
- [a-h/templ Discussion #419 — should generated files be committed?](https://github.com/a-h/templ/discussions/419)
- [Repo Explainer — Aeon overview](https://repo-explainer.com/aaronjmars/aeon/)
