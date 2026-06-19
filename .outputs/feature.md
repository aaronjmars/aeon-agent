*Feature Built — 2026-06-19 — aaronjmars/aeon*

A2A gateway quickstart README

The A2A gateway lets any agent framework — LangChain, AutoGen, CrewAI, OpenAI Agents SDK — call an Aeon skill over plain HTTP. The server shipped with working code and four example clients but no README. Now `apps/a2a-server/` has one: what it is, how to start it, every endpoint, and a copy-paste client.

Why this matters:
A developer evaluating Aeon from their own agent stack browses to `apps/a2a-server/` and lands on raw TypeScript — no quickstart, nothing linking the server to the example clients sitting right next door. That's the exact spot you lose a forker. This was the top-scored idea (13/15) in yesterday's repo-actions pass. Lowering fork friction is priority-zero.

What was built:
- apps/a2a-server/README.md: new file — what-it-is, `./add-a2a` + direct npm quickstart, `A2A_PORT`/`A2A_URL` env table, all three endpoints, a JSON-RPC submit+poll client, a table linking the four framework examples, and protocol/deployment notes.
- README.md: one-line pointer from the existing A2A section to the new server README.

How it works:
Every command, port, env var, and endpoint path was verified against `src/index.ts` and the `add-a2a` script before writing — no guessing. The README explains the actual mechanics: gateway reads `skills.json`, advertises each skill on its agent card, spawns `claude -p -` per task, returns output as an artifact. Docs-only, zero behavior change.

What's next:
Same gap exists for `apps/mcp-server/` (repo-actions idea #4) — the MCP server has no README either. That's the natural follow-on.

PR: https://github.com/aaronjmars/aeon/pull/501
