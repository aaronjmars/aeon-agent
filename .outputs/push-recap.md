*Push Recap — 2026-05-01*
aaronjmars/aeon — 2 commits by aaronjmars. aaronjmars/aeon-agent — 25 routine bot auto-commits, no human work.

Smithery + MCP Registry submission pipeline: new `smithery-manifest` skill auto-generates the three artifacts (server.json, smithery.yaml, paste-ready submission body) needed to list aeon-mcp on Smithery and the MCP Registry — closes the longest-carried 6-week growth unbuilt (Apr-22 #1). Maintainer pastes one yaml + opens one registry PR; the writing work is done.

README cleanup: agent-status badge removed from header. Status page itself still ships; only the discoverability surface in the README is trimmed.

Key changes:
- skills/smithery-manifest/SKILL.md (+281): weekly cron, byte-equality diff vs disk before notify, exit taxonomy OK | NO_INPUT | NO_CHANGE
- docs/smithery-manifest.json (+420): full 95-tool catalog, reverse-DNS name `io.github.aaronjmars/aeon-mcp`, MCP Registry schema 2025-12-11
- docs/smithery.yaml (+29): stdio + commandFunction → node mcp-server/dist/index.js; `repoPath` configSchema optional

Stats: 7 files changed, +906/-3 lines across 2 substantive commits
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-01.md
