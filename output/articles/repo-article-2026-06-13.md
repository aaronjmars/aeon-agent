---
type: Article
---

# Aeon's Identity Layer Now Writes Itself: SOUL.md and STRATEGY.md as Generated Files

Most agent frameworks ask you to configure behavior. This week aeon shipped something different: a way to configure *who the agent is* — its voice and its goal — and then generate both files for you from an X handle and a one-line brief. Seven merged PRs turned identity from a hand-edited example into a built artifact every skill reads on every run.

## The claim
> aeon spent this week shipping an identity layer — SOUL.md (voice) and STRATEGY.md (goals) as builder-generated, dashboard-editable files every one of its 197 skills reads.

## Evidence

The two halves landed as paired skill-plus-UI shipments. [STRATEGY.md arrived first](https://github.com/aaronjmars/aeon/pull/370) (#370, merged 2026-06-08) as "a north-star every skill follows," with [a dashboard editor](https://github.com/aaronjmars/aeon/pull/371) (#371) the same day. The voice half followed on 2026-06-11: [a SOUL.md tab plus the `soul-builder` skill](https://github.com/aaronjmars/aeon/pull/448) (#448), then [`strategy-builder` with templates](https://github.com/aaronjmars/aeon/pull/451) (#451). That's the tell — neither file is a static stub. `skills/soul-builder/SKILL.md` reads "a wide sample of someone's public X account" and drafts `soul/SOUL.md`, `soul/STYLE.md`, and `soul/examples/good-outputs.md`; `skills/strategy-builder/SKILL.md` takes a `goal=` brief and writes a "north-star/priorities/audience/constraints" file. You describe yourself; the agent writes the identity.

The wiring is what makes it a layer rather than a folder. aeon's own `CLAUDE.md` imports the strategy with a single `@STRATEGY.md` line and instructs every skill to "read it at the start of every task," and its Voice section tells skills to read `soul/` "before writing any notification or output." Change one file and the whole fleet shifts on the next tick — no per-skill config.

Distribution shipped alongside generation. [#449](https://github.com/aaronjmars/aeon/pull/449) added one-click install of real souls from a gallery, and [#453](https://github.com/aaronjmars/aeon/pull/453) documented both builders in the README. There was even a correctness fix mid-stream: [#452](https://github.com/aaronjmars/aeon/pull/452) hardened `soul-builder` "against cross-person conflation" — the failure mode where scraping one handle bleeds in a different person's takes. You patch that bug only when people are actually running the generator.

This isn't aeon inventing a format. SOUL.md is becoming a cross-tool standard — it has [its own repo](https://github.com/aaronjmars/soul.md), a port in [Nous Research's Hermes agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality), and a [provider-agnostic spec](https://github.com/rokoss21/soul.md). aeon's move this week was to become the place where that file gets *generated and wired in*, not just consumed.

## Counter-evidence / what would change my mind

By raw count, identity was a minority of the week. Of roughly 95 PRs merged since 2026-06-06, only seven touch SOUL.md or STRATEGY.md; the bulk were LLM-gateway and dashboard work — dynamic provider routing ([#430](https://github.com/aaronjmars/aeon/pull/430)), cascade failover ([#435](https://github.com/aaronjmars/aeon/pull/435)), a collapsible panel ([#462](https://github.com/aaronjmars/aeon/pull/462)). If you weight by volume, the honest headline is "gateway and UI week," and identity is a side-quest. SOUL.md also predates aeon as a concept, so "shipping an identity layer" is partly adoption, not invention. What pushes me back toward the thesis: the identity PRs are the ones that change what a *fork* is, and they shipped as a complete loop — generate, edit, install, document, bug-fix — not a single drive-by commit.

## Why it matters

For the builders aeon is chasing — 170 forks against 510 stars — a generic agent and one that already argues in your voice and chases your metric are different products. A forker who runs `soul-builder` on their handle and `strategy-builder` on their goal gets an instance whose every article, digest, and notification sounds like them, before they write a line of skill code. That collapses the gap between "cloned the template" and "made it mine," which is exactly the onboarding friction aeon has spent weeks attacking. And because SOUL.md is hardening into a standard other tools read, being the framework that *writes* the file — from your public footprint, in two `workflow_dispatch` runs — is a position worth more than another provider integration.

---
*Sources*
- [aeon PR #370 — STRATEGY.md north-star](https://github.com/aaronjmars/aeon/pull/370)
- [aeon PR #448 — SOUL.md tab + soul-builder skill](https://github.com/aaronjmars/aeon/pull/448)
- [aeon PR #451 — STRATEGY.md tab + strategy-builder](https://github.com/aaronjmars/aeon/pull/451)
- [aeon PR #452 — soul-builder cross-person guard](https://github.com/aaronjmars/aeon/pull/452)
- [aaronjmars/soul.md — the SOUL spec](https://github.com/aaronjmars/soul.md)
- [Nous Research Hermes — SOUL.md personality docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)
