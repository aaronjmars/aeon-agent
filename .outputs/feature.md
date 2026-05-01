*Feature Built — 2026-05-01*

smithery-manifest skill
Aeon now has a skill that auto-generates the submission docs needed to list its MCP server on Smithery.ai and the official Model Context Protocol Registry. Re-running the skill regenerates three files in docs/ — a server.json manifest, a smithery.yaml deployment config, and a paste-ready submission body — so listing aeon-mcp goes from 'write everything by hand' to 'fill in the form.'

Why this matters:
The Smithery + MCP Registry submission has been Aeon's highest-priority unbuilt growth play for six straight weeks (Apr-22 repo-actions idea #1, carried through every cycle since). The actual blocker was never the submission process — it was always 'manifest not written.' Inbound discovery from the growing MCP ecosystem has been quietly missing Aeon for over a month because of one missing JSON file and a paste-ready doc. This skill closes that gap and automates it forward, so the catalog stays in sync with skills.json without anyone touching YAML.

What was built:
- skills/smithery-manifest/SKILL.md: New skill that reads skills.json + aeon.yml + mcp-server/package.json + README, generates three submission artifacts, byte-diffs them against the current docs/, and PRs + notifies only on real change. Idempotent re-runs on stable input are silent.
- docs/smithery-manifest.json: server.json compatible with the MCP Registry schema (https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json). Reverse-DNS name io.github.aaronjmars/aeon-mcp; full 95-tool catalog mirrored under _meta.io.github.aaronjmars/aeon, sorted alphabetically by tool name.
- docs/smithery.yaml: Smithery deployment config — startCommand: stdio plus a commandFunction that spawns 'node {repoPath}/mcp-server/dist/index.js' with the operator's existing env (so ANTHROPIC_API_KEY / CLAUDE_CODE_OAUTH_TOKEN flow through without an extra config step).
- docs/smithery-submission.md: Paste-ready submission body — field values, short and long descriptions, the full 95-row tool table, and Claude Desktop install instructions for macOS, Linux, and Windows.
- skills.json + aeon.yml: smithery-manifest registered (productivity, weekly Monday 06:00 UTC, sonnet model). Total skill count synced to actual length, 93 → 95.

How it works:
The skill is pure local file I/O — no curl, no env-var-in-headers, no prefetch script needed. It loads the catalog once, builds the augmented skills array (sorted alphabetically), maps each entry to an aeon-<slug> tool description matching mcp-server/src/index.ts:skillToToolName() exactly so the static manifest stays 1:1 with the live MCP server. Tool descriptions follow the format '[Aeon · <Category>] <skill description> (cron: <schedule>)' — workflow_dispatch and reactive schedules render as '(on-demand)'. After writing the three files, it byte-compares against existing docs and only opens a PR when something actually changed; this makes the weekly cron quiet by default and lets the manifest auto-refresh whenever skills are added or descriptions edited.

What's next:
Maintainer reviews PR #149, optionally publishes aeon-mcp to npm (currently referenced in packages[] but unpublished — the block can be stripped if not), then submits docs/smithery.yaml to https://smithery.ai/server/new and opens a PR at modelcontextprotocol/registry adding servers/io.github.aaronjmars/aeon-mcp.json. Once the listing lands, Aeon becomes discoverable from inside Claude Desktop's Smithery picker — closing the loop on six weeks of carried unbuilt growth.

PR: https://github.com/aaronjmars/aeon/pull/149
