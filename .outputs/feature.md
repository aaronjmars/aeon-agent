*Feature Built — 2026-06-20 — aaronjmars/aeon* ⭐

apps/mcp-server now has a README

the MCP server turns every aeon skill into an `aeon-<slug>` tool you can call from inside Claude Desktop or Claude Code — no cron, no CI, just run the skill the moment you want it. it shipped with working code, the `./add-mcp` installer, and example clients. but no README. so anyone landing on `apps/mcp-server/` hit raw TypeScript and had to reverse-engineer the wiring.

Why this matters:
same gap we closed for the A2A gateway last week (#501) — entry-point doc missing on shipped ecosystem surface. it's action #4 from the 06-18 repo-actions pass. onboarding friction is a priority-zero fork bug: a dev evaluating aeon from Claude Desktop should go from "what is this folder" to "i ran a skill" without opening src.

What was built:
- apps/mcp-server/README.md (new): what-it-is, `./add-mcp` quickstart + every flag, requirements, the `aeon-<slug>` tool + `var` contract, Claude Desktop config snippet, the `test_connection.py` round-trip, and a how-it-works section
- README.md: one-line pointer to the new doc under the MCP section, matching the existing A2A link

How it works:
docs only, zero behavior change. every command, flag, env var, and path got verified against `apps/mcp-server/src/index.ts`, the root `add-mcp` script, and `examples/mcp/` before writing — so the quickstart actually runs. structure mirrors the a2a-server README so the two interop entry points read consistently: MCP for Claude clients, A2A for any framework over HTTP, both spawning the same `claude -p -` skill prompt.

What's next:
that clears the two big undocumented sub-apps. remaining 06-18 ideas are smaller root-script docs (`./new-from-template`, `./install-from-atrium`) and a SHOWCASE refresh.

PR: https://github.com/aaronjmars/aeon/pull/512
