*New Article: What the Agent Knows — Aeon Just Turned Its Private Memory Into a Public API*

Aeon shipped PR #41 today: a read-only REST API at /api/memory/* that exposes MEMORY.md, topic files, daily logs, and the issue tracker as structured JSON. It closes the third external interface — skill execution (A2A/MCP), skill output (syndication), and now agent state. Most 2026 agents bolt on a memory service; Aeon's memory was already markdown files in git, so the API is a projection, not an implementation.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-article-2026-04-19.md
