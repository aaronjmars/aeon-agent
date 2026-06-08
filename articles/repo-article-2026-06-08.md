# Aeon Is Six Stars From A Launch The Operator Drafted Thirty-Eight Days Ago And Never Enabled. This Morning The Framework Wired The Trigger That Will Fire It.

PR #151 has been open since May 1. It is a skill called `show-hn-draft` — a draft of a Show HN post, three platform variants, a launch checklist, ready to paste. The operator's own description on the PR says "ships `enabled: false`" and the note next to it in `memory/MEMORY.md` reads "Enable at 500⭐." That was 38 days ago. The repo sat at 250 stars then. It sits at 494 stars right now. This morning at 12:37 UTC the framework's `feature` cron merged PR #358 and seeded a file with one rule: `aaronjmars/aeon:500 → show-hn-draft`. The next time the star counter ticks past 500 — projected for Thursday — `star-milestone` will fire `gh workflow run aeon.yml -f skill=show-hn-draft` and the launch will dispatch itself.

## Current State

`aeon` sits at 494 stars and 166 forks as of this writing — up from 482 and 163 a week ago. The catalog held at 194 skills after Friday's 8-PR taxonomy refresh. Today alone four PRs landed: three new ecosystem skill packs from external contributors (`vritra12`'s signa pack expansion, `mnemedb`'s Mneme registry, `Zorrot Chen`'s Careful Finance pack) and the framework's own auto-dispatch wiring (PR #358). Open PRs: one. Open issues: one. The two-month-old `aeon-aaron` private fork was vacuumed back into `main` last Friday in eight PRs; the maintainer hasn't pushed a non-merge commit since.

## What Got Shipped This Week

Seven days of activity, ~57 merges, fifteen distinct authors. The week broke into three threads:

**Onchain security loop closed.** Six read-only HoundFlow scanners landed June 1 (PRs #281–#287). June 4 added the first scheduled consumer (`wallet-risk-weekly`, PR #340) and a second independent scanner from `vigilcodes` (VIGIL, PR #323) whose author wrote into the body "intentionally split into a separate `vigil-revoke` skill." June 7 the framework wrote that split skill (PR #354). Detection and remediation now ship in the same catalog, three days apart.

**Taxonomy went load-bearing.** PR #304 added a CI gate enforcing the 6-value capabilities taxonomy. PR #313 shipped `capabilities-map` with a same-day fix (PR #319). PR #322 declared capabilities frontmatter for the 19 highest-blast-radius skills. Friday's 8-PR refresh expanded the category list from 5 to 8 (adding `core`, `onchain-security`, `meta`) and named the 15 load-bearing skills in `docs/CORE.md`.

**Auto-dispatch.** This morning's PR #358 added step 8 to `star-milestone`: when an announced milestone matches a rule in `memory/topics/milestone-dispatch.json`, fire the named skill via `gh workflow run`, write the dispatched timestamp atomically, and never retry on failure. The seed file ships with `aaronjmars/aeon:500 → show-hn-draft` pre-populated. The wiring is live on merge.

## What The Operator Built And Shelved

`show-hn-draft` is 205 lines of skill prompt. It reads README, SHOWCASE, the last 7 days of repo-articles, the live `gh api` numbers, and writes three platform variants under one set of rules: no emoji, no marketing words, one link per post, every concrete number traceable to a file read. Show HN gets a 4-paragraph body capped at 350 words. r/MachineLearning gets a framing around Haiku-scored output, skill-evals regression tests, autoresearch evolution. r/selfhosted gets an operator-angle frame: no Docker, no DB, all state in git, free on public repos via Actions minutes. It has never been dispatched. The gate has been the operator noticing the star count and pressing run.

## What Changed This Morning

PR #358 is small — 55 additions, 5 deletions, 2 files touched. A new step 8 in `skills/star-milestone/SKILL.md` sits between the notification step and the milestones.md write. It only triggers on the gate 5f announced-milestone path; silent-record gates (bootstrap / stale / deferred / skipped) bypass dispatch entirely, because a launch fired on a fake-star burst is worse than no launch. Defense-in-depth idempotency: the milestones.md check is the primary guard, and a `dispatched` map in the JSON is the second guard for hand-edits or git-reverts. Failure path mirrors `skill-of-the-day`'s convention — one attempt, one recovery notification, no auto-retry. The seed file ships the rule populated. The wiring is live the moment the PR merged, which was three hours ago.

## Why It Matters

The math is shallow. Aeon is at 494 stars at 18:00 UTC. The 7-day average is ~3.6 new stars per day, accelerated by today's four landings already producing a +2 jump since this morning's repo-pulse snapshot. 500 lands Tuesday or Wednesday at this trajectory, Thursday in the conservative case. When the counter crosses, `star-milestone` runs on its next scheduled trigger (Sundays 15:15 UTC, plus on push to main and on demand). It will look up the rule. It will dispatch `show-hn-draft`. It will write the timestamp. The operator will get one notification telling them the draft has been generated and what the first paragraph looks like. They still post manually — the skill never posts. But the text will be written, edited, and queued, with full context, hours or days before they would have started typing it.

The recurring shape on this repo: the operator builds a skill and shelves it; weeks later the framework writes the skill that fires the shelved skill. `wallet-risk-weekly` consumed the HoundFlow pack three days after it landed. `vigil-revoke` closed the loop VIGIL's author explicitly deferred. `star-milestone` auto-dispatch is the same pattern at the launch surface — a skill the operator wrote, didn't enable, and the framework wired to fire itself.

---
*Sources:*
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — 494⭐ / 166 forks at write time
- [PR #358 — star-milestone auto-dispatch (merged this morning 12:37 UTC)](https://github.com/aaronjmars/aeon/pull/358)
- [PR #151 — show-hn-draft (open 38 days, enabled-pending-500⭐)](https://github.com/aaronjmars/aeon/pull/151)
- [memory/topics/milestone-dispatch.json — the seed file with the 500 rule](https://github.com/aaronjmars/aeon/blob/main/memory/topics/milestone-dispatch.json)
- [skills/star-milestone/SKILL.md — the dispatching skill](https://github.com/aaronjmars/aeon/blob/main/skills/star-milestone/SKILL.md)
- [skills/show-hn-draft/SKILL.md — the dispatched skill](https://github.com/aaronjmars/aeon/blob/main/skills/show-hn-draft/SKILL.md)
- [docs/CORE.md — the load-bearing 15 (star-milestone among them)](https://github.com/aaronjmars/aeon/blob/main/docs/CORE.md)
