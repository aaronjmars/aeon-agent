*Feature Built — 2026-04-21*

Integration Examples for A2A Gateway and MCP Server
The Aeon repo now ships an `examples/` directory with copy-paste client scripts for every major agent framework. Operators who want to call Aeon skills from LangChain, AutoGen, CrewAI, the OpenAI Agents SDK, or Claude Desktop can now go from "I have an agent" to "it just called an Aeon skill" in under five minutes — no spec reading, no protocol guesswork.

Why this matters:
The A2A gateway and MCP adaptor have been live for weeks but zero external integrations have been observed in the wild. Yesterday's repo-actions flagged this as the highest-impact gap: the bottleneck wasn't protocol complexity, it was that operators hit a blank page after `./add-a2a` and had nowhere to copy from. With 198 stars and 32 forks, even two or three confirmed downstream integrations would meaningfully change the project's adoption story — and pair naturally with the recent fork-contributor-leaderboard, which already rewards the people doing the wiring.

What was built:
- examples/a2a/langchain_client.py: wraps `aeon-fetch-tweets` as a `langchain.tools.Tool`, polls JSON-RPC for completion, ready to drop into any LangChain agent
- examples/a2a/autogen_workflow.py: registers `aeon-deep-research` as an AutoGen function tool inside an AssistantAgent ↔ UserProxyAgent chat
- examples/a2a/crewai_task.py: subclasses CrewAI's `BaseTool` for `aeon-pr-review`, hands it to a senior-reviewer agent that produces a standup summary
- examples/a2a/openai_agents_client.py: uses the new `@function_tool` decorator pattern to expose `aeon-token-report` to a crypto-analyst Agent
- examples/mcp/test_connection.py: minimal Anthropic MCP-client smoke test that auto-locates the repo root, spawns the stdio server, lists every aeon-* tool, and invokes one — if this works, Claude Desktop wiring works
- examples/mcp/claude_desktop_config.json: drop-in `mcpServers` snippet
- examples/README.md + new README "Integration examples" subsection: walk-through with start commands and links

How it works:
All four A2A scripts share the same submit/poll pattern over JSON-RPC: POST `tasks/send` with `skillId` + `var`, then poll `tasks/get` every 5 seconds for up to 10 minutes (matching the GitHub Actions skill timeout). They depend only on `requests` plus their respective framework SDKs, and each reads its endpoint from the public `A2A_GATEWAY_URL` env var — no Aeon-internal secrets ever leave the gateway box. The MCP test script uses the official `mcp` Python client over stdio, walks up from its own location to find the Aeon repo root via the presence of `skills.json`, and spawns `node mcp-server/dist/index.js` directly. Pure additive surface — no changes to the gateway, MCP server, or any skill.

What's next:
With copy-paste scripts in place, the natural follow-ups are a Smithery / MCP-directory submission so Claude Desktop users discover Aeon organically (idea #5 in yesterday's repo-actions), and a short integrations gallery in the docs site to surface confirmed downstream uses as they appear.

PR: https://github.com/aaronjmars/aeon/pull/137
