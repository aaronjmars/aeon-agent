*Push Recap — 2026-06-21*
aaronjmars/aeon — SHIPPING — Charon policy pack in registry, MCP docs ship, Dependabot first run

Shipped to users:
• `25d2544` MCP server README lands — `./add-mcp` quickstart, `aeon-<slug>` tool naming, Claude Desktop config snippet, and `test_connection.py` round-trip now documented in `apps/mcp-server/README.md`
• `1f08cd9` Charon policy pack joins the registry (external contributor) — `charon-setup` + `charon-policy`, repo-local policy enforcement, no secrets required, installable via `./install-skill-pack`

Under the hood:
• Dependabot config shipped yesterday (#513) fired 12 PRs today — all merged, including TypeScript 5→6 on mcp-server and a2a-server with a one-line tsconfig fix (`types: ["node"]`); actions/checkout 4→7 and setup-node 5→6 also through

Shape: 2 user-visible · 4 internal · 3 infra · 10 bot-filtered · 19 merged PRs (7 human + 12 dependabot)
Volume: ~25 files, ~500 lines

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-21.md
