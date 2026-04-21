*Push Recap — 2026-04-21*
aaronjmars/aeon — 82 commits · aaronjmars/aeon-agent — 2 meaningful commits · @aaronjmars all authors

Autoresearch Evolution sweep: 80 skills rewritten in one day on aeon. Every PR runs the same four-variation scoring loop (better inputs / sharper output / more robust / rethink) and merges the winner as the new SKILL.md — almost always Variation B by design. Shared pattern: kill flat-list output, add tier/rank + delta classification + significance-gated notifications + explicit exit taxonomy. Largest: spawn-instance (+354/-172), fork-fleet (+277/-121), skill-leaderboard (+250/-91 — now scores against *configured* fork denominator only, outputs Promote/Match/Sunset tiers), fleet-control (+248/-124), vuln-scanner (+248/-161). workflow-security-audit (#127) replaces hand-rolled 5-category checklist with zizmor + actionlint + NEW/REINTRODUCED/UNCHANGED/RESOLVED delta classification + attack-chain narrative (entry → vector → sink → reachable secrets → blast radius).

A2A + MCP Integration Examples (PR #137): closes the adoption gap flagged in yesterday's repo-actions. New examples/a2a/langchain_client.py, autogen_workflow.py, crewai_task.py, openai_agents_client.py + examples/mcp/test_connection.py + claude_desktop_config.json. Every framework gets a <100-line copy-paste demo pointed at aeon-fetch-tweets / aeon-deep-research / aeon-pr-review / aeon-token-report / aeon-cost-report. First production-ready external-integration surface for the gateway.

XAI Prefetch Error Marker merged (aeon-agent PR #16): prefetch retry budget 2→3, --connect-timeout 30, writes .xai-cache/<outfile>.error on failure, fetch-tweets short-circuits dead-end Paths B/C when marker present. Saves ~10K tokens per failed run. Squash-time fix aligns marker filename with what the script actually writes (fetch-tweets.json.error, not fetch-tweets.error — the original short-circuit would never have fired).

Key changes:
- 80 skill SKILL.md rewrites on aeon under a uniform tier+delta+gate+taxonomy contract (+12,118/-4,935 lines across 80 files) — NOT yet deployed on this aeon-agent instance; will arrive via skill-update-check PRs or fork sync
- examples/ directory added to aeon with six working client scripts + walk-through README (+520 lines, 8 new files); README 'Integration examples' subsection links them
- scripts/prefetch-xai.sh + skills/fetch-tweets/SKILL.md on aeon-agent: XAI-outage-observable short-circuit replaces 10K-token dead-end probing

Stats: 89 files changed, +12,213/-4,961 lines across 83 meaningful commits (26 autonomous chore auto-commits excluded).
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-21.md
