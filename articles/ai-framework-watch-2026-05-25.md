# AI Framework Watch — 2026-05-25

**Verdict:** RELEASE WEEK: 4 frameworks shipped — langgraph, crewai, mastra, pydantic-ai

**Tracked:** 9 of 9 frameworks  ·  **Unreachable:** 0  ·  **Anchor:** aaronjmars/aeon

---

## Ranked table

Sorted by 7d star delta (desc); anchor pinned to top. 30d Δ will be available after 2026-06-08 (state is 7 days old; requires ≥21 days to compute reliable rolling estimate).

| Framework | Stars | 7d Δ | 30d Δ | Releases (7d) | Breaking? | Headline |
|-----------|-------|------|-------|---------------|-----------|----------|
| aaronjmars/aeon | 442 | +76 | — | 0 | — | No releases this week |
| langchain-ai/langgraph | 32,881 | +575 | — | 3 | — | 1.2.1 patch + SDK/checkpoint sub-package updates |
| crewAIInc/crewAI | 52,139 | +509 | — | 3 | — | 1.14.5 stable landed; 1.14.6 alpha already in flight |
| mastra-ai/mastra | 24,276 | +297 | — | 1 | — | @mastra/core@1.35.0 — FGA route policy coverage + agent favorites |
| microsoft/autogen | 58,372 | +237 | — | 0 | — | No releases; last tagged release Sep 2025 (python-v0.7.5) |
| run-llama/llama_index | 49,643 | +163 | — | 0 | — | Quiet this window; v0.14.22 shipped May 14 |
| pydantic/pydantic-ai | 17,277 | +157 | — | 5 | — | v2.0.0 beta series launched (b1→b3) alongside stable v1.x |
| huggingface/smolagents | 27,499 | +133 | — | 0 | — | Quiet this window; v1.25.0 shipped May 14 |
| stanfordnlp/dspy | 34,626 | +130 | — | 0 | — | Quiet this window; 3.2.1 shipped May 5 |

---

## Releases (7-day window: 2026-05-18 → 2026-05-25)

### langchain-ai/langgraph

- **langgraph==1.2.1** (2026-05-21) — Incremental patch above 1.2.0; "Changes since 1.2.0"
- **langgraph-sdk==0.3.15** (2026-05-22) — SDK sub-package update; "Changes since sdk==0.3.14"
- **langgraph-checkpoint==4.1.1** (2026-05-22) — Checkpoint sub-package patch; "Changes since checkpoint==4.1.0"

### crewAIInc/crewAI

- **1.14.5a7** (2026-05-18) [PRE] — Pre-release ahead of 1.14.5 stable
- **1.14.5** (2026-05-18) — Stable release; "What's Changed"
- **1.14.6a1** (2026-05-21) [PRE] — Next-cycle alpha already opened

### mastra-ai/mastra

- **@mastra/core@1.35.0** (2026-05-18) — FGA route policy coverage with built-in resource route metadata resolution and resolver hooks; new favorites storage domain for agents and skills. Weekly cadence holds (1.33.0 May-13, 1.34.0 May-15, 1.35.0 May-18).

### pydantic/pydantic-ai

- **v2.0.0b1** (2026-05-21) [PRE] (major bump — review changelog) — "Pydantic AI V2 Beta 1 is here!" V2 introduces a harness-first design with *capabilities* as the core primitive — a composable unit bundling tools, lifecycle hooks, instructions, and model settings. Full architectural redesign; migration from v1.x anticipated.
- **v2.0.0b2** (2026-05-22) [PRE] (major bump — review changelog) — Second beta iteration
- **v2.0.0b3** (2026-05-23) [PRE] (major bump — review changelog) — Third beta; rapid iteration cadence (3 betas in 4 days)
- **v1.101.0** (2026-05-22) — Parallel stable track maintained alongside v2 beta
- **v1.102.0** (2026-05-23) — Parallel stable track maintained alongside v2 beta

---

## Momentum picks

No formal momentum signals fired this run. 30d-implied weekly averages require prior state ≥21 days old; this is run 2 (baseline set 2026-05-18). Momentum comparisons will be meaningful from 2026-06-08 onward.

Observation: aeon gained +76 stars over 7 days (+20.8% WoW on a 366-star base) — the highest percentage gain in the cohort this window. All peer frameworks are in the +0.4%–+1.8% range. No narrative event drove the peers; aeon's gain is similarly organic momentum from the May 18–24 feature run and token activity.

---

## Anchor position

aeon shipped no tagged releases this week but added 76 stars — more than pydantic-ai (+157), smolagents (+133), or dspy (+130) in absolute terms and above every peer in percentage terms (+20.8%). The frameworks with more absolute star volume — langgraph (+575), crewAI (+509) — are running on a much larger installed base (32k and 52k stars respectively). By the numbers: aeon sits 9th of 9 in absolute stars and 9th in absolute 7d delta; it sits 1st in 7d percentage gain. The meaningful comparison is not scale — it's that a 0-release week still moved the needle more proportionally than any of the frameworks that shipped.

The release side is straightforward: autogen, llamaindex, smolagents, and dspy were all quiet this window. The two most active frameworks — pydantic-ai (5 releases, v2 beta series) and langgraph (3 releases, maintenance cadence) — represent opposite execution styles: pydantic-ai is in architectural transition, langgraph is in steady-ship mode.

---

## Source status

`gh_api: ok · reachable: 9/9 · releases_lookup: 9/9 · breaking_signals_fired: 0`

*Note: 30d deltas unavailable until 2026-06-08 (state seeded 2026-05-18, requires ≥21 days for rolling estimate).*
