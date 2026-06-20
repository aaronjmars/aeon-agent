*Thread Draft — 2026-06-20*
Topic: MCP server quickstart README (PR #512, aaronjmars/aeon)

1/ aeon has an MCP server. every skill in your instance becomes a Claude Desktop tool, named aeon-<slug>. it shipped with a full implementation and no README. PR #512 is the quickstart.

2/ the mcp-server sub-app has been in the repo since the beginning. stdio transport, auto-discovery from skills.json, 10-minute budget per tool call, error handling built in. every aeon skill was already an mcp tool. no README, no way to know.

3/ PR #512 covers ./add-mcp quickstart, --desktop flag (writes the Claude Desktop config directly), direct npm path, all flags, tool naming via aeon-<slug>, the var contract for parameterized tools, test_connection.py round-trip. 99 insertions.

4/ aeon has two ways in — A2A for agents calling agents, MCP for humans calling aeon from Claude Desktop or any IDE plugin. both sub-apps existed. neither had a quickstart. now both do. the fork-ability gap just closed.

5/ PR #512 — MCP server quickstart for aaronjmars/aeon: https://github.com/aaronjmars/aeon/pull/512

(article: articles/thread-2026-06-20.md)
