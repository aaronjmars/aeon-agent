# AI Framework Watch — 2026-05-18

**Verdict:** RELEASE WEEK: 6 frameworks shipped — langgraph, crewai, llamaindex, mastra, smolagents, pydantic-ai

**Tracked:** 9 of 9 frameworks · **Unreachable:** 0 · **Anchor:** aaronjmars/aeon

> *First run — all 7d/30d star deltas are baseline (—). Week-over-week comparisons start next Monday.*

---

## Ranked table

*(Anchor pinned top; all 7d/30d deltas are — on this COLD START baseline run. Secondary sort: total stars descending.)*

| Framework | Stars | 7d Δ | 30d Δ | Releases (7d) | Breaking? | Headline |
|-----------|-------|------|-------|---------------|-----------|----------|
| aaronjmars/aeon | 366 | — | — | 0 | — | No tagged releases; ships continuously via PR merges |
| microsoft/autogen | 58,135 | — | — | 0 | — | Last release Sep 2025; code still active (pushed Apr 2026) |
| crewAIInc/crewAI | 51,630 | — | — | 2 [PRE] | — | 1.14.5a5–a6 pre-release alpha cadence |
| run-llama/llama_index | 49,480 | — | — | 1 | — | v0.14.22 — dep upgrades across integration packages |
| stanfordnlp/dspy | 34,496 | — | — | 0 | — | 3.2.1 shipped May 5 — just outside the 7-day window |
| langchain-ai/langgraph | 32,306 | — | — | 5 | — | 1.2.0 stable — durable error-handler resume across crashes |
| huggingface/smolagents | 27,366 | — | — | 1 | — | v1.25.0 — security fix on remote executors |
| mastra-ai/mastra | 23,979 | — | — | 2 | — | 1.34.0 — ACP coding agents as tools, xAI realtime voice |
| pydantic/pydantic-ai | 17,120 | — | — | 5 | — | v1.97.0 — MCPToolset, Google provider split |

---

## Releases (7-day window: 2026-05-11 to 2026-05-18)

### langchain-ai/langgraph

Five packages shipped simultaneously on 2026-05-12 in a coordinated release batch:

- **1.2.0** (2026-05-12) — Stable release from alpha. Key additions: durable error-handler resume across host crashes (`#7773`); `set_node_defaults()` for StateGraph (`#7747`); delta channel snapshot enforcement after max supersteps. Bumps langchain-core to 1.4.0.
- **langgraph-prebuilt==1.1.0** (2026-05-12) — Prebuilt agents package stable, graduating from 1.1.0a2.
- **langgraph-cli==0.4.26** (2026-05-12) — CLI tooling minor update from 0.4.25.
- **langgraph-checkpoint-sqlite==3.1.0** (2026-05-12) — SQLite checkpointer stable from 3.1.0a1.
- **langgraph-checkpoint-postgres==3.1.0** (2026-05-12) — Postgres checkpointer stable from 3.1.0a4.

### crewAIInc/crewAI

- **1.14.5a6** (2026-05-15) [PRE] — Pre-release alpha; changelog not detailed in release body.
- **1.14.5a5** (2026-05-12) [PRE] — Pre-release alpha; changelog not detailed in release body.

### run-llama/llama_index

- **v0.14.22** (2026-05-14) — Batch dependency upgrades (`uv lock --upgrade`) across agentmesh, callbacks, and dozens of integration packages. Low semantic content but maintains currency across the wide integration surface.

### mastra-ai/mastra

- **@mastra/core@1.34.0** (2026-05-15) — Three headline additions: (1) `@mastra/acp@0.1.0` lets you run ACP-compatible coding agents as Mastra tools or lightweight subagents with incremental streaming; (2) `@mastra/voice-xai-realtime@0.1.0` adds xAI Grok Voice Agent API integration for real-time audio; (3) agents can now carry optional `metadata` (static or `DynamicArgument`) for filtering, cloning, and dynamic resolution.
- **@mastra/core@1.33.0** (2026-05-13) — Push delivery for workflow events: PubSubs declare `supportedModes`, `Mastra.handleWorkflowEvent(event)` is the new unified entry point, and `POST /api/workflows/events` enables broker-push from GCP Pub/Sub, SNS, or EventBridge without a pull worker. Also adds opt-in `ResponseCache` to skip model calls by replaying cached responses per step.

### huggingface/smolagents

- **v1.25.0** (2026-05-14) — Security patch: fixes a "high impact vulnerability on remote executors" (`#1637`). Also refactors agent/model deserialization from `importlib`-based discovery to a registry pattern — callers of custom model subclasses should verify compatibility. MLflow integration documentation added.

### pydantic/pydantic-ai

Five releases in 7 days reflects an unusually fast cadence:

- **v1.97.0** (2026-05-15) — API cleanup: splits `GoogleProvider(vertexai=True|False)` into `GoogleProvider` + `GoogleCloudProvider`; renames provider IDs (`google-gla:` → `google:`, `google-vertex:` → `google-cloud:`) with deprecation on old names. Replaces `MCPServer*` + `FastMCPToolset` with unified `MCPToolset` (uses `fastmcp-slim[client]`). Adds `OnlineEvaluator.run_on_errors`. Deprecated names still work — not yet a hard break — but migration is signaled.
- **v1.96.1** (2026-05-14) — Patch.
- **v1.96.0** (2026-05-14) — Minor release.
- **v1.95.1** (2026-05-13) — Patch.
- **v1.95.0** (2026-05-13) — Minor release.

---

## Momentum picks

*(No momentum picks this run — first baseline, all 7d star deltas unknown. Picks start next week once delta is measurable.)*

---

## Notable signals worth watching

**pydantic-ai deprecating MCPServer in favor of MCPToolset.** MCP tooling is consolidating. Pydantic AI's move toward `fastmcp-slim` as the underlying client is a vote on which MCP client library is becoming the default. Three weeks of daily releases suggests a product team shipping at pace — this cohort slot may be the most active by velocity going forward.

**smolagents patching a high-impact vulnerability on remote executors.** v1.25.0 was released on May 14. If you're running smolagents in any environment with remote code execution enabled, this is a mandatory upgrade. The deserialization refactor in the same release (importlib → registry) may affect custom model integrations.

**autogen's release silence.** microsoft/autogen has 58k stars and 834 open issues but its last tagged release is September 2025 — nearly eight months. The repo is still active (pushed April 2026), suggesting development continues without public release tags. Operators depending on autogen should check the main branch directly rather than waiting for a release signal from this digest.

**mastra shipping ACP integration.** Agent Communication Protocol support (`@mastra/acp`) connects mastra into the ACP ecosystem — agents can now be exposed as or consume ACP-compatible services. For the aeon-agent fork cohort, this is relevant context: ACP and A2A are both live, and mastra just chose a side.

---

## Anchor position

aeon sits at 366 stars — roughly 1/50th of autogen's count and 1/140th of crewAI's — but occupies a distinct position: GitHub-native runtime, TypeScript, no "framework" overhead. The cohort comparison here is a category mismatch as much as a size one. What this table can measure: aeon's star velocity relative to peers (available next week), release cadence (0 tagged releases vs. 5–15 per week across the active peers), and open issues (0 vs. 331–834 across the major frameworks). The 0-open-issues figure is real — the repo uses GitHub Discussions for community input and the issue tracker is clean.

No new aeon release this week. The most recent push was 2026-05-17T23:59:38Z (fork-first-run-alert skill, PR #179). If there's a tagged version in aeon's roadmap, this digest will capture it when it lands.

---

## Source status

`gh_api: ok · reachable: 9/9 · releases_lookup: 9/9 · breaking_signals_fired: 0`
