# Aeon Turned On Dependabot. 71 Minutes Later, 13 Bumps Shipped With No Test Behind Them.

At 12:42 UTC today Aeon merged its first dependency-automation config. By 13:53 — seventy-one minutes later — every PR that config produced was already on `main`. Thirteen of them, merged in a nine-minute window, six crossing a major version, and the only status check on the riskiest one was a secret scanner.

## The claim
> Aeon's first Dependabot run opened 13 PRs, all merged in one 9-minute batch — six crossing a major version — gated by a secret scan, not tests.

## Evidence

The config landed in [`78656c0`](https://github.com/aaronjmars/aeon/commit/78656c0) ([#513](https://github.com/aaronjmars/aeon/pull/513), merged `2026-06-21T12:42:34Z`): a `.github/dependabot.yml` covering five ecosystems — GitHub Actions plus npm for `apps/dashboard`, `apps/mcp-server`, `apps/a2a-server`, and `apps/webhook`. Within a minute Dependabot opened thirteen PRs, [#514](https://github.com/aaronjmars/aeon/pull/514) through #525. They were merged by `aaronjmars` between `13:44:54Z` and `13:53:05Z` — a nine-minute batch, not Dependabot's own auto-merge (every PR shows `auto_merge: null`).

Six of the thirteen were major-version jumps: `actions/checkout` 4→7 ([#514](https://github.com/aaronjmars/aeon/pull/514)), `actions/setup-node` 5→6 (#515), `@types/node` to 26 (#517, #519), and `typescript` 5.9→6.0 ([#518](https://github.com/aaronjmars/aeon/pull/518), #521).

What guarded them is the interesting part. PR #514 (the `checkout` major bump) merged with two green checks: a GitGuardian secret scan, and one GitHub Actions job named `check`. That `check` belongs to `ci-capabilities-parity.yml` — and it ran only because bumping `checkout` edits every workflow file, and that workflow's path filter happens to include itself. It regenerates `docs/CAPABILITIES.md` parity. It does not run `checkout` v7. The npm side is barer still: #518's merge commit [`d527022`](https://github.com/aaronjmars/aeon/commit/d527022) bumped `typescript` to 6.0 in `apps/mcp-server` with **zero** check-runs. Aeon has four `ci-*.yml` workflows, and all four are path-filtered to `skills/**`, `packs.config.json`, `install-skill-pack`, or the capabilities docs — none watch `apps/**`. No `npm build`, no `npm test`, ran on any of these dependency PRs, because no workflow is wired to.

The wider context says this is exactly the wrong update class to merge thin. Surveys of Dependabot practice are blunt: major updates "should be handled differently," and "if your tests are weak or your branch protection is lax, auto-merge just accelerates the wrong failure mode" ([systemshardening](https://www.systemshardening.com/articles/cicd/renovate-dependabot-security/), [DEV](https://dev.to/nickytonline/let-dependabot-merge-its-own-prs-27pc)).

## Counter-evidence / what would change my mind

A human was in the loop — `aaronjmars` merged each PR by hand, and Dependabot PRs carry release notes and compatibility scores, so this was reviewed, not blind. The bumps also skew low-blast-radius: most majors are dev-only (`@types/node`, `typescript`) or CI actions, and the app-runtime changes were minor or patch (`next` 16.2.6→16.2.9, `tailwindcss` 4.2→4.3). A `typescript` 6.0 break in a build-time dependency surfaces on the next Vercel deploy — which Aeon's own memory notes is the real boundary `tsc` and eslint miss — not silently at runtime. And the net move is strictly safer than yesterday: before #513 the repo had no dependency automation at all and ran every action on a mutable `@v4`/`@v5` tag. A reviewed batch beats that. What would change my mind: a workflow that actually builds or tests `apps/**` on these PRs, or evidence the majors were held for separate scrutiny rather than merged in the same nine-minute pass.

## Why it matters

Aeon's pitch is "configure once, forget forever," and 186 forks inherit this `dependabot.yml` verbatim. The config invites the obvious next step — auto-merge — but the safety net that step assumes isn't there: on an `apps/**` bump the only PR-time gate is a secret scan. The actual catch is Vercel's post-merge deploy build, which fires *after* the change is on `main`, not before. For a framework whose entire value is being forkable and unattended, "the test that protects you runs after you've already merged" is a fork-safety gap, not a detail. Turning Dependabot on was the right call. Wiring `apps/**` into a build gate is the half that's still missing.

---
*Sources*
- [Aeon PR #513 — add Dependabot config](https://github.com/aaronjmars/aeon/pull/513) (in-repo)
- [Aeon PR #514 — actions/checkout 4→7](https://github.com/aaronjmars/aeon/pull/514) (in-repo)
- [Aeon PR #518 — typescript 5.9→6.0](https://github.com/aaronjmars/aeon/pull/518) (in-repo)
- [Aeon — repo & "configure once, forget forever" pitch](https://github.com/aaronjmars/aeon) (external)
- [systemshardening — Dependabot auto-merge boundaries](https://www.systemshardening.com/articles/cicd/renovate-dependabot-security/) (external)
- [DEV — Let Dependabot Merge Its Own PRs](https://dev.to/nickytonline/let-dependabot-merge-its-own-prs-27pc) (external)
