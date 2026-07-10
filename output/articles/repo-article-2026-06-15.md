---
type: Article
---

# Aeon Spent Six Months Adding Skills. This Week It Started Hiding Them.

For three months the pitch was "more": 91 skills became 197. On June 15, [aaronjmars/aeon](https://github.com/aaronjmars/aeon) reversed course in a single afternoon — pruning the catalog from 202 to 182, then packaging the survivors so a fresh fork sees only 13. The framework that bragged about skill count just decided count was the wrong number to grow.

## The claim
> This week aaronjmars/aeon reversed its skill-count growth — pruning 202→182 ([#473](https://github.com/aaronjmars/aeon/pull/473)) and hiding everything but a 13-skill Core behind opt-in packs ([#474](https://github.com/aaronjmars/aeon/pull/474), [#479](https://github.com/aaronjmars/aeon/pull/479)).

## Evidence

The prune landed first. PR [#473](https://github.com/aaronjmars/aeon/pull/473) removed 20 skills and deleted 3,765 lines, dropping the catalog from 202 to 182. It wasn't a cull for its own sake — the body calls it "the first, highest-confidence batch from a full skill audit," and ~16 of the 20 are merges where the capability survives in another skill: `polymarket` and `polymarket-comments` fold into `monitor-polymarket`, `token-report` and `monitor-runners` into `token-movers`, `wallet-digest` into `onchain-monitor`. Only 4 were true deletions.

Then came the structure. PR [#474](https://github.com/aaronjmars/aeon/pull/474) introduced a "core + opt-in packs" model — a hand-authored `packs.config.json` that a `generate-packs-json` step compiles into the catalog the dashboard reads. The rule is strict: "every skill in skills.json must land in exactly one pack here, or the generator fails." The Core set is 13 skills — `create-skill`, `self-improve`, `skill-health`, `skill-repair`, `skill-evals`, `heartbeat`, `onboard`, `digest`, and five more — the self-evolution, self-healing, and liveness loop a fork can't run without. Everything else got sorted into named packs: Fleet & Replication, Crypto & Markets, Onchain Security, Dev & Code.

The decisive move was [#479](https://github.com/aaronjmars/aeon/pull/479), which fixed the mental model: "a pack is a visibility lens, not a bulk on-switch." By default you see only Core, everywhere — sidebar and HQ both. Enabling a pack reveals its skills; it doesn't run them. Of the 13 Core skills, only two (`heartbeat`, `digest`) are enabled by default. That's the real reversal: the default surface area of an Aeon fork shrank from 182 skills to 2 running, 13 visible. Supporting commits reinforce it — [#477](https://github.com/aaronjmars/aeon/pull/477) defaults the sidebar to enabled skills only, [#475](https://github.com/aaronjmars/aeon/pull/475) moved category into `SKILL.md` frontmatter, and [#476](https://github.com/aaronjmars/aeon/pull/476) added a `ci-skill-category` gate so every new skill must declare a pack or fail CI. Curation is now enforced, not aspirational.

## Counter-evidence / what would change my mind

The catalog didn't really lose much. PR #474 is explicit that the packs are "in-repo virtual packs — no skills move or get deleted"; existing forks "keep every skill and every enabled toggle." Of the prune's 20, only 4 were genuine removals — the rest live on under a different name. So "reversed its growth" overstates a permanent cut; this is reorganization plus a default-visibility change you can undo by toggling a pack on. And the timing cuts against a clean narrative: a week ago Aaron was still *adding* — `wc-resale` ([#442](https://github.com/aaronjmars/aeon/pull/442)), `capabilities-sweep` ([#416](https://github.com/aaronjmars/aeon/pull/416)) — and external contributors shipped three new skill packs the same week (signa #355, Mneme #356, Careful Finance #357). The growth didn't stop. It got a filter in front of it.

## Why it matters

Skill count was always a vanity metric pretending to be a capability metric. The industry has a name for the failure mode now — "skill sprawl" and "shadow skills," where capabilities pile up faster than anyone can govern them, and where more tools in an agent's context measurably degrade which tool it picks. A 182-skill catalog with everything on is a worse agent *and* a worse first-run: a forker who clones Aeon shouldn't have to reason about polymarket monitors before the thing boots. Core-by-default makes the day-one surface legible — 13 skills that explain themselves — and turns the other 169 into something you opt into when you have a reason. For a framework whose whole bet is fork-ability, hiding skills is the feature. The pitch quietly changed from "look how much it does" to "look how little you have to configure."

---
*Sources*
- [PR #473 — prune 20 redundant skills (202→182)](https://github.com/aaronjmars/aeon/pull/473)
- [PR #474 — first-party skill-pack system + dashboard Packs view](https://github.com/aaronjmars/aeon/pull/474)
- [PR #479 — packs are a visibility lens, show only Core by default](https://github.com/aaronjmars/aeon/pull/479)
- [PR #476 — fold packs into README/CONTRIBUTING + ci-skill-category gate](https://github.com/aaronjmars/aeon/pull/476)
- [aaronjmars/aeon repository](https://github.com/aaronjmars/aeon)
- [JFrog — What is an Agent Skills Repository? (skill sprawl / shadow skills)](https://jfrog.com/learn/ai-security/agent-skills-repository/)
